import os
import asyncio
import logging
import tauntaun_live_editor.config as config
from tauntaun_live_editor.first_time_setup import get_dcs_directory as get_local_dcs_dir, get_missions_directory as get_local_missions_dir


class Timer:
    def __init__(self, timeout, callback, periodic = False):
        self._timeout = timeout
        self._callback = callback
        self._running = False
        self._periodic = periodic

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback()
        if self._periodic:
            self._task = asyncio.ensure_future(self._job())

    def start(self):
        self._task = asyncio.ensure_future(self._job())
        self._running = True

    def cancel(self):
        self._task.cancel()
        self._running = False

    def is_running(self):
        return self._running

def get_saved_games_dir():
    saved_games = os.path.abspath(os.path.join(os.environ['USERPROFILE'],
                                               'Saved Games'))
    return saved_games

def get_dcs_dir():
    # First try local config (from first-time setup)
    local_dcs_dir = get_local_dcs_dir()
    if local_dcs_dir and os.path.exists(local_dcs_dir):
        logging.debug(f"Using DCS directory from local config: {local_dcs_dir}")
        return local_dcs_dir
    
    # Fall back to config file
    dcs_dir = config.config.dcs_directory
    if dcs_dir and os.path.exists(dcs_dir):
        logging.debug(f"Using DCS directory from config: {dcs_dir}")
        return dcs_dir

    # Fall back to Saved Games detection - prioritize regular DCS over OpenBeta
    saved_games = get_saved_games_dir()
    possible_paths = [
        os.path.join(saved_games, "DCS"),  # Regular DCS World (prioritized)
        os.path.join(saved_games, "DCS.openbeta"),  # DCS OpenBeta
        os.path.join(saved_games, "DCS.openbeta_server")  # DCS Server
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            logging.debug(f"Found DCS directory: {path}")
            return path

    # Also check common installation directories
    common_install_paths = [
        "C:\\Program Files\\Eagle Dynamics\\DCS World",
        "C:\\Program Files (x86)\\Eagle Dynamics\\DCS World",
        "C:\\Program Files\\Eagle Dynamics\\DCS World OpenBeta",
        "C:\\Program Files (x86)\\Eagle Dynamics\\DCS World OpenBeta",
        "I:\\DCS World",
        "I:\\DCS World OpenBeta"
    ]
    
    for path in common_install_paths:
        if os.path.exists(path):
            logging.debug(f"Found DCS installation: {path}")
            return path

    logging.warning("No DCS directory found in common locations")
    return ""


def knots_to_kph(knots):
    return knots * 1.8502

def feet_to_meters(feet):
    return feet * 0.3048

def point_along_route(p1, p2, distance):
    heading = p1.heading_between_point(p2)
    if distance < 0:
        distance = p1.distance_to_point(p2) - distance
    return p1.point_from_heading(heading, distance)

def is_instance_of_any(obj, types):
    return any(isinstance(obj, t) for t in types)

def fixup_jsonlike(x):
    def fixup_helper(x): 
        if isinstance(x, dict):
            for key in x:
                val = x[key]
                if is_instance_of_any(val, (dict, list)):
                    fixup_jsonlike(val)
                elif not is_instance_of_any(val, (int, float, str)):
                    x[key] = str(val)
        elif isinstance(x, list):
            for idx, val in enumerate(x):
                if is_instance_of_any(val, (dict, list)):
                    fixup_jsonlike(val)
                elif not is_instance_of_any(val, (int, float, str)):
                    x[idx] = str(val)

    fixup_helper(x)
    return x

_ROOT = os.path.abspath(os.path.dirname(__file__))
def get_data_path():
    return os.path.join(_ROOT, 'data')

def is_posix():
    return os.name == 'posix'

def get_miz_path():
    # First try local config (from first-time setup)
    local_missions_dir = get_local_missions_dir()
    if local_missions_dir and os.path.exists(local_missions_dir):
        return local_missions_dir
    
    # Fall back to config file
    if os.path.exists(config.config.missions_directory):
        return os.path.join(config.config.missions_directory)
    
    # Fall back to default detection
    if is_posix():
        dcs_dir = get_data_path()
    else:
        dcs_dir = get_dcs_dir()
        if not dcs_dir:
            logging.info("No DCS dir found. Not saving")
            return

    return os.path.join(dcs_dir, "Missions")
