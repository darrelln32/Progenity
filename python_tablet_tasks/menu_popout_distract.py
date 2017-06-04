import csv
import datetime
import random
import pygame
from pygame.locals import *
from Tkinter import *

# This program was design for training non-human primates on some basic tasks for neuroscience studies
# POPOUT Task with distractors
#
# This program run a training task where a box flashes on the screen.
# First, a menu appears to allow the user to set certain parameters for the task.
# The goal is to touch the box when the screen appears.
# When the box is touched, there is a delay period followed by another box that will flash with
#  5 other boxes that will be of a different color.
# If the second box is touched anong the other boxes,
# the primate receives an award via a hardware system to which the tablet is attached.
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
target_size.set(200)
target_outline = BooleanVar()
target_outline.set(True)
negative_feedback = BooleanVar()
negative_feedback.set(True)
fp_center = IntVar()
fp_center.set(800)
fp_range = IntVar()
fp_range.set(800)


# menu choices and its corresponding options
shapes = [("SQUARE",1), ("CIRCLE",2)]
outline = [("YES",True), ("NO",False)]
feedback = [("YES",True), ("NO",False)]

# set up frames to make them global, then i can grab the values from the variables
frame1 = Frame()
frame2 = Frame()
frame3 = Frame()
frame4 = Frame()
frame5 = Frame()
frame6 = Frame()

# grab the values and force the data tye once button is pressed
def execute_options():
    global r_value,g_value,b_value,shape,target_size,target_outline,negative_feedback, fp_center, fp_range
    r_value = int(r_value.get())
    g_value = int(g_value.get())
    b_value = int(b_value.get())
    shape = int(shape.get())
    target_size =  int(target_size.get())
    target_outline =  bool(target_outline.get())
    negative_feedback =  bool(negative_feedback.get())
    fp_center = int(fp_center.get())
    fp_range = int(fp_range.get())
    menu.destroy()

# menu function
def display_menu():
    global r_value,g_value,b_value,shape,target_size,target_outline,negative_feedback, fp_center, fp_range
    
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
    
    # label for target size
    Label(menu, text='Enter Target Size', padx = 10).pack()
    frame4.pack(fill=X)
    Label(frame4, text='Target Size',  padx = 10).pack(side='left')
    target_size=Entry(frame4,width=10)
    target_size.pack(side="left")
    target_size.insert(0,200)

    # label for target outline option
    Label(menu, text='Target Outline?', padx = 10).pack()
    for txt, val in outline:
        Radiobutton(menu, text=txt,padx = 10, variable=target_outline, value=val).pack(anchor=W)
    
    # label for negative feedback option
    Label(menu, text='Negative Feedback Response?',padx = 10).pack(anchor=W)
    for txt, val in feedback:
        Radiobutton(menu, text=txt,padx = 10, variable=negative_feedback, value=val).pack(anchor=W)

    # label for the fore period time length and the center
    # the user has the option to set a range of time intervals
    # as well as set the center time interval
    Label(menu, text='Fore Period Time Length?', padx = 10).pack()
    frame5.pack(fill=X)
    Label(frame5, text='Fore Period Center', padx = 10).pack(side = 'left')
    fp_center = Entry(frame5,width=10)
    fp_center.pack(side='left')
    fp_center.insert(0,800)
    
    frame6.pack(fill=X)
    Label(frame6, text='Fore Period Range', padx = 10).pack(side = 'left')
    fp_range = Entry(frame6,width=10)
    fp_range.pack(side='left')
    fp_range.insert(0,800)

    # label for the button to start the task once data is gathered
    b = Button(menu, text ="Start Task", command = execute_options)
    b.pack()
    
    # this starts the menu
    mainloop()

# set up for sound
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
grey = pygame.Color(174,202,212,255)

# data collection lists
trial_start_times = list()
center_target_selected_times = list()
popout_target_selected_times = list()
popout_start_times = list()
center_target_react_times = list()
popout_target_react_times = list()
popout_intervals = list()
results = list()
durations = list()
loc_x = list()
loc_y = list()
popout_box = list()

# set up some variables before entering loops
color = black
start_game = True
correct_choice = False
missed_box = False
pl = 'None'
popout_interval = 0

# disable mouse functions to allow for only 1 function when ready
pygame.event.set_blocked(pygame.MOUSEMOTION)
pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
pygame.event.set_blocked(pygame.MOUSEBUTTONUP)

#timer and time variables
timer = USEREVENT
timer_on = 2300
timer_off = 0
trial_start_time = 0
center_target_selected_time = 0
popout_start_time = 0
popout_target_selected_time = 0
center_target_react_time = 0
popout_target_react_time = 0
end_time = 0

# special trial counter for debug purposes
trials = 0

# print user choices for debug purposes
print r_value, ',', g_value, ',', b_value
print shape
print target_size
print target_outline
print negative_feedback
print fp_center,',', fp_range

# set the user-defined color and the shape
tile_color = pygame.Color(r_value,g_value,b_value,255)
param_color = '(R = ' + str(r_value) + ', G = ' + str(g_value) + ', B = ' + str(b_value) + ')'
if shape is 1:
    shape = 'square'
else:
    shape = 'circle'

# create a list of random popout_intervals
start_end_range_num = fp_range / 2
random_popout_intervals = range(fp_center - start_end_range_num, fp_center + start_end_range_num + 100, 100)
if fp_center not in random_popout_intervals:
    random_popout_intervals.append(fp_center)
    random_popout_intervals.sort()

# print out the random popout intervals and a choice for debug purposes
print random_popout_intervals
print random.choice(random_popout_intervals)


# manipulating strings for output file
date = str(datetime.datetime.now().date())
time = str(datetime.datetime.now().time()).replace(':','_')
time = time.replace('.','_')
filename_str = 'c:\RESULTS\POPOUT_distractors__' + date + '__' + time + '.csv'


# the center and radius for each ball
circle_radius = 50
target_radius = target_size / 2
center =[ [400,640],[700,640],[550,345],[250,345],[100,640],[250,940],[550,940] ]

# define the boxes to be touched/to be distractorscenter_box = pygame.Rect(350,590,100,100)
center_box = pygame.Rect(350,590,100,100)
box_1 = pygame.Rect(650,590,100,100)
box_4 = pygame.Rect(50,590,100,100)
box_5 = pygame.Rect(200,890,100,100)
box_3 = pygame.Rect(200,295,100,100)
box_6 = pygame.Rect(500,890,100,100)
box_2 = pygame.Rect(500,295,100,100)
    
# define target boxes
target_center_box = pygame.Rect(center[0][0]-(target_size/2), center[0][1]-(target_size/2),target_size,target_size)
target_1 = pygame.Rect(center[1][0]-(target_size/2), center[1][1]-(target_size/2),target_size,target_size)
target_4 = pygame.Rect(center[4][0]-(target_size/2), center[4][1]-(target_size/2),target_size,target_size)
target_5 = pygame.Rect(center[5][0]-(target_size/2), center[5][1]-(target_size/2),target_size,target_size)
target_3 = pygame.Rect(center[3][0]-(target_size/2), center[3][1]-(target_size/2),target_size,target_size)
target_6 = pygame.Rect(center[6][0]-(target_size/2), center[6][1]-(target_size/2),target_size,target_size)
target_2 = pygame.Rect(center[2][0]-(target_size/2), center[2][1]-(target_size/2),target_size,target_size)

# defineregular circles
center_circle = pygame.Rect(center[0][0]-circle_radius, center[0][1]-circle_radius, circle_radius*2, circle_radius*2)
circle_1 = pygame.Rect(center[1][0]-circle_radius, center[1][1]-circle_radius, circle_radius*2, circle_radius*2)
circle_4 = pygame.Rect(center[4][0]-circle_radius, center[4][1]-circle_radius, circle_radius*2, circle_radius*2)
circle_5 = pygame.Rect(center[5][0]-circle_radius, center[5][1]-circle_radius, circle_radius*2, circle_radius*2)
circle_3 = pygame.Rect(center[3][0]-circle_radius, center[3][1]-circle_radius, circle_radius*2, circle_radius*2)
circle_6 = pygame.Rect(center[6][0]-circle_radius, center[6][1]-circle_radius, circle_radius*2, circle_radius*2)
circle_2 = pygame.Rect(center[2][0]-circle_radius, center[2][1]-circle_radius, circle_radius*2, circle_radius*2)
    
# define target circles
target_center = pygame.Rect(center[0][0]-target_radius, center[0][1]-target_radius, target_radius*2, target_radius*2)
circle_target_1 = pygame.Rect(center[1][0]-target_radius, center[1][1]-target_radius, target_radius*2, target_radius*2)
circle_target_4 = pygame.Rect(center[4][0]-target_radius, center[4][1]-target_radius, target_radius*2, target_radius*2)
circle_target_5 = pygame.Rect(center[5][0]-target_radius, center[5][1]-target_radius, target_radius*2, target_radius*2)
circle_target_3 = pygame.Rect(center[3][0]-target_radius, center[3][1]-target_radius, target_radius*2, target_radius*2)
circle_target_6 = pygame.Rect(center[6][0]-target_radius, center[6][1]-target_radius, target_radius*2, target_radius*2)
circle_target_2 = pygame.Rect(center[2][0]-target_radius, center[2][1]-target_radius, target_radius*2, target_radius*2)
    

# set the user-defined default value
current_target = target_center
current_shape = center_box


# set up the the shape arrays according to the chosen shape
if shape is 'circle':
    shapes = [circle_1,circle_2,circle_3,circle_4,circle_5,circle_6]
    targets = [circle_target_1,circle_target_2,circle_target_3,circle_target_4,circle_target_5,circle_target_6]
elif shape is 'square':
    shapes = [box_1,box_2,box_3,box_4,box_5,box_6]
    targets = [target_1,target_2,target_3,target_4,target_5,target_6]

# function to set up the current shape and target for the upcoming trial
def set_target_and_shape(current_target,current_shape):
    if shape is 'circle':
        current_target = target_center
        current_shape = center_circle
    elif shape is 'square':
        current_target = target_center_box
        current_shape = center_box
    return current_target, current_shape
    
# function to draw the current shape and target from the trial
def draw_shape():
    if shape is 'circle':
        if target_outline:
            pygame.draw.circle(display,color,current_target.center,target_radius,1)
        else:
            pygame.draw.circle(display,black,current_target.center,target_radius)
        pygame.draw.circle(display,color,current_shape.center,circle_radius)
    elif shape is 'square':
        if target_outline:
            pygame.draw.rect(display,color,current_target,1)
        else:
            pygame.draw.rect(display,black,current_target)
        pygame.draw.rect(display,color,current_shape)

# functionm to draw the distractor boxes
def draw_distractors():
    for sha in shapes:
        if sha is current_shape: continue
        if shape is 'circle':
            pygame.draw.circle(display,grey,sha.center,circle_radius)
        elif shape is 'square':
            pygame.draw.rect(display,grey,sha)

# function to draw the correct negative feedback screen color
# if negative feedback was chosen
def draw_feedback():
    if negative_feedback:
        color = red
    else:
        color = black
    pygame.draw.rect(display,color,whole_screen)

# start game!
pygame.init()
pygame.time.set_timer(timer,timer_on)

# while loop for the continuous running screen for the game
while running:
    event = pygame.event.poll()
    if event.type == pygame.QUIT:
        running = 0
        # grab stop time
        stop_time = str(datetime.datetime.now().time()).replace(':','_')
        stop_time = stop_time.replace('.','_')
        # write data to output file
        with open(filename_str,'w') as output_csv:
            writer = csv.DictWriter(output_csv,fieldnames = ['TASK','DATE','START','END'])
            writer.writeheader()
            writer.writerow({'TASK':'Popout with Distractors','DATE':date,'START':time,'END':stop_time})
            output_csv.write('\n')
            writer = csv.DictWriter(output_csv,fieldnames = ['R','G','B','SHAPE','TARGET SIZE','TARGET OUTLINE','NEGATIVE FEEDBACK','FORE PERIOD CENTER','FORE PERIOD RANGE'])
            writer.writeheader()
            writer.writerow({'R':r_value,'G':g_value,'B':b_value,'SHAPE':shape,'TARGET SIZE':target_size,'TARGET OUTLINE':target_outline,'NEGATIVE FEEDBACK':negative_feedback,'FORE PERIOD CENTER':fp_center,'FORE PERIOD RANGE':fp_range})
            output_csv.write('\n')
            writer = csv.DictWriter(output_csv,fieldnames = ['Trial Start','Center Target Selected','Center Target React','Popout Start','Popout Target Selected','Popout Target React','Popout Box','Intermediate Interval','X-Coord','Y-Coord','Result'])
            writer.writeheader()
            for row in range(0,len(results),1):
                writer.writerow({'Trial Start':trial_start_times[row],'Center Target Selected':center_target_selected_times[row],'Center Target React':center_target_react_times[row],'Popout Start':popout_start_times[row],'Popout Target Selected':popout_target_selected_times[row],'Popout Target React':popout_target_react_times[row],'Popout Box':popout_box[row],'Intermediate Interval':popout_intervals[row],'X-Coord':loc_x[row],'Y-Coord':loc_y[row],'Result':results[row]})

    # start main cycle.  display box for 3 seconds
    # grab the input from the mouse
    # determine whether the box was touched or missed or if the trial was aborted
    # this section is not executed in between trials
    #
    # at beginning of trial, if box is touched, the next box that will appear
    # is the popout box along with the distractor boxes. from here we will determine the outcome of the trial once
    # action is taken (abort, error or correct choice)

    # start game determines if we need to display the popout box or the main center box
    # for this pass thru in the loop
    if start_game:
        current_target, current_shape = set_target_and_shape(current_target,current_shape)
        correct_choice = False
        
    draw_shape()
    if (event.type == pygame.MOUSEBUTTONUP and event.button == left):
        end_time = pygame.time.get_ticks()
        mouse_location = pygame.mouse.get_pos()
        pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
        if current_target.collidepoint(mouse_location) and ((display.get_at(mouse_location) == tile_color) or  (display.get_at(mouse_location) == black)):
            if start_game:
                center_target_selected_time = end_time
                pygame.draw.rect(display,black,whole_screen)
                current_shape = random.choice(shapes)
                pl = shapes.index(current_shape)
                current_target = targets[pl]
                start_game = False
                # make the program wait before displaying the popout box (popout interval times will be from a random list)
                popout_interval = random.choice(random_popout_intervals)
                pygame.time.wait(popout_interval)
                draw_distractors()
                pygame.time.set_timer(timer,timer_off)
                pygame.time.set_timer(timer,timer_on)
                # get the popout_start_time
                popout_start_time = pygame.time.get_ticks()
                pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
            elif not start_game:
                popout_target_selected_time = end_time
                sound.play()
                pygame.time.wait(2500)
                pygame.draw.rect(display,black,whole_screen)
                pygame.display.flip()
                correct_choice = True
        else:
            missed_box = True
            if start_game:
                center_target_selected_time = end_time
            elif not start_game:
                popout_target_selected_time = end_time
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
            center_target_react_time = center_target_selected_time - trial_start_time
            popout_target_react_time = popout_target_selected_time - popout_start_time
            if correct_choice:
                print 'correct'
                result = 'correct'
            elif missed_box:
                print 'error'
                result = 'error'
                if start_game:
                    popout_start_time = 0
                    popout_target_selected_time = 0
                    popout_target_react_time = 0
                    #mouse_location = ('None','None')
                    pl = 'None'
                    popout_interval = 'None'
            else:
                print 'abort'
                result = 'abort'
                popout_target_selected_time = 0
                popout_target_react_time = 0
                mouse_location = ('None','None')
                if start_game:
                    center_target_selected_time = 0
                    center_target_react_time = 0
                    popout_start_time = 0
                    pl = 'None'
                    popout_interval = 'None'
            # send data to lists
            trial_start_times.append(trial_start_time)
            center_target_selected_times.append(center_target_selected_time)
            popout_start_times.append(popout_start_time)
            popout_target_selected_times.append(popout_target_selected_time)
            center_target_react_times.append(center_target_react_time)
            popout_target_react_times.append(popout_target_react_time)
            popout_intervals.append(popout_interval)
            loc_x.append(mouse_location[0])
            loc_y.append(mouse_location[1])
            if pl is not 'None':
                pl = int(pl) + 1                    # add 1 to the index so the boxes read normally in the output (1,2,3,4,5,6)
            popout_box.append(pl)
            results.append(result)
            trials += 1
            print 'interval = ', popout_interval
            print 'trial # ', trials
            # set start_game to prepare for next trial
            start_game = True
        else:
            color = tile_color
            pygame.event.set_allowed(pygame.MOUSEBUTTONUP)
            trial_start_time = pygame.time.get_ticks()
        # get ready for the next game
        correct_choice = False
        missed_box = False
        pygame.time.set_timer(timer,timer_on)

    pygame.display.flip()


