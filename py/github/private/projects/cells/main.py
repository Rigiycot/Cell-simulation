import pygame
import random
import time

from food import Food
from agent import Agent

DISPLAY = (800, 600)  # init display size

# init colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode(DISPLAY)

# the first agent
agents = [Agent((400, 300), 0, 100)]
food_list = []

food_count = 0
FOOD_SPAWN_RATE = 0

i = 0
running = True
while running:
    i += 1
    print(i)
    screen.fill(BLACK)  # очистка экрана

    if food_count >= FOOD_SPAWN_RATE:
        food_position = (random.randint(0, DISPLAY[0]), random.randint(0, DISPLAY[1]))
        food_list.append(Food(food_position))
        food_count = 0
    else:
        food_count += 1

    # Отрисовываем агентов
    for agent in agents:
        agent.draw(screen)

    # Отрисовываем еду
    for food in food_list:
        food.update()
        food.test(food_list)
        food.draw(screen)

    # Обрабатываем действия агентов
    for agent in agents:
        nearest_food = agent.find_food(food_list)
        if nearest_food:
            agent.move(DISPLAY, nearest_food.position, 0.01)
            agent.eat(food_list, 10)
            new_agent = agent.replicate()
            if new_agent is not None:
                agents.append(new_agent)

    for event in pygame.event.get():
        print(f"Event: {event}")  # Выводим информацию о событии
        if event.type == pygame.QUIT:
            running = False


    pygame.display.flip()  # обновляем экран
    time.sleep(0.0)

pygame.quit()
