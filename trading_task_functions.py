import pygame
from pygame.locals import *
from pygame import gfxdraw
#from pylab import *
import math
import numpy
from slot_buttons import SlotButton
from time import strftime,localtime
import time
import random

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
GOLD   = ( 254, 195,  13)
TX_GREEN = (57, 255, 20)
BLACK = (0,0,0)
TX_RED = (249, 15, 0)


# Load images
intro = pygame.image.load('./images/trading_task_welcome_banner.png').convert_alpha()
small_win = pygame.image.load('./images/symbols_smallwin.png').convert_alpha()
big_win = pygame.image.load('./images/symbols_megawin.png').convert_alpha()


# Load tickers
tickers = {}
tickers['0'] = pygame.image.load('./images/trading_task_ticker0.png').convert_alpha()
tickers['1'] = pygame.image.load('./images/trading_task_ticker1.png').convert_alpha()
tickers['2'] = pygame.image.load('./images/trading_task_ticker2.png').convert_alpha()
tickers['3'] = pygame.image.load('./images/trading_task_ticker3.png').convert_alpha()

win_banner = pygame.image.load('./images/symbols_banner.png').convert_alpha()
# Pull in sounds:
spinsound = pygame.mixer.Sound('./sounds/spinning.wav')
spinsound.set_volume(0.2)
winsound = pygame.mixer.Sound('./sounds/winsound.wav')
winsound.set_volume(0.5)
bigwinsound = pygame.mixer.Sound('./sounds/bigwinsound.wav')
bigwinsound.set_volume(0.3)
spinstopsound = pygame.mixer.Sound('./sounds/spinstop.wav')
spinstopsound.set_volume(0.7)

# Load fonts
ticker_font = pygame.font.Font('./fonts/ASTRII__.TTF',60)
ticker_font_small = pygame.font.Font('./fonts/ASTRII__.TTF',35)
money_font = pygame.font.Font('./fonts/DS-DIGIB.TTF',80)
split_font = pygame.font.Font('./fonts/Oswald-Bold.ttf', 60)
def sigmoid(x):
    s =  1.0/(1.0 + numpy.exp(-1.0*x))
    return s

def logit(x):
    l = numpy.log(x) - numpy.log(1-x)
    return l

def is_odd(num):
    return num & 0x1

def welcome_screen(c, wait_time=3000):
    c.blank_screen()
    winsound.play()
    c.attn_screen(attn=intro,wait_time=wait_time)


def cashout(c, positions, buttons, sizes, task):   

    c.screen.fill(c.background_color)
    cashout_or_back = c.title.render("Leave trading floor or go back?", True, GOLD)
    c.center_text(cashout_or_back,y_offset=-100, center_x=c.center_x, center_y=c.center_y)

    button_clicked = c.choice_screen(button_txt1="Leave", button_txt2="Stay")
    if button_clicked[0] == 'left':
        c.log('Did not cash out ' + str(task['trial']) +  ' ' + repr(time.time()) + '\n')
        draw_screen(c, positions, buttons, sizes, task)
        pygame.display.update()
    elif button_clicked[0] == 'right':
        c.log('Cashing out ' + str(task['trial']) +  ' ' + repr(time.time()) + '\n')
        c.blank_screen()
        c.text_screen('Leaving the trading floor!', font=c.title, font_color=GOLD, valign='top', y_displacement= -45, wait_time=3000)  
        c.blank_screen()
        c.text_screen('Entering the market on a new day!', font=c.title, font_color=GOLD, valign='top', y_displacement= -45, wait_time=3000)  
        welcome_screen(c) 
        c.blank_screen()
    

def get_screen_elements(c, task):

    # One hold button
    hold_offset = 100

    # Button sizes
    sizes = {}
    sizes['sw'] = c.screen_width
    sizes['sh'] = c.screen_height
    sizes['bbw'] = sizes['sw']*0.2
    sizes['bbh'] = sizes['sh']*0.2

    sizes['mbw'] = sizes['sw']*0.15
    sizes['mbh'] = sizes['sh']*0.15

    sizes['sbw'] = sizes['sw']*0.1
    sizes['sbh'] = sizes['sh']*0.1

    sizes['xsbh'] = sizes['sw']*0.05
    sizes['xsbw'] = sizes['sh']*0.05    

    positions = {};
    positions['banner_x'] = 300
    positions['banner_y'] = 40

    x0 = sizes['sh']/40
    positions['bet_5_x'] = c.left_center_x+(sizes['sh']/9) - x0
    positions['bet_5_y'] = c.center_y+(sizes['sh']/3) - hold_offset

    positions['scoreboard_x'] = 20
    positions['scoreboard_y'] = c.bottom_y - 100

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

    positions['scoreboard_x'] = 20
    positions['scoreboard_y'] = c.bottom_y - 100
    positions['account_screen_y'] = c.top_y+0.1*sizes['sh']

    positions['yesterdays_close_x'] = c.center_x+80
    positions['yesterdays_close_y'] = 190

    # Side stocks
    positions['mini_stocks'] = {}
    positions['mini_stocks']['x'] = c.right_x - 200
    positions['mini_stocks']['y0'] = c.center_y - 310
    positions['mini_stocks']['y1'] = c.center_y - 85
    positions['mini_stocks']['y2'] = c.center_y + 140

    positions['ticker'] = {}
    positions['ticker']['base_x'] = c.center_x-(tickers['0'].get_width()/2)
    positions['ticker']['base_y'] = 50
    positions['ticker']['x1'] =  c.center_x-(tickers['0'].get_width()/2) + 100 - 50
    positions['ticker']['x2'] = c.center_x-(tickers['0'].get_width()/2) + 300 - 40
    positions['ticker']['x3'] = c.center_x-(tickers['0'].get_width()/2) + 500 - 15
    positions['ticker']['y']  =  7*tickers['0'].get_height()/10

    # Set up buttons
    buttons = {}
    
    buttons['add_five'] = SlotButton(rect=(positions['bet_5_x'],positions['bet_5_y'], sizes['sbw'],sizes['sbh']),\
    caption="+5 shares", fgcolor=c.background_color, bgcolor=BLUE, font=c.button,highlight=YELLOW)

    buttons['add_ten']= SlotButton(rect=(positions['bet_10_x'],positions['bet_10_y'], sizes['sbw'],sizes['sbh']),\
    caption="+10 shares", fgcolor=c.background_color, bgcolor=GREEN, font=c.button)

    buttons['cashout'] = SlotButton(rect=(positions['cashout_x'],positions['cashout_y'], sizes['bbw']+35,sizes['xsbh']),\
        caption="Cashout", fgcolor=c.background_color, bgcolor=WHITE, font=c.button)
   
    buttons['place_order'] = SlotButton(rect=(positions['pull_x'],positions['pull_y'], sizes['mbw'],1.42*sizes['sbh']),\
    caption="Place Order", fgcolor=c.background_color, bgcolor=PURPLE, font=c.header)

    buttons['stop'] = SlotButton(rect=(positions['pull_x'],positions['stop_y']+40, sizes['mbw'],1.42*sizes['sbh']),\
    caption="Stop", fgcolor=c.background_color, bgcolor=RED, font=c.header)

    buttons['clear'] = SlotButton(rect=(positions['bet_5_x'],positions['clear_y'], sizes['sbw']+(positions['bet_10_x']-positions['bet_5_x']),sizes['xsbh']),\
    caption="Clear", fgcolor=c.background_color, bgcolor=BRIGHT_ORANGE, font=c.button)

    c.screen.fill(c.background_color)

    return positions, buttons, sizes

def draw_screen(c, positions, buttons, sizes, task):
    c.screen.fill(c.background_color)
    all_stocks = [0,1,2,3]
    all_stocks.remove(task['stock'])

    for idx,num in enumerate(all_stocks):
        buttons['mini_stock_' + str(idx) ] = SlotButton(normal='./images/trading_task_stock' + str(num) + '.png', 
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

    yesterdays_close = task['current_price'][task['stock']][-1]
    close_price = ticker_font_small.render('Prev. Close: ' + str(yesterdays_close), True, WHITE)
    c.screen.blit(close_price,(positions['yesterdays_close_x'],positions['yesterdays_close_y']))


    for key in buttons:
        buttons[key].draw(c.screen)

    task['all_stocks'] = all_stocks
    display_assets(c,positions,sizes,task)

    return buttons

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
    if task['trial_stage'] == 'trade': 
        task['account'][task['trial']] = task['account'][task['trial']]
    elif task['trial_stage'] == 'result':     
        # Update the account with the latest win or loss
        task['account'][task['trial']] = task['account'][task['trial']] + task['winloss'][task['trial']]

  #  task['account_balance'] = task['account_balance'] - task['buy_price']*task['trade_size']
    return task

def clear(c,task):
    if len(task['trade_sequence']) > 0:
        if task['trade_size'][task['trial']] > 0:
            task['account'][task['trial']] += task['trade_sequence'][-1]
            task['trade_size'][task['trial']] = task['trade_size'][task['trial']] - task['trade_sequence'][-1]
            del task['trade_sequence'][-1]
    return task

def stock_split(c,task, positions, sizes):
    c.screen.fill(WHITE)
    card_back = pygame.image.load('./images/trading_task_news1.png').convert_alpha()
    card_won = pygame.image.load('./images/trading_task_news_win.png').convert_alpha()
    card_lost = pygame.image.load('./images/trading_task_news_lose.png').convert_alpha()

    x_pos = c.center_x-card_back.get_width()/2
    y_pos = c.center_y-card_back.get_height()/2 - 20

    fpos_x = c.center_x
    fpos_y = c.center_y-50
    
   
    c.screen.blit(card_back,(x_pos,y_pos))
    c.make_banner(split_font.render("Hold position to see if your stock splits?", True, BLACK))
    c.screen.blit(split_font.render("?",True,BLACK),(fpos_x,fpos_y))
    pygame.display.update()
    waitfun(1000)

    gamble_button = SlotButton(rect=(c.left_center_x-sizes['bbw']/2,c.bottom_y+sizes['sbh'], sizes['bbw'],sizes['sbh']),\
        caption="Hold",  fgcolor=c.background_color, bgcolor=RED, font=c.button)
    no_gamble_button = SlotButton(rect=(c.right_center_x-sizes['bbw']/2,c.bottom_y+sizes['sbh'],sizes['bbw'],sizes['sbh']),\
        caption="No thanks.", fgcolor=c.background_color, bgcolor=GREEN, font=c.button)

    decided = False
    CARD = pygame.USEREVENT + 1
    pygame.time.set_timer(CARD, 1000)
    time_elapsed = 0
    start_time = time.time()
    c.screen.blit(card_back,(x_pos,y_pos))
    c.screen.blit(split_font.render("3",True,BLACK),(fpos_x,fpos_y))
    c.make_banner(split_font.render("Hold position to see if your stock splits?", True, BLACK))
    gamble_button.draw(c.screen)
    no_gamble_button.draw(c.screen)
    pygame.display.update()


    while not decided and time_elapsed < 3:
        time_elapsed = int(round(time.time()-start_time))
        for event in pygame.event.get():
            if event.type in (MOUSEBUTTONUP, MOUSEBUTTONDOWN):
                if 'click' in gamble_button.handleEvent(event): 
                    c.log('Decided to Gamble on trial ' + str(task['trial']) +  ' ' + repr(time.time()) + '\n')
                    if int(task['result_sequence'][task['trial']][5]) == 1:
                        task['account'][task['trial']] = task['account'][task['trial']] + task['winloss'][task['trial']]
                        c.screen.blit(card_won,(x_pos,y_pos))
                        gamble_button.draw(c.screen)
                        pygame.display.flip()
                        winsound.play()
                        waitfun(1000)
                        task['winloss'][task['trial']] = 2*task['winloss'][task['trial']]
                        #show_win_banner(c, positions, task['winloss'][task['trial']])
                        #winsound.play()
                        decided = True
                    elif int(task['result_sequence'][task['trial']][5]) == 0:
                        gamble_button.draw(c.screen)
                        pygame.display.flip()
                        c.screen.blit(card_lost,(x_pos,y_pos))
                        pygame.display.flip()
                        waitfun(1000)
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
                c.make_banner(split_font.render("Hold position to see if your stock splits?", True, BLACK))
                pygame.display.flip()
def win_screen(c,positions, buttons, sizes, task):
    counter = 0

    if task['reward_grade'][task['trial']] < 8:
        numsparkle = 3  
        winnerblit = small_win
        
    else:
        numsparkle = 5
        winnerblit = big_win
        

    while counter < numsparkle:
        if numsparkle == 5:
            bigwinsound.play()
        else:
            winsound.play()
        c.screen.blit(pygame.transform.scale(winnerblit, (c.screen_width, c.screen_height)),(10,10))
        pygame.display.update()
        waitfun(800)
        draw_screen(c, positions, buttons, sizes, task)
        counter += 1

    draw_screen(c, positions, buttons, sizes, task)

def show_win_banner(c,positions,reward):
    c.screen.blit(win_banner,(positions['banner_x'],positions['banner_y'])) 
    winsound.play()
    c.text_screen('You gained ' + str(reward) + '!!', font=c.title, valign='top', y_displacement= -200, wait_time=800)

def result(c, positions, buttons, sizes, task):
    percent_change = [.001,.002,.003,.004,.005,.006,.007,.008,.009,.01]
    wait = 190

    c.screen.blit(tickers[str(task['stock'])],(positions['ticker']['base_x'],positions['ticker']['base_y']))

    yesterdays_close = task['current_price'][task['stock']][-1]

    if task['result_sequence'][task['trial']][0] == '1': # win
        task['reward_grade'][task['trial']] = int(task['result_sequence'][task['trial']][2])
        reward = task['trade_size'][task['trial']]*percent_change[task['reward_grade'][task['trial']]]*task['current_price'][task['stock']][-1] 
        task['winloss'][task['trial']] = reward
        task['current_price'][task['stock']].append(task['current_price'][task['stock']][-1]+reward)

        increment = math.floor(reward)
        open_price = yesterdays_close+increment
        op = ticker_font.render('+' + str(open_price), True, TX_GREEN)
        c.screen.blit(op,(positions['ticker']['x1'],positions['ticker']['y']))

        midday_price = open_price+increment
        mp = ticker_font.render('+' + str(midday_price), True, TX_GREEN)
        c.screen.blit(mp,(positions['ticker']['x2'],positions['ticker']['y']))

        close_price = ticker_font.render('+' + str(task['current_price'][task['stock']][-1]), True, TX_GREEN)
        c.screen.blit(close_price,(positions['ticker']['x3'],positions['ticker']['y']))
        pygame.display.flip()
        waitfun(500)
        #win_screen(c,positions, buttons, sizes, task)
        show_win_banner(c,positions,reward)

    elif task['result_sequence'][task['trial']][0] == '2': # near miss

        open_price = yesterdays_close+round(100*random.uniform(0,5))/100
        op = ticker_font.render('+' + str(open_price), True, TX_GREEN)
        c.screen.blit(op,(positions['ticker']['x1'],positions['ticker']['y']))

        midday_price = open_price+round(100*random.uniform(0,5))/100
        mp = ticker_font.render('+' + str(midday_price), True, TX_GREEN)
        c.screen.blit(mp,(positions['ticker']['x2'],positions['ticker']['y']))

        close_price = yesterdays_close-round(100*random.uniform(0,5))/100
        cp = ticker_font.render(str(close_price), True, TX_RED)
        c.screen.blit(cp,(positions['ticker']['x3'],positions['ticker']['y']))
        pygame.display.flip()
        waitfun(500)

        task['reward_grade'][task['trial']] = 0
        task['winloss'][task['trial']] = (close_price-yesterdays_close)*task['trade_size'][task['trial']]

    elif task['result_sequence'][task['trial']][0] == '0': # loss
        task['reward_grade'][task['trial']] = 0
        task['winloss'][task['trial']] = 0

        open_price,px_o,o1 = print_prices_spin(yesterdays_close)
        c.screen.blit(open_price,(positions['ticker']['x1']+o1,positions['ticker']['y']))
        midday_price, px_m,o2 = print_prices_spin(px_o)
        c.screen.blit(midday_price,(positions['ticker']['x2']+o2,positions['ticker']['y']))

        close_price = yesterdays_close-round(100*random.uniform(0,5))/100
        cp = ticker_font.render(str(close_price), True, TX_RED)
        c.screen.blit(cp,(positions['ticker']['x3'],positions['ticker']['y']))
        pygame.display.flip()
        waitfun(500)

        task['reward_grade'][task['trial']] = 0
        task['winloss'][task['trial']] = (close_price-yesterdays_close)*task['trade_size'][task['trial']]

    if int(task['result_sequence'][task['trial']][4]) == 1:
        stock_split(c, task, positions, sizes)
        c.screen.fill(c.background_color)

    task = update_account(c,positions, sizes, task)
    return task
        
def display_assets(c,positions,sizes,task):

    bet_screen_inside = pygame.Rect(positions['bet_screen_x']+5,positions['bet_screen_y']+5,sizes['bbw']+35, sizes['sbh']-13)
    pygame.draw.rect(c.screen,c.background_color,bet_screen_inside,0)

    bet_banner = money_font.render(str(task['trade_size'][task['trial']]),True,RED) 
    c.surf_center_text(bet_banner, bet_screen_inside,0,0)

    bet_label = c.title.render("Shares",True,RED) 
    c.screen.blit(bet_label,(positions['bet_screen_x']+5, positions['bet_screen_y']-60))

    account_screen_inside = pygame.Rect(positions['scoreboard_x']+1,positions['account_screen_y']+1,sizes['bbw']+33, 1.2*sizes['bbh']-2)
    pygame.draw.rect(c.screen,c.background_color,account_screen_inside,0)

    account_banner = c.header.render("Account Balance:",True,GOLD) 
    c.screen.blit(account_banner, (positions['scoreboard_x'] + 10,positions['account_screen_y'] + 10))
    
    account_balance = money_font.render(str(task['account'][task['trial']]), True, RED)
    c.screen.blit(account_balance,(positions['scoreboard_x'] + 20,positions['account_screen_y'] + account_banner.get_height() + 10))
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

# def show_win_banner(c,positions,reward):
#     c.screen.blit(win_banner,(positions['banner_x'],positions['banner_y'])) 
#     winsound.play()
#     c.text_screen('You won ' + str(reward) + ' AUD!!', font=c.title, valign='top', y_displacement=-100, wait_time=800)


def spin_prices(c,positions,buttons,task):
    pygame.event.clear()    
    yesterdays_close = task['current_price'][task['stock']][-1]
    n = 400
    show1 = True
    show4 = False

    counter = 0
    while counter < 20:
        if pygame.event.peek([MOUSEBUTTONDOWN,KEYDOWN,MOUSEBUTTONUP,KEYUP]):
            for event in pygame.event.get():
                if event.type==MOUSEBUTTONDOWN:
                    c.log('Trial ' + str(task['trial']) + ': Stopping wheels at ' + repr(time.time()) + '\n')
                    buttons['stop'].handleEvent(event)
                    buttons['stop'].draw(c.screen)
                    pygame.display.update()
                elif event.type==MOUSEBUTTONUP:
                    if 'click' in buttons['stop'].handleEvent(event):
                        c.press_sound.play()
                        buttons['place_order'].handleEvent(event)
                        buttons['place_order'].draw(c.screen)
                        buttons['stop'].draw(c.screen)
                        task['pressed_stop'][task['trial']] = 1;
                        pygame.display.update()
                        c.wait_fun(100)
                        counter = 40
                elif event.type == KEYDOWN and event.key == K_SPACE: 
                    buttons['stop'].handleEvent(event)
                    buttons['stop'].draw(c.screen)
                    pygame.display.update()
                elif event.type == KEYUP and event.key == K_SPACE:
                    buttons['place_order'].handleEvent(event)
                    buttons['place_order'].draw(c.screen)
                    buttons['stop'].handleEvent(event)
                    buttons['stop'].draw(c.screen)
                    pygame.display.update()
                    counter = 40
        else:   
            if 0 < round(time.time()*1000) % n < n/4 and show1:
                open_price,px_o,o1 = print_prices_spin(yesterdays_close)
                c.screen.blit(open_price,(positions['ticker']['x1']+o1,positions['ticker']['y']))
                midday_price, px_m,o2 = print_prices_spin(px_o)
                c.screen.blit(midday_price,(positions['ticker']['x2']+o2,positions['ticker']['y']))
                close_price, px_c,o3 = print_prices_spin(px_m)
                c.screen.blit(close_price,(positions['ticker']['x3']+o3,positions['ticker']['y']))
                show1 = False
                show4 = True
                pygame.display.flip()
            elif n-10 < round(time.time()*1000) % n < n and show4:
                c.screen.blit(tickers[str(task['stock'])],(positions['ticker']['base_x'],positions['ticker']['base_y']))
                yesterdays_close = task['current_price'][task['stock']][-1]
                close_price = ticker_font_small.render('Prev. Close: ' + str(yesterdays_close), True, WHITE)
                c.screen.blit(close_price,(positions['yesterdays_close_x'],positions['yesterdays_close_y']))
                pygame.display.flip()
                show4 = False
                show1 = True
                counter += 1


