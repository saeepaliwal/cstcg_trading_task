# -*- coding: utf-8 -*-   

import pygame
from pygame.locals import *
from pygame import gfxdraw
#from pylab import *
import math
import numpy
from trading_buttons import TradingButton
from time import strftime,localtime
import time
import random
import serial
import platform
from psychopy import core

if platform.system() == 'Windows': # Windows
    from ctypes import windll

ue = u"ü"
ae = u"ä"
Ue = u"Ü"
# Define colors:
#BLUE =   (  0,   0, 128)
GREEN =  ( 58, 138, 112)
#GREEN =  (  0, 100,   0)
#RED =    (178,  34,  34)
#YELLOW = (255, 215,   0)
GRAY =   (139, 139, 131)
PURPLE = (178, 102, 255)
CARROT = (255, 140,   0)
WHITE =  (255, 255, 255)
BLUE   = (  58, 134, 207)
ORANGE = ( 208, 112,  43)
RED    = ( 205,  73,  57)
YELLOW = ( 231, 182,  40)
BRIGHT_ORANGE = ( 242, 101,  34)
GOLD   = ( 242, 153,  36)
TX_GREEN = (57, 255, 20)
BLACK = (0,0,0)
TX_RED = (249, 15, 0)
PX_BLUE = ( 102, 255, 255)


# Load images
intro = pygame.image.load('./images/trading_task_welcome_banner.png').convert_alpha()
small_win = pygame.image.load('./images/symbols_smallwin.png').convert_alpha()
big_win = pygame.image.load('./images/symbols_megawin.png').convert_alpha()
scoreboard = pygame.image.load('./images/trading_task_scoreboard.png').convert_alpha()
selector_box = pygame.image.load('./images/trading_task_selector.png').convert_alpha()


# Load symbols
symbols = {}
symbols['1'] = pygame.image.load('./images/trading_task_symbol1.png').convert_alpha()
symbols['2']  = pygame.image.load('./images/trading_task_symbol2.png').convert_alpha()
symbols['3'] = pygame.image.load('./images/trading_task_symbol3.png').convert_alpha()
symbols['4'] = pygame.image.load('./images/trading_task_symbol4.png').convert_alpha()
symbols['5']  = pygame.image.load('./images/trading_task_symbol5.png').convert_alpha()
symbols['6']  = pygame.image.load('./images/trading_task_symbol6.png').convert_alpha()
symbols['7'] = pygame.image.load('./images/trading_task_symbol7.png').convert_alpha()
symbols['8']  = pygame.image.load('./images/trading_task_symbol8.png').convert_alpha()
symbols['9'] = pygame.image.load('./images/trading_task_symbol9.png').convert_alpha()
symbols['10'] = pygame.image.load('./images/trading_task_symbol10.png').convert_alpha()


# Load tickers
tickers = {}
tickers['0'] = pygame.image.load('./images/trading_task_ticker0.png').convert_alpha()
tickers['1'] = pygame.image.load('./images/trading_task_ticker1.png').convert_alpha()
tickers['2'] = pygame.image.load('./images/trading_task_ticker2.png').convert_alpha()
tickers['3'] = pygame.image.load('./images/trading_task_ticker3.png').convert_alpha()

# Load instructions
# Load instructions
instructions = {}
instructions['1'] = pygame.image.load('./instructions/Slide01.png').convert_alpha()
instructions['2'] = pygame.image.load('./instructions/Slide02.png').convert_alpha()
instructions['3'] = pygame.image.load('./instructions/Slide03.png').convert_alpha()
instructions['4'] = pygame.image.load('./instructions/Slide04.png').convert_alpha()
instructions['5'] = pygame.image.load('./instructions/Slide05.png').convert_alpha()
instructions['6'] = pygame.image.load('./instructions/Slide06.png').convert_alpha()
instructions['7'] = pygame.image.load('./instructions/Slide07.png').convert_alpha()
instructions['8'] = pygame.image.load('./instructions/Slide08.png').convert_alpha()
instructions['9'] = pygame.image.load('./instructions/Slide09.png').convert_alpha()
instructions['10'] = pygame.image.load('./instructions/Slide10.png').convert_alpha()
instructions['11'] = pygame.image.load('./instructions/Slide11.png').convert_alpha()
instructions['12'] = pygame.image.load('./instructions/Slide12.png').convert_alpha()
instructions['13'] = pygame.image.load('./instructions/Slide13.png').convert_alpha()
instructions['14'] = pygame.image.load('./instructions/Slide14.png').convert_alpha()
instructions['15'] = pygame.image.load('./instructions/Slide15.png').convert_alpha()


# Load training 
training_info = {}
training_info['1'] = pygame.image.load('./images/train_1.png').convert_alpha()
training_info['2'] = pygame.image.load('./images/train_2.png').convert_alpha()
training_info['3'] = pygame.image.load('./images/train_3.png').convert_alpha()
training_info['4'] = pygame.image.load('./images/train_4.png').convert_alpha()
training_info['5'] = pygame.image.load('./images/train_5.png').convert_alpha()


spin_cover =  pygame.image.load('./images/trading_task_spin_cover.png').convert_alpha()

win_banner = pygame.image.load('./images/trading_task_banner.png').convert_alpha()
# Pull in sounds:
spinsound = pygame.mixer.Sound('./sounds/spinning.wav')
spinsound.set_volume(0.0)
winsound = pygame.mixer.Sound('./sounds/winsound.wav')
winsound.set_volume(0.0)
bigwinsound = pygame.mixer.Sound('./sounds/bigwinsound.wav')
bigwinsound.set_volume(0.0)
spinstopsound = pygame.mixer.Sound('./sounds/spinstop.wav')
spinstopsound.set_volume(0.0)

# Load fonts
ticker_font = pygame.font.Font('./fonts/ASTRII__.TTF',60)
progress_font = pygame.font.Font('./fonts/DS-DIGIB.TTF',30)
ticker_font_small = pygame.font.Font('./fonts/ASTRII__.TTF',35)
money_font = pygame.font.Font('./fonts/DS-DIGIB.TTF',50)
split_font = pygame.font.Font('./fonts/Oswald-Bold.ttf', 60)
def sigmoid(x):
    s =  1.0/(1.0 + numpy.exp(-1.0*x))
    return s

def logit(x):
    l = numpy.log(x) - numpy.log(1-x)
    return l

def is_odd(num):
    return num & 0x1

def show_instruction(c,stage):
    c.screen.blit(training_info[stage],(c.center_x-training_info[stage].get_width()/2, c.center_y-training_info[stage].get_height()/2))
    pygame.display.update()
    c.wait_fun(2000)

def selector(c,task,positions,index,selector_pos):
    if platform.system() == 'Windows':
        sel_positions=[(110,430), # loss
                   (8,500), # orange
                   (8,580), # grape 
                   (8,650), # cherry 
                   (8,730), # lemon 
                   (8,800), # plum
                   (180,500), # bar 
                   (180,580), # bell 
                   (180,650),#watermelon
                   (180,730),#seven
                   (180,800)] # jackpot
    else:
        sel_positions=[(110,360), # loss
               (8,430), # orange
               (8,510), # grape 
               (8,580), # cherry 
               (8,660), # lemon 
               (8,730), # plum
               (180,430), # bar 
               (180,510), # bell 
               (180,580),#watermelon
               (180,660),#seven
               (180,730)] # jackpot

    pos = sel_positions[selector_pos-1]
    selected = False
    if index == 1:
        selector_pos += 1
        if selector_pos == 12:
            selector_pos = 1
        pos = sel_positions[selector_pos-1]
    elif index == 8:
        selected = True
        c.log('Selected guess on Trial ' + str(task['trial']) +  ' ' + repr(time.time()) + '\n')
        if task['training']:
            show_instruction(c,'2')
            show_instruction(c,'3')
    c.screen.blit(selector_box,pos)
    pygame.display.update()

    return selector_pos, selected

    
def welcome_screen(c, wait_time=3000):
    c.blank_screen()
    c.attn_screen(attn=intro,wait_time=wait_time)

def get_screen_elements(c, task):

    # Button sizes
    sizes = {}
    sizes['sw'] = c.screen_width
    sizes['sh'] = c.screen_height
    sizes['bbw'] = sizes['sw']*0.2
    sizes['bbh'] = sizes['sh']*0.21

    sizes['mbw'] = sizes['sw']*0.15
    sizes['mbh'] = sizes['sh']*0.15

    sizes['sbw'] = sizes['sw']*0.1
    sizes['sbh'] = sizes['sh']*0.1

    sizes['xsbh'] = sizes['sw']*0.05
    sizes['xsbw'] = sizes['sh']*0.05    

    positions = {};
    positions['banner_x'] = 300
    positions['banner_y'] = 40

    shift = 5
    positions['hold1_x'] = c.left_center_x+(sizes['sh']/9) - shift
    positions['hold2_x'] = c.left_center_x+(sizes['sh']/3) - shift
    positions['hold3_x'] = c.left_center_x+(0.55*sizes['sh']) - shift
    positions['hold_y'] = c.center_y+sizes['sh']*0.12
    hold_offset = 0

    x0 = sizes['sh']/40
    positions['bet_5_x'] = c.left_center_x+(sizes['sh']/9) - x0
    positions['bet_5_y'] = c.center_y+(sizes['sh']/3) - hold_offset

    positions['scoreboard_x'] = 10
    positions['scoreboard_y'] = c.center_y - 150

    positions['bet_10_x'] = c.left_center_x+(0.32*sizes['sh']) - x0
    positions['bet_10_y'] = c.center_y+(sizes['sh']/3) - hold_offset

    positions['pull_x'] = c.center_x+(sizes['sh']/9) - x0
    positions['pull_y'] = c.center_y+(sizes['sh']/3)-(sizes['sbh']*1.1) - hold_offset
    positions['stop_y'] = c.center_y+(sizes['sh']/3) - hold_offset

    positions['cashout_x'] = 20
    positions['cashout_y'] = c.top_y+0.1*sizes['sh']+1.2*sizes['bbh'] + 10

    positions['clear_x'] = positions['bet_5_x']
    positions['clear_y'] = c.center_y+(sizes['sh']/3)+2*sizes['sbw']/3 - hold_offset
    
    positions['bet_screen_x'] = positions['bet_5_x']
    positions['bet_screen_y'] = positions['pull_y']
    #positions['account_screen_y'] = c.top_y+0.1*sizes['sh']

    positions['account_screen_y'] = c.top_y

    positions['yesterdays_close_x'] = c.center_x+80
    positions['yesterdays_close_y'] = 190


    positions['gamble_x'] = c.left_center_x-sizes['bbw']/2
    positions['gamble_y'] = c.bottom_y+sizes['sbh']/2

    positions['no_gamble_x'] = c.right_center_x-sizes['bbw']/2
    positions['no_gamble_y'] = c.bottom_y+sizes['sbh']/2

    # Side stocks
    positions['mini_stocks'] = {}
    positions['mini_stocks']['x'] = c.right_x - 200
    positions['mini_stocks']['y0'] = c.center_y - 310
    positions['mini_stocks']['y1'] = c.center_y - 85
    positions['mini_stocks']['y2'] = c.center_y + 140

    positions['ticker'] = {}
    positions['ticker']['base_x'] = c.center_x-(tickers['0'].get_width()/2)
    positions['ticker']['base_y'] = 0
    positions['ticker']['x1'] =  c.center_x-(tickers['0'].get_width()/2) + 100 - 20
    positions['ticker']['x2'] = c.center_x-(tickers['0'].get_width()/2) + 300 - 45
    positions['ticker']['x3'] = c.center_x-(tickers['0'].get_width()/2) + 500 - 75
    positions['ticker']['y']  = tickers['0'].get_height() - 165
    positions['ticker']['px1'] = c.center_x-(tickers['0'].get_width()/2) + 20
    positions['ticker']['px2'] = c.center_x-(tickers['0'].get_width()/2) + 250
    positions['ticker']['px3'] = c.center_x-(tickers['0'].get_width()/2) + 480

    positions['ticker']['py'] = tickers['0'].get_height()/2 +30

    buttons = make_buttons(c,positions,sizes,task,'guess')
    c.screen.fill(c.background_color)

    return positions, buttons, sizes

def process_rtb(positions,index, stage, hold_on,task=None):
    fix = 50
    events = []
    event_set = False
    if stage == 'instructions':
        event1 = pygame.event.Event(MOUSEBUTTONDOWN)
        event2 = pygame.event.Event(MOUSEBUTTONUP)
        if index == 1:
            event1.pos = (positions['gamble_x'],positions['gamble_y'])
            event_set = True
        elif index == 8:
            event1.pos = (positions['no_gamble_x'],positions['no_gamble_y'])  
            event_set = True  

    if stage == 'bet' or stage == 'clear' or stage == 'pull' or stage == 'gamble': 
        event1 = pygame.event.Event(MOUSEBUTTONDOWN)
        event2 = pygame.event.Event(MOUSEBUTTONUP)
        if stage == 'bet' or stage == 'clear':
            if index == 1:
                event1.pos = (positions['bet_5_x']+fix,positions['bet_5_y']+fix)
                event_set = True
            elif index == 2:
                event1.pos = (positions['bet_10_x']+fix,positions['bet_10_y']+fix)
                event_set = True
            elif index == 4:
                event1.pos = (positions['pull_x']+2*fix,positions['pull_y']+2*fix)
                event_set = True
            elif index == 8:
                event1.pos = (positions['pull_x']+2*fix,positions['pull_y']+2*fix)
                event_set = True
             #   event1.pos = (positions['clear_x']+fix,positions['clear_y']+fix)
             #   event_set = True
        elif stage == 'pull' and hold_on:
            if index == 1:
                if not task['wheel1'] and not task['wheel2'] and not task['wheel3']:
                    event1.pos = (positions['hold1_x']+fix, positions['hold_y']+fix)
                    event_set = True
                elif task['wheel1'] and not task['wheel2'] and not task['wheel3']:
                    event1.pos = (positions['hold2_x']+fix, positions['hold_y']+fix)
                    event_set = True
                elif task['wheel2'] and task['wheel2'] and not task['wheel3']:
                    event1.pos = (positions['hold3_x']+fix, positions['hold_y']+fix)
                    event_set = True
        elif stage == 'gamble':
            if index == 1:
                event1.pos = (positions['gamble_x'],positions['gamble_y'])
                event_set = True
            elif index == 8:
                event1.pos = (positions['no_gamble_x'],positions['no_gamble_y'])  
                event_set = True  
    if event_set:    
        event2.pos = event1.pos       
        events.append(event1)  
        events.append(event2)
    return events

def end_training_screen(c):
    waitfun(1000)
    c.log('Training end at ' + repr(time.time()) + '\n')
    c.blank_screen()
    c.text_screen('Das Training ist fertig. Das Spiel beginnt jetzt! Viel Gl'+ue+'ck!', font=c.header, font_color=GOLD, valign='center', y_displacement= -45, wait_time=4000) 


def draw_screen(c, positions, buttons, sizes, task):
    c.screen.fill(c.background_color)
    all_stocks = [0,1,2,3]
    all_stocks.remove(task['stock'])

    buttons = make_buttons(c,positions,sizes,task,task['trial_stage'])


    for idx,num in enumerate(all_stocks):
        buttons['mini_stock_' + str(idx) ] = TradingButton(normal='./images/trading_task_stock' + str(num) + '.png', 
            down='./images/trading_task_stock' + str(num) + '_gray.png',
            highlight='./images/trading_task_stock' + str(num) + '_gray.png', 
            pos1=positions['mini_stocks']['x'], pos2=positions['mini_stocks']['y' + str(idx)])


    # Draw bet screen
    bet_screen = pygame.Rect(positions['bet_screen_x'],positions['bet_screen_y'],sizes['bbw']+45, sizes['sbh']-3)
    pygame.draw.rect(c.screen,WHITE,bet_screen,0)

    account_screen = pygame.Rect(positions['scoreboard_x'],positions['account_screen_y'],sizes['bbw']+35, 1.2*sizes['bbh'])
    pygame.draw.rect(c.screen,GOLD,account_screen,0)

    # Draw main ticker
    c.screen.blit(tickers[str(task['stock'])],(positions['ticker']['base_x'],positions['ticker']['base_y']))
    c.screen.blit(scoreboard,(positions['scoreboard_x'],positions['scoreboard_y']))


    for key in buttons:
        buttons[key].draw(c.screen)


    if task['trial_stage'] != 'guess':
        selector(c,task,positions,0,task['guess_trace'][task['trial']])

    task['all_stocks'] = all_stocks
    display_assets(c,positions,sizes,task)

    return buttons, task

def waitfun(milliseconds):
    nowtime = pygame.time.get_ticks()
    while pygame.time.get_ticks()-nowtime < milliseconds:
        pygame.time.wait(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

def update_account(c,positions, sizes, task):
    # Update the account to the new trade
    if task['trial_stage'] == 'bet': 
        task['account'][task['trial']] = task['account'][task['trial']]
    elif task['trial_stage'] == 'result':     
        # Update the account with the latest win or loss
        task['account'][task['trial']] = task['account'][task['trial']] + task['winloss'][task['trial']]

  #  task['account_balance'] = task['account_balance'] - task['buy_price']*task['trade_size']
    return task

def instruction_screen(c,positions,sizes,RTB):

    back_button = TradingButton(rect=(positions['gamble_x'],positions['gamble_y'], sizes['bbw'],sizes['sbh']),\
        caption="Zurueck",  fgcolor=c.background_color, bgcolor=RED, font=c.button)
    next_button = TradingButton(rect=(positions['no_gamble_x'],positions['no_gamble_y'],sizes['bbw'],sizes['sbh']),\
        caption="Weiter", fgcolor=c.background_color, bgcolor=GREEN, font=c.button)

    finish_button = TradingButton(rect=(positions['no_gamble_x'],positions['no_gamble_y'],sizes['bbw'],sizes['sbh']),\
        caption="Fertig", fgcolor=c.background_color, bgcolor=GREEN, font=c.button)

    counter = 1
    c.blank_screen()
    c.screen.blit(instructions[str(counter)],(c.center_x-instructions[str(counter)].get_width()/2,\
        c.top_y-instructions[str(counter)].get_height()/8))  
    next_button.draw(c.screen)
    pygame.display.update()
    instructions_done = False
    while not instructions_done:
        key_press = RTB.read() 
        if len(key_press):
            key_index = ord(key_press)
            events = process_rtb(positions,key_index, 'instructions','False')
            if len(events) > 0:
                pygame.event.post(events[0])
                pygame.event.post(events[1])

            for event in pygame.event.get():
                if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                    if 'click' in next_button.handleEvent(event): 
                        counter += 1
                        if counter == len(instructions)+1:
                            instructions_done = True
                    elif 'click' in back_button.handleEvent(event):
                        if counter > 1:
                            counter  = counter - 1
                if event.type == MOUSEBUTTONUP and counter <= len(instructions):
                    c.blank_screen()
                    c.screen.blit(instructions[str(counter)],(c.center_x-instructions[str(counter)].get_width()/2,\
                        c.top_y-instructions[str(counter)].get_height()/8))  
                    if counter > 1:
                        back_button.draw(c.screen)
                    
                    if counter == len(instructions):
                        finish_button.draw(c.screen)
                    else:
                        next_button.draw(c.screen)
                    pygame.display.update()

def clear(c,task):
    if len(task['trade_sequence']) > 0:
        if task['trade_size'][task['trial']] > 0:
            task['account'][task['trial']] += task['trade_sequence'][-1]
            task['trade_size'][task['trial']] = task['trade_size'][task['trial']] - task['trade_sequence'][-1]
            del task['trade_sequence'][-1]
    return task

def stock_split(c,task, positions, sizes,RTB):
    c.screen.fill(WHITE)
    card_back = pygame.image.load('./images/trading_task_news1.png').convert_alpha()
    card_won = pygame.image.load('./images/trading_task_news_win.png').convert_alpha()
    card_lost = pygame.image.load('./images/trading_task_news_lose.png').convert_alpha()

    x_pos = c.center_x-card_back.get_width()/2
    y_pos = c.center_y-card_back.get_height()/2 - 20

    fpos_x = c.center_x
    fpos_y = c.center_y-50
    
   
    c.screen.blit(card_back,(x_pos,y_pos))
    c.make_banner(split_font.render("Aktiensplit", True, BLACK))
    c.screen.blit(split_font.render("?",True,BLACK),(fpos_x,fpos_y))
    eeg_trigger(c,task,'gamble_screen')
    #pygame.display.update()
    #waitfun(1000)

    gamble_button = TradingButton(rect=(positions['gamble_x'],positions['gamble_y'], sizes['bbw'],sizes['sbh']),\
        caption="Halten",  fgcolor=c.background_color, bgcolor=RED, font=c.button)
    no_gamble_button = TradingButton(rect=(positions['no_gamble_x'],positions['no_gamble_y'],sizes['bbw'],sizes['sbh']),\
        caption="Nein danke.", fgcolor=c.background_color, bgcolor=GREEN, font=c.button)

    decided = False
    CARD = pygame.USEREVENT + 1
    pygame.time.set_timer(CARD, 1000)
    time_elapsed = 0
    start_time = time.time()
    c.screen.blit(card_back,(x_pos,y_pos))
    c.screen.blit(split_font.render("3",True,BLACK),(fpos_x,fpos_y))
    c.make_banner(split_font.render("Doppelt oder nichts?", True, BLACK))
    gamble_button.draw(c.screen)
    no_gamble_button.draw(c.screen)
    pygame.display.update()

    if task['training']:
        show_instruction(c,'5')
    c.screen.fill(WHITE)
    c.screen.blit(card_back,(x_pos,y_pos))
    c.screen.blit(split_font.render("3",True,BLACK),(fpos_x,fpos_y))
    c.make_banner(split_font.render("Doppelt oder nichts?", True, BLACK))
    gamble_button.draw(c.screen)
    no_gamble_button.draw(c.screen)
    pygame.display.update()




    while not decided and time_elapsed < 3:
        time_elapsed = int(round(time.time()-start_time))
        key_press = RTB.read() 
        if len(key_press):
            key_index = ord(key_press)
            events = process_rtb(positions,key_index, 'gamble',task['wheel_hold_buttons'])
            if len(events) > 0:
                pygame.event.post(events[0])
                pygame.event.post(events[1])
        for event in pygame.event.get():
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                if 'click' in gamble_button.handleEvent(event): 
                    c.log('Decided to Gamble on trial ' + str(task['trial']) +  ' ' + repr(time.time()) + '\n')
                    if int(task['result_sequence'][task['trial']][5]) == 1:
                        task['account'][task['trial']] = task['account'][task['trial']] + task['winloss'][task['trial']]
                        c.screen.blit(card_won,(x_pos,y_pos))
                        gamble_button.draw(c.screen)
                        eeg_trigger(c,task,'won_gamble')
                        pygame.display.flip()
                        c.log('Won gamble on trial ' + str(task['trial']) +  '  at ' + repr(time.time()) + '\n')
                        #winsound.play()
                        waitfun(2000)
                        task['winloss'][task['trial']] = 2*task['winloss'][task['trial']]
                        eeg_trigger(c,task,'gamble_money_banner')
                        show_win_banner(c, positions, task['winloss'][task['trial']])
                        #winsound.play()
                        decided = True
                    elif int(task['result_sequence'][task['trial']][5]) == 0:
                        gamble_button.draw(c.screen)
                        pygame.display.flip()
                        c.screen.blit(card_lost,(x_pos,y_pos))
                        pygame.display.flip()
                        waitfun(2000)
                        c.log('Lost gamble on trial ' + str(task['trial']) +  '  at ' + repr(time.time()) + '\n')
                        task['winloss'][task['trial']] = 0
                        decided = True
                elif 'click' in no_gamble_button.handleEvent(event):
                    c.log('Did not gamble on trial ' + str(task['trial']) +  ' ' + repr(time.time()) + '\n')
                    no_gamble_button.draw(c.screen)
                    pygame.display.update()
                    decided = True
            elif event.type == CARD:
                c.screen.blit(card_back,(x_pos,y_pos))
                c.screen.blit(split_font.render(str(3-time_elapsed),True,BLACK),(fpos_x,fpos_y))
                c.make_banner(split_font.render("Doppelt oder nichts?", True, BLACK))
                pygame.display.flip()

            gamble_button.draw(c.screen)
            no_gamble_button.draw(c.screen)
            pygame.display.update()
    return task

def win_screen(c,positions, buttons, sizes, task):
    counter = 0
    percent_change = [.1,.2,.3,.4,.5,.6,.7,.8,.9,1]
    if task['reward_grade'][task['trial']] < 8:
        numsparkle = 1  
        winnerblit = small_win
        
    else:
        numsparkle = 1
        winnerblit = big_win
        

    while counter < numsparkle:
        # if numsparkle == 5:
        #     bigwinsound.play()
        # else:
        #     winsound.play()
        if task['wheel_hold_buttons']:
            if task['wheel3']:
                eeg_trigger(c,task,'win_screen_pressed')
            else:
                eeg_trigger(c,task,'win_screen_auto')
        else:
            eeg_trigger(c,task,'win_screen_norm')
        c.screen.blit(win_banner,(positions['banner_x']+100,positions['banner_y']+70)) 
        c.text_screen('Gewinnprozent: ' + str(percent_change[task['reward_grade'][task['trial']]]*100) + '%', font=c.title,font_color=GOLD, valign='top', y_displacement= -200, wait_time=1500)
       # c.screen.blit(pygame.transform.scale(winnerblit, (c.screen_width, c.screen_height)),(10,10))
        pygame.display.update()
        waitfun(task['win_screen_interval'])
        #draw_screen(c, positions, buttons, sizes, task)
        counter += 1

    draw_screen(c, positions, buttons, sizes, task)

def show_win_banner(c,positions,reward):
    c.screen.blit(win_banner,(positions['banner_x']+100,positions['banner_y']+70)) 
    #winsound.play()
    c.text_screen('Gewinnbericht: ' + str(reward) + 'points', font=c.title,font_color=GOLD, valign='top', y_displacement= -200, wait_time=1500)

def show_result(c,positions,buttons,task, spinning=False):
    percent_change = [.1,.2,.3,.4,.5,.6,.7,.8,.9,1]

    wait = task['inter_wheel_interval']
 
    if task['wheel_hold_buttons']:
        if spinning:
            if task['wheel1']:
                eeg_trigger(c,task,'pressed_stop_1')
                c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))

            if task['wheel2']:
                eeg_trigger(c,task,'pressed_stop_2')
                c.screen.blit(symbols[task['result_sequence'][task['trial']][2]],(positions['ticker']['x2'],positions['ticker']['y']))

            if task['wheel3']:
                if task['result_sequence'][task['trial']][0] == '1':
                    eeg_trigger(c,task,'pressed_stop_3_win')
                else:
                    eeg_trigger(c,task,'pressed_stop_3_loss')

                c.screen.blit(symbols[task['result_sequence'][task['trial']][3]],(positions['ticker']['x3'],positions['ticker']['y']))
        else:
            spin_prices(c, positions, buttons, task)

    #     else:
    #         eeg_trigger(c,task,'automatic_stop_1')
    #         c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))

    #         #c.screen.blit(tickers[str(task['stock'])],(positions['ticker']['base_x'],positions['ticker']['base_y']))
    #         c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
    #         pygame.display.flip()
    #         waitfun(wait)

    #         eeg_trigger(c,task,'automatic_stop_2')
    #         c.screen.blit(symbols[task['result_sequence'][task['trial']][2]],(positions['ticker']['x2'],positions['ticker']['y']))
    #         pygame.display.flip()
    #         waitfun(wait)

    #         if task['result_sequence'][task['trial']][0] == '1':
    #             eeg_trigger(c,task,'automatic_stop_3_win')
    #         else:
    #             eeg_trigger(c,task,'automatic_stop_3_loss')
    #         c.screen.blit(symbols[task['result_sequence'][task['trial']][3]],(positions['ticker']['x3'],positions['ticker']['y']))
    #         pygame.display.flip()
    #         waitfun(wait) 
    # else:
    #     c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
    #     c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
    #     eeg_trigger(c,task,'stop_1')
    #     pygame.display.flip()
    #     waitfun(wait)

    #     c.screen.blit(symbols[task['result_sequence'][task['trial']][2]],(positions['ticker']['x2'],positions['ticker']['y']))
    #     eeg_trigger(c,task,'stop_2')
    #     pygame.display.flip()
    #     waitfun(wait)

    #     c.screen.blit(symbols[task['result_sequence'][task['trial']][3]],(positions['ticker']['x3'],positions['ticker']['y']))
    #     if task['result_sequence'][task['trial']][0] == '1':
    #         eeg_trigger(c,task,'stop_3_win')
    #     else:
    #         eeg_trigger(c,task,'stop_3_loss')

    #     pygame.display.flip()
    #     waitfun(1000)

def change_machine_screen(c):
    waitfun(1000)
    c.log('Changing machines at ' + repr(time.time()) + '\n')
    c.blank_screen()
    c.text_screen('Gut gemacht! Jetzt geht es weiter auf der n'+ae+'chsten strukturiertes Produkt!', font=c.header, font_color=GOLD, valign='center', y_displacement= -45, wait_time=4000) 


def process_result(c,positions,buttons,sizes,task, RTB):
    percent_change = [.1,.2,.3,.4,.5,.6,.7,.8,.9,1]
    task['current_price'][task['trial']] = task['current_price'][task['trial']-1]

    reward = 0
    if task['result_sequence'][task['trial']][0] == '1': # win
        task['reward_grade'][task['trial']] = int(task['result_sequence'][task['trial']][2])
        reward = task['trade_size'][task['trial']]*percent_change[task['reward_grade'][task['trial']]]*task['current_price'][task['trial']-1]
        task['winloss'][task['trial']] = reward
        win_screen(c,positions, buttons, sizes, task)
        eeg_trigger(c,task,'money_banner')
        show_win_banner(c,positions,reward)

    elif task['result_sequence'][task['trial']][0] == '2': # near miss
        task['reward_grade'][task['trial']] = 0
        task['winloss'][task['trial']] = -task['trade_size'][task['trial']]*task['current_price'][task['trial']-1]

    elif task['result_sequence'][task['trial']][0] == '0': # loss
        task['reward_grade'][task['trial']] = 0
        task['winloss'][task['trial']] = 0
        task['reward_grade'][task['trial']] = 0
        task['winloss'][task['trial']] = -task['trade_size'][task['trial']]*task['current_price'][task['trial']-1]


    if task['result_sequence'][task['trial']][0] == '1':
        if task['guess_trace'][task['trial']] == int(task['result_sequence'][task['trial']][2]):
            reward = reward + 200
            task['winloss'][task['trial']] = reward
    elif task['result_sequence'][task['trial']][0] == '0' and task['guess_trace'][task['trial']] == 1:
        reward = reward + 200
        task['winloss'][task['trial']] = reward
    else:
        reward = reward - 200
        task['winloss'][task['trial']] = reward

    if int(task['result_sequence'][task['trial']][4]) == 1:
        task = stock_split(c, task, positions, sizes, RTB)
        c.screen.fill(c.background_color)

    task = update_account(c,positions, sizes, task)
    return task
        
def make_buttons(c,positions,sizes,task,trial_stage):

# Set up buttons
    buttons = {}

    if trial_stage == 'guess':
        buttons['add_five'] = TradingButton(rect=(positions['bet_5_x'],positions['bet_5_y'], sizes['sbw'],sizes['sbh']),\
        caption="Anteile +", fgcolor=GRAY, bgcolor=c.background_color, font=c.button,highlight=YELLOW)

        buttons['place_order'] = TradingButton(rect=(positions['pull_x'],positions['pull_y'], sizes['mbw'],sizes['bbh']),\
        caption="Kaufen", fgcolor=GRAY, bgcolor=c.background_color, font=c.header)

        buttons['clear'] = TradingButton(rect=(positions['bet_10_x'],positions['bet_10_y'], sizes['sbw'],sizes['sbh']),\
        caption="Anteile -", fgcolor=GRAY, bgcolor=c.background_color, font=c.button)

        if task['wheel_hold_buttons']:
            buttons['hold1'] = TradingButton(rect=(positions['hold1_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Verkaufen", fgcolor=WHITE, bgcolor=GRAY, font=c.button)

            buttons['hold2'] = TradingButton(rect=(positions['hold2_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Verkaufen", fgcolor=WHITE, bgcolor=GRAY, font=c.button)
            
            buttons['hold3'] = TradingButton(rect=(positions['hold3_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Verkaufen", fgcolor=WHITE, bgcolor=GRAY, font=c.button)
    elif trial_stage == 'pull' or trial_stage == 'result': 
        buttons['add_five'] = TradingButton(rect=(positions['bet_5_x'],positions['bet_5_y'], sizes['sbw'],sizes['sbh']),\
        caption="Anteile +", fgcolor=GRAY, bgcolor=c.background_color, font=c.button,highlight=YELLOW)

        buttons['place_order'] = TradingButton(rect=(positions['pull_x'],positions['pull_y'], sizes['mbw'],sizes['bbh']),\
        caption="Kaufen", fgcolor=GRAY, bgcolor=c.background_color, font=c.header)

        buttons['clear'] = TradingButton(rect=(positions['bet_10_x'],positions['bet_10_y'], sizes['sbw'],sizes['sbh']),\
        caption="Anteile -", fgcolor=GRAY, bgcolor=c.background_color, font=c.button)

        if task['wheel_hold_buttons']:
            buttons['hold1'] = TradingButton(rect=(positions['hold1_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Verkaufen", fgcolor=WHITE, bgcolor=GOLD, font=c.button)
            if task['ungrey_wheel2']:
                buttons['hold2'] = TradingButton(rect=(positions['hold2_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
                caption="Verkaufen", fgcolor=WHITE, bgcolor=GOLD, font=c.button)
            else:
                buttons['hold2'] = TradingButton(rect=(positions['hold2_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
                caption="Verkaufen", fgcolor=WHITE, bgcolor=GRAY, font=c.button)

            if task['ungrey_wheel3']:     
                buttons['hold3'] = TradingButton(rect=(positions['hold3_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
                caption="Verkaufen", fgcolor=WHITE, bgcolor=GOLD, font=c.button)
            else:
                buttons['hold3'] = TradingButton(rect=(positions['hold3_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
                caption="Verkaufen", fgcolor=WHITE, bgcolor=GRAY, font=c.button)
    elif trial_stage == 'bet' or trial_stage == 'clear':
        buttons['add_five'] = TradingButton(rect=(positions['bet_5_x'],positions['bet_5_y'], sizes['sbw'],sizes['sbh']),\
        caption="Anteile +", fgcolor=WHITE, bgcolor=c.background_color, font=c.button,highlight=YELLOW)

        buttons['place_order'] = TradingButton(rect=(positions['pull_x'],positions['pull_y'], sizes['mbw'],sizes['bbh']),\
        caption="Kaufen", fgcolor=WHITE, bgcolor=c.background_color, font=c.header)

        buttons['clear'] = TradingButton(rect=(positions['bet_10_x'],positions['bet_10_y'], sizes['sbw'],sizes['sbh']),\
        caption="Anteile -", fgcolor=WHITE, bgcolor=c.background_color, font=c.button)

        if task['wheel_hold_buttons']:
            buttons['hold1'] = TradingButton(rect=(positions['hold1_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Verkaufen", fgcolor=WHITE, bgcolor=GRAY, font=c.button)

            buttons['hold2'] = TradingButton(rect=(positions['hold2_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Verkaufen", fgcolor=WHITE, bgcolor=GRAY, font=c.button)
            
            buttons['hold3'] = TradingButton(rect=(positions['hold3_x'],positions['hold_y'], sizes['sbw'],sizes['xsbh']),\
            caption="Verkaufen", fgcolor=WHITE, bgcolor=GRAY, font=c.button)
      
    return buttons

def display_assets(c,positions,sizes,task):

    bet_screen_inside = pygame.Rect(positions['bet_screen_x']+5,positions['bet_screen_y']+5,sizes['bbw']+35, sizes['sbh']-13)
    pygame.draw.rect(c.screen,c.background_color,bet_screen_inside,0)

    bet_banner = money_font.render(str(task['trade_size'][task['trial']]),True,RED) 
    c.surf_center_text(bet_banner, bet_screen_inside,0,0)

    account_screen_inside = pygame.Rect(positions['scoreboard_x']+1,positions['account_screen_y']+1,sizes['bbw']+33, 1.2*sizes['bbh']-2)
    pygame.draw.rect(c.screen,c.background_color,account_screen_inside,0)

    account_banner = c.header.render("Kontostand:",True,GOLD) 
    c.screen.blit(account_banner, (positions['scoreboard_x'] + 10,positions['account_screen_y'] + 10))
    
    account_balance = money_font.render(str(task['account'][task['trial']]), True, RED)
    c.screen.blit(account_balance,(positions['scoreboard_x'] + 20,positions['account_screen_y'] + account_banner.get_height() + 10))
    

    if not task['training']:
        progress = progress_font.render(str(task['progress'])+'/4', True, WHITE)
        c.screen.blit(progress,(positions['scoreboard_x'] + 20,20))

    pygame.display.update()

def print_prices_spin(px1):
    px2 = px1+round(100*random.uniform(-5,5))/100
    if px2 > px1 and px2>0:
        px = ticker_font.render('+' + str(px2), True, TX_GREEN)
        offset = 0
    elif px2 < px1: 
        px = ticker_font.render(str(px2), True, TX_RED)
        offset = 10
    elif px2 == px1:
        px = ticker_font.render(str(px2), True, WHITE)
        offset = 0
    return px,px2,offset

def individual_price_spin(c,positions,buttons,sizes,task, RTB):
    pygame.event.clear()
    n = 100
    lag = 10
    show1 = True
    show2 = False
    show3 = False
    show4 = False

    len_spin = 30
    width = round(210/(len_spin+5))

    task['wheel1'] = False
    task['wheel2'] = False
    task['wheel3'] = False
    task['ungrey_wheel2'] = False
    task['ungrey_wheel3'] = False

    counter = 0
    time_start = int(round(time.time()*1000))

    keep_spinning = True
    while keep_spinning:
        key_press = RTB.read() 
        if len(key_press):
            key_index = ord(key_press)

            events = process_rtb(positions,key_index, 'pull', task['wheel_hold_buttons'], task)
            if len(events) > 0:
                pygame.event.post(events[0])
                pygame.event.post(events[1])
            if pygame.event.peek([MOUSEBUTTONDOWN,MOUSEBUTTONUP]):
                for event in pygame.event.get():
                    if event.type==MOUSEBUTTONDOWN:
                        c.log('Trial ' + str(task['trial']) + ': Holding wheels at ' + repr(time.time()) + '\n')
                        buttons['hold1'].handleEvent(event)
                        buttons['hold1'].draw(c.screen)

                        if task['ungrey_wheel2']:
                            buttons['hold2'].handleEvent(event)
                            buttons['hold2'].draw(c.screen)

                        if task['ungrey_wheel3']:
                            buttons['hold3'].handleEvent(event)
                            buttons['hold3'].draw(c.screen)

                        pygame.display.update()
                    elif event.type==MOUSEBUTTONUP:
                        if 'click' in buttons['hold1'].handleEvent(event):
                            task['wheel1'] = True
                            #c.press_sound.play()
                            #c.screen.blit(tickers[str(task['stock'])],(positions['ticker']['base_x'],positions['ticker']['base_y']))
                            c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                            show_result(c,positions,buttons,task,spinning=True)
                            buttons['hold1'].draw(c.screen)
                            pygame.display.update()
                            
                        if task['ungrey_wheel2']:
                            if 'click' in buttons['hold2'].handleEvent(event):
                                task['wheel2'] = True
                                #c.press_sound.play()
                                #c.screen.blit(tickers[str(task['stock'])],(positions['ticker']['base_x'],positions['ticker']['base_y']))
                                c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                                show_result(c,positions,buttons,task, spinning=True)
                                buttons['hold2'].draw(c.screen)                                
                                pygame.display.update()

                        if task['ungrey_wheel3']:
                            if 'click' in buttons['hold3'].handleEvent(event):
                                task['wheel3'] = True
                                #c.press_sound.play()
                                #c.screen.blit(tickers[str(task['stock'])],(positions['ticker']['base_x'],positions['ticker']['base_y']))
                                c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                                show_result(c,positions,buttons,task, spinning=True)
                                buttons['hold3'].draw(c.screen)
                                pygame.display.update()
                                counter = len_spin
                                                                        
        else:
            counter += 1
            c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
            c.wait_fun(lag)
            show_result(c,positions,buttons,task, spinning=True)

            if counter == 10:
                task['ungrey_wheel2'] = True
                buttons = make_buttons(c,positions,sizes,task,task['trial_stage'])
                for key in buttons:
                    buttons[key].draw(c.screen)
            elif counter == 20:
                task['ungrey_wheel3'] = True
                buttons = make_buttons(c,positions,sizes,task,task['trial_stage'])
                for key in buttons:
                    buttons[key].draw(c.screen)
            pygame.display.flip()

            if not task['wheel1']:
                num1 = random.randint(1,9)
                num1_b = random.randint(1,3)
                c.screen.blit(symbols[str(num1)],(positions['ticker']['x1'],positions['ticker']['y']))
                px_update = pygame.Rect(positions['ticker']['px1']+counter*width-1,positions['ticker']['py']-num1_b*15,width,num1_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update,0)
                pygame.display.flip()

            if not task['wheel2']:
                if task['wheel1']:
                    s = task['result_sequence'][task['trial']][1]
                    idx = round(random.betavariate(1,1),1)
                    if idx > 0.7:
                        c.screen.blit(symbols[str(s)],(positions['ticker']['x2'],positions['ticker']['y']))
                        px_update2 = pygame.Rect(positions['ticker']['px2']+counter*width-1,positions['ticker']['py']-int(s)*15,width,int(s)*15)
                        pygame.draw.rect(c.screen,PX_BLUE,px_update2,0)
                    else:
                        num2 = random.randint(1,9)
                        num2_b = random.randint(7,9)
                        c.screen.blit(symbols[str(num2)],(positions['ticker']['x2'],positions['ticker']['y']))
                        px_update2 = pygame.Rect(positions['ticker']['px2']+counter*width-1,positions['ticker']['py']-num2_b*15,width,num2_b*15)
                        pygame.draw.rect(c.screen,PX_BLUE,px_update2,0)
                else:
                    num2 = random.randint(1,9)
                    num2_b = random.randint(7,9)
                    c.screen.blit(symbols[str(num2)],(positions['ticker']['x2'],positions['ticker']['y']))
                    px_update2 = pygame.Rect(positions['ticker']['px2']+counter*width-1,positions['ticker']['py']-num2_b*15,width,num2_b*15)
                    pygame.draw.rect(c.screen,PX_BLUE,px_update2,0)
                pygame.display.flip()
                c.wait_fun(lag)

            if not task['wheel3']:
                num3 = random.randint(1,9)
                num3_b = random.randint(4,6)
                c.screen.blit(symbols[str(num3)],(positions['ticker']['x3'],positions['ticker']['y']))
                px_update3 = pygame.Rect(positions['ticker']['px3']+counter*width-1,positions['ticker']['py']-num3_b*15,width,num3_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update3,0)
                pygame.display.flip()
                c.wait_fun(lag)


            if task['wheel1'] and task['wheel2'] and task['wheel3']:
                keep_spinning=False
            if counter == len_spin:
                keep_spinning=False

    if not task['wheel1'] or not task['wheel2'] or not task['wheel3']:
        c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
        show_result(c,positions,buttons,task, spinning=False)
        pygame.display.flip()
    c.wait_fun(500)
    spinsound.stop()


def spin_prices(c, positions, buttons, task):
    wait = 300
    pygame.event.clear()    
    lag = 10

    if task['wheel_hold_buttons']:
        counter_max = 1
        counter = 1
    else:
        counter_max = 10
        counter = 1

    len_spin = counter_max+40
    width = round(210/(len_spin))

    keep_spinning = True
    while keep_spinning:
        spinsound.play(100,0)
        
        if counter < counter_max:
            c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
            pygame.display.flip()
            c.wait_fun(lag)

            num1 = random.randint(1,9)
            c.screen.blit(symbols[str(num1)],(positions['ticker']['x1'],positions['ticker']['y']))
            num1_b = random.uniform(1,2)
            px_update = pygame.Rect(positions['ticker']['px1']+counter*width-1,positions['ticker']['py']-num1_b*15,width,num1_b*15)
            pygame.draw.rect(c.screen,PX_BLUE,px_update,0)
            pygame.display.flip()
            c.wait_fun(lag)

            num2 = random.randint(1,9)
            c.screen.blit(symbols[str(num2)],(positions['ticker']['x2'],positions['ticker']['y']))
            num2_b = random.uniform(7,8)
            px_update2 = pygame.Rect(positions['ticker']['px2']+counter*width-1,positions['ticker']['py']-num2_b*15,width,num2_b*15)
            pygame.draw.rect(c.screen,PX_BLUE,px_update2,0)
            pygame.display.flip()
            c.wait_fun(lag)

            num3 = random.randint(1,9)
            c.screen.blit(symbols[str(num3)],(positions['ticker']['x3'],positions['ticker']['y']))
            num3_b = random.uniform(4,5)
            px_update3 = pygame.Rect(positions['ticker']['px3']+counter*width-1,positions['ticker']['py']-num3_b*15,width,num3_b*15)
            pygame.draw.rect(c.screen,PX_BLUE,px_update3,0)
            pygame.display.flip()
            c.wait_fun(lag)

        elif counter == counter_max:
            if task['wheel1']:
                c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
            else:
                c.wait_fun(lag)
                c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                pygame.display.flip()
                c.wait_fun(lag)

                c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))

                if task['wheel_hold_buttons']:
                    eeg_trigger(c,task,'automatic_stop_1')
                else:
                    eeg_trigger(c,task,'stop_1')
                num1_b = random.uniform(1,2)
                px_update = pygame.Rect(positions['ticker']['px1']+counter*width-1,positions['ticker']['py']-num1_b*15,width,num1_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update,0)

                num2_b = random.uniform(7,8)
                px_update2 = pygame.Rect(positions['ticker']['px2']+counter*width-1,positions['ticker']['py']-num2_b*15,width,num2_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update2,0)

                num3_b = random.uniform(4,5)
                px_update3 = pygame.Rect(positions['ticker']['px3']+counter*width-1,positions['ticker']['py']-num3_b*15,width,num3_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update3,0)

                pygame.display.flip()
                c.wait_fun(lag)
                pygame.display.flip()
                c.wait_fun(lag)

        elif counter_max < counter < counter_max+20:
            if task['wheel_hold_buttons']:
                if not task['wheel2']:   
                    c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                    c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
                    pygame.display.flip()
                    c.wait_fun(lag)

                    c.screen.blit(symbols[str(random.randint(1,9))],(positions['ticker']['x2'],positions['ticker']['y']))
                    pygame.display.flip()
                    c.wait_fun(lag)

                    c.screen.blit(symbols[str(random.randint(1,9))],(positions['ticker']['x3'],positions['ticker']['y']))
                    pygame.display.flip()
                    c.wait_fun(2*lag)
                else:
                    c.wait_fun(lag)

                    c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                    c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
                    c.screen.blit(symbols[task['result_sequence'][task['trial']][2]],(positions['ticker']['x2'],positions['ticker']['y']))
                    pygame.display.flip()
                    c.wait_fun(lag)

                    c.screen.blit(symbols[str(random.randint(1,9))],(positions['ticker']['x3'],positions['ticker']['y']))
                    pygame.display.flip()
                    c.wait_fun(lag)
            else:
                c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
                pygame.display.flip()
                c.wait_fun(lag)

                num2 = random.randint(1,9)
                c.screen.blit(symbols[str(num2)],(positions['ticker']['x2'],positions['ticker']['y']))
                num2_b = random.uniform(7,8)
                px_update2 = pygame.Rect(positions['ticker']['px2']+counter*width-1,positions['ticker']['py']-num2_b*15,width,num2_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update2,0)
                pygame.display.flip()
                c.wait_fun(lag)

                num3 = random.randint(1,9)
                c.screen.blit(symbols[str(num3)],(positions['ticker']['x3'],positions['ticker']['y']))
                num3_b = random.uniform(4,5)
                px_update3 = pygame.Rect(positions['ticker']['px3']+counter*width-1,positions['ticker']['py']-num3_b*15,width,num3_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update3,0)
                pygame.display.flip()
                c.wait_fun(lag)

        elif counter == counter_max+20:
            if task['wheel2']:
                c.screen.blit(symbols[task['result_sequence'][task['trial']][2]],(positions['ticker']['x2'],positions['ticker']['y']))
            else:  
                c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
                pygame.display.flip()
                c.wait_fun(lag)

                c.screen.blit(symbols[task['result_sequence'][task['trial']][2]],(positions['ticker']['x2'],positions['ticker']['y']))
                if task['wheel_hold_buttons']:
                    eeg_trigger(c,task,'automatic_stop_2')
                else:
                    eeg_trigger(c,task,'stop_2')
                num2_b = random.uniform(7,8)
                px_update2 = pygame.Rect(positions['ticker']['px2']+counter*width-1,positions['ticker']['py']-num2_b*15,width,num2_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update2,0)

                num3_b = random.uniform(4,5)
                px_update3 = pygame.Rect(positions['ticker']['px3']+counter*width-1,positions['ticker']['py']-num3_b*15,width,num3_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update3,0)

                pygame.display.flip()
                c.wait_fun(lag)

        elif counter_max+20 < counter < counter_max+40:
            if task['wheel_hold_buttons']:
                c.wait_fun(lag)
                c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
                c.screen.blit(symbols[task['result_sequence'][task['trial']][2]],(positions['ticker']['x2'],positions['ticker']['y']))
         
                pygame.display.flip()
                c.wait_fun(2*lag)

                c.screen.blit(symbols[str(random.randint(1,9))],(positions['ticker']['x3'],positions['ticker']['y']))
                pygame.display.flip()
                c.wait_fun(lag)
            else:
                c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
                c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
                c.screen.blit(symbols[task['result_sequence'][task['trial']][2]],(positions['ticker']['x2'],positions['ticker']['y']))
                pygame.display.flip()
                c.wait_fun(lag)

                num3 = random.randint(1,9)
                c.screen.blit(symbols[str(num3)],(positions['ticker']['x3'],positions['ticker']['y']))
                num3_b = random.randint(4,6)
                px_update3 = pygame.Rect(positions['ticker']['px3']+counter*width-1,positions['ticker']['py']-num3_b*15,width,num3_b*15)
                pygame.draw.rect(c.screen,PX_BLUE,px_update3,0)
                pygame.display.flip()
                c.wait_fun(lag)

        elif counter == counter_max+40:
            c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
            c.screen.blit(symbols[task['result_sequence'][task['trial']][1]],(positions['ticker']['x1'],positions['ticker']['y']))
            c.screen.blit(symbols[task['result_sequence'][task['trial']][2]],(positions['ticker']['x2'],positions['ticker']['y']))

            pygame.display.flip()
            c.wait_fun(lag)

            c.screen.blit(symbols[task['result_sequence'][task['trial']][3]],(positions['ticker']['x3'],positions['ticker']['y']))
            if task['wheel_hold_buttons']:
                if task['result_sequence'][task['trial']][0] == '1':
                    eeg_trigger(c,task,'automatic_stop_3_win')
                else:
                    eeg_trigger(c,task,'automatic_stop_3_loss')
            else:
                if task['result_sequence'][task['trial']][0] == '1':
                    eeg_trigger(c,task,'stop_3_win')
                else:
                    eeg_trigger(c,task,'stop_3_loss')
            pygame.display.flip()
            keep_spinning = False
            waitfun(wait)
        counter += 1


# def spin_prices(c,positions,buttons,task):
#     pygame.event.clear()    
#     yesterdays_close = task['current_price'][-1]
#     n = 100
#     show1 = True
#     show2 = False
#     show3 = False
#     show4 = False

#     len_spin = 20
#     width = round(210/len_spin)
#     counter = 0
#     while counter < len_spin:
#         if pygame.event.peek([MOUSEBUTTONDOWN,KEYDOWN,MOUSEBUTTONUP,KEYUP]):
#             for event in pygame.event.get():
#                 if event.type==MOUSEBUTTONDOWN:
#                     c.log('Trial ' + str(task['trial']) + ': Stopping wheels at ' + repr(time.time()) + '\n')
#                     buttons['stop'].handleEvent(event)
#                     buttons['stop'].draw(c.screen)
#                     pygame.display.update()
#                 elif event.type==MOUSEBUTTONUP:
#                     if 'click' in buttons['stop'].handleEvent(event):
#                         c.press_sound.play()
#                         buttons['place_order'].handleEvent(event)
#                         buttons['place_order'].draw(c.screen)
#                         buttons['stop'].draw(c.screen)
#                         task['pressed_stop'][task['trial']] = 1;
#                         pygame.display.update()
#                         c.wait_fun(100)
#                         counter = 40
#                 elif event.type == KEYDOWN and event.key == K_SPACE: 
#                     buttons['stop'].handleEvent(event)
#                     buttons['stop'].draw(c.screen)
#                     pygame.display.update()
#                 elif event.type == KEYUP and event.key == K_SPACE:
#                     buttons['place_order'].handleEvent(event)
#                     buttons['place_order'].draw(c.screen)
#                     buttons['stop'].handleEvent(event)
#                     buttons['stop'].draw(c.screen)
#                     pygame.display.update()
#                     counter = 40
#         else:  
#             if 0 < round(time.time()*1000) % n < n/4 and show1:
#                 num1 = random.randint(1,9)
#                 c.screen.blit(symbols[str(num1)],(positions['ticker']['x1'],positions['ticker']['y']))

#                 num1_b = random.randint(1,3)
#                 px_update = pygame.Rect(positions['ticker']['px1']+counter*width-1,positions['ticker']['py']-num1_b*15,width,num1_b*15)
#                 pygame.draw.rect(c.screen,PX_BLUE,px_update,0)

#                 pygame.display.flip()
#                 show1 = False
#                 show2 = True
#             elif n/4 < round(time.time()*1000) % n < n/2 and show2:
#                 num2 = random.randint(1,9)
#                 c.screen.blit(symbols[str(num2)],(positions['ticker']['x2'],positions['ticker']['y']))

#                 num2_b = random.randint(7,9)
#                 px_update2 = pygame.Rect(positions['ticker']['px2']+counter*width-1,positions['ticker']['py']-num2_b*15,width,num2_b*15)
#                 pygame.draw.rect(c.screen,PX_BLUE,px_update2,0)

#                 pygame.display.flip()
#                 show2 = False;
#                 show3 = True
#             elif n/2 < round(time.time()*1000) % n < 3*n/4 and show3:
#                 num3 = random.randint(1,9)
#                 c.screen.blit(symbols[str(num3)],(positions['ticker']['x3'],positions['ticker']['y']))
           
#                 num3_b = random.randint(4,6)
#                 px_update3 = pygame.Rect(positions['ticker']['px3']+counter*width-1,positions['ticker']['py']-num3_b*15,width,num3_b*15)
#                 pygame.draw.rect(c.screen,PX_BLUE,px_update3,0)

#                 counter += 1

#                 pygame.display.flip()
#                 show3 = False
#                 show4 = True
#             elif n-10 < round(time.time()*1000) % n < n and show4:
#                 c.screen.blit(spin_cover,(positions['ticker']['base_x'],positions['ticker']['base_y']))
#                 pygame.display.flip()
#                 show4 = False
#                 show1 = True

def begin_training_screen(c):
    c.blank_screen()
    c.log('Training beginning at ' + repr(time.time()) + '\n')

    c.text_screen('Die n'+ae+'chsten 6 Spiele sind zum '+Ue+'ben da. Die Punkte z'+ae+'hlen nicht zu ihrem Endergebnis dazu.', font=c.header, font_color=GOLD, valign='center', y_displacement= -45, wait_time=4000) 


def eeg_trigger(c,task,stage):

    if platform.system() == 'Windows':
        port = windll.inpoutx64
        address = 45072

    if not task['training']:
        # Set value
        if stage == 'trial':
            value = task['trial'] - task['num_training_trials']
        elif stage == 'guess_on':
            if task['current_block'] == 1:
                value = 181
            elif task['current_block'] == 2:
                value = 197
            elif task['current_block'] == 3:
                value = 213
            elif task['current_block'] == 4:
                value = 235
        elif stage == 'pressed_guess':
            if task['current_block'] == 1:
                value = 182
            elif task['current_block'] == 2:
                value = 198
            elif task['current_block'] == 3:
                value = 214
            elif task['current_block'] == 4:
                value = 236
        elif stage == 'bet+':
            if task['current_block'] == 1:
                value = 183
            elif task['current_block'] == 2:
                value = 199
            elif task['current_block'] == 3:
                value = 215
            elif task['current_block'] == 4:
                value = 237
        elif stage == 'bet-':
            if task['current_block'] == 1:
                value = 184
            elif task['current_block'] == 2:
                value = 200
            elif task['current_block'] == 3:
                value = 216
            elif task['current_block'] == 4:
                value = 238
        elif stage == 'pressed_pull':
            if task['current_block'] == 1:
                value = 185
            elif task['current_block'] == 2:
                value = 201
            elif task['current_block'] == 3:
                value = 217
            elif task['current_block'] == 4:
                value = 239
        elif stage == 'stop_1':
            if task['current_block'] == 1:
                value = 186
            elif task['current_block'] == 2:
                value = 202
        elif stage == 'pressed_stop_1':
            if task['current_block'] == 3:
                value = 218
            elif task['current_block'] == 4:
                value = 240
        elif stage == 'automatic_stop_1':
            if task['current_block'] == 3:
                value = 219
            elif task['current_block'] == 4:
                value = 241
        elif stage == 'stop_2':
            if task['current_block'] == 1:
                value = 187
            elif task['current_block'] == 2:
                value = 203
        elif stage == 'pressed_stop_2':
            if task['current_block'] == 3:
                value = 220
            elif task['current_block'] == 4:
                value = 242
        elif stage == 'automatic_stop_2':
            if task['current_block'] == 3:
                value = 221
            elif task['current_block'] == 4:
                value = 243
        elif stage == 'stop_3_win':
            if task['current_block'] == 1:
                value = 188
            elif task['current_block'] == 2:
                value = 204
        elif stage == 'stop_3_loss':
            if task['current_block'] == 1:
                value = 189
            elif task['current_block'] == 2:
                value = 205
        elif stage == 'pressed_stop_3_win':
            if task['current_block'] == 3:
                value = 222
            elif task['current_block'] == 4:
                value = 244
        elif stage == 'pressed_stop_3_loss':
            if task['current_block'] == 3:
                value = 223
            elif task['current_block'] == 4:
                value = 245
        elif stage == 'automatic_stop_3_win':
            if task['current_block'] == 3:
                value = 224
            elif task['current_block'] == 4:
                value = 246
        elif stage == 'automatic_stop_3_loss':
            if task['current_block'] == 3:
                value = 225
            elif task['current_block'] == 4:
                value = 247
        elif stage == 'win_screen_norm':
            if task['current_block'] == 1:
                value = 190
            elif task['current_block'] == 2:
                value = 206
        elif stage == 'win_screen_pressed':
            if task['current_block'] == 3:
                value = 226
            elif task['current_block'] == 4:
                value = 248
        elif stage == 'win_screen_auto':
            if task['current_block'] == 3:
                value = 227
            elif task['current_block'] == 4:
                value = 249
        elif stage == 'money_banner':
            if task['current_block'] == 1:
                value = 191
            elif task['current_block'] == 2:
                value = 207
            elif task['current_block'] == 3:
                value = 228
            elif task['current_block'] == 4:
                value = 250
        elif stage == 'gamble_screen':
            if task['current_block'] == 1:
                value = 192
            elif task['current_block'] == 2:
                value = 208
            elif task['current_block'] == 3:
                value = 229
            elif task['current_block'] == 4:
                value = 251
        elif stage == 'did_gamble':
            if task['current_block'] == 1:
                value = 193
            elif task['current_block'] == 2:
                value = 209
            elif task['current_block'] == 3:
                value = 230
            elif task['current_block'] == 4:
                value = 252
        elif stage == 'lost_gamble':
            if task['current_block'] == 1:
                value = 194
            elif task['current_block'] == 2:
                value = 210
            elif task['current_block'] == 3:
                value = 231
            elif task['current_block'] == 4:
                value = 253
        elif stage == 'won_gamble':
            if task['current_block'] == 1:
                value = 195
            elif task['current_block'] == 2:
                value = 211
            elif task['current_block'] == 3:
                value = 232
            elif task['current_block'] == 4:
                value = 254
        elif stage == 'gamble_money_banner':
            if task['current_block'] == 1:
                value = 196
            elif task['current_block'] == 2:
                value = 212
            elif task['current_block'] == 3:
                value = 233
            elif task['current_block'] == 4:
                value = 255
        


        trigger_on = value
        trigger_off = 0

        if platform.system() == 'Windows':
            #Send trigger
            port.Out32(address,trigger_on)
            core.wait(0.05)
            port.Out32(address,trigger_off)
            print "Trigger: " + str(value)
        else:
            print "Trigger: " + str(value)
        c.log('EEG: Sent trigger ' + str(value) +  ' at ' + repr(time.time()) + '\n')



