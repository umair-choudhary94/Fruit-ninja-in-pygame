import pygame
import random

pygame.init()

width, height = 800, 600
fruit_radius = 30
score = 0

window = pygame.display.set_mode((width, height))
pygame.display.set_caption("2D Fruit Ninja")

background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (width, height))

fruits = []
sliced_fruits = []

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

def create_fruit():
    is_bomb = random.random() < 0.1
    if is_bomb:
        color = (0, 0, 0)
        speed = random.uniform(3, 5 + score * 0.1)
        points = -50
    else:
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        speed = random.uniform(3, 5 + score * 0.1)
        points = 10

    return {'x': random.randint(fruit_radius, width - fruit_radius),
            'y': height + fruit_radius,
            'speed': speed,
            'color': color,
            'sliced': False,
            'is_bomb': is_bomb,
            'points': points,
            'direction': 1}

def draw_fruit_with_effect(surface, x, y, color, radius, sliced, is_bomb):
    if not sliced:
        pygame.draw.circle(surface, color, (int(x), int(y)), radius)
    else:
        num_slices = 8
        for i in range(num_slices):
            angle = (2 * i * 3.1416) / num_slices
            slice_x = x + radius * 0.7 * (random.random() + 0.3) * (i % 2 * 2 - 1)
            slice_y = y + radius * 0.7 * (random.random() + 0.3) * (i % 2 * 2 - 1)
            pygame.draw.circle(surface, color, (int(slice_x), int(slice_y)), int(radius / 4))

    if is_bomb:
        pygame.draw.circle(surface, (255, 255, 0), (int(x), int(y)), radius, 5)

def draw_slice_line(surface, start, end):
    pygame.draw.line(surface, (255, 255, 255), start, end, 5)

running = True
slicing = False
sliced_path = []
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mx, my = pygame.mouse.get_pos()

    for fruit in fruits:
        if not fruit['sliced']:
            fruit_pos = pygame.math.Vector2(fruit['x'] - mx, fruit['y'] - my)
            distance = fruit_pos.length()
            if distance < fruit_radius:
                fruit['sliced'] = True
                score += fruit['points']
                sliced_fruits.append({'x': fruit['x'], 'y': fruit['y'], 'speed_x': random.uniform(-5, 5),
                                      'speed_y': -10, 'color': fruit['color'], 'sliced': True, 'timer': 30,
                                      'blink': 10})

    if random.random() < 0.02:
        fruits.append(create_fruit())

    window.blit(background, (0, 0))
    for fruit in fruits:
        fruit['y'] -= fruit['speed']
        if fruit['is_bomb']:
            fruit['x'] += fruit['speed'] * fruit['direction']
            if fruit['x'] <= fruit_radius or fruit['x'] >= width - fruit_radius:
                fruit['direction'] *= -1
        draw_fruit_with_effect(window, fruit['x'], fruit['y'], fruit['color'], fruit_radius, fruit['sliced'],
                               fruit['is_bomb'])

    fruits = [fruit for fruit in fruits if fruit['y'] > -fruit_radius]

    for sliced_fruit in sliced_fruits:
        draw_fruit_with_effect(window, sliced_fruit['x'], sliced_fruit['y'], sliced_fruit['color'], fruit_radius,
                               True, False)
        sliced_fruit['y'] += sliced_fruit['speed_y']
        sliced_fruit['x'] += sliced_fruit['speed_x']
        sliced_fruit['timer'] -= 1

    sliced_fruits = [sliced_fruit for sliced_fruit in sliced_fruits if sliced_fruit['timer'] > 0]

    if slicing and len(sliced_path) > 1:
        draw_slice_line(window, sliced_path[0], sliced_path[-1])

    score_text = font.render(f'Score: {score}', True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
