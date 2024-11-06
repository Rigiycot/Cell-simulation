import random
from math import atan2, sin, cos, pi
import pygame

class Agent:
    speed = 5
    repl_time = 100

    def __init__(self, position: tuple, voice_size: int, energy: int = 100):
        self.position = position
        self.size = energy * 0.05
        self.voice_size = voice_size
        self.energy = energy
        self.angle = 0
        self.last_repl = 0
        self.target_food = None  # Цель для еды

    def draw(self, surface) -> None:
        color = self.get_color_by_voice_size()
        self.size = self.energy * 0.05
        pygame.draw.circle(surface, color, self.position, self.size)

    def get_color_by_voice_size(self):
        if self.voice_size < 10:
            return (245, 155, 66)
        elif self.voice_size < 25:
            return (245, 215, 66)
        elif self.voice_size < 50:
            return (179, 245, 66)
        elif self.voice_size < 75:
            return (66, 245, 66)
        elif self.voice_size < 100:
            return (66, 245, 167)
        elif self.voice_size < 125:
            return (66, 230, 245)
        elif self.voice_size < 150:
            return (66, 108, 245)
        elif self.voice_size < 175:
            return (79, 25, 130)
        else:
            return (130, 25, 116)

    def move(self, DISPLAY: tuple, food_list: list, cost: float = 1) -> None:
        # Если нет цели (еды), ищем новую
        if not self.target_food:
            self.target_food = self.find_food(food_list)  # Находим ближайшую еду

        if self.target_food:
            self.energy -= cost
            tx, ty = self.target_food.position
            x, y = self.position

            # Вычисляем угол
            angle_to_target = atan2(ty - y, tx - x)
            angle_diff = (angle_to_target - self.angle + pi) % (2 * pi) - pi        
            self.angle += angle_diff * 0.1

            # Новая позиция агента
            dx = x + sin(self.angle) * Agent.speed
            dy = y + cos(self.angle) * Agent.speed
            self.position = (
                    max(0, min(dx, DISPLAY[0])), 
                    max(0, min(dy, DISPLAY[1]))
                )

            # Если агент съел еду, ищем новую
            distance_to_food = self.calculate_distance(self.position, self.target_food.position)
            if distance_to_food < self.size:
                self.eat([self.target_food])  # Съедаем еду
                self.target_food = None  # Убираем старую цель

    def find_food(self, food_list):
        closest_food = None
        dist = float("inf")
        for food in food_list:
            distance = self.calculate_distance(self.position, food.position)
            if distance < dist:
                dist = distance
                closest_food = food
        return closest_food

    def calculate_distance(self, pos1: tuple, pos2: tuple) -> float:
        return ((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2) ** 0.5

    def replicate(self, plus_minus: int = 1):
        if self.energy < 200 or Agent.repl_time > self.last_repl:
            self.last_repl += 1
            return None
        self.last_repl = 0
        pm = random.randint(-1, 1)
        self.energy -= 100 + pm
        return Agent(self.position, self.voice_size + random.randint(-plus_minus, plus_minus), 100 + pm)

    def eat(self, food_list: list, gain: float = 1):
        for food in food_list:
            distance = ((self.position[0] - food.position[0]) ** 2 + (self.position[1] - food.position[1]) ** 2) ** 0.5

            # Увеличиваем размер допустимого радиуса еды для более точного взаимодействия
            if distance < self.size + food.size:  # food.size добавляется для учета размера еды
                food_list.remove(food)
                self.energy += gain
                break

