import pygame
import math
from nn import NeuralNetwork
from tracks import WALL_COLOR

CAR_COLOR = (255, 50, 50)
SENSOR_COLOR = (0, 255, 0)

class Car:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 3
        self.rotation_speed = 5
        self.alive = True
        self.time_alive = 0
        self.total_fitness = 0

        self.sensor_angles = [-75, -50, -25, 0, 25, 50, 75]
        self.max_sensor_dist = 150
        self.sensors = [self.max_sensor_dist] * len(self.sensor_angles)
        self.brain = NeuralNetwork(input_size=7, hidden_size=6, output_size=1)

        try:
            self.original_image = pygame.image.load("car.png").convert_alpha()
            self.original_image = pygame.transform.scale(self.original_image, (25, 14))
        except FileNotFoundError:
            self.original_image = None

    def reset_for_track(self, start_pos, start_angle=0):
        self.x, self.y = start_pos
        self.angle = start_angle
        self.alive = True
        self.time_alive = 0

    def think_and_drive(self, track_surface, width=800, height=600, wall_type="red_black"):
        if not self.alive:
            return

        self.time_alive += 1
        if self.time_alive > 1800:
            self.alive = False
            return
        
        self.cast_sensors(track_surface, width, height, wall_type)

        normalized_inputs = [dist / self.max_sensor_dist for dist in self.sensors]
        steer_decision = self.brain.forward(normalized_inputs)

        self.angle += steer_decision * self.rotation_speed
        rad = math.radians(self.angle)
        self.x += math.cos(rad) * self.speed
        self.y += math.sin(rad) * self.speed

    def cast_sensors(self, track_surface, width, height, wall_type):
        for i, rel_angle in enumerate(self.sensor_angles):
            abs_angle = math.radians(self.angle + rel_angle)
            dist = 0
            while dist < self.max_sensor_dist:
                dist += 5
                px = int(self.x + math.cos(abs_angle) * dist)
                py = int(self.y + math.sin(abs_angle) * dist)

                if px < 0 or px >= width or py < 0 or py >= height:
                    break

                r, g, b = track_surface.get_at((px, py))[:3]

                if wall_type == "red_black":
                    if r > 80 or g > 40:
                        break
                elif wall_type == "white" and (r > 200 and g > 200 and b > 200):
                    break
                elif wall_type == "black" and (r < 50 and g < 50 and b < 50):
                    break
             

            self.sensors[i] = dist
            if dist <= 8:
                self.alive = False

    def draw(self, surface, draw_sensors=True):
        if not self.alive:
            return
        if draw_sensors:
            for i, rel_angle in enumerate(self.sensor_angles):
                abs_angle = math.radians(self.angle + rel_angle)
                dist = self.sensors[i]
                end_x = self.x + math.cos(abs_angle) * dist
                end_y = self.y + math.sin(abs_angle) * dist
                pygame.draw.line(surface, SENSOR_COLOR, (self.x, self.y), (end_x, end_y), 1)

        if self.original_image:
            rotated_image = pygame.transform.rotate(self.original_image, -self.angle)
            new_rect = rotated_image.get_rect(center=(int(self.x), int (self.y)))
            surface.blit(rotated_image, new_rect.topleft)
        else:

            pygame.draw.circle(surface, CAR_COLOR, (int(self.x), int(self.y)), 8)