from py_trees.behaviour import Behaviour
from py_trees.common import Status
from component.robot import Robot
from component.misc import Position
from utils.blackboard import RobotBlackBoard as RBB
from component.area import ZoneManager

class aiming(Behaviour):
    def __init__(self, robot_ID: int, robot_target_ID: int):
        super(aiming,self).__init__(f"Robot {robot_ID} Aiming at Robot {robot_target_ID}")
        self.robot = RBB.getRobot(RBB.getMyTeam(), robot_ID)
        self.target_robot = RBB.getRobot(RBB.getMyTeam(), robot_target_ID)
        self.ball_position = RBB.getBallPosition()

    def update(self):
        RBB.setRobotReceiver(self.target_robot.id)
        print("I somehow stuck at aiming!!")
        if self.robot.aiming(self.ball_position, self.target_robot.getPosition()) :
            return Status.SUCCESS
        elif ZoneManager.isInZone(RBB.getBallPosition(), ZoneManager.getZoneFromRole(self.robot.getRole())):
            return Status.FAILURE
        elif RBB.getPreviousBallPossession() < 0:
            return Status.FAILURE
        else:
            return Status.RUNNING