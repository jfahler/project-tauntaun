import json
import unittest

import os
import sys
sys.path.append(f"{os.path.dirname(os.path.realpath(__file__))}/../tauntaun_live_editor/dcs")

from tauntaun_live_editor.server.mission_encoder import MissionEncoder
from test.test_common import create_mission


class MissionEncoderTestCase(unittest.TestCase):
     def test_to_json_no_exception(self):
        mission = create_mission()

        encoded = json.dumps(
            mission,
            terrain=mission.terrain,
            convert_coords=True,
            add_sidc=True,
            cls=MissionEncoder,
        )

        result = json.loads(encoded)

        # the root object represents the mission and must at least include
        # terrain information and coalition data
        self.assertIn("terrain", result)
        self.assertIn("coalition", result)

