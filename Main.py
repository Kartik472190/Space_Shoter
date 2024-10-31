import pygame
import sys

pygame.init()

# Setting up the display window
win = pygame.display.set_mode((700, 500))
pygame.display.set_caption("Naruto vs Sasuke")

# Load images for character animations, background, and health icons
def load_image(path):
    try:
        return pygame.image.load(path)
    except pygame.error:
        print(f"Error loading image at {path}")
        sys.exit()  # Exit if any image is not found

# Load character images
walkRight = [
    load_image('C:/Users/pc/Desktop/Pics/NR2.png'),
    load_image('C:/Users/pc/Desktop/Pics/NR3.png'),
    load_image('C:/Users/pc/Desktop/Pics/NR1.png')
]
walkLeft = [
    load_image('C:/Users/pc/Desktop/Pics/Nl2.png'),
    load_image('C:/Users/pc/Desktop/Pics/Nl3.png'),
    load_image('C:/Users/pc/Desktop/Pics/Nl1.png')
]

# Load background, standing image, shuriken, and health bar icons
bg = load_image('C:/Users/pc/Desktop/Pics/bg.png')
stand = load_image('C:/Users/pc/Desktop/Pics/Nstanding.png')
shuriken_img = load_image('C:/Users/pc/Desktop/Pics/shur.png')
naruto_health_img = load_image('C:/Users/pc/Desktop/Pics/NH.png')
sasuke_health_img = load_image('C:/Users/pc/Desktop/Pics/SH.png')

# Load sound effects
hit_sound = pygame.mixer.Sound('C:/Users/pc/Desktop/Pics/hit.wav')
shuriken_sound = pygame.mixer.Sound('C:/Users/pc/Desktop/Pics/shuriken.wav')

# Character properties
x = 50
y = 400
width = 30
height = 70
speed = 10
health = 100

# Jump variables
isJump = False
jumpCount = 10

# Animation variables
left = False
right = False
walkCount = 0
facing = 1

# Weapon properties
class Weapon:
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.vel = 8 * facing

    def draw(self, win):
        win.blit(shuriken_img, (self.x, self.y))

# List to hold shuriken projectiles
weapons = []

# Enemy class
class Enemy:
    walkRightS = [
        load_image('C:/Users/pc/Desktop/Pics/SR2.png'),
        load_image('C:/Users/pc/Desktop/Pics/SR3.png'),
        load_image('C:/Users/pc/Desktop/Pics/SR1.png')
    ]
    walkLeftS = [
        load_image('C:/Users/pc/Desktop/Pics/Sl2.png'),
        load_image('C:/Users/pc/Desktop/Pics/Sl3.png'),
        load_image('C:/Users/pc/Desktop/Pics/Sl1.png')
    ]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.speed = 8
        self.walkCount = 0
        self.health = 100
        self.visible = True

    def draw(self, win):
        if self.visible:
            self.move()
            if self.walkCount + 1 >= 6:
                self.walkCount = 0
            if self.speed > 0:
                win.blit(self.walkRightS[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeftS[self.walkCount // 2], (self.x, self.y))
                self.walkCount += 1

            # Draw Sasuke's health bar
            pygame.draw.rect(win, (255, 0, 0), (self.x, self.y - 20, 100, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.x, self.y - 20, self.health, 10))

        if self.health <= 0:
            self.visible = False

    def move(self):
        if self.speed > 0:
            if self.x + self.speed < self.end:
                self.x += self.speed
            else:
                self.speed = -self.speed
                self.walkCount = 0
        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed = -self.speed
                self.walkCount = 0

# Function to redraw the game window
def redrawGameWindow():
    win.blit(bg, (0, 0))

    global walkCount
    if walkCount + 1 >= 9:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount // 3], (x, y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount // 3], (x, y))
        walkCount += 1
    else:
        win.blit(stand, (x, y))

    # Draw Naruto's health bar and icon
    win.blit(naruto_health_img, (10, 15))
    pygame.draw.rect(win, (255, 0, 0), (50, 20, 100, 10))
    pygame.draw.rect(win, (0, 255, 0), (50, 20, health, 10))

    if health <= 0:
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render('Game Over', True, (255, 0, 0))
        win.blit(text, (250, 200))

    # Draw Sasuke's health bar icon
    if sasuke.visible:
        win.blit(sasuke_health_img, (600, 15))
        pygame.draw.rect(win, (255, 0, 0), (550, 20, 100, 10))
        pygame.draw.rect(win, (0, 255, 0), (550, 20, sasuke.health, 10))

    for weapon in weapons:
        weapon.draw(win)
    sasuke.draw(win)

    pygame.display.update()

# Initialize characters
sasuke = Enemy(30, 400, 100, 100, 600)

# Main loop
run = True
while run:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if health <= 0:
        redrawGameWindow()
        pygame.time.delay(3000)
        run = False
        continue

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > 0:
        x -= speed
        left = True
        right = False
        facing = -1
    elif keys[pygame.K_RIGHT] and x < 700 - width:
        x += speed
        left = False
        right = True
        facing = 1
    else:
        left = False
        right = False
        walkCount = 0

    if not isJump:
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            neg = 1 if jumpCount > 0 else -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10

    if keys[pygame.K_f]:
        if len(weapons) < 5:
            weapons.append(Weapon(round(x + width // 2), round(y + height // 2), facing))
            shuriken_sound.play()  # Play shuriken sound on fire

    # Collision detection between Naruto and Sasuke
    if sasuke.visible and x < sasuke.x + sasuke.width and x + width > sasuke.x and y < sasuke.y + sasuke.height and y + height > sasuke.y:
        health -= 10  # Reduce Naruto's health on collision
        if health <= 0:
            health = 0  # Ensure health doesn't go below zero

    for weapon in weapons:
        if 0 < weapon.x < 700:
            weapon.x += weapon.vel
            if sasuke.visible and sasuke.x < weapon.x < sasuke.x + sasuke.width and sasuke.y < weapon.y < sasuke.y + sasuke.height:
                sasuke.health -= 10
                hit_sound.play()  # Play hit sound on collision
        else:
            weapons.pop(weapons.index(weapon))

    redrawGameWindow()

pygame.quit()
