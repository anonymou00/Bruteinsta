#!/usr/bin/env python3
from ursina import *
import random

class RacingGame(Ursina):
    def __init__(self):
        super().__init__()
        self.setup_game()
        
    def setup_game(self):
        window.title = "3D Racing Game"
        window.borderless = False
        window.fullscreen = False
        
        self.create_world()
        self.create_car()
        self.create_ui()
        
    def create_world(self):
        self.ground = Entity(
            model='plane',
            scale=(50, 1, 50),
            color=color.green,
            collider='box'
        )
        
        self.road = Entity(
            model='plane',
            scale=(10, 1, 50),
            color=color.gray,
            position=(0, 0.01, 0)
        )
        
        for i in range(5):
            building = Entity(
                model='cube',
                scale=(2, 5, 2),
                color=color.blue,
                position=(random.uniform(-20, 20), 2.5, random.uniform(-20, 20))
            )
        
    def create_car(self):
        self.car = Entity(
            model='cube',
            scale=(2, 1, 4),
            color=color.red,
            position=(0, 1, 0)
        )
        
        self.camera_3rd = Entity(
            parent=self.car,
            position=(0, 3, -8),
            rotation=(15, 0, 0)
        )
        
        self.camera_1st = Entity(
            parent=self.car,
            position=(0, 1.5, 0.5)
        )
        
        camera.parent = self.camera_3rd
        self.camera_mode = '3rd'
        
    def create_ui(self):
        self.speed_text = Text(
            text="Speed: 0 km/h",
            position=(0.7, 0.4),
            scale=1.2,
            color=color.white
        )
        
        self.instructions = Text(
            text="WASD - Move, C - Camera, ESC - Quit",
            position=(-0.8, -0.4),
            scale=1.0,
            color=color.white
        )
        
    def update(self):
        if held_keys['w']:
            self.car.position += self.car.forward * time.dt * 20
        if held_keys['s']:
            self.car.position += self.car.back * time.dt * 10
            
        if held_keys['a']:
            self.car.rotation_y += 100 * time.dt
        if held_keys['d']:
            self.car.rotation_y -= 100 * time.dt
            
        speed = 0
        if held_keys['w']:
            speed = 100
        self.speed_text.text = f"Speed: {speed:.0f} km/h"
        
    def input(self, key):
        if key == 'escape':
            quit()
        elif key == 'c':
            self.switch_camera()
            
    def switch_camera(self):
        if self.camera_mode == '3rd':
            camera.parent = self.camera_1st
            self.camera_mode = '1st'
        else:
            camera.parent = self.camera_3rd
            self.camera_mode = '3rd'

if __name__ == '__main__':
    game = RacingGame()
    print("=== 3D Racing Game ===")
    print("Controls:")
    print("WASD - Move car")
    print("C - Switch camera")
    print("ESC - Quit")
    game.run()