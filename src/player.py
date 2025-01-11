
import pygame
from input_handler import  InputHandler



class Player:
    def __init__(self, isHuman, player_number):
        self.isHuman = isHuman
        self.player_number = player_number
        self.crows = 0
