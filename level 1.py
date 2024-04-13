import turtle
import random

score = 0
lives = 5

wn = turtle.Screen()
wn.title("Catch the letter")
wn.bgcolor("black")
wn.setup(width=2515, height=1536)
wn.tracer(0)

wn.register_shape("harry.png")
wn.register_shape("letter.png")
wn.register_shape("uncle.png")

# Player
player = turtle.Turtle()
player.speed(20)
#player.shape("harry.png")
player.color("white")
player.penup()
player.goto(0, -250)
player.direction = "stop"

#Create a list of letters
letterS = []

# Good Guys
for _ in range(20):
    letter = turtle.Turtle()
    letter.speed(0)
    letter.shape("letter.png")
    letter.color("blue")
    letter.penup()
    letter.goto(-500, 250)
    letter.speed = random.randint(1,4)
    letterS.append(letter)

#Create a list of bad guys
uncleS = []

#Bad Guys
for _ in range(20):
    uncle = turtle.Turtle()
    uncle.speed(0)
    uncle.shape("circle")
    uncle.color("red")
    uncle.penup()
    uncle.goto(500, 250)
    uncle.speed = random.randint(1,4)
    uncleS.append(uncle)

#Make the pen
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.shape("uncle.png")
pen.color("white")
pen.penup()
pen.goto(0, 260)
font = ("Courier", 24, "normal")
pen.write("Score: {} Lives: {}".format(score, lives), align = "center", font = font)

# Functions
def go_left():
    player.direction = "left"

def go_right():
    player.direction = "right"

def stop_left():
    player.direction = "stop"

def stop_right():
    player.direction = "stop"


# Keyboard
wn.listen()
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")
wn.onkeyrelease(stop_left, "Left")
wn.onkeyrelease(stop_right, "Right")


while True:
    if lives <= 0:
        break
    wn.update()

    # Move Player
    if player.direction == "left":
        x = player.xcor()
        x -= 1
        player.setx(x)
    elif player.direction == "right":
        x = player.xcor()
        x += 1
        player.setx(x)

    # Move the good guy
    for letter in letterS:
        y = letter.ycor()
        y -= letter.speed - 0.9
        letter.sety(y)

        # Check if off the screen
        if y < -300:
            x = random.randint(-380, 380)
            y = random.randint(300, 400)
            letter.goto(x, y)
            score += 1
            pen.clear()
            pen.write("Score: {} Lives: {}".format(score, lives), align="center", font=font)

        # Check for collision with player
        if letter.distance(player) < 20:
            x = random.randint(-380, 380)
            y = random.randint(300, 400)
            letter.goto(x, y)

    # Move the bad guy
    for uncle in uncleS:
        y = uncle.ycor()
        y -= uncle.speed - 0.9
        uncle.sety(y)

        # Check if off the screen
        if y < -300:
            x = random.randint(-380, 380)
            y = random.randint(300, 400)
            uncle.goto(x, y)

        # Check for collision with player
        if uncle.distance(player) < 20:
            x = random.randint(-380, 380)
            y = random.randint(300, 400)
            uncle.goto(x, y)
            score -= 1
            lives -= 1
            pen.clear()
            pen.write("Score: {} Lives: {}".format(score, lives), align="center", font=font)

    # Add this code after the game loop

# Clear the screen
wn.clear()

# Create a semi-transparent overlay to darken the background
overlay = turtle.Turtle()
overlay.hideturtle()
overlay.speed(0)
overlay.color("black")
overlay.penup()
overlay.goto(-wn.window_width() / 2, -wn.window_height() / 2)
overlay.begin_fill()
for _ in range(2):
    overlay.forward(wn.window_width())
    overlay.left(90)
    overlay.forward(wn.window_height())
    overlay.left(90)
overlay.end_fill()

# Display "Game Over" in the middle of the screen
game_over_text = turtle.Turtle()
game_over_text.hideturtle()
game_over_text.speed(0)
game_over_text.color("white")
game_over_text.penup()
game_over_text.goto(0, 0)
game_over_text.write("Game Over", align="center", font=("Courier", 48, "bold"))

# Update the display
wn.update()

# Keep the window open until the user closes it
wn.mainloop()

    
wn.mainloop()


