import random

import pyglet

from config import *

# Creating Window
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT)

grid = [
    [[pyglet.shapes.Circle(x=(i + 1) * CELL_SPACING, y=WINDOW_HEIGHT - (j + 1) * CELL_SPACING, radius=5,
                           color=(255, 255, 255)), False]
     for i in range(GRID_SIZE)] for j in range(GRID_SIZE)]

connection_bar_list = []
position_list = []

# Random start location
starty, startx = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
grid[starty][startx][1] = True
grid[starty][startx][0].color = RED
current_pos = {'y': starty, 'x': startx}
position_list.append(current_pos)

# N O S W
directions = [{'y': -1, 'x': 0},
              {'y': 0, 'x': 1},
              {'y': 1, 'x': 0},
              {'y': 0, 'x': -1}]


@window.event
def on_draw():
    window.clear()
    for row in grid:
        for cell in row:
            cell[0].draw()
    for connection_bar in connection_bar_list:
        connection_bar.draw()


def update(dt):
    possible_directions = []
    current_pos_object = grid[current_pos['y']][current_pos['x']][0]

    # Get possible directions
    for direction in directions:
        newx = current_pos['x'] + direction['x']
        newy = current_pos['y'] + direction['y']
        if 0 <= newx < GRID_SIZE and 0 <= newy < GRID_SIZE:
            if not grid[newy][newx][1]:
                possible_directions.append(directions.index(direction))

    # Revert last changes
    if len(possible_directions) == 0:
        current_pos_object.color = WHITE
        grid[current_pos['y']][current_pos['x']][1] = False
        del position_list[-1]
        connection_bar_list.remove(connection_bar_list[-1])
        current_pos['x'] = position_list[-1]['x']
        current_pos['y'] = position_list[-1]['y']
    else:
        choosen_direction = random.choice(possible_directions)

        # Changes current position
        current_pos['x'] += directions[choosen_direction]['x']
        current_pos['y'] += directions[choosen_direction]['y']
        new_pos_object = grid[current_pos['y']][current_pos['x']][0]

        # Adds Connection Bar between dots
        if choosen_direction == 0:
            connection_bar = pyglet.shapes.Rectangle(x=current_pos_object.position[0] - BAR_WIDTH // 2,
                                                     y=current_pos_object.position[1], width=BAR_WIDTH,
                                                     height=CELL_SPACING, color=RED)
            connection_bar_list.append(connection_bar)
        elif choosen_direction == 1:
            connection_bar = pyglet.shapes.Rectangle(x=current_pos_object.position[0],
                                                     y=current_pos_object.position[1] - BAR_WIDTH // 2,
                                                     width=CELL_SPACING, height=BAR_WIDTH,
                                                     color=RED)
            connection_bar_list.append(connection_bar)
        elif choosen_direction == 2:
            connection_bar = pyglet.shapes.Rectangle(x=new_pos_object.position[0] - BAR_WIDTH // 2,
                                                     y=new_pos_object.position[1], width=BAR_WIDTH, height=CELL_SPACING,
                                                     color=RED)
            connection_bar_list.append(connection_bar)
        elif choosen_direction == 3:
            connection_bar = pyglet.shapes.Rectangle(x=new_pos_object.position[0],
                                                     y=new_pos_object.position[1] - BAR_WIDTH // 2, width=CELL_SPACING,
                                                     height=BAR_WIDTH,
                                                     color=RED)
            connection_bar_list.append(connection_bar)

        new_pos_object.color = RED
        grid[current_pos['y']][current_pos['x']][1] = True
        position_list.append(current_pos.copy())


if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/125)
    pyglet.app.run()
