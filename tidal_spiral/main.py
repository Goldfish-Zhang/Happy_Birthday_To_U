"""Pygame visualization: tidal data as a moving spiral.

Run: python main.py
"""
import sys
import math
import csv
import os
from datetime import datetime

import pygame
import numpy as np

from tidal_data import generate_synthetic_tide, save_csv


def load_csv(path):
    times = []
    vals = []
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            times.append(datetime.fromisoformat(r['datetime']))
            vals.append(float(r['height']))
    return times, np.array(vals)


def map_to_spiral(idx, total, radius_scale=200):
    # Map index to angle and radius: angle increases with idx, radius depends on value
    theta = idx * 0.1
    r = radius_scale * (0.1 + idx / total)
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


def run(path='data/tides.csv'):
    if not os.path.exists(path):
        print('Generating synthetic tide data...')
        data = generate_synthetic_tide(datetime.now(), hours=24*30)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        save_csv(data, path)

    times, vals = load_csv(path)
    total = len(vals)

    pygame.init()
    size = (900, 900)
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    center = (size[0]//2, size[1]//2)

    running = True
    idx = 0
    speed = 1  # frames per data step

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_UP:
                    speed += 1
                elif event.key == pygame.K_DOWN:
                    speed = max(1, speed - 1)

        screen.fill((10, 10, 10))

        # draw spiral points up to idx
        for i in range(max(0, idx-1000), idx+1):
            if i >= total: break
            x_off, y_off = map_to_spiral(i, total, radius_scale=300)
            x = int(center[0] + x_off)
            y = int(center[1] + y_off)
            h = vals[i]
            # color by height: normalize roughly into blue->cyan->yellow
            t = (h - vals.min()) / (vals.max() - vals.min() + 1e-6)
            color = (int(255 * t), int(200 * (1 - t)), int(255 * (1 - t)))
            alpha = int(255 * (i - (idx-1000)) / 1000) if idx-1000 >= 0 else 255
            # pygame doesn't support per-point alpha in draw.circle; create a small surface
            s = pygame.Surface((6,6), pygame.SRCALPHA)
            s.fill((0,0,0,0))
            pygame.draw.circle(s, color + (max(30, alpha),), (3,3), 3)
            screen.blit(s, (x-3, y-3))

        # draw head point larger
        if idx < total:
            x_off, y_off = map_to_spiral(idx, total, radius_scale=300)
            x = int(center[0] + x_off)
            y = int(center[1] + y_off)
            pygame.draw.circle(screen, (255,255,255), (x,y), 6)

        pygame.display.flip()
        idx = (idx + speed) % total
        clock.tick(30)

    pygame.quit()


if __name__ == '__main__':
    run()
