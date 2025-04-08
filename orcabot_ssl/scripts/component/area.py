from enum import Enum
from component.misc import Position
from utils.blackboard import RobotBlackBoard

from copy import deepcopy

#zone definition
class Zone(Enum):
    GOALKEEPER = 1
    DEFENSIVE_LEFT = 2
    DEFENSIVE_RIGHT = 3
    CENTER_LEFT = 4
    CENTER_RIGHT = 5
    ATTACKING = 6

class ZoneManager():
    _initialized: bool = False
    zone_position: dict = None
    opponent_zone_position: dict = None

    def __init__(self):
        if self._initialized:
            return
        else:
            self._initialized = True
            [x, y] = RobotBlackBoard.getConfig("field", "field_size")
            self.DIVIDING_FACTOR = RobotBlackBoard.getConfig("field", "field_dividing_factor")
            [df, cf, af] = self.DIVIDING_FACTOR
            ff = sum(self.DIVIDING_FACTOR)

            [goal_x, goal_y] = RobotBlackBoard.getConfig("field", "goal_size")
            team_offset = 1 if RobotBlackBoard.getConfig("match", "teams").index(RobotBlackBoard.getConfig("match", "our_team")) == 0 else -1

            x_without_goal = x - goal_x*2

            drange = x_without_goal/ff * df
            crange = x_without_goal/ff * cf
            arange = x_without_goal/ff * af

            def getEvaluatedPositionForSpecificTeam(input_dict: dict, team_offset: int) -> dict:
                if team_offset == 1:
                    return input_dict
                else:
                    temp_input_dict = deepcopy(input_dict)
                    for keys in input_dict.keys():
                        if keys.endswith("left"):
                            temp_input_dict[keys[0:-4] + "right"] = input_dict[keys]
                        elif keys.endswith("right"):
                            temp_input_dict[keys[0:-5] + "left"] = input_dict[keys]

                    for keys, values in temp_input_dict.items():
                        temp_dict = {"x_min": 0, "x_max": 0, "y_min": values["y_min"], "y_max": values["y_max"]}
                        for key in values.keys():
                            if key == "x_min":
                                temp_dict["x_max"] = -input_dict[keys][key]
                            elif key == "x_max":
                                temp_dict["x_min"] = -input_dict[keys][key]
                        temp_input_dict[keys] = temp_dict
                return temp_input_dict

            Zone_def = {
                "goal": {
                    "x_min": -x / 2,
                    "x_max": -x / 2 + goal_x,
                    "y_min": -goal_y / 2,
                    "y_max": goal_y / 2
                },
                "goalkeeper": {
                    "x_min": -x / 2 + goal_x,
                    "x_max": -x / 2 + goal_x + drange / 2,
                    "y_min": -goal_y / 2,
                    "y_max": goal_y / 2
                },
                "defensive_left": {
                    "x_min": -x / 2 + goal_x,
                    "x_max": -x / 2 + goal_x + drange,
                    "y_min": 0,
                    "y_max": y / 2
                },
                "defensive_right": {
                    "x_min": -x / 2 + goal_x,
                    "x_max": -x / 2 + goal_x + drange,
                    "y_min": -y / 2,
                    "y_max": 0
                },
                "center_left": {
                    "x_min": -x / 2 + goal_x + drange,
                    "x_max": -x / 2 + goal_x + drange + crange,
                    "y_min": 0,
                    "y_max": y / 2
                },
                "center_right": {
                    "x_min": -x / 2 + goal_x + drange,
                    "x_max": -x / 2 + goal_x + drange + crange,
                    "y_min": -y / 2,
                    "y_max": 0
                },
                "attacking": {
                    "x_min": -x / 2 + goal_x + drange + crange,
                    "x_max": -x / 2 + goal_x + drange + crange + arange,
                    "y_min": -y / 2,
                    "y_max": y / 2
                }
            }

            ZoneManager.zone_position = getEvaluatedPositionForSpecificTeam(deepcopy(Zone_def), team_offset)
            ZoneManager.opponent_zone_position = getEvaluatedPositionForSpecificTeam(deepcopy(Zone_def), team_offset * -1)


    @staticmethod
    def getAllZones() -> dict:
        return ZoneManager.zone_position

    @staticmethod
    def getAllOpponentZones() -> dict:
        return ZoneManager.opponent_zone_position

    @staticmethod
    def __getZoneBoundary(zone: Zone) -> dict:
        if zone == Zone.GOALKEEPER:
            return ZoneManager.zone_position["goalkeeper"]
        elif zone == Zone.DEFENSIVE_LEFT:
            return ZoneManager.zone_position["defensive_left"]
        elif zone == Zone.DEFENSIVE_RIGHT:
            return ZoneManager.zone_position["defensive_right"]
        elif zone == Zone.CENTER_LEFT:
            return ZoneManager.zone_position["center_left"]
        elif zone == Zone.CENTER_RIGHT:
            return ZoneManager.zone_position["center_right"]
        elif zone == Zone.ATTACKING:
            return ZoneManager.zone_position["attacking"]
        else:
            raise ValueError("Invalid zone type")

    @staticmethod
    def isInZone(position: Position, zone: Zone) -> bool:
        zone_def = ZoneManager.__getZoneBoundary(zone)
        if position.x >= zone_def["x_min"] and position.x <= zone_def["x_max"] and position.y >= zone_def["y_min"] and position.y <= zone_def["y_max"]:
            return True
        return False

    @staticmethod
    def getZoneFromPosition(position: Position) -> Zone:
        for zone in Zone:
            if ZoneManager.isInZone(position, zone):
                return zone
        return None

ZoneManager()