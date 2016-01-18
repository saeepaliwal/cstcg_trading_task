# -*- coding: utf-8 -*-    
from __future__ import division
from choice_task import ChoiceTask
import pygame
from pygame.locals import *
from trading_task_functions import *
import random
import numpy as np
import trading_buttons
import pdb
from scipy.io import savemat

#This experiment needs:
# 1. Underlying probability trace
# 2. 

# Components of th and equivalent for trading task:
# Bet sizes: buy 20 shares, buy 60 shares
# Machine Switch: change asset
# Cashout: New trading day
# Gamble: stock split
# Add money: Increase account
# Note: long-only 
# Narrative: you place your order before the market opens. 
# At the end of the trading session, your order closes and you see your performance


# Define special characters
ae = u"ä";
ue = u"ü";

# Define colors:
BLUE =   (  0,   0, 128)
GREEN =  (  0, 100,   0)
RED =    (178,  34,  34)
YELLOW = (255, 215,   0)
GRAY =   (139, 139, 131)
PURPLE = ( 72,  61, 139)
ORANGE = (255, 140,   0)
WHITE =  (255, 255, 255)
DARK_GRAY = ( 20, 20, 20)
GOLD   = ( 254, 195,  13)
BLACK  = (   0,   0,   0)


background_music = pygame.mixer.Sound('./sounds/ticker1_music.wav')
background_music.set_volume(0.2)

c = ChoiceTask(background_color=BLACK, 
    title  = pygame.font.Font('./fonts/SansSerifFLF.otf', 40),
    body  = pygame.font.Font('./fonts/Oswald-Bold.ttf', 30),
    header = pygame.font.Font('./fonts/SansSerifFLF.otf', 40),
    instruction = pygame.font.Font('./fonts/GenBasR.ttf',30),
    choice_text = pygame.font.Font('./fonts/GenBasR.ttf', 30),
    button = pygame.font.Font('./fonts/SansSerifFLF.otf',30))

(subjectname) = c.subject_information_screen()
subject = subjectname.replace(" ","")
matlab_output_file = c.create_output_file(subjectname)
c.blank_screen()
welcome_screen(c)
instruction_screen(c)

# Pull in task backend
with open ('taskBackend_finance_test.txt','r') as f:
    probability_trace = f.read().replace('\n', '')

result_sequence = probability_trace.split(',')
NUM_TRIALS=10

# Screens I need to write:
#display_instructions()
    # for instrutions, let users click forward with arrow keys 
# display prices() will show random prices as the player waits
# lost_all_money()
# check_perfomance()
# switch_asset()
# start fresh game()
# close_postision()
# goodbye_screen
# entering_trading_floor()
# random_prices() random price activity between market open and market closed

# the wait time is as the market refreshes, i can have some sort of roll or news
# or something
# then the prices show up --yesterday, your trade, sell price.

# Define open prices for the four stocks
open_prices = [20, 40, 60, 80]

# Define dictionary of task attributes:
task = {'trade_size': np.zeros(NUM_TRIALS).astype('int'),
        'account': np.zeros(NUM_TRIALS).astype('int'),
        'result_sequence': result_sequence,
        'stock_sequence': np.zeros(NUM_TRIALS).astype('int'),
        'reward_grade': np.zeros(NUM_TRIALS).astype('int'),
        'winloss': np.zeros(NUM_TRIALS).astype('int'),
        'pressed_stop': np.zeros(NUM_TRIALS).astype('int'),
        }

# Start with initial account and stock
task['account'][0] = 500
task['stock'] = 0
task['current_price'] = {}
task['current_price'][0] = []
task['current_price'][1] = []
task['current_price'][2] = []
task['current_price'][3] = []

# Set up initial screen 
positions, buttons, sizes = get_screen_elements(c, task)

for trial in range(NUM_TRIALS):
    print trial
    next_trial = False    

    # TODO: Training trials here
    if trial < 5:
        if trial == 0:
            #begin_training_screen(c)
            background_music.play(100,0)

    task['trade_sequence'] = []
    task['trial'] = trial
    task['current_price'][task['stock']].append(open_prices[task['stock']])

    task['stock_sequence'][trial] = task['stock']
    if trial > 0:
        task['account'][trial] = task['account'][trial-1] 

    task['reward_grade'][trial] = int(str(result_sequence[trial])[1])

    task['trial_stage'] = 'trade'
    buttons = draw_screen(c, positions, buttons, sizes, task)

    while not next_trial:   
        pygame.time.wait(20)
        for event in pygame.event.get():
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                if 'click' in buttons['add_five'].handleEvent(event): 
                    c.press_sound.play()
                    task['trial_stage'] = 'trade'
                    task['trade_size'][trial] += 5
                    task['trade_sequence'].append(5)
                    task = update_account(c,positions, sizes, task)
                    display_assets(c,positions,sizes,task)
                    c.log('Trial ' + str(trial) + ': Added 5 shares to trade. ' + repr(time.time()) + '\n')
                elif 'click' in buttons['add_ten'].handleEvent(event): 
                    c.press_sound.play()
                    task['trial_stage'] = 'trade'
                    task['trade_size'][trial] += 10
                    task['trade_sequence'].append(10)
                    task = update_account(c,positions, sizes, task)
                    display_assets(c,positions,sizes,task)
                    c.log('Trial ' + str(trial) + ': Added 10 shares to trade. ' + repr(time.time()) + '\n')
                elif 'click' in buttons['clear'].handleEvent(event):
                    c.press_sound.play()
                    if len(task['trade_sequence']) > 0:   
                        c.log('Trial ' + str(trial) + ': Clearing ' + str(task['trade_sequence'][-1]) + 'from trade. ' + repr(time.time()) + '\n')
                        task['trial_stage'] = 'clear'
                        task = clear(c,task)
                        task = update_account(c,positions, sizes, task)
                        display_assets(c,positions,sizes,task)
                # Add clear functionality here
                elif 'click' in buttons['place_order'].handleEvent(event):
                    if task['trade_size'][trial] > 0:
                        buttons['place_order'].draw(c.screen)
                        pygame.display.update()
                        #leversound.play()
                        #c.wait_fun(100)
                        #leversound.stop()
                        c.log('Trial ' + str(trial) + ': Pulling wheels ' + repr(time.time()) + '\n')
                        c.log('Summary Trial' + str(trial) + ': Trade:' + str(task['trade_size'][trial]) + 'Account: ' + str([task['account'][trial]]))
                        task['trial_stage'] = 'result'
                        spin_prices(c, positions, buttons, task)
                        result(c,positions,buttons,sizes,task)
                        next_trial = True
                elif 'click' in buttons['cashout'].handleEvent(event):
                    c.log('Deciding to cash out ' + str(task['trial']) +  ' ' + repr(time.time()) + '\n')
                    c.press_sound.play()
                    background_music.stop()
                    c.log('Trial ' + str(trial) + ': Cashing out ' + repr(time.time()) + '\n')
                    cashout(c, positions, buttons, sizes, task)
                    draw_screen(c, positions, buttons, sizes, task)     
                    background_music.play(100,0)
                elif 'click' in buttons['mini_stock_0'].handleEvent(event):
                    c.press_sound.play()
                    background_music.stop()
                    task['trial_stage'] = 'change_asset'
                    task['stock'] = task['all_stocks'][0]
                    task['stock_sequence'][trial] = task['stock']
                    if len(task['current_price'][task['stock']]) == 0:
                        task['current_price'][task['stock']].append(open_prices[task['stock']])
                    background_music = pygame.mixer.Sound('./sounds/ticker' + str(task['stock']) + '_music.wav')
                    background_music.set_volume(0.2)
                    buttons = draw_screen(c, positions, buttons, sizes, task)
                    background_music.play(100,0)
                    c.log('Trial ' + str(trial) + ': Changing stocks to stock ' + str(task['stock_sequence'][trial]) + ' at ' + repr(time.time()) + '\n')
                elif 'click' in buttons['mini_stock_1'].handleEvent(event):
                    c.press_sound.play()
                    background_music.stop()
                    task['trial_stage'] = 'change_asset'
                    task['stock'] = task['all_stocks'][1]
                    task['stock_sequence'][trial] = task['stock']
                    if len(task['current_price'][task['stock']]) == 0:
                        task['current_price'][task['stock']].append(open_prices[task['stock']])
                    background_music = pygame.mixer.Sound('./sounds/ticker' + str(task['stock']) + '_music.wav')
                    background_music.set_volume(0.2)
                    buttons = draw_screen(c, positions, buttons, sizes, task)
                    background_music.play(100,0)
                    c.log('Trial ' + str(trial) + ': Changing stocks to stock ' + str(task['stock_sequence'][trial]) + ' at ' + repr(time.time()) + '\n')
                elif 'click' in buttons['mini_stock_2'].handleEvent(event):
                    c.press_sound.play()
                    background_music.stop()
                    task['trial_stage'] = 'change_asset'
                    task['stock'] = task['all_stocks'][2]
                    task['stock_sequence'][trial] = task['stock']
                    if len(task['current_price'][task['stock']]) == 0:
                        task['current_price'][task['stock']].append(open_prices[task['stock']])
                    background_music = pygame.mixer.Sound('./sounds/ticker' + str(task['stock']) + '_music.wav')
                    background_music.set_volume(0.2)
                    buttons = draw_screen(c, positions, buttons, sizes, task)    
                    background_music.play(100,0)
                    c.log('Trial ' + str(trial) + ': Changing stocks to ' + str(task['stock_sequence'][trial]) + ' at ' + repr(time.time()) + '\n')
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
            for key in buttons:
                buttons[key].draw(c.screen)
            pygame.display.update()
        
c.exit_screen("Thanks for playing!")