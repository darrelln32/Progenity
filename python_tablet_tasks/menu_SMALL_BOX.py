import csv
import datetime
import random
import pygame
from pygame.locals import *
from Tkinter import *

# This program was design for training non-human primates on some basic tasks for neuroscience studies
# SMALL BOX
#
# this program run a training task where a box flashes on the screen.
# First, a menu appears to allow the user to set certain parameters for the task.
# The goal is to touch the box when the screen appears.
# If the box is touched, the primate receives an award via a hardware system to which the tablet is attached.
# This will repeat over and over until the program is closed.
# The program keeps the result of each trial and records them to a CSV file once the program is done

#set the menu object and size
menu = Tk()
menu.geometry('400x500')

# set up variables for menu
r_value = IntVar()
r_value.set(255)
g_value = IntVar()
g_value.set(255)
b_value = IntVar()
b_value.set(255)
shape  = IntVar()
shape.set(1)
target_size = IntVar()
target_size.set(400)
target_outline = BooleanVar()
target_outline.set(True)
negative_feedback = BooleanVar()
negative_feedback.set(True)


# menu choices and its corresponding options
shapes = [("SQUARE",1), ("CIRCLE",2)]
outline = [("YES",True), ("NO",False)]
feedback = [("YES",True), ("NO",False)]

# set up frames to make them global, then i can grab the values from the variables
frame1 = Frame()
frame2 = Frame()
frame3 = Frame()
frame4 = Frame()

# grab the values and force the data type once button is pressed
def execute_options():
    global r_value,g_value,b_value,shape,target_size,target_outline,negative_feedback
    r_value = int(r_value.get())
    g_value = int(g_value.get())
    b_value = int(b_value.get())
    shape = int(shape.get())
    target_size =  int(target_size.get())
    target_outline =  bool(target_outline.get())
    negative_feedback =  bool(negative_feedback.get())
    menu.destroy()

# menu function
def display_menu():
    global r_value,g_value,b_value,shape,target_size,target_outline,negative_feedback

    # label for RGB colors
    Label(menu, text='Enter RGB color values',padx = 10).pack()
    
    # set up menu for entering the RGB colors
    frame1.pack(fill=X)
    Label(frame1, text='R value',padx=10).pack(side='left')
    r_value=Entry(frame1,width=10)
    r_value.pack(side="left")
    r_value.insert(0,255)
    
    frame2.pack(fill=X)
    Label(frame2, text='G value',padx=10).pack(side='left')
    g_value=Entry(frame2,width=10)
    g_value.pack(side="left")
    g_value.insert(0,255)
    
    frame3.pack(fill=X)
    Label(frame3, text='B value',padx=10).pack(side='left')
    b_value=Entry(frame3,width=10)
    b_value.pack(side="left")
    b_value.insert(0,255)
    
    # label for shape
    Label(menu, text='Choose Shape',padx = 10).pack()
    for txt, val in shapes:
        Radiobutton(menu, text=txt,padx = 10, variable=shape, value=val).pack(anchor=W)

    #label for target size
    Label(menu, text='Enter Target Size', padx = 10).pack()
    frame4.pack(fill=X)
    Label(frame4, text='Target Size',  padx = 10).pack(side='left')
    target_size=Entry(frame4,width=10)
    target_size.pack(side="left")
    target_size.insert(0,400)

    #label for target outline option
    Label(menu, text='Target Outline?', padx = 10).pack()
    for txt, val in outline:
        Radiobutton(menu, text=txt,padx = 10, variable=target_outline, value=val).pack(anchor=W)

    # label for negative feedback option
    Label(menu, text='Negative Feedback Response?',padx = 10).pack(anchor=W)
    for txt, val in feedback:
        Radiobutton(menu, text=txt,padx = 10, variable=negative_feedback, value=val).pack(anchor=W)


    # button to start task
    b = Button(menu, text ="Start Task", command = execute_options)
    b.pack()
    
    mainloop()


#set up for sound
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)
sound = pygame.mixer.Sound('c:\INPUT_FILES\Air_Plane_Ding.ogg')

# display the menu and grab the choices from the user
display_menu()


# set up background and variables for main loop
running = 1
left = 1
display = pygame.display.set_mode((800,1280))
display.fill((0,0,0))

# whole screen
whole_screen = pygame.Rect(0,0,800,1280)

# colors
cyan = pygame.Color(97,240,242,255)
black = pygame.Color(0,0,0,255)
magenta = pygame.Color(255,0,217,255)
red = pygame.Color(255,0,0,255)
orange = pygame.Color(255,187,0,255)

# data collection lists
target_start_times = list()
target_selected_times = list()
results = list()
target_react_times = list()
loc_x = list()
loc_y = list()

# set up some variables before entering loops
color = black
missed_box = False
correct_choice = False


# disable mouse functions to allow for only 1 function when ready
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
pygame.event.set_blocked(pygame.MOUSEBUTTONUP)


#timer and time variables
timer = USEREVENT
timer_on = 3000
timer_off = 0
target_start_time = 0
target_selected_time = 0

# trials:  variable for debug purposes
trials = 0

# print user choices for debug purposes
print r_value, ',', g_value, ',', b_value
print shape
print target_size
print target_outline
print negative_feedback

#set the user-defined color and the shape
tile_color = pygame.Color(r_value,g_value,b_value,255)
if shape is 1:
    shape = 'square'
else:
    shape = 'circle'


# manipulating strings for output file
date = str(datetime.datetime.now().date())
time = str(datetime.datetime.now().time()).replace(':','_')
time = time.replace('.','_')
filename_str = 'c:\RESULTS\SMALL_BOX__' + date + '__' + time + '.csv'


# set the box size and the radius size
circle_radius = 100
target_radius = target_size / 2
center = [400,640]


# box and its target area
square = pygame.Rect(300,540,200,200)
square_target = pygame.Rect(center[0]-(target_size/2), center[1]-(target_size/2),target_size,target_size)


#circle and its target area
circle = pygame.Rect(center[0]-circle_radius, center[1]-circle_radius, circle_radius*2, circle_radius*2)
circle_target = pygame.Rect(center[0]-target_radius, center[1]-target_radius, target_radius*2, target_radius*2)


# set up the the shape arrays according to the chosen shape
if shape is 'circle':
    target = circle_target
else:
    target = square_target

#function to draw the user-defined shape
def draw_shape():
    if shape is 'circle':
        if target_outline:
            pygame.draw.circle(display,color,target.center,target_radius,1)
        else:
            pygame.draw.circle(display,black,target.center,target_radius)
        pygame.draw.circle(display,color,circle.center,circle_radius)
    elif shape is 'square':
        if target_outline:
            pygame.draw.rect(display,color,target,1)
        else:
            pygame.draw.rect(display,black,target)
        pygame.draw.rect(display,color,square)

# function to implement option of negative feedback
def draw_feedback():
    if negative_feedback:
        color = red
    else:
        color = black
    pygame.draw.rect(display,color,whole_screen)

# start game!
pygame.init()
pygame.time.set_timer(timer, timer_on)

# while loop for the continuous running screen for the game
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
        # grab stop time from system
        stop_time = str(datetime.datetime.now().time()).replace(':','_')
        stop_time = stop_time.replace('.','_')
        # send data to output file
        with open(filename_str,'w') as output_csv:
            writer = csv.DictWriter(output_csv,fieldnames = ['TASK','DATE','START','END'])
            writer.writeheader()
            writer.writerow({'TASK':'SMALL BOX','DATE':date,'START':time,'END':stop_time})
            output_csv.write('\n')
            writer = csv.DictWriter(output_csv,fieldnames = ['R','G','B','SHAPE','TARGET SIZE','TARGET OUTLINE','NEGATIVE FEEDBACK'])
            writer.writeheader()
            writer.writerow({'R':r_value,'G':g_value,'B':b_value,'SHAPE':shape,'TARGET SIZE':target_size,'TARGET OUTLINE':target_outline,'NEGATIVE FEEDBACK':negative_feedback})
            output_csv.write('\n')
            writer = csv.DictWriter(output_csv,fieldnames = ['Target Start','Target Selected','Target React','X-coord','Y-coord','Result'])
            writer.writeheader()
            for row in range(0,len(results),1):
                writer.writerow({'Target Start':target_start_times[row],'Target Selected':target_selected_times[row],'Target React':target_react_times[row],'X-coord':loc_x[row],'Y-coord':loc_y[row],'Result':results[row]})
    
    # start main cycle.  display box for 3 seconds
    # grab the input from the mouse
    # determine whether the box was touched or missed or if the trial was aborted
    # this section is not executed in between trials
    draw_shape()
    if (event.type == pygame.MOUSEBUTTONUP and event.button == left):
        target_selected_time = pygame.time.get_ticks()
        mouse_location = pygame.mouse.get_pos()
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        if target.collidepoint(mouse_location) and ((display.get_at(mouse_location) == tile_color) or  (display.get_at(mouse_location) == black)):
            sound.play()
            pygame.time.wait(2500)
            pygame.draw.rect(display,black,whole_screen)
            pygame.display.flip()
            correct_choice = True
        else:
            missed_box = True
            draw_feedback()
            pygame.display.flip()
            pygame.time.wait(2500)
            pygame.draw.rect(display,black,whole_screen)

    # draw black screen
    if correct_choice or missed_box:
        pygame.draw.rect(display,black,whole_screen)

    # events for expired timer
    # record the results of the trial (correct, error, abort)
    # reset variables for the next trial
    if event.type == timer:
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        if color is tile_color:
            color = black
            pygame.draw.rect(display,black,whole_screen)
            target_react_time = target_selected_time - target_start_time
            if correct_choice:
                print 'correct'
                result = 'correct'
            elif missed_box:
                print 'error'
                result = 'error'
            else:
                print 'abort'
                result = 'abort'
                target_selected_time = 0
                target_react_time = 0
                mouse_location = ('None','None')
            # send data to lists
            target_start_times.append(target_start_time)
            target_selected_times.append(target_selected_time)
            target_react_times.append(target_react_time)
            loc_x.append(mouse_location[0])
            loc_y.append(mouse_location[1])
            results.append(result)
            trials += 1
            print 'trial #  ', trials
        else:
            color = tile_color
            pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
            target_start_time = pygame.time.get_ticks()
        # get ready for the next game
        correct_choice = False
        missed_box = False
        pygame.time.set_timer(timer,timer_on)

    pygame.display.flip() 