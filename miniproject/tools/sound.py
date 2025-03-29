import pygame
import math
from settings import comms


class PositionalSound:
    def __init__(self, sound_file, emitter, listener):
        self.sound = pygame.mixer.Sound(sound_file)
        self.emitter = emitter
        self.listener = listener

        self.channel = pygame.mixer.Channel(0)

    def calculate_offset(self, distance):
        left_ear = (self.listener.x + self.listener.radius * math.cos(self.listener.angle + math.pi / 2),
                    self.listener.y + self.listener.radius * math.sin(self.listener.angle + math.pi / 2)
        )
        right_ear = (self.listener.x + self.listener.radius * math.cos(self.listener.angle + math.pi * 1.5),
                     self.listener.y + self.listener.radius * math.sin(self.listener.angle + math.pi * 1.5)
        )

        left_dist = math.hypot((left_ear[0] - self.emitter.x), (left_ear[1] - self.emitter.y))
        right_dist = math.hypot((right_ear[0] - self.emitter.x), (right_ear[1] - self.emitter.y))

        if left_dist > right_dist:
            pan = -1 + (right_dist / left_dist)  # Closer to right ear
        else:
            pan = 1 - (left_dist / right_dist)

        center_vol = max(0, 1 - distance / 500)
        left_vol = max(0, (1 - pan) / 2 * center_vol)
        right_vol = max(0, (1 + pan) / 2 * center_vol)

        self.channel.set_volume(left_vol, right_vol)

    def play(self):
        distance = math.hypot((self.emitter.x - self.listener.x), (self.emitter.y - self.listener.y))
        self.calculate_offset(distance)
        if not self.channel.get_busy():
            if distance > 50:
                self.channel.play(self.sound)
            else:
                self.sound.play()

        pygame.draw.circle(
            comms.screen,
            (0, 255, 255),
            (self.listener.x + self.listener.radius * math.cos(self.listener.angle + math.pi / 2),
                    self.listener.y + self.listener.radius * math.sin(self.listener.angle + math.pi / 2)
             ),
            5
        )
        pygame.draw.circle(
            comms.screen,
            (0, 255, 255),
            (self.listener.x + self.listener.radius * math.cos(self.listener.angle + math.pi * 1.5),
             self.listener.y + self.listener.radius * math.sin(self.listener.angle + math.pi * 1.5)
             ),
            5
        )
