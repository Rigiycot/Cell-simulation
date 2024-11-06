import pygame

class Food:
    size = 5
    color = (191, 131, 57)

    max_time = 1000

    def __init__(self, position):
        self.position = position
        self.color = Food.color
        self.size = Food.size
        self.time = 0

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.position, self.size)

    def update(self):
        self.time += 1

    def test(self, food_list):
        food_to_remove = []
        for food in food_list:
            if food.time > Food.max_time:
                food_to_remove.append(food)

        for food in food_to_remove:
            food_list.remove(food)