# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console
import random
import simplegui
import math
# initialize global variables used in your code
range_limit = 100
secret_number = random.randint(0,100)
max_guess = math.ceil(math.log(range_limit+1,2))

def new_game():
    
    # initialize global variables used in your code here
    global secret_number
    secret_number = random.randrange(0,limit)
        
def range100():
    global range_limit,secret_number,max_guess
    range_limit = 100
    secret_number = random.randint(0,100)
    max_guess = math.ceil(math.log(range_limit+1,2))
    print "New game. Enter guess between 0 and 100."
    print "Number of remaining guesses ", max_guess, "\n"
    # button that changes range to range [0,100) and restarts

def range1000():
    global range_limit,secret_number,max_guess
    secret_number = random.randint(0,1000)
    range_limit = 1000
    max_guess = math.ceil(math.log(range_limit+1,2))
    print "New game. Enter guess between 0 and 1000."
    print "Number of remaining guesses ", max_guess, "\n"
    # button that changes range to range [0,1000) and restarts
    
def input_guess(guess):
    global max_guess,secret_number
    max_guess-=1
    cnvtd_guess = int(guess)
    print "Guess was",guess
    if cnvtd_guess < secret_number:
        print "Higher"
    elif cnvtd_guess > secret_number:
        print "Lower."
    elif cnvtd_guess == secret_number:
        print "Correct."
    
    if max_guess > 0:
        print "You have",max_guess,"guesses left.\n"
    else:
        print "You have no remaining guesses. Let's start again\n"
        max_guess = math.ceil(math.log(range_limit+1,2))
        secret_number = random.randint(0,range_limit)


    # main game logic goes here	

    
# create frame
frame = simplegui.create_frame("Game", 200, 200)

# register event handlers for control elements
game1 = frame.add_button("Range: 0 - 100", range100)
game2 = frame.add_button("Range: 0 - 1000", range1000)
inp = frame.add_input("Enter guess", input_guess, 100)

# start frame
print "New game. Enter guess between 0 and 100."
print "Number of remaining guesses 7.0\n"
frame.start()

# always remember to check your completed program against the grading rubric