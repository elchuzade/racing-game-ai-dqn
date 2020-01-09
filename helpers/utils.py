from constants import Constants
from helpers.core import *
import random
import pygame
import numpy as np


def map_cars_to_state(cars, my_car):
    my_position = find_my_position(my_car)
    lines = map_cars_to_lines(cars, my_car)
    all_distances = find_all_distances(lines)
    state = [my_position, all_distances[0], all_distances[1], all_distances[2]]
    return state


def find_all_distances(lines):
    # Returns an array of 3 numbers representing distances to the nearest cars on each road line
    all_distances = []

    distance_0 = find_closest_car(lines, 0)
    all_distances.append(distance_0)

    distance_1 = find_closest_car(lines, 1)
    all_distances.append(distance_1)

    distance_2 = find_closest_car(lines, 2)
    all_distances.append(distance_2)

    return all_distances


def find_my_position(my_car):
    # returns index of a line my car is at (0 or 1 or 2)
    return int(my_car.x // Constants.LINE_WIDTH.value)


def map_cars_to_lines(cars, my_car):
    # lines will represent 3 arrays corresponsding to 3 vertical road lines
    lines = [[0, 0, 0, 0, 0, 0, 0, 0], [
        0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    for car in cars:
        # 2 is a label for enemy cars
        coord_x = car.x // Constants.LINE_WIDTH.value
        coord_y = car.y // Constants.LINE_WIDTH.value
        lines[int(coord_x)][int(coord_y)] = 2

    # 1 is a label for my car
    my_coord_x = my_car.x // Constants.LINE_WIDTH.value
    my_coord_y = my_car.y // Constants.LINE_WIDTH.value
    lines[int(my_coord_x)][int(my_coord_y)] = 1
    return lines


def check_if_lost(cars, my_car):
    # For all cars on map check if x and y coordinates are equal to my_car's
    for car in cars:
        if car.x == my_car.x and car.y == my_car.y:
            return True

    return False


def find_closest_car(lines, index):
    # Find and return the distance to the first car on a line given by index
    count = -1
    # Loops through each line and finds the number 2 which represents the enemy car
    for i in reversed(lines[index]):
        # When found an enemy car returns a distance from my car to enemy car
        if i == 2:
            return count
        count += 1
    # If there are no cars on the line, returns max possible number ie length of the line
    return count


def deactivate_cars(cars):
    # deactivate_cars checks if a car is outside of map boundaries and deactivates it
    for car in cars:
        # If the enemy_car has reached the bottom of any road line, deactivate it
        if car.y > Constants.HEIGHT.value - Constants.MARGIN.value - Constants.CAR_HEIGHT.value/2:
            car.active = False

    return cars


def move_cars(cars):
    # move_cars calls move method of each car in cars state if the car is active
    for car in cars:
        if car.active == True:
            car.move()
    return cars


def move_my_car(my_car, action):
    if action == 0:
        my_car.move("left")
    elif action == 2:
        my_car.move("right")
    elif action == 1:
        my_car.move("up")
    return my_car


def perform_action(action, cars, my_car):
    cars = move_cars(cars)
    my_car = move_my_car(my_car, action)
    cars = deactivate_cars(cars)
    for car in cars:
        if car.active == False:
            cars.remove(car)

    return cars, my_car


def add_new_car(cars):
    # add_new_car will add a new enemy_car on the top level of one of the lines picked randomly
    index = random.randint(0, 2)
    # Y coordinate of new cars
    y = Constants.MARGIN.value + Constants.CAR_HEIGHT.value/2
    if index == 0:
        # Center of first line
        x = Constants.MARGIN.value + Constants.CAR_WIDTH.value/2
    elif index == 1:
        # Center of second line
        x = Constants.MARGIN.value + Constants.CAR_WIDTH.value/2 + Constants.LINE_WIDTH.value
    elif index == 2:
        # Center of third line
        x = Constants.MARGIN.value + Constants.CAR_WIDTH.value / \
            2 + Constants.LINE_WIDTH.value*2
    car = Enemy_car(x, y)
    cars.append(car)
    return cars


def initialize_screen():
    # Size is the game screen size in pixels
    SIZE = width, height = Constants.WIDTH.value, Constants.HEIGHT.value
    SCREEN = pygame.display.set_mode(SIZE)
    pygame.display.flip()

    return SCREEN


def draw_cars(screen, cars):
    # draw_cars will draw each car from cars array on screen using its icon
    for car in cars:
        screen.blit(
            Constants.ENEMY_CAR_ICON.value, (car.x - car.width/2, car.y - car.height/2))


def draw_my_car(screen, my_car):
    # draw_my_car will draw my car on screen using its icon
    screen.blit(Constants.MY_CAR_ICON.value, (my_car.x - my_car.width /
                                              2, my_car.y - my_car.height/2))


def draw_vertical_lines(screen):
    # draw left vertical line to separate roads
    pygame.draw.rect(screen, Constants.GREY.value,
                     (Constants.LINE_WIDTH.value - Constants.ROAD_LINE_WIDTH.value / 2, 0, Constants.ROAD_LINE_WIDTH.value, Constants.HEIGHT.value))
    # draw right vertical line to separate roads
    pygame.draw.rect(screen, Constants.GREY.value, (Constants.LINE_WIDTH.value *
                                                    2 - Constants.ROAD_LINE_WIDTH.value / 2, 0, Constants.ROAD_LINE_WIDTH.value, Constants.HEIGHT.value))


def ai_model(model, cars, my_car):
    # AI will put state into model, predict the action and perform it
    # Build input array for ai model
    input_state = map_cars_to_state(cars, my_car)
    # Pass input through model to find action
    action = predict(input_state, model)
    lost = check_if_lost(cars, my_car)
    if lost:
        print("Ops! Your model has crashed!")
    # Perform the action suggested by ai model
    perform_action(action, cars, my_car)


def predict(input_array, model):
    # Puts input state into neural network and returns an action predicted by model
    # Convert array into model input format
    input_state = np.array([input_array])
    # Pass input through model to get prediction
    action = model.predict_classes(input_state)
    return action
