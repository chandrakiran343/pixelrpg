from csv import reader
from os import walk
import pygame

def read_csv(path):
    with open(path) as f:
        csv_reader = reader(f)
        return list(csv_reader)

def import_folder(path):
    graphics = []
    for data in walk(path):
        for img_file in data[2]:
            graphics.append(pygame.image.load(path+'/'+img_file).convert_alpha())
    return graphics
            
