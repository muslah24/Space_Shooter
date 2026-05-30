import time
import turtle
import random

# ---------------- SCREEN ----------------
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Space Shooter Game")

# Background image
screen.bgpic("space.gif")

# Smooth animation
screen.tracer(0)

# ---------------- REGISTER IMAGES ----------------
screen.register_shape("ship.gif")
screen.register_shape("enemy.gif")
screen.register_shape("bullet.gif")
screen.register_shape("explosion.gif")
# ---------------- PLAYER ----------------
player = turtle.Turtle()
player.shape("ship.gif")
player.shapesize(2, 2)
player.penup()
player.goto(0, -250)

player_speed = 20

# ---------------- BULLET ----------------
bullet = turtle.Turtle()
bullet.shape("triangle")
bullet.color("yellow")
bullet.shapesize(0.7,1.5)
bullet.setheading(90)
bullet.penup()
bullet.hideturtle()

bullet_speed = 15
bullet_state = "ready"

# ---------------- ENEMIES ----------------
enemies = []

number_of_enemies = 5

for i in range(number_of_enemies):

    enemy = turtle.Turtle()

    enemy.shape("enemy.gif")

    enemy.shapesize(1.5,1.5)

    enemy.penup()

    x = random.randint(-300, 300)
    y = random.randint(100, 250)

    enemy.goto(x, y)

    enemy.speed_value = random.choice([1, 2])

    enemies.append(enemy)

#Game variables
score = 0
lives = 3
level = 1
game_over = False
paused = False

# ---------------- BOSS (Level 5) ----------------
boss = turtle.Turtle()
boss.shape("enemy.gif")
boss.penup()
boss.goto(0, 250)
boss.hideturtle() # hide at start

boss_health = 20
boss_active = False

# ---------------- SCORE ----------------

pen = turtle.Turtle()
pen.hideturtle()
pen.color("white")
pen.penup()
pen.goto(-370, 260)

def update_score():
    pen.clear()
    pen.write(f"Score: {score}",
              font=("Arial", 16, "bold"))

update_score()

#-------Lives display-----------------
life_pen = turtle.Turtle()
life_pen.hideturtle()
life_pen.color("white")
life_pen.penup()
life_pen.goto(250, 260)

def update_lives():
    life_pen.clear()
    life_pen.write(
        f"Lives: {lives}",
        font=("Arial", 16, "bold")
    )

update_lives()
#------------------Level display-----------------
level_pen = turtle.Turtle()
level_pen.hideturtle()
level_pen.color("white")
level_pen.penup()
level_pen.goto(-50, 260)

def update_level():
    level_pen.clear()
    level_pen.write(
        f"Level: {level}",
        font=("Arial", 16, "bold")
    )

update_level()
#-------------------start menu-----------------
menu = turtle.Turtle()
menu.hideturtle()
menu.color("white")
menu.penup()
menu.goto(0, 0)

menu.write(
    "SPACE SHOOTER\n\nPress ENTER To Start",
    align="center",
    font=("Arial", 24, "bold")
)

started = False

def start_game():
    global started
    started = True
    menu.clear()

screen.listen()
screen.onkeypress(start_game, "Return")

while not started:
    screen.update()
#------------------Game over display-----------------
game_pen = turtle.Turtle()
game_pen.hideturtle()
game_pen.color("red")
# ---------------- PLAYER MOVEMENT ----------------
def move_left():

    x = player.xcor()
    x -= player_speed

    if x < -350:
        x = -350

    player.setx(x)

def move_right():

    x = player.xcor()
    x += player_speed

    if x > 350:
        x = 350

    player.setx(x)

# ---------------- FIRE BULLET ----------------
def fire_bullet():

    global bullet_state

    if bullet_state == "ready":

        bullet_state = "fire"
        bullet.color(random.choice(["yellow", "orange", "red"]))

        x = player.xcor()
        y = player.ycor() + 10

        bullet.goto(x, y)

        bullet.showturtle()

#---------------paused-----------------
def toggle_pause():
    global paused
    paused = not paused

screen.onkeypress(toggle_pause, "p")        

# ---------------- KEYBOARD ----------------
screen.listen()

screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")

# ---------------- COLLISION FUNCTION ----------------
def is_collision(t1, t2):

    distance = t1.distance(t2)

    if distance < 25:
        return True
    else:
        return False
# star loop
stars = []

for i in range(50):

    star = turtle.Turtle()

    star.shape("circle")

    star.color("white")

    star.shapesize(0.1,0.1)

    star.penup()

    star.speed(0)

    star.goto(random.randint(-400,400),
              random.randint(-300,300))

    stars.append(star)    
# ---------------- GAME LOOP ----------------
try:

    while not game_over:


        if paused:
            screen.update()
            continue

        
        # Boss activation
        if level == 5 and not boss_active:
            boss_active = True
            boss.showturtle()
        if boss_active:

           boss.setx(boss.xcor() + boss_speed)

           if boss.xcor() > 350 or boss.xcor() < -350:
              boss_speed *= -1
              boss.sety(boss.ycor() - 20)

        

        #Moving stars
        for star in stars:
            y=star.ycor()
            y-=1

            if y<-300:
                y=300

            star.sety(y)

        # Enemy movement
        for enemy in enemies:

            enemy.left(0.3)
            enemy.setx(enemy.xcor() + enemy.speed_value)
            
            #Right boundary
            if enemy.xcor() > 350:
                enemy.speed_value *= -1
                enemy.sety(enemy.ycor() - 40)

            #left boundary
            if enemy.xcor() < -350:
                enemy.speed_value *= -1
                enemy.sety(enemy.ycor() - 40)
        # Enemy reaches player
            if enemy.ycor() < -200:
                lives -= 1
                update_lives()
                enemy.goto(random.randint(-300,300), random.randint(150,250))
                if lives <=0:
                   game_over = True  
                   break      

            # collision with bullet
            if is_collision(bullet, enemy):

                bullet.hideturtle()
                bullet_state = "ready"
                bullet.goto(0, -400)
                #explosion Effect
                enemy.shape("explosion.gif")
                screen.update()
                turtle.delay(50)

                enemy.shape("enemy.gif")
                
                enemy.goto(random.randint(-300, 300), random.randint(150,250))
                score += 10
                update_score()

            # boss collision
            if boss_active and is_collision(bullet, boss):

               bullet.hideturtle()
               bullet_state = "ready"
               bullet.goto(0, -400)

               boss_health -= 1

               if boss_health <= 0:
                  boss.hideturtle()
                  game_over = True



        # Bullet movement
        if bullet_state == "fire":

            y = bullet.ycor()
            y += bullet_speed

            bullet.sety(y)
            bullet.shapesize(random.uniform(0.5, 0.8), random.uniform(1.2,1.8))

        # Bullet reset
        if bullet.ycor() > 300:

            bullet.hideturtle()

            bullet_state = "ready"
            bullet.goto(0, -400)

        # Collision
        if is_collision(bullet, enemy):

            # Hide bullet
            bullet.hideturtle()

            bullet_state = "ready"

            bullet.goto(0, -400)

            # Reset enemy
            enemy.goto(random.randint(-300, 300), 250)

            # Update score
            if  score % 100 == 0:
                level += 1
                update_level()

                for e in enemies:
                    if e.speed_value > 0:
                        e.speed_value += 1
                    else:
                        e.speed_value -= 1    
  
        
                 

        screen.update()
        turtle.delay(10)
        

except turtle.Terminator:

    print("Game Closed")

screen.update()

time.sleep(0.5)

game_pen = turtle.Turtle()
game_pen.hideturtle()
game_pen.penup()
game_pen.color("red")

game_pen.goto(0,0)
game_pen.write(
    "Game Over",
    align="center",
    font=("Arial", 36, "bold")
)

screen.update()

