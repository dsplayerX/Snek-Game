from tkinter import *
import random
import time

GAME_WIDTH = 600
GAME_HEIGHT = 600
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOUR = "#333333"
FOOD_COLOUR = "#de0713"
BACKGROUND_COLOR = "#8cb281"

snake_speed = 100

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x + 1.5, y + 1.5, x + SPACE_SIZE - 1.5, y + SPACE_SIZE - 1.5, fill=SNAKE_COLOUR, tag="snake")
            self.squares.append(square)


class Food:

    def __init__(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        canvas.create_oval(x + 5, y + 5, x + SPACE_SIZE - 5, y + SPACE_SIZE - 5, fill=FOOD_COLOUR, outline=FOOD_COLOUR, tag="food")


def next_turn(snake, food):

    global snake_speed
    
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x + 1.5, y + 1.5, x + SPACE_SIZE - 1.5, y + SPACE_SIZE - 1.5, fill=SNAKE_COLOUR, outline=SNAKE_COLOUR)

    snake.squares.insert(0, square)

    if (x == food.coordinates[0]) and (y == food.coordinates[1]):

        global score

        score += 1
        
        label.config(text="Score:{} ".format(score))

        canvas.delete("food")

        food = Food()

    else: 
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        global highscore

        if score > highscore:
            highscore = score

        window.after(350)

        game_over()
        
        window.after(3000, start_game)
    
    else:
        window.after(snake_speed, next_turn, snake, food)


def change_direction(new_direction):
    
    global direction
    
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction


def check_collisions(snake):
    
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
     

def game_over():
    global score
    global highscore

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/3.5, font=("arial", 60, "bold"), text="GAME OVER!", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("arial", 36), text="Your Score: {}".format(score), fill="white", tag="yourscore")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.5, font=("arial", 24), text="High Score: {}".format(highscore), fill="white", tag="highscore")

    gamestart_string = "Game will restart in... "
    county = canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.2, font=("arial", 14), text=gamestart_string, fill="white", tag="gamestart")

    count_string = "3 2 1"
    #Time delay in milliseconds
    delta = 500 
    delay = 0
    for i in range(len(count_string) + 1):
        s = count_string[:i]
        update_text = lambda s=s: canvas.itemconfigure(county, text=gamestart_string + s)
        canvas.after(delay, update_text)
        delay += delta


def start_game():

    global score
    global direction

    canvas.delete(ALL)

    score = 0
    direction = 'down'

    label.config(text="Score:{}".format(score))

    snake = Snake()
    food = Food()

    next_turn(snake, food)


def stop_game():

    window.destroy()


window = Tk()
window.title("Snek Game")
window.resizable(False, False)

score = 0
highscore = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font=('arial', 40))
label.pack()

button = Button(window, text= "Quit", font=("arial",12), command=stop_game, bg="#2d2e2e", fg="#F5F5F5")
button.place(x = 520, y = 20)

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Keybinds
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))

# Alternate Keybinds
window.bind('<w>', lambda event: change_direction('up'))
window.bind('<s>', lambda event: change_direction('down'))
window.bind('<a>', lambda event: change_direction('left'))
window.bind('<d>', lambda event: change_direction('right'))

start_game()

window.mainloop()