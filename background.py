# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 19:17:50 2019

@author: Admin
"""
import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location, background):
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location