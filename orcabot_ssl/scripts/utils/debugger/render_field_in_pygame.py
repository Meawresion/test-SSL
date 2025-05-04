import pygame
import random

from utils.blackboard import RobotBlackBoard
from component.robot import Robot
from component.robotEx import RobotDict, RobotList
from component.misc import Position

def render(data):
    # Pygame setup
    pygame.init()
    window_width, window_height = 900, 600  # Pygame window size
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Rendering Boxes")

    field_x_min, field_x_max = -5500, 5500
    field_y_min, field_y_max = -4000, 4000

    field_data = data

    def normalize_coordinates(x, y, field_x_min, field_x_max, field_y_min, field_y_max, window_width, window_height):
        # Normalize x
        screen_x = (x - field_x_min) / (field_x_max - field_x_min) * window_width
        # Normalize y
        screen_y = (-y - field_y_min) / (field_y_max - field_y_min) * window_height
        return screen_x, screen_y

    def random_color():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    box_colors = [random_color() for i in range(len(field_data.items()))]

    def draw_boxes_and_labels():
        screen.fill((255, 255, 255))

        font = pygame.font.SysFont(None, 24)

        i = 0

        for label, coords in field_data.items():
            x_min, y_max = normalize_coordinates(coords['x_min'], coords['y_min'], field_x_min, field_x_max, field_y_min, field_y_max, window_width, window_height)
            x_max, y_min = normalize_coordinates(coords['x_max'], coords['y_max'], field_x_min, field_x_max, field_y_min, field_y_max, window_width, window_height)

            box_color = box_colors[i]
            i += 1

            pygame.draw.rect(screen, box_color, pygame.Rect(x_min, y_min, x_max - x_min, y_max - y_min), 2)

            label_text = font.render(label, True, (0, 0, 0))
            screen.blit(label_text, (x_min + 15, y_min + 15))


    def drawRobot():

        font = pygame.font.SysFont(None, 14)

        for robot in RobotBlackBoard.getRobotList("blue"):
            position: Position = robot.getPosition()
            rid: int = robot.id

            norm_position = normalize_coordinates(position.x, position.y, field_x_min, field_x_max, field_y_min, field_y_max, window_width, window_height)

            pygame.draw.circle(screen, pygame.Color(0, 0, 255), norm_position, 10)

            label_text = font.render("blue " + str(rid), True, (0, 0, 0))
            screen.blit(label_text, (norm_position[0] + 1, norm_position[1] - 19))

        for robot in RobotBlackBoard.getRobotList("yellow"):
            position: Position = robot.getPosition()
            rid: int = robot.id

            norm_position = normalize_coordinates(position.x, position.y, field_x_min, field_x_max, field_y_min, field_y_max, window_width, window_height)

            pygame.draw.circle(screen, pygame.Color(255, 255, 0), norm_position, 10)

            label_text = font.render("yellow " + str(rid), True, (0, 0, 0))
            screen.blit(label_text, (norm_position[0] + 1, norm_position[1] - 19))

    # draw_boxes_and_labels()

    running = True
    while running:
        draw_boxes_and_labels()
        drawRobot()
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


    pygame.quit()