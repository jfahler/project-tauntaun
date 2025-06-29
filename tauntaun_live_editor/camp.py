import os
import os.path
import itertools
import argparse
import logging
import sys
import contextlib
import io

# Set DCS path environment variables before importing pydcs
# This might prevent the "Couldn't detect" warnings
from tauntaun_live_editor.first_time_setup import get_dcs_directory as get_local_dcs_dir
local_dcs_dir = get_local_dcs_dir()
if local_dcs_dir and os.path.exists(local_dcs_dir):
    os.environ['DCS_PATH'] = local_dcs_dir
    os.environ['DCS_DIR'] = local_dcs_dir
    os.environ['DCS_WORLD_PATH'] = local_dcs_dir
    os.environ['DCS_OPENBETA_PATH'] = local_dcs_dir  # Some tools look for this
    os.environ['DCS_INSTALL_PATH'] = local_dcs_dir  # Alternative name

sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/dcs")

# Temporarily suppress both stdout and stderr during pydcs import to catch all warnings
with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
    import dcs
    from dcs.flyingunit import FlyingUnit
    from dcs.point import PointAction, MovingPoint
    from dcs.translation import String
    from dcs.unit import Skill
    from dcs.weapons_data import weapon_ids
    from dcs import terrain
    from dcs.terrain.terrain import NoParkingSlotError
    import dcs.mapping as mapping
    import dcs.task

import tauntaun_live_editor.server as server
import tauntaun_live_editor.config as config
from tauntaun_live_editor.util import get_dcs_dir, get_data_path, is_posix, Timer, get_miz_path
from tauntaun_live_editor.coord import lat_lon_to_xz
from tauntaun_live_editor.sessions import SessionManager
from tauntaun_live_editor.first_time_setup import run_first_time_setup_if_needed

# Run first-time setup if needed
run_first_time_setup_if_needed()

# Suppress noisy livery parsing errors from pydcs
logging.getLogger('dcs.liveries.livery').setLevel(logging.ERROR)

# Suppress other pydcs warnings
logging.getLogger('dcs').setLevel(logging.WARNING)

# Suppress specific livery parsing errors that are harmless
logging.getLogger('dcs.lua.parse').setLevel(logging.ERROR)

# Suppress all livery-related errors at the module level
for logger_name in ['dcs.liveries', 'dcs.lua', 'dcs.terrain']:
    logging.getLogger(logger_name).setLevel(logging.ERROR)

# Suppress all pydcs warnings completely
logging.getLogger('dcs').setLevel(logging.ERROR)
logging.getLogger('dcs.terrain').setLevel(logging.ERROR)
logging.getLogger('dcs.aircraft').setLevel(logging.ERROR)
logging.getLogger('dcs.vehicles').setLevel(logging.ERROR)
logging.getLogger('dcs.ships').setLevel(logging.ERROR)
logging.getLogger('dcs.weapons').setLevel(logging.ERROR)

_data_dir = get_data_path()
_build_in_default_mission = os.path.join(_data_dir, 'Missions/default.miz')

def _convert_point(terrain, p):
    lat = float(p['lat'])
    lon = float(p['lon'])
    x, z = lat_lon_to_xz(terrain.name, lat, lon)
    return mapping.Point(x, z, terrain)

class GameService:
    def __init__(self, campaign):
        self.campaign: Campaign = campaign                
        self.group_route_request_handler = GameService.GroupRouteRequestHandler(campaign)

    def add_jtac(self, coalition, countryName, location):
        logging.debug(f"add_jtac {coalition} {countryName} {location}")

        location = _convert_point(self.campaign.mission.terrain, location)
        country = self.campaign.get_countries(coalition)[countryName]

        # add jtac humwv
        jtac = self.campaign.mission.vehicle_group(
            country,
            "jtac",
            dcs.vehicles.Unarmed.Hummer,
            location
        )

        jtac.units[0].player_can_drive = True
        jtac.points[0].tasks.append(dcs.task.SetInvisibleCommand())

    def add_flight(self, coalition, countryName, location, airport, plane, number_of_planes):
        logging.debug(f"add_flight {location} {airport} {plane} {number_of_planes}")

        # TODO validate values

        location = _convert_point(self.campaign.mission.terrain, location)
        country = self.campaign.get_countries(coalition)[countryName]

        airport = self.campaign.mission.terrain.airport_by_id(airport)
        if not airport:
            logging.warning("add_flight airport not found")
            return

        planeFinder = (p for p in country.planes if p.id == plane)
        try:
            plane = next(iter(planeFinder))
        except StopIteration:
            logging.warning("add_flight plane not found")
            return

        try:
            new_flight = self.campaign.mission.flight_group_from_airport(country,
                                                                         'DefaultName',
                                                                         aircraft_type=plane,
                                                                         airport=airport,
                                                                         group_size=number_of_planes)
        except NoParkingSlotError as e:
            logging.warning(f"add_flight failed error: {e}")
            return

        new_flight.add_waypoint(location, altitude=5000)
        new_flight.set_skill(Skill.Client)

        logging.info("add_flight success")

    def update_unit_loadout(self, unit_id, pylons, chaff, flare, gun, fuel):
        logging.info(f"update_unit_loadout {unit_id} {pylons} {chaff} {flare} {gun} {fuel}")

        # TODO Add proper validation as this function will "hard overwrite"
        # unit attributes and can corrupt the mission file
        # ("good enough for mvp" :tm:)

        unit: FlyingUnit = self.campaign.lookup_unit(unit_id)

        mapped_pylons = {}
        for k in pylons:
            clsid = weapon_ids[pylons[k]]['clsid']
            assert(clsid is not None)
            mapped_pylons[int(k)] = {
                'CLSID': clsid
           }
        unit.pylons = mapped_pylons

        # TODO validate chaff/flare
        unit.chaff = chaff
        unit.flare = flare
        assert(0 <= gun <= 100)
        unit.gun = gun
        # TODO validate fuel
        unit.fuel = fuel

        logging.info("update_unit_loadout success")

        return unit

    def set_bullseye(self, coalition, bullseye):
        coalitions = self.campaign.mission.coalition
        if coalition not in coalitions:
            logging.warning(f"set_bullseye failed, invalid coalition {coalition}")

        converted_point = _convert_point(self.campaign.mission.terrain, bullseye)
        coalitions[coalition].bullseye = {'x': converted_point.x, 'y': converted_point.y}
        logging.info(f"Bullseye set {bullseye} for {coalition}")

        return coalitions[coalition].bullseye

    class GroupRouteRequestHandler:
        def __init__(self, campaign):
            self.campaign = campaign

        @staticmethod
        def _is_same_point(a, b):
            # For now the position uniquely identifies the waypoint
            coord_drift_threshold = 1  # meter
            return a.distance_to_point(b) < coord_drift_threshold

        def remove(self, group_id, wp):
            group = self.campaign.lookup_group(group_id)
            if group is None:
                raise ValueError(f"no group found with id {group_id}")

            converted_wp = _convert_point(self.campaign.mission.terrain, wp)
            wp_index = [u_index for u_index, u in enumerate(group.points) if self._is_same_point(u.position, converted_wp)]

            if wp_index:
                logging.info(f"Removing waypoint {wp_index}")
                group.points.pop(wp_index[0])
            else:
                logging.warning("Failed to remove waypoint")

            return group

        def insert_at(self, group_id, new_wp, at_wp):
            group = self.campaign.lookup_group(group_id)            
            if group is None:
                raise ValueError(f"no group found with id {group_id}")

            converted_at_wp = _convert_point(self.campaign.mission.terrain, at_wp)
            at_index = [u_index for u_index, u in enumerate(group.points) if self._is_same_point(u.position, converted_at_wp)]

            if at_index:
                converted_new_wp = _convert_point(self.campaign.mission.terrain, new_wp)
                logging.info(f"New waypoint added at position {at_index}")
                at_index = at_index[0]
                if issubclass(group.__class__, dcs.unitgroup.FlyingGroup):
                    prev_waypoints_altitude = group.points[at_index - 1].alt
                    wp = group.add_waypoint(converted_new_wp, altitude=prev_waypoints_altitude)
                else:
                    wp = group.add_waypoint(converted_new_wp)
                group.points.pop()
                group.points.insert(at_index, wp)
            else:
                logging.warning("Failed to add new waypoint")

            return group

        def modify(self, group_id, old_wp, new_wp):
            group = self.campaign.lookup_group(group_id)
            if group is None:
                raise ValueError(f"no group found with id {group_id}")

            converted_old_wp = _convert_point(self.campaign.mission.terrain, old_wp)
            old_wp_index = [u_index for u_index, u in enumerate(group.points) if self._is_same_point(u.position, converted_old_wp)]

            if old_wp_index:
                wp = group.points[old_wp_index[0]]
                wp.alt = new_wp['alt']
                wp.type = new_wp['type']
                wp.name = new_wp['name']

                wp.position = _convert_point(self.campaign.mission.terrain, new_wp['position'])
                wp.speed = new_wp['speed']
                wp.action = PointAction[new_wp['action']]
                if isinstance(wp, MovingPoint):
                    wp.alt_type = new_wp['alt_type']

                logging.info(f"Waypoint {old_wp_index} modified")
            else:
                logging.warning("Failed to modify waypoint")

            return group

class Campaign():
    def __init__(self):
        self.mission: dcs.Mission = None
        self.game_service = GameService(self)
        self.autosave_timer = Timer(15, self.create_autosave_callback(), True)
        self.loaded_mission_path = None

    def create_autosave_callback(self):
        async def autosave_callback():
            self.save_mission()
            logging.debug("Autosave: mission saved.")

        return autosave_callback

    def get_countries(self, side):
        return self.mission.coalition[side].countries

    def get_plane_groups(self, side):
        countries = self.get_countries(side)
        return itertools.chain(*(countries[cname].plane_group for cname in countries))

    def get_plane_group_units(self, side):
        return itertools.chain(*(group.units for group in self.get_plane_groups(side)))

    def get_airport(self, name):
        return self.mission.terrain.airport[name]

    def get_ship_groups(self, side):
        countries = self.get_countries(side)
        return itertools.chain(*(countries[cname].ship_group for cname in countries))

    def get_helicopter_groups(self, side):
        countries = self.get_countries(side)
        return itertools.chain(*(countries[cname].helicopter_group for cname in countries))

    def get_vehicle_groups(self, side):
        countries = self.get_countries(side)
        return itertools.chain(*(countries[cname].vehicle_group for cname in countries))

    def lookup_unit(self, unit_id):
        # TODO
        for unit in self.get_plane_group_units('blue'):
            if unit_id == unit.id:
                return unit

        for unit in self.get_plane_group_units('red'):
            if unit_id == unit.id:
                return unit

    def lookup_group(self, group_id):

        # TODO
        for group in self.get_plane_groups('blue'):
            if group_id == group.id:
                return group

        for group in self.get_ship_groups('blue'):
            if group_id == group.id:
                return group

        for group in self.get_helicopter_groups('blue'):
            if group_id == group.id:
                return group

        for group in self.get_vehicle_groups('blue'):
            if group_id == group.id:
                return group

        for group in self.get_plane_groups('red'):
            if group_id == group.id:
                return group

        for group in self.get_ship_groups('red'):
            if group_id == group.id:
                return group

        for group in self.get_helicopter_groups('red'):
            if group_id == group.id:
                return group

        for group in self.get_vehicle_groups('red'):
            if group_id == group.id:
                return group

    def update_unit_route(self, unit_id, points):
        group = self.lookup_group(unit_id)
        if group is None:
            raise ValueError(f"no group found with id {unit_id}")
        for point, new_pos in zip(group.points, points):
            lat = float(new_pos['lat'])
            lon = float(new_pos['lon'])
            x, z = lat_lon_to_xz(self.mission.terrain.name, lat, lon)
            point.position = mapping.Point(x, z, self.mission.terrain)

    def load_mission(self, filename):
        if self.autosave_timer.is_running():
            self.autosave_timer.cancel()

        if not os.path.isfile(filename):
            logging.warning(f"Unable to load mission file not found {filename}")
            return
        
        self.mission.load_file(filename, True)
        self.loaded_mission_path = filename
        logging.info(f"Mission loaded from {filename}")

        if _build_in_default_mission != filename:
            if config.config.autosave:
                logging.debug("Autosave enabled: starting timer.")
                self.autosave_timer.start()


    def save_mission(self, filename=None):
        if _build_in_default_mission == filename:
            if self.autosave_timer.is_running():
                self.autosave_timer.cancel()

        if not filename:
            if self.loaded_mission_path is not None:
                filename = self.loaded_mission_path
            else:
                logging.error("No filename given, unable to save mission.")
                return

        self.mission.save(filename)

        if filename != self.loaded_mission_path:
            self.loaded_mission_path = filename

        logging.info(f"Mission saved to {filename}")

def _setup_logging(log_path = None):
    rootLogger = logging.getLogger()
    logFormatter = logging.Formatter("%(asctime)s.%(msecs)03d [%(levelname)-5.5s]  %(message)s",
                                     "%Y-%m-%d %H:%M:%S")

    consoleHandler = rootLogger.handlers[0]
    consoleHandler.setFormatter(logFormatter)

    log_path = log_path if log_path else "tauntaun.log"
    fileHandler = logging.FileHandler(log_path)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

def main():
    parser = argparse.ArgumentParser(description='Tauntaun live editor server.')
    parser.add_argument('--config', help="path to config.json", type=str)
    parser.add_argument('--log', help="path to tauntaun.log", type=str)

    args = parser.parse_args()

    _setup_logging(args.log)
    logging.info("--------------------------------------------------")
    logging.info("Tauntaun started.")

    try:
        config.load_config(args.config)

        # Check DCS directory before creating mission to suppress warnings
        dcs_dir = get_dcs_dir()
        if dcs_dir:
            logging.info(f"DCS directory detected: {dcs_dir}")
        else:
            logging.warning("DCS directory not found - some features may be limited")

        c = Campaign()
        
        # Suppress stderr during mission creation to catch pydcs warnings
        with contextlib.redirect_stderr(io.StringIO()):
            c.mission = dcs.Mission(terrain.Caucasus())
        
        session_manager = SessionManager()

        if config.config.default_mission:
            logging.info("Using default mission set in config")
            defualt_miz_path = os.path.join(get_miz_path(), config.config.default_mission + ".miz")
        else:
            defualt_miz_path = _build_in_default_mission

        if os.path.isfile(defualt_miz_path):
            c.load_mission(defualt_miz_path)
        else:
            logging.warning("Unable to load default mission, using empty mission!")
            batumi = next(a for a in c.mission.terrain.airports.values() if a.name == 'Batumi')
            if batumi is None:
                logging.error("Batumi airport not found in terrain.airports")
            else:
                batumi.set_blue()

        server.run(c, session_manager, config.config.port)

    except Exception as e:
        logging.exception('Got exception on main handler')

    logging.info("Tauntaun stopped gracefully.")
    logging.info("--------------------------------------------------")


if __name__ == '__main__':
    main()
