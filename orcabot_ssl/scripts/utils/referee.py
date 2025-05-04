from enum import Enum

class GameState(Enum):
    # The first half is about to start.
    # A kickoff is called within this stage.
    # This stage ends with the NORMAL_START.
    NORMAL_FIRST_HALF_PRE = 0
    # The first half of the normal game, before half time.
    NORMAL_FIRST_HALF = 1
    # Half time between first and second halves.
    NORMAL_HALF_TIME = 2
    # The second half is about to start.
    # A kickoff is called within this stage.
    # This stage ends with the NORMAL_START.
    NORMAL_SECOND_HALF_PRE = 3
    # The second half of the normal game, after half time.
    NORMAL_SECOND_HALF = 4
    # The break before extra time.
    EXTRA_TIME_BREAK = 5
    # The first half of extra time is about to start.
    # A kickoff is called within this stage.
    # This stage ends with the NORMAL_START.
    EXTRA_FIRST_HALF_PRE = 6
    # The first half of extra time.
    EXTRA_FIRST_HALF = 7
    # Half time between first and second extra halves.
    EXTRA_HALF_TIME = 8
    # The second half of extra time is about to start.
    # A kickoff is called within this stage.
    # This stage ends with the NORMAL_START.
    EXTRA_SECOND_HALF_PRE = 9
    # The second half of extra time.
    EXTRA_SECOND_HALF = 10
    # The break before penalty shootout.
    PENALTY_SHOOTOUT_BREAK = 11
    # The penalty shootout.
    PENALTY_SHOOTOUT = 12
    # The game is over.
    POST_GAME = 13

    # The number of microseconds left in the stage.
    # The following stages have this value the rest do not:
    # NORMAL_FIRST_HALF
    # NORMAL_HALF_TIME
    # NORMAL_SECOND_HALF
    # EXTRA_TIME_BREAK
    # EXTRA_FIRST_HALF
    # EXTRA_HALF_TIME
    # EXTRA_SECOND_HALF
    # PENALTY_SHOOTOUT_BREAK
    #
    # If the stage runs over its specified time, this value
    # becomes negative.
stage_time_left = 3

class GameCommand(Enum):
    # All robots should completely stop moving.
    HALT = 0
    # Robots must keep 50 cm from the ball.
    STOP = 1
    # A prepared kickoff or penalty may now be taken.
    NORMAL_START = 2
    # The ball is dropped and free for either team.
    FORCE_START = 3
    # The yellow team may move into kickoff position.
    PREPARE_KICKOFF_YELLOW = 4
    # The blue team may move into kickoff position.
    PREPARE_KICKOFF_BLUE = 5
    # The yellow team may move into penalty position.
    PREPARE_PENALTY_YELLOW = 6
    # The blue team may move into penalty position.
    PREPARE_PENALTY_BLUE = 7
    # The yellow team may take a direct free kick.
    DIRECT_FREE_YELLOW = 8
    # The blue team may take a direct free kick.
    DIRECT_FREE_BLUE = 9
    # The yellow team may take an indirect free kick.
    INDIRECT_FREE_YELLOW = 10
    # The blue team may take an indirect free kick.
    INDIRECT_FREE_BLUE = 11
    # The yellow team is currently in a timeout.
    TIMEOUT_YELLOW = 12
    # The blue team is currently in a timeout.
    TIMEOUT_BLUE = 13
    # The yellow team just scored a goal.
    # For information only.
    # Deprecated: Use the score field from the team infos instead. That way, you can also detect revoked goals.
    GOAL_YELLOW = 14
    # The blue team just scored a goal. See also GOAL_YELLOW.
    GOAL_BLUE = 15
    # Equivalent to STOP, but the yellow team must pick up the ball and
    # drop it in the Designated Position.
    BALL_PLACEMENT_YELLOW = 16
    # Equivalent to STOP, but the blue team must pick up the ball and drop
    # it in the Designated Position.
    BALL_PLACEMENT_BLUE = 17

    def idToEnum(self, id: int) -> "GameCommand":
        """
        Convert an integer ID to a GameCommand enum value.
        """
        if id == 0:
            return GameCommand.HALT
        elif id == 1:
            return GameCommand.STOP
        elif id == 2:
            return GameCommand.NORMAL_START
        elif id == 3:
            return GameCommand.FORCE_START
        elif id == 4:
            return GameCommand.PREPARE_KICKOFF_YELLOW
        elif id == 5:
            return GameCommand.PREPARE_KICKOFF_BLUE
        elif id == 6:
            return GameCommand.PREPARE_PENALTY_YELLOW
        elif id == 7:
            return GameCommand.PREPARE_PENALTY_BLUE
        elif id == 8:
            return GameCommand.DIRECT_FREE_YELLOW
        elif id == 9:
            return GameCommand.DIRECT_FREE_BLUE
        elif id == 10:
            return GameCommand.INDIRECT_FREE_YELLOW
        elif id == 11:
            return GameCommand.INDIRECT_FREE_BLUE
        elif id == 12:
            return GameCommand.TIMEOUT_YELLOW
        elif id == 13:
            return GameCommand.TIMEOUT_BLUE
        elif id == 14:
            return GameCommand.GOAL_YELLOW
        elif id == 15:
            return GameCommand.GOAL_BLUE