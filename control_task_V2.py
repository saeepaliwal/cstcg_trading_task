# -*- coding: utf-8 -*-    
from __future__ import division
from choice_task import ChoiceTask
import pygame
from pygame.locals import *
from control_task_V2_functions import *
import random
import numpy
import pygbutton
import pdb

# Three sections of this experiment 
# Bigger is better, but if you feed the globs too much, they get sick and lose weight
# 
# Why would you pick? You are an expert--farm globs are controlled for pesticides 
# so you want to be able to tell which are which
# Secton 1: You are trained on farm fish and freshwater fish
# Section 2: You are told to watch the marketplace and pick which are farm and which are fresh globs
# Section 3: You are in full control of the farm 
# 

# Define special characters
ae = u"ä";
ue = u"ü";
NUM_TRIALS=5

c = ChoiceTask()
(subjectname) = c.subject_information_screen()
subject = subjectname.replace(" ","")
c.create_output_file(subjectname)
c.blank_screen()

scale = 100
offset_farm = 200
offset_fresh = 100

# Section to run:
section = [1,2,3,4]

# Section 1: Training on farm globs and fresh-water globs
if 1 in section:
    c.log("Training on different distributions.")
    c.blank_screen()
    c.make_banner(c.header.render("Raising globs!", True, c.header_color))
    c.text_screen("Globs are delightful creatures that garner big bucks at the local market. You're interested in learning more about globs and glob farming as a new career path. Before you can start as an apprentice at the farm, you have to know the difference between fresh globs and farm globs. The farmer puts you to the test. Decide which of the following globs are fresh globs and which are farm globs. Farm globs tend to be slight larger and more homogenous. Fresh globs tend to be more erratic in size.", valign='top', wait_time=1)
    

    continue_button = pygbutton.PygButton(rect=(c.center_x-80,c.bottom_y+150, 200,80),\
    caption="Continue", fgcolor=c.button_color, bgcolor=c.background_color, font=c.button)

    continue_button.draw(c.screen)
    pygame.display.update()
    continue_task = False
    while not continue_task:
        for event in pygame.event.get():
            if 'click' in continue_button.handleEvent(event): 
                continue_button.buttonDown = True;
                continue_task=True
            
    continue_button.draw(c.screen)
    pygame.display.update()   
    c.attn_screen(wait_time=1000)

    # Farm and fresh globs
    # Farm globs = lognormal with an offset of 200 pixels
    # Fresh globs = uniformly distributed with an offset of 100 pixels
   
    
    # One image, two coices
    # Two choices, farm or fresh
    for i in range(NUM_TRIALS):
        c.blank_screen()

        if is_odd(i): #farm
            r_glob_frac = sigmoid(numpy.random.normal(logit(0.5),1))
            r_glob = int(round(r_glob_frac*scale)) + offset_farm
        else: #fresh
            r_glob_frac = numpy.random.beta(1,1)
            r_glob = int(round(r_glob_frac*scale)) + offset_fresh
        draw_glob(c,r_glob, c.center_x, c.center_y)

        button = c.choice_screen(button_txt1="Farm",  button_txt2="Fresh")
        # Write process choice function
        if is_odd(i):
            correct = process_choice_training(c, button, r_glob,'farm')
        else:
            correct = process_choice_training(c, button, r_glob,'fresh')

        if correct:
            c.blank_screen()
            c.text_screen("Correct answer! Well done!", valign='top', wait_time=1000)
            c.blank_screen()
        else:
            c.blank_screen()
            c.text_screen("Sorry, that's incorrect.", valign='top', wait_time=1000)
            c.blank_screen()

if 2 in section:
    c.log("No control, just observing.")
    c.make_banner(c.header.render("Day on the farm", True, c.header_color))
    c.text_screen("You now observe the amount of food the farm feeds globs. You go to market with the farmer and have to decide which glob is a true farm glob.", valign='top', wait_time=1)
    

    continue_button = pygbutton.PygButton(rect=(c.center_x-80,c.bottom_y+150, 200,80),\
    caption="Continue", fgcolor=c.button_color, bgcolor=c.background_color, font=c.button)

    continue_button.draw(c.screen)
    pygame.display.update()
    continue_task = False
    while not continue_task:
        for event in pygame.event.get():
            if 'click' in continue_button.handleEvent(event): 
                continue_button.buttonDown = True;
                continue_task=True
            
    continue_button.draw(c.screen)
    pygame.display.update()   

    c.attn_screen(wait_time=1000)

    r_farm_frac = []
    r_fresh_frac = []

    for i in range(3):
        r_farm_frac.append(sigmoid(numpy.random.normal(logit(0.5),1)))
        r_fresh_frac.append(numpy.random.beta(1,1))

    chains = range(3)

    # change num trials?

    # Farm Fish

    c.blank_screen()

    amount = 100
    increment = 10

    administer_food(c,control=False)
       
    for i in range(NUM_TRIALS):
        for x in range(len(chains)):
            c.make_banner(c.header.render("Which of these is a farm glob?", True, c.header_color))
            r_proposal_frac = sigmoid(numpy.random.normal(logit(0.5),1))
            r_proposal = int(round(r_proposal_frac*scale)) + offset_farm

            r_farm = int(round(r_farm_frac[x]*scale)) + offset_farm

            draw_glob(c,r_farm, c.right_center_x,c.top_y+70)
            draw_glob(c,r_proposal,c.left_center_x,c.top_y+70)
            button = c.choice_screen(button_txt1="Yes",  button_txt2="Yes") 
            r_farm_frac = process_choice_experiment(c,button,r_farm_frac,r_proposal_frac,x)
            c.blank_screen()

if 3 in section:
    c.log("Experiment: Full Control")
    c.make_banner(c.header.render("Running the farm!", True, c.header_color))
    c.text_screen("You are now given full control of the farm and have to sell your globs at market. Bigger globs get more money and grow the more you feed them, but if you feed them too much, they get sick and lose weight. In the next section, you have to decide how much to feed your globs. The amount of food you specify will be administered to your globs every day that week. You then go to market at the end of the week and have to choose which of the globs is yours.", valign='top', wait_time=1)

    # Subsection 1: Farm globs
   
    continue_button = pygbutton.PygButton(rect=(c.center_x-80,c.bottom_y+150, 200,80),\
    caption="Continue", fgcolor=c.button_color, bgcolor=c.background_color, font=c.button)

    continue_button.draw(c.screen)
    pygame.display.update()
    continue_task = False
    while not continue_task:
        for event in pygame.event.get():
            if 'click' in continue_button.handleEvent(event): 
                continue_button.buttonDown = True;
                continue_task=True
            
    continue_button.draw(c.screen)
    pygame.display.update() 

    c.attn_screen(wait_time=1000)
    r_farm_frac = []
    r_fresh_frac = []

    for i in range(3):
        r_farm_frac.append(sigmoid(numpy.random.normal(logit(0.5),1)))
        r_fresh_frac.append(numpy.random.beta(1,1))

    chains = range(3)

    # Farm globs
    c.blank_screen()

    amount = 100
    increment = 10

    administer_food(c,control=True)
       
    for i in range(NUM_TRIALS):
        for x in range(len(chains)):
            c.make_banner(c.header.render("Which of these is your farm glob?", True, c.header_color))
            r_proposal_frac = sigmoid(numpy.random.normal(logit(0.5),1))
            r_proposal = int(round(r_proposal_frac*scale)) + offset_farm

            r_farm = int(round(r_farm_frac[x]*scale)) + offset_farm

            draw_glob(c,r_farm, c.right_center_x,c.top_y+70)
            draw_glob(c,r_proposal,c.left_center_x,c.top_y+70)
            button = c.choice_screen(button_txt1="Yes",  button_txt2="Yes") 
            r_farm_frac = process_choice_experiment(c,button,r_farm_frac,r_proposal_frac,x)
            c.blank_screen()

if 4 in section: 
    c.log("Partial control (shared control with farm hand)")
    c.log("Experiment: Full Control")
    c.make_banner(c.header.render("Hired help!", True, c.header_color))
    c.text_screen("You now hire a helper to help care for the globs. The amount of food you specify will only be administered to the globs 3 out of 6 days before market. The other three days, Henrietta will feed the globs. You now go to market and have to decide which globs are yours.", valign='top', wait_time=1)

    continue_button = pygbutton.PygButton(rect=(c.center_x-80,c.bottom_y+150, 200,80),\
    caption="Continue", fgcolor=c.button_color, bgcolor=c.background_color, font=c.button)

    continue_button.draw(c.screen)
    pygame.display.update()
    continue_task = False
    while not continue_task:
        for event in pygame.event.get():
            if 'click' in continue_button.handleEvent(event): 
                continue_button.buttonDown = True;
                continue_task=True
            
    continue_button.draw(c.screen)
    pygame.display.update() 

    c.attn_screen(wait_time=1000)

    r_farm_frac = []
    r_fresh_frac = []

    for i in range(3):
        r_farm_frac.append(sigmoid(numpy.random.normal(logit(0.5),1)))
        r_fresh_frac.append(numpy.random.beta(1,1))

    chains = range(3)

    # Farm globs
    c.blank_screen()

    amount = 100
    increment = 10

    administer_food(c,control=True)
       
    for i in range(NUM_TRIALS):
        for x in range(len(chains)):
            c.make_banner(c.header.render("Which of these is your farm glob?", True, c.header_color))
            r_proposal_frac = sigmoid(numpy.random.normal(logit(0.5),1))
            r_proposal = int(round(r_proposal_frac*scale)) + offset_farm

            r_farm = int(round(r_farm_frac[x]*scale)) + offset_farm

            draw_glob(c,r_farm, c.right_center_x,c.top_y+70)
            draw_glob(c,r_proposal,c.left_center_x,c.top_y+70)
            button = c.choice_screen(button_txt1="Yes",  button_txt2="Yes") 
            r_farm_frac = process_choice_experiment(c,button,r_farm_frac,r_proposal_frac,x)
            c.blank_screen()


c.exit_screen("Thanks for playing!")