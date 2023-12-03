import random

width = 12  # Adjust according to your LED matrix width
height = 8  # Adjust according to your LED matrix height

drunk = {
    'wallCountdown': 1500,
    'padding': 2,
    'x': int(width / 2),
    'y': int(height / 2)
}

def getLevelRow():
    return [1] * width  # Use 1 to represent the land in the LED matrix

level = [getLevelRow() for _ in range(height)]

while drunk['wallCountdown'] >= 0:
    x = drunk['x']
    y = drunk['y']

    if level[y][x] == 1:
        level[y][x] = 0  # Use 0 to represent empty space in the LED matrix
        drunk['wallCountdown'] -= 1

    roll = random.randint(1, 4)

    if roll == 1 and x > drunk['padding']:
        drunk['x'] -= 1

    if roll == 2 and x < width - 1 - drunk['padding']:
        drunk['x'] += 1

    if roll == 3 and y > drunk['padding']:
        drunk['y'] -= 1

    if roll == 4 and y < height - 1 - drunk['padding']:
        drunk['y'] += 1

# Print the LED matrix
for row in level:
    print(''.join(map(str, row)))
