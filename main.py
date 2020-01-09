import pygame
from helpers.core import *
from helpers.utils import *
from constants import Constants
from keras.models import load_model


class Game(object):
    def __init__(self):
        print("initializing racing game")
        self.counter = 0
        self.constants = Constants
        self.my_car = My_car(self.constants.MY_CAR_X.value,
                             self.constants.MY_CAR_Y.value)
        self.cars = []

    def reset(self):
        print("resetting environment")
        self.counter = 0
        self.cars = []
        self.my_car = My_car(self.constants.MY_CAR_X.value,
                             self.constants.MY_CAR_Y.value)
        state = [0, 7, 7, 7]
        return state

    def step(self, action):
        self.counter += 1
        state = map_cars_to_state(self.cars, self.my_car)
        self.cars, self.my_car = perform_action(action, self.cars, self.my_car)
        next_state = map_cars_to_state(self.cars, self.my_car)
        done = check_if_lost(self.cars, self.my_car)

        if self.counter % 2 == 0:
            self.cars = add_new_car(self.cars)

        return next_state, done

    def play_model(self, keras_model):
        self.model = load_model(keras_model)
        pygame.init()
        pygame.display.set_caption('Racing Car AI DQN')
        SCREEN = initialize_screen()
        # Clock is set to keep track of frames
        clock = pygame.time.Clock()
        player_control = False
        self.counter = 0
        self.ai = True
        while 1:
            # limit runtime speed to 30 frames/second
            clock.tick(30)
            self.counter += 1
            pygame.event.pump()
            for event in pygame.event.get():
                # Look for any button press action
                if event.type == pygame.KEYDOWN:
                    # Press Left key to move my_car to left
                    if event.key == pygame.K_LEFT:
                        if player_control == True:
                            action = 0
                            current_state, next_state, reward, step_counter, self.cars = make_action(
                                action, step_counter, self.cars, self.my_car)
                            print(current_state, next_state, reward, action)

                    # Press Right key to move my_car to right
                    elif event.key == pygame.K_RIGHT:
                        if player_control == True:
                            action = 2
                            current_state, next_state, reward, step_counter, self.cars = make_action(
                                action, step_counter, self.cars, self.my_car)
                            print(current_state, next_state, reward, action)

                    # Press Right key to move my_car to right
                    elif event.key == pygame.K_UP:
                        if player_control == True:
                            action = 1
                            current_state, next_state, reward, step_counter, self.cars = make_action(
                                action, step_counter, self.cars, self.my_car)
                            print(current_state, next_state, reward, action)

                    # Press Escape key to quit game
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        raise SystemExit

                # Quit the game if the X symbol is clicked
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit

                
            if self.counter % 1 == 0:
                if self.ai == True:
                    ai_model(self.model, self.cars, self.my_car)
            
            if self.counter % 2 == 0:
                self.cars = add_new_car(self.cars)

            # Build up a black screen as a game background
            SCREEN.fill(Constants.BLACK.value)
            # Draw two road separater lines
            draw_vertical_lines(SCREEN)
            # Draw cars
            draw_cars(SCREEN, self.cars)
            # Draw player car
            draw_my_car(SCREEN, self.my_car)
            # update display
            pygame.display.flip()
