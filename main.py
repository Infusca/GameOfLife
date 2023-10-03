import pygame
import random

pygame.init()

BLACK = (0,0,0)
GREY = (128,128,128)
YELLOW = (255,255,0)

# set dimensions of grid
WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE

FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT)) # pass in tuple

clock = pygame.time.Clock()

def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for _ in range(num)]) # _ is place holder, could use "i" but since we're not actually using the variable you can use placeholder "_"
        # converting this so a set will remove any duplicates

def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE)) # * takes the 2 elements passed in (unpacks) and writes out as individual values, rather than passing in a tuple

    # rather than loop through ALL grid positions to check if they are alive,
    # we will only look at all the LIVE positions and check their neighbors
    for row in range(GRID_HEIGHT):
        # draw line for each row in grid
        # grid top left is (0,0) in pygame
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE)) #(draw canvas, color, start pos, end pos)

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def adjust_grid(positions):
    # only looks at positions that could potentially be updated, ie. live cells
    all_neighbors = set() # store all neighbors from live cells from current set of positions
    new_positions = set() 

    for position in positions:
        neighbors = get_neighbors(position)
        all_neighbors.update(neighbors)

        neighbors = list(filter(lambda x: x in positions, neighbors)) # anonymous fxn, takes list (of neighbor positions), loops thru, and passes each pos to fxn, is x in positions, ie is x a live cell? if so, keep the pos in the filtered list
            # filter gives iterator but we want a list so convert filter to list

        if len(neighbors) in [2, 3]:
            new_positions.add(position)

    # check if any cells need to come alive / create
    for position in all_neighbors:
        neighbors = get_neighbors(position)
        neighbors = list(filter(lambda x: x in positions, neighbors))

        if len(neighbors) == 3:
            new_positions.add(position)


    return new_positions

def get_neighbors(pos):
    x, y = pos
    neighbors = []
    for dx in [-1, 0, 1]: 
        if x + dx < 0 or x + dx > GRID_WIDTH: # check to make sure not looking for positions off screen
            continue
        for dy in [-1, 0, 1]: # 'for displacement in x', y 
            if y + dy < 0 or y + dy > GRID_HEIGHT: # check to make sure not looking for positions off screen
                continue
            if dx == 0 and dy == 0: # looking at current position
                continue

            neighbors. append((x + dx, y + dy))

    return neighbors


def main():
    running = True
    playing = False
    count = 0
    update_freq = 30

    # grid positions
    positions = set()
    positions.add((10,10))

    while running:
        clock.tick(FPS) # runs max of 60 times per second

        if playing:
            count += 1 # this will happen a max of 60 times per second

        if count >= update_freq:
            count = 0
            positions = adjust_grid(positions)

        pygame.display.set_caption("Playing" if playing else "Paused")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                pos = (col, row)

                if pos in positions:
                    positions.remove(pos)
                else:
                    positions.add(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_c:
                    positions = set() # clear screen
                    playing = False
                    count = 0

                if event.key == pygame.K_g:
                    positions = gen(random.randrange(4, 10) * GRID_WIDTH) # generate new positions

        screen.fill(GREY)
        draw_grid(positions)
        pygame.display.update() # updates screen after we draw

    pygame.quit()

# call main function - ensures this will only call this fxn if we directly run this file, not if we are importing it from another file
if __name__ == "__main__":
    main()