import py_trees
from py_trees.composites import Selector, Sequence
from py_trees.behaviour import Behaviour
from utils.blackboard import RobotBlackBoard
from component.robot import Robot
from component.misc import Role
from component.area import ZoneManager, Zone
# from action import HaltAction, StopAction, KickoffAction, ForceStartAction, DirectFreeKickAction, PenaltyAction, NormalStartAction, IndirectFreeKickAction

from utils.referee import GameCommand
from CentralBT import CentralBT

class RefereeCommandBT(Selector):
    def __init__(self, robot: Robot):
        super(RefereeCommandBT, self).__init__(name=f"check RefereeCommandBT on Robot {robot.id}", memory=True)
        self.robot = robot
        # Stop, Halt, Normal Start, Kick-Off, Free kick, Force Start, Penalty Kick
        self.add_children([
            # BallPlacementActionT(self.robot),
            # StopActionT(self.robot),
            # HaltActionT(self.robot),
            # NormalStartActionT(self.robot),
            # KickoffActionT(self.robot),
            # FreeKickActionT(self.robot),
            # ForceStartActionT(self.robot),
            # PenaltyActionT(self.robot),
            # TimeoutAction(self.robot)
            HaltActionT(self.robot),
            StopActionT(self.robot),
            NormalStartActionT(self.robot),
            KickoffActionT(self.robot),
            ForceStartActionT(self.robot),
        ])

# class BallPlacementActionT(Sequence):
#     def __init__(self, robot: Robot):
#         super(BallPlacementActionT, self).__init__(name=f"BallPlacementActionT on Robot {robot.id}", memory=True)
#         self.robot = robot
#         self.add_children([
#             checkIsBallPlacement(robot),
#             # stop all robots motion (send command velocity 0)
#             self.robot.halt()
#         ])

# class checkIsBallPlacement(Behaviour):
#     def __init__(self, robot: Robot):
#         super(checkIsBallPlacement, self).__init__(name=f"checkIsBallPlacement on Robot {robot.id}", memory=True)
#         self.robot = robot

#     def update(self):
#         if RobotBlackBoard.getGameState() == GameState.BALLPLACEMENT:
#             return py_trees.common.Status.SUCCESS
#         else:
#             return py_trees.common.Status.FAILURE

class HaltActionT(Sequence):
    def __init__(self, robot: Robot):
        super(HaltActionT, self).__init__(name=f"HaltActionT on Robot {robot.id}", memory=True)
        self.robot = robot
        self.add_children([
            checkIsHalted(robot),
            # stop all robots motion (send command velocity 0)
            RobotHaltAction(robot),
        ])

class checkIsHalted(Behaviour):
    def __init__(self, robot: Robot):
        super(checkIsHalted, self).__init__(name=f"checkisHalted on Robot {robot.id}", memory=True)
        self.robot = robot

    def update(self):
        if RobotBlackBoard.getGameState() == GameCommand.HALT:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class RobotHaltAction(Behaviour):
    def __init__(self, robot: Robot):
        super(RobotHaltAction, self).__init__(name=f"RobotHaltAction on Robot {robot.id}", memory=True)
        self.robot = robot

    def update(self):
        # stop all robots motion (send command velocity 0)
        self.robot.halt()
        return py_trees.common.Status.RUNNING

class StopActionT(Sequence):
    def __init__(self, robot: Robot):
        super(StopActionT, self).__init__(name=f"StopActionT on Robot {robot.id}", memory=True)
        self.robot = robot
        self.add_children([
            checkIsStopped(robot),
            # Stop slow less than 1.5 m/s and at least 0.5 m to ball
            # RobotHaltAction(robot), # no implementation yet
            # For now, back to our field 
        ])

class checkIsStopped(Behaviour):
    def __init__(self, robot: Robot):
        super(checkIsStopped, self).__init__(name=f"checkIsStopped on Robot {robot.id}", memory=True)
        self.robot = robot

    def update(self):
        if RobotBlackBoard.getGameState() == GameCommand.STOP:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class NormalStartActionT(Sequence):
    def __init__(self, robot: Robot):
        super(NormalStartActionT, self).__init__(name=f"NormalStartActionT on Robot {robot.id}", memory=True)
        self.robot = robot
        self.add_children([
            checkIsNormalStart(robot),
            # just start the behavior
            # this state will only sent from game controller when after for kick-offs and penalty kicks behavior
            CentralBT(robot)
        ])
class checkIsNormalStart(Behaviour):
    def __init__(self, robot: Robot):
        super(checkIsNormalStart, self).__init__(name=f"checkIsNormalStart on Robot {robot.id}", memory=True)
        self.robot = robot

    def update(self):
        if RobotBlackBoard.getGameState() == GameCommand.NORMAL_START:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

class KickoffActionT(Sequence):
    def __init__(self, robot: Robot):
        super(KickoffActionT, self).__init__(name=f"KickoffActionT on Robot {robot.id}", memory=True)
        self.robot = robot
        self.add_children([
            checkIsKickoff(robot),
            # all robots move to own half field exclude center circ. except one inside center circle
# ██╗███╗░░░███╗██████╗░██╗░░░░░███████╗███╗░░░███╗███████╗███╗░░██╗████████╗  ████████╗██╗░░██╗██╗░██████╗
# ██║████╗░████║██╔══██╗██║░░░░░██╔════╝████╗░████║██╔════╝████╗░██║╚══██╔══╝  ╚══██╔══╝██║░░██║██║██╔════╝
# ██║██╔████╔██║██████╔╝██║░░░░░█████╗░░██╔████╔██║█████╗░░██╔██╗██║░░░██║░░░  ░░░██║░░░███████║██║╚█████╗░
# ██║██║╚██╔╝██║██╔═══╝░██║░░░░░██╔══╝░░██║╚██╔╝██║██╔══╝░░██║╚████║░░░██║░░░  ░░░██║░░░██╔══██║██║░╚═══██╗
# ██║██║░╚═╝░██║██║░░░░░███████╗███████╗██║░╚═╝░██║███████╗██║░╚███║░░░██║░░░  ░░░██║░░░██║░░██║██║██████╔╝
# ╚═╝╚═╝░░░░░╚═╝╚═╝░░░░░╚══════╝╚══════╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚══╝░░░╚═╝░░░  ░░░╚═╝░░░╚═╝░░╚═╝╚═╝╚═════╝░

# ██████╗░██╗░░░░░███████╗░█████╗░░██████╗███████╗██╗
# ██╔══██╗██║░░░░░██╔════╝██╔══██╗██╔════╝██╔════╝██║
# ██████╔╝██║░░░░░█████╗░░███████║╚█████╗░█████╗░░██║
# ██╔═══╝░██║░░░░░██╔══╝░░██╔══██║░╚═══██╗██╔══╝░░╚═╝
# ██║░░░░░███████╗███████╗██║░░██║██████╔╝███████╗██╗
# ╚═╝░░░░░╚══════╝╚══════╝╚═╝░░╚═╝╚═════╝░╚══════╝╚═╝
        ])

class checkIsKickoff(Behaviour):
    def __init__(self, robot: Robot):
        super(checkIsKickoff, self).__init__(name=f"checkIsKickoff on Robot {robot.id}", memory=True)
        self.robot.id = robot.id
        self.robot = RobotBlackBoard.getRobot(RobotBlackBoard.getMyTeam(), robot.id)

    def update(self):
        if RobotBlackBoard.getGameState() == GameCommand.KICK_OFF:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

# class FreeKickActionT(Sequence):
#     def __init__(self, robot: Robot):
#         super(FreeKickActionT, self).__init__(name=f"FreeKickActionT on Robot {robot.id}", memory=True)
#         self.robot.id = robot.id
#         self.add_children([
#             checkIsFreeKick(robot),
#             # we might no need to implement this action lol
#             self.robot.halt()
#         ])

# class checkIsFreeKick(Behaviour):
#     def __init__(self, robot: Robot):
#         super(checkIsFreeKick, self).__init__(name=f"checkIsFreeKick on Robot {robot.id}", memory=True)
#         self.robot.id = robot.id
#         self.robot = RobotBlackBoard.getRobot(RobotBlackBoard.getMyTeam(), robot.id)

#     def update(self):
#         if RobotBlackBoard.getGameState() == GameState.FREE_KICK:
#             return py_trees.common.Status.SUCCESS
#         else:
#             return py_trees.common.Status.FAILURE

class ForceStartActionT(Sequence):
    def __init__(self, robot: Robot):
        super(ForceStartActionT, self).__init__(name=f"ForceStartActionT on Robot {robot.id}", memory=True)
        self.robot.id = robot.id
        self.add_children([
            checkIsForceStart(robot),
            # all robots move to own half field exclude center circ. except one inside center circle
            CentralBT(robot)
        ])

class checkIsForceStart(Behaviour):
    def __init__(self, robot: Robot):
        super(checkIsForceStart, self).__init__(name=f"checkIsForceStart on Robot {robot.id}", memory=True)
        self.robot.id = robot.id
        self.robot = RobotBlackBoard.getRobot(RobotBlackBoard.getMyTeam(), robot.id)

    def update(self):
        if RobotBlackBoard.getGameState() == GameCommand.FORCE_START:
            return py_trees.common.Status.SUCCESS
        else:
            return py_trees.common.Status.FAILURE

# class PenaltyActionT(Sequence):
#     def __init__(self, robot: Robot):
#         super(PenaltyActionT, self).__init__(name=f"PenaltyActionT on Robot {robot.id}", memory=True)
#         self.robot.id = robot.id
#         self.add_children([
#             checkIsPenaltyKick(robot),
#             # all robots move to own half field exclude center circ. except one inside center circle
#             self.robot.halt()
#         ])

# class checkIsPenaltyKick(Behaviour):
#     def __init__(self, robot: Robot):
#         super(checkIsPenaltyKick, self).__init__(name=f"checkIsPenaltyKick on Robot {robot.id}", memory=True)
#         self.robot.id = robot.id
#         self.robot = RobotBlackBoard.getRobot(RobotBlackBoard.getMyTeam(), robot.id)

#     def update(self):
#         if RobotBlackBoard.getGameState() == GameState.PENALTY_KICK:
#             return py_trees.common.Status.SUCCESS
#         else:
#             return py_trees.common.Status.FAILURE