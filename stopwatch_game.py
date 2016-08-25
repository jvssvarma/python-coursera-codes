# template for "Stopwatch: The Game"
import simplegui
# define global variables
tens = 0
success = 0
count_start = 0
count_stop = 0
minute = 0
second = 0
t = 0
present_status = 0
interval = 100
# define helper function format that converts integer
# counting tens of second into formatted string A:BC.D
def format(t):
    minute = str(tens/600)
    t = str(tens % 10)
    second = tens/10
    if second < 10:
        second = "0"+str(tens/10)
    else:
        second = str(tens/10)
    return minute+":"+second+"."+t+"   "+str(success)+"/"+str(count_stop)
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global count_start,present_status
    if present_status == 0:
        count_start += 1
        present_status = 1
        timer.start()
    
def stop():
    global count_stop,present_status,success
    if present_status == 1:
        present_status = 0
        count_stop += 1
        timer.stop()
        if tens % 10 == 0:
            success +=1

def reset():
    global minute, second, present_status, t, tens, count_start,count_stop,success
    minute = 0
    second = 0
    t = 0
    success = 0
    count_start = 0
    count_stop = 0
    tens = 0
    present_status = 0
    timer.stop()

# define event handler for timer with 0.1 sec interval
def tick_handler():
    global tens
    tens += 1

    
def draw(canvas):
    canvas.draw_text(format(t), [20,102], 35, "White")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 200)
# register event handlers
start_button = frame.add_button("Start", start)
stop_button = frame.add_button("Stop", stop)
reset_button = frame.add_button("Reset", reset)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval, tick_handler)

# start timer and frame
frame.start()

# remember to review the grading rubric