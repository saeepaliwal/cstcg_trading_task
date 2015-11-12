# -*- coding: utf-8 -*-

## Import libraries
import pygame, os, string, time
from time import strftime,localtime

from pygame.locals import *
# Load all the variables and the screen from load_all
from load_all import *

#from pygame.locals import *
pygame.init()
x = 0
y = 0
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
background = pygame.Surface(screen.get_size())
screen = pygame.display.set_mode((600,750))


# Define where the wheel images will blit
def sprite_disp(num,pos):
      
    if pos == 1:
        screenpos = 45
    elif pos == 2:
        screenpos = 225
    elif pos == 3:
        screenpos = 405

    if num == 1:
        picnum = 'one'
    elif num == 2:
        picnum = 'two'
    elif num == 3:
        picnum = 'three'
    elif num == 4:
        picnum = 'four'
    elif num == 5:
        picnum = 'five'
    elif num == 6:
        picnum = 'six'
    elif num == 7:
        picnum = 'seven'
    elif num == 8:
        picnum = 'eight'
    elif num == 9:
        picnum = 'nine'
    elif num == 10:
        picnum = 'jackpot'

    return (picnum,screenpos)

def center_text(text, destsurf,destsurfposx,destsurfposy):
    blitsurf = pygame.Surface(destsurf.get_size())
    textpos = text.get_rect()
    textpos.centerx = blitsurf.get_rect().centerx+destsurfposx
    textpos.centery = blitsurf.get_rect().centery+destsurfposy
    return textpos

 
# Truncates a written line for wrapped texts (in the final questionnaire)
def truncline(text, font, maxwidth):
    real=len(text)       
    stext=text           
    l=font.size(text)[0]
    cut=0
    a=0                  
    done=1
    while l > maxwidth:
        a=a+1
        n=text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext= n[:-cut]
        else:
            stext = n
            l=font.size(stext)[0]
            real=len(stext)               
            done=0                        
    return real, done, stext             
        
# Wraps text for multi-line user input
def wrapline(text, font, maxwidth): 
    done=0                      
    wrapped=[]                  
                               
    while not done:         
        nl, done, stext=truncline(text, font, maxwidth) 
        wrapped.append(stext.strip())                  
        text=text[nl:]                                 
    return wrapped
 
 # Non busy wait function for python
def waitfun(milliseconds):
    nowtime = pygame.time.get_ticks()
    while pygame.time.get_ticks()-nowtime < milliseconds:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Check if buttons on the game screen are pressed
def pressed(mouse,button,num):
        
    if num == 1:
        testpress = button.get_rect(center=(135,540)).collidepoint(mouse[0],mouse[1])
    elif num == 3:
        testpress = button.get_rect(center=(265,540)).collidepoint(mouse[0],mouse[1])
    elif num == 4:
        testpress = button.get_rect(center=(455,540)).collidepoint(mouse[0],mouse[1])
    elif num==5:
        testpress = button.get_rect(center=(130,610)).collidepoint(mouse[0],mouse[1])
    elif num==6:
        testpress = button.get_rect(center=(470,610)).collidepoint(mouse[0],mouse[1])
    elif num==7:
        testpress = button.get_rect(center=(310, 610)).collidepoint(mouse[0],mouse[1])
    elif num==8:
        testpress = button.get_rect(center=(535,645)).collidepoint(mouse[0],mouse[1])
    elif num==9:
        testpress = button.get_rect(center=(130,660)).collidepoint(mouse[0],mouse[1])
    elif num==10:
        testpress = button.get_rect(center=(308,660)).collidepoint(mouse[0],mouse[1])
        
    return testpress

# Display box for the final questionnaire
def display_box_fq(screen, message):
    fqnamebox = pygame.image.load('./images/fqnamebox.png').convert_alpha()
    screen.blit(fqnamebox,(75,400))
    yoffset = 25
    if len(message) != 0:
        blitmessage = wrapline(message,calibri18,430)
        
        for j in range(len(blitmessage)):
            screen.blit(calibri18.render(blitmessage[j],True,black),(90,415+yoffset*j))
        pygame.display.flip()

# Mechanics of the introductory screen
def intro_screen():
    global q1slide1pos, q1slide2pos, q1slide3pos, q1slide4pos

    screen.fill(black)
    screen.blit(capth150.render("Slots!", True, gold),(180,200))
    pygame.display.update()
    waitfun(1500)
    screen.fill(black)
    slide1 = pygame.image.load('./introscreen/Slide1.png').convert()
    screen.blit(slide1,(0,0))
   
    # End screen
    einleitung = pygame.Rect(257,158,385,35)
    gewinn = pygame.Rect(254,216,385,35)
    addcash = pygame.Rect(254,278,385,35)
    automatwech = pygame.Rect(254,342,385,35)
    auszahlen = pygame.Rect(254,402,385,35)
    
    zurueck = pygame.Rect(41,589,160,50)
    weiter = pygame.Rect(699,590,160,50)
     
    pygame.display.update()

    introduced = False
    slidecount = 1
    numslides = 13
   
    while not introduced and slidecount < numslides:
        for event in pygame.event.get():

            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                
                if weiter.collidepoint(mouse[0],mouse[1]):
                    presssound.play()
                    slidecount += 1
                    screen.blit(pygame.image.load('./introscreen/Slide' + repr(slidecount) + '.png').convert(),(0,0))
                    pygame.display.update()      
                elif zurueck.collidepoint(mouse[0],mouse[1]) and slidecount > 1:
                    presssound.play()
                    slidecount = slidecount - 1
                    screen.blit(pygame.image.load('./introscreen/Slide' + repr(slidecount) + '.png').convert(),(0,0))
                    pygame.display.update()
                elif slidecount == 12:
                    introduced = True;
                    if einleitung.collidepoint(mouse[0],mouse[1]):
                        presssound.play()
                        slidecount = 5
                        screen.blit(pygame.image.load('./introscreen/Slide' + repr(slidecount) + '.png').convert(),(0,0))
                        pygame.display.update()
                        slidecount = 11
                        introduced = False;
                    elif gewinn.collidepoint(mouse[0],mouse[1]):
                        presssound.play()
                        slidecount = 6
                        screen.blit(pygame.image.load('./introscreen/Slide' + repr(slidecount) + '.png').convert(),(0,0))
                        pygame.display.update()
                        slidecount = 11
                        introduced = False;
                    elif addcash.collidepoint(mouse[0],mouse[1]):
                        presssound.play()
                        slidecount = 9
                        screen.blit(pygame.image.load('./introscreen/Slide' + repr(slidecount) + '.png').convert(),(0,0))
                        pygame.display.update()
                        slidecount = 11
                        introduced = False;
                    elif automatwech.collidepoint(mouse[0],mouse[1]):
                        presssound.play()
                        slidecount = 10
                        screen.blit(pygame.image.load('./introscreen/Slide' + repr(slidecount) + '.png').convert(),(0,0))
                        pygame.display.update()
                        slidecount = 11
                        introduced = False;
                    elif auszahlen.collidepoint(mouse[0],mouse[1]):
                        presssound.play()
                        slidecount = 11
                        screen.blit(pygame.image.load('./introscreen/Slide' + repr(slidecount) + '.png').convert(),(0,0))
                        pygame.display.update()
                        slidecount = 11
                        introduced = False;
            elif event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                
            
    screen.blit(pygame.image.load('./introscreen/Slide' + repr(numslides) + '.png').convert(),(0,0))
    pygame.display.update()
    waitfun(1000)


# Credits aufladen screen refresh (for when credits are added)
def cash_screen():
    global cash, initial_cash, credits, currentwinloss, to10, to30, addtwoeur, cleared
    
    screen.fill(black)
    kontocash = float(cash)*conversionfactor
    screen.blit(dsdgib35.render(str('%.2f' % kontocash) + " EUR",True,red),(370,200))
    moneyinmachine = float(credits)*conversionfactor
    screen.blit(dsdgib35.render(str('%.2f' % moneyinmachine) + " EUR",True,red),(370,250))
 
    screen.blit(csbutton, (220,400))
    screen.blit(pull,(203,600))

    if not cleared:
        screen.blit(clear,(220,500))
    else:
        screen.blit(press4,(220,500))
    screen.blit(clearme,center_text(clearme,clear,220,500))

    # Text:
    if deutsch:
        geld = capth65.render("Geld aufladen", True, gold)
        screen.blit(geld,center_text(geld,screen,0,-280))
        screen.blit(capth25.render("Geldbeutel: ",True,gold),(153,200))
        screen.blit(capth25.render("Geld im Automaten: ",True,gold),(18,250))    
        oneeur1 = capth25.render("Einen Euro aus Ihrem",True,gold)
        oneeur2 = capth25.render("Geldbeutel in den Automaten:",True,gold)
                
        screen.blit(oneeur1,center_text(oneeur1,screen,-40,-55))
        screen.blit(oneeur2,center_text(oneeur1,screen,-40,-15))
        to10 = capth25.render("1 EUR zum",True,black)
        to102 = capth25.render("Spiel",True,black)
        screen.blit(to10,center_text(to10,csbutton,220,385))
        screen.blit(to102,center_text(to102,csbutton,220,415))
        fertigtext = capth25.render("Fertig",True,black)
        screen.blit(fertigtext,center_text(fertigtext,pull,203,600))
    else:
        screen.blit(capth150.render("Cash", True, gold),(80,0))
        screen.blit(capth25.render("Current Account: ",True,gold),(90,200))
        screen.blit(capth25.render("Win/loss: ",True,gold),(217,250))    
        screen.blit(capth40.render("Top up:",True,gold), (200,320))           
        to10 = capth25.render("To 10",True,black)
        to30 = capth25.render("To 30",True,black)
        screen.blit(to10,(160,420))    
        screen.blit(to30,(360,420))

    pygame.display.update()

# Credits aufladen main screen mechanics
def top_up():
    global cash, initial_cash, credits, csbutton, currentwinloss, to10, to30, savings, cashforgame, addtwoeur, cleared, counter

    of.write('Topping up after trial ' + repr(counter-1) + ' cash in pocket is still: ' + repr(cash) + ' at ' + repr(time.time() ) + ' \n')
    sof.write('Topping up after trial ' + repr(counter-1) + ' cash in pocket is still: ' + repr(cash) + ' at ' + repr(time.time() ) + ' \n')    

    currentwinloss = cash + credits - initial_cash
    cash_screen()
    cspressed = pygame.image.load(pressed12).convert_alpha()
    checkedcash = False
    #toppedup = False
    cleared = False
    topup_amt = 0
    while not checkedcash:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                
                # Top up to 10
                if csbutton.get_rect(center=(300,440)).collidepoint(mouse[0],mouse[1]):
                    presssound.play()
                    cleared = False
                    topup = min(100,cash)
                    topup_amt = topup
                    if topup_amt < 0:
                        topup_amt = 0
                    cash = cash - topup_amt
                    cashforgame += topup_amt
                    credits = credits + topup_amt
                    of.write('Toping up ' + repr(topup) + 'adding ' + repr(topup_amt) + ' at ' + repr(time.time()) + '\n')
                    sof.write('Top up: ' + repr(topup_amt) + ' New cash: ' + repr(cash) + ' at ' + repr(time.time()) + '\n')
                    cash_screen()
                    screen.blit(cspressed, (220,400))
                    to10 = capth25.render("1 EUR zum",True,black)
                    to102 = capth25.render("Spiel",True,black)
                    screen.blit(to10,center_text(to10,csbutton,220,385))
                    screen.blit(to102,center_text(to102,csbutton,220,415))
                    pygame.display.update()
                    waitfun(300)
                    screen.blit(csbutton, (220,400))
                    screen.blit(to10,center_text(to10,csbutton,220,385))
                    screen.blit(to102,center_text(to102,csbutton,220,415))
                    pygame.display.update()
                    #toppedup = True
                elif clear.get_rect(center=(300,520)).collidepoint(mouse[0],mouse[1]) and not cleared:
                    presssound.play()
                    screen.blit(press4,(220,500))
                    screen.blit(clearme,center_text(clearme,press4,220,500))
                    pygame.display.update()
                    #toppedup = False
                    cleared = True
                    cash = cash + topup_amt
                    cashforgame = cashforgame - topup_amt
                    credits = credits - topup_amt
                    of.write('Cancelled top up of ' + repr(topup_amt) + ' at ' + repr(time.time()) + '\n')
                    sof.write('Cancelled top up of ' + repr(topup_amt) + ' at ' + repr(time.time()) + '\n')
                    cash_screen()
                elif pull.get_rect(center=(302,640)).collidepoint(mouse[0],mouse[1]):
                    presssound.play()
                    of.write('Back to main screen ' + repr(time.time()) + '\n')
                    topup = 0
                    refresh_screen()
                    checkedcash = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
                                       
# Display box for the intro screen and the patient information scren
def display_box(screen, message):
    namebox = pygame.image.load('./images/namebox.png').convert_alpha()
    screen.blit(namebox,(45,200))
    if len(message) != 0:
        screen.blit(calibri23.render(message, 1, black),
                    (60,215))
        pygame.display.flip()
        
# Mechanics of the patient information screen
def patient_information_screen():
        
    question = "Name"
    current_string = []
    display_box(screen, question + ": " + string.join(current_string,""))
        
    trace1txt = capth20.render("Deutsch", True, black)
    trace2txt = capth20.render("English", True, black)
    tracebutton = pygame.image.load(etbutton).convert_alpha()
    tracebuttonpressed = pygame.image.load(pressed12).convert_alpha()
    startbutton = pygame.image.load(button4).convert_alpha()
    starttxt = capth20.render("Begin",True, black)
    welcomebanner = capth65.render("Willkommen!",True,gold)
    screen.blit(welcomebanner,center_text(welcomebanner,screen,0,-250))
    screen.blit(tracebutton,(105,350))
    screen.blit(tracebuttonpressed,(305,350))
    screen.blit(trace1txt, (135,373))
    screen.blit(trace2txt, (338,373))
    screen.blit(startbutton, (200,450))
    screen.blit(starttxt, center_text(starttxt,startbutton,200,450))
    pygame.display.update()
    deutsch = False
    
    clicked = False
    formdone = False
    while not formdone:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if tracebutton.get_rect(center=(185,390)).collidepoint(mouse[0],mouse[1]):
                    screen.blit(tracebuttonpressed,(105,350))
                    screen.blit(trace1txt, (135,373))
                    pygame.display.update()
                    presssound.play()
                    deutsch = True
                    clicked = True
                elif startbutton.get_rect(center=(290,470)).collidepoint(mouse[0],mouse[1]) and len(current_string)>0 and clicked:
                    presssound.play()
                    formdone = True
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    current_string = current_string[0:-1]
                elif event.key == K_MINUS:
                    current_string.append("_")
                elif event.key != 13:
                    current_string.append(event.unicode)
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
            display_box(screen, question + ": " + string.join(current_string,""))

    return (string.join(current_string,""), deutsch) # this will utimately be the foldername

    
# Primary exit screen (for when the hot pink button is pressed)
def exit_screen():
    loopmusic.stop()
    of.write('Trying to exit the game ' + repr(time.time()) + '\n')
    waitfun(200)
    screen.fill(black) 
    current_string = []
    screen.blit(pull, (200,550))
    
    # Text:
    if deutsch:
        ende = capth150.render("Ende", True, gold)
        screen.blit(ende,center_text(ende,screen,0,-300))
        zumbeenden = capth20.render("Zum Beenden Code eingeben und Enter dr"+ue+"cken:",True,gold)
        screen.blit(zumbeenden,center_text(zumbeenden,screen,0,-200))
        display_box(screen, "Code: " + string.join(current_string,"")) 
        zr = capth25.render("Zur"+ue+"ck",True,black)
        screen.blit(zr,center_text(zr,pull,200,550))
        pygame.display.update()
    else:
        screen.blit(capth150.render("Exit", True, gold),(110,0))
        screen.blit(capth20.render("Enter the exit code below and hit enter:",True,gold),(45,170))
        display_box(screen, "Exit code: " + string.join(current_string,""))        
        screen.blit(capth25.render("Back",True,black),(265,570))
        pygame.display.update()
       
    formdone = False
    exitme = False
    while not formdone:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    current_string = current_string[0:-1]
                elif event.key == K_MINUS:
                    current_string.append("_")
                elif event.key <= 127 and event.key != 13:
                    current_string.append(chr(event.key))
                elif event.key == 13 and string.join(current_string,"") == "tnuz":
                    formdone = True
                    exitme = True
                if deutsch:
                    display_box(screen,"Code: " + string.join(current_string,""))
                else:
                    display_box(screen,"Exit code: " + string.join(current_string,""))
            elif event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if pull.get_rect(center=(300,590)).collidepoint(mouse[0],mouse[1]):
                    presssound.play()
                    of.write('Cancelled exit ' + repr(time.time()) + '\n')
                    refresh_screen()
                    loopmusic.play(100,0)
                    formdone = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    if exitme:
        of.write('Exiting the game at ' + repr(time.time()) + '\n')
        exit()


# Exit screen after all trials are up
def final_exit_screen():
    global initial_cash, cash, wlpergame, credits, totaltrialsplayed
    done_screen()
    
    finalperf = 0
    for i in wlpergame:
        finalperf = finalperf+i
    finalperf = initial_cash + finalperf;

    perf_by_game_screen()
    gameoversound.play()
    waitfun(5000)
    of.write('Final balance: ' + repr(cash+credits) + ' Final w/l: ' + repr(cash+credits-initial_cash) + ' ' + repr(time.time()) + '\n')
    of.write('Now sending to final questionnaire ' + ' ' + repr(time.time()) + '\n')
    sof.write('Final balance: ' + repr(cash+credits) + ' Final w/l: ' + repr(cash+credits-initial_cash) + ' ' + repr(time.time()) + '\n')
    done_screen()
    waitfun(1000)
    exit()

    # Close the output file
    final_questionnaire()
    
    pygame.display.set_mode((600,750))
    screen.fill(black)
    et = capth150.render("Exit", True, gold)
    screen.blit(et,center_text(et,screen,0,-300))
    screen.blit(capth25.render("Final cash: ",True,gold),(110,200))
    convertedfinalperf = float(finalperf)*conversionfactor
    screen.blit(dsdgib35.render(str('%.2f' % convertedfinalperf),True,red),(300,200))
    screen.blit(capth25.render("Final wins: ",True,gold),(110,250))
    convertedtic = conversionfactor*(float(finalperf)-float(initial_cash))
    screen.blit(dsdgib35.render(str('%.2f' % convertedtic),True,red),(300,250))
    screen.blit(pull, (200,550))
    exitmetext = capth30.render("Exit",True,black)
    screen.blit(exitmetext,center_text(exitmetext,pull,200,550))
    pygame.display.update()
    exited = False
    while not exited:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()  
                if pull.get_rect(center=(300,590)).collidepoint(mouse[0],mouse[1]):
                    header.write('Total trials played: ' + repr(totaltrialsplayed) + '\n')
                    exited=True
                    of.close()
                    dof.close()
                    qof.close()
                    sof.close()
                    header.close()
                    f.close()
                    exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

# Quick done screen that tells the players they are finished with a particular section (or the game)
def done_screen():
    loopmusic.stop()
    waitfun(200)
    screen.fill(black)

    of.write('Done ' + repr(time.time()) + '\n')
    if deutsch:
        donetext = capth150.render("Fertig", True,gold)
    else:
        donetext = capth150.render("DONE!!", True,gold)
        
    of.write('Fertig screen at ' + repr(time.time()) + '\n')    
    screen.blit(donetext,center_text(donetext,screen,0,-50))
    pygame.display.update()
    waitfun(1000) 

# Screen that has the table of scores to check point values
def score_screen():
    
    # Write to file
    of.write('Checking scores ' + repr(time.time()) + '\n')
    sof.write('Checking scores ' + repr(time.time()) + '\n')
    screen.fill(black)    

    screen.blit(scoreboard,(60,160))
    backbutton = pygame.image.load(button4).convert_alpha()
    screen.blit(backbutton, (210,640))
    screen.blit(scorebet1, (132,125))
    screen.blit(scorebet3,(309,125))
    
    # Text:
    if deutsch:
        takemeback = capth20.render("Zur"+ue+"ck",True,black)
        screen.blit(scorebanner,center_text(scorebanner,screen,0,-300))
        screen.blit(takemeback, center_text(takemeback,backbutton,210,640))
    else:
        takemeback = capth20.render("BACK",True,black)     
        screen.blit(scorebanner,center_text(scorebanner,screen,0,-300))
        screen.blit(takemeback, center_text(takemeback,backbutton,210,640))

    pygame.display.update()
    
    goback = False
    while not goback:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if backbutton.get_rect(center=(300,660)).collidepoint(mouse[0],mouse[1]):
                    of.write('Done checking scores ' + repr(time.time()) + '\n')
                    sof.write('Done checking scores ' + repr(time.time()) + '\n')
                    refresh_screen()
                    goback = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

def perf_by_game_screen():
    global cash, initial_cash, credits, csbutton,  to10, to30
    
    of.write('Perf by game screen at ' + repr(time.time()) + '\n')
    screen.fill(black)

    # Text:
    if deutsch:
        perf = capth65.render("Kasinobesuche", True, gold)
        screen.blit(perf, center_text(perf,screen,0,-330))
        
        wins = capth40.render("Gewinn/Verlust: ",True,gold)
        screen.blit(wins,center_text(wins,screen,0,-270))

    else:
        perf = capth65.render("Performance", True, gold)
        screen.blit(perf, center_text(perf,screen,0,-300))
        
        wins = capth25.render("Win/loss: ",True,gold)
        screen.blit(wins,center_text(wins,screen,0,-200))
        
    convertedsavings = cash*conversionfactor
    screen.blit(capth20.render("Geldbeutel: ", True, gold),(80,150))
    screen.blit(dsdgib25.render(str('%.2f' % convertedsavings) + " EUR",True,red),(270,150))
    
    j = 1
    for i in wlpergame:
        gamedough = float(i)*conversionfactor
        if deutsch:
            screen.blit(capth20.render("Spiel "+ str(j) + ":",True,gold),(150,170+25*j))
        else:
            screen.blit(capth20.render("Game "+ str(j) + ":",True,gold),(150,170+25*j))

        screen.blit(dsdgib25.render(str('%.2f' % gamedough) + " EUR",True,red),(270,170+25*j))
        of.write('Performance by game. Game ' + repr(j) + ': ' + repr('%.2f' % gamedough) + '\n')
        j += 1
        
    pygame.display.update()
    waitfun(5000)
    

def lost_all_money():
    ue = u"ü"
    ae = u"ä"
    loopmusic.stop()
    
    of.write('Lost all money at ' + repr(time.time()) + '\n')
    sof.write('Lost all money at ' + repr(time.time()) + '\n')
    screen.fill(black)
    
    border = pygame.image.load('./images/border0.png').convert_alpha()
      
    wart = capth65.render("Sie haben",True,gold)
    textpos = wart.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 150
    screen.blit(wart, textpos)

    bis = capth65.render("ihren Einsatz",True,gold)
    textpos = bis.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 250
    screen.blit(bis, textpos)

    spielautomat = capth65.render("verspielt und",True,gold)
    textpos = spielautomat.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 350
    screen.blit(spielautomat, textpos)
    
    undhaben = capth65.render("haben kein",True,gold)
    textpos = undhaben.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 450
    screen.blit(undhaben, textpos)

    einsparungen = capth65.render("Geld mehr",True,gold)
    textpos = einsparungen.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 550
    screen.blit(einsparungen, textpos)

    pygame.display.update()
    waitfun(4000)

def next_time():

    casino_goodbye()
    ae = u"ä"
    screen.fill(black)
    
    ns = capth65.render("Bis zum",True,gold)
    textpos = ns.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 300
    screen.blit(ns, textpos)
    
    ng = capth65.render("n"+ae+"chsten Mal!",True,gold)
    textpos = ng.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 400
    screen.blit(ng, textpos)
    pygame.display.update()
    waitfun(3000)

def start_fresh_game():
    global cash, initial_cash, addtwoeur, startfresh, timescashedout, f, credits, wlpergame, cashforgame, cancashout, currentbet
        
    loopmusic.stop()
    presssound.play()
    cancashout = False
    timescashedout += 1
    wlpergame.append(credits-cashforgame)
    startfresh = True
    
    pick_newgame_screen() # select a new game
    of.write('Current performance before starting again: current cash: ' + repr(cash) + ' at ' + repr(time.time()) + '\n')
    sof.write('Current performance before starting again: current cash: ' + repr(cash) + ' at ' + repr(time.time()) + '\n')
    
    cash = cash+credits
    credits = 0
    cashforgame = 0 
    currentbet = 0

    of.write('Starting a fresh game ' + repr(time.time()) + '\n')

def cashout_screen():
    global inception_cash, cash, initial_cash, totalgamesplayed, timescashedout, credits, cashforgame, addtwoeur
    
    loopmusic.stop()
    #pygame.mixer.pause()
    # Text
    oe = u"ö"
    if deutsch:
        etbanner = capth90.render("Auszahlen", True, gold)
        keepplaying = capth25.render("Zur"+ue+"ck zum Spiel? Kasino verlassen?",True,gold)    
        trials = capth25.render("Spiel",True,black)
        takemeback = capth25.render("Zur"+ue+"ck",True,black)
        leave = capth20.render("Kasino",True,black)
        casino = capth20.render("verlassen",True,black)
    else:
        etbanner = capth100.render("Cash out!", True, gold)
        keepplaying = capth25.render("Go back to game? Leave the casino?",True,gold)    
        trials = capth25.render("Game",True,black)
        takemeback = capth25.render("Back",True,black)
        leave = capth20.render("Leave",True,black)
        casino = capth20.render("casino",True,black)

    screen.fill(black)
    etbutton1 = pygame.image.load(cashoutback).convert_alpha()
    etbutton2 = pygame.image.load(etbutton).convert_alpha()
    
    screen.blit(etbanner,center_text(etbanner,screen,0,-200))
    screen.blit(keepplaying,center_text(keepplaying, screen,0,-100))
    screen.blit(etbutton1, (100,400))
    screen.blit(etbutton2, (320,400))
    screen.blit(takemeback,center_text(takemeback,etbutton1,100,400))
    screen.blit(leave,center_text(leave,etbutton2,320,390))
    screen.blit(casino,center_text(casino,etbutton2,320,410))
    pygame.display.update()
    
    chosen = False
    while not chosen:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if etbutton1.get_rect(center=(180,440)).collidepoint(mouse[0],mouse[1]): # nope, don't want to cash out
                    presssound.play()
                    refresh_screen()
                    #loopmusic.play(100,0)
                    of.write('Cancelled cashout ' + repr(time.time()) + '\n')
                    sof.write('Cancelled cashout ' + repr(time.time()) + '\n')
                    chosen = True
                elif etbutton2.get_rect(center=(400,440)).collidepoint(mouse[0],mouse[1]): # yes, I want to cash out
                    pygame.mixer.stop()
                    of.write('Cashed out ' + repr(time.time()) + '\n')
                    sof.write('Cashed out ' + repr(time.time()) + '\n')
                    start_fresh_game()
                    chosen = True


# Display box for in-between survey
def display_box_cs(screen, message):
    csnamebox = pygame.image.load('./images/csnamebox.png').convert_alpha()
    screen.blit(csnamebox,(50,200))
    yoffset = 25
    if len(message) != 0:
        blitmessage = wrapline(message,cal,330)
        for j in range(len(blitmessage)):
            screen.blit(calibri18.render(blitmessage[j],True,black),(70,215+yoffset*j))
        pygame.display.flip()


def casino_goodbye():

    screen.fill(black)
    treasureisland = pygame.image.load('./images/casinologo.png')
    screen.blit(treasureisland,center_text(treasureisland,screen,0,-100))
    
    herz = capth48.render("sagt",True,gold)
    wilk = capth48.render("auf wiedersehen!",True,gold)

    screen.blit(herz,center_text(herz, screen,0,150))
    screen.blit(wilk,center_text(wilk, screen, 0 ,230))

    pygame.display.update()
    waitfun(3000)

def enter_casino():
    screen.fill(black)
    treasureisland = pygame.image.load('./images/casinologo.png')
    screen.blit(treasureisland,center_text(treasureisland,screen,0,110))
    
    herz = capth65.render("Herzlich",True,gold)
    wilk = capth65.render("Willkommen",True,gold)
    ik = capth65.render("im",True,gold)
    screen.blit(herz,center_text(herz, screen,0,-290))
    screen.blit(wilk,center_text(wilk, screen, 0 ,-220))
    screen.blit(ik,center_text(ik,screen,0,-150))
    pygame.display.update()
    waitfun(1500)

    screen.fill(black)
    entrance = pygame.image.load('./images/casino_entrance.jpg')
   
    of.write('Entering casino at ' + repr(time.time()) + '\n')
    for i in range(0,1000,8):
        i = i-300
        screen.blit(entrance,(0,i))
        pygame.display.update()
            
        if i == 140:
            winsound.play()
            waitfun(500)
    screen.fill(black)

def want_to_change():
    screen.fill(black)
    wanttochange = capth40.render("Wollen Sie an einer anderen Maschine weiter spielen?",True, gold)
    screen.blit(wanttochange,(100,100))

# Screen that asks the player if they want to play x more trials and then sends them into those new trials                                                                                          
def extra_trials_screen():
    
    of.write('Now at the extra trials screen. ' + repr(time.time()) + '\n')
    sof.write('Now at the extra trials screen. ' + repr(time.time()) + '\n')
    
    # Text    
    oe = u"ö"
    if deutsch:
        etbanner = capth100.render("Weiter?", True, gold)
        keepplaying = capth25.render("M"+oe+"chten Sie noch weiter spielen?",True,gold)
        no = capth25.render("Nein",True,black)
        thanks = capth25.render("Danke.",True,black)
        trials = capth25.render("Spiele",True,black)
    else:
        etbanner = capth100.render("Continue?", True, gold)
        keepplaying = capth25.render("Would you like to keep playing?",True,gold)
        no = capth25.render("No",True,black)
        thanks = capth25.render("thanks.",True,black)
        trials = capth25.render("games",True,black)

    screen.fill(black)
    etbutton1 = pygame.image.load(etbutton).convert_alpha()
    etbutton2 = pygame.image.load(etbutton).convert_alpha()
    fivetrials = capth25.render("25",True,black)

    screen.blit(etbanner,(60,100))
    screen.blit(keepplaying,(50,295))
    screen.blit(etbutton1, (100,400))
    screen.blit(etbutton2, (320,400))

    screen.blit(no, (140,410))
    screen.blit(thanks,(130,435))
    screen.blit(fivetrials,(385,410))
    screen.blit(trials,(355, 435))

    pygame.display.update()

    chosen = False
    while not chosen:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                if etbutton1.get_rect(center=(180,440)).collidepoint(mouse[0],mouse[1]): 
                    presssound.play()
                    num_extra_trials = 0
                    of.write('Chose 0 extra trials ' + repr(time.time()) + '\n')
                    chosen = True
                elif etbutton2.get_rect(center=(400,440)).collidepoint(mouse[0],mouse[1]):
                    presssound.play()
                    num_extra_trials = 25
                    of.write('Chose 25 extra trials ' + repr(time.time()) + '\n')
                    chosen = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
    waitfun(500)
    if num_extra_trials > 0 and itnum<=4:
        extra_trials(num_extra_trials,itnum)
    else:
        num_extra_trials = 0
    return num_extra_trials

# This function will pick the appropriate text file for the extra trials. The text files are named with their relevant features (zB near miss, etc)                                                 
def extra_trials(num_extra_trials,itnum):

    # Define the output file for the extra trial                                                                                                                                                    
    if itnum == 1:
        newfile = 'probtraces/losingstreak'+repr(num_extra_trials)+'.txt'
    elif itnum == 2:
        newfile = 'probtraces/winstreak'+repr(num_extra_trials)+'.txt'
    elif itnum == 3:
        newfile = 'probtraces/nearmiss'+repr(num_extra_trials)+'.txt'
    elif itnum == 4:
        newfile = 'probtraces/random'+repr(num_extra_trials)+'.txt'

    of.write('Running ' + repr(itnum) + 'extra trials at ' + repr(time.time()) + '\n')
    opennew = open(newfile,'r')

    #start_fresh_game()
    game_loop(opennew)

def training_end_screen():
    
    screen.fill(black)
    border = pygame.image.load('./images/border0.png').convert_alpha()
    screen.blit(border,(0,0))
    danke1 = capth48.render("Ende der",True,gold)
    danke2 = capth48.render("Probeversuche!",True,gold)
    danke3 = capth48.render("Kasinobesuch",True,gold)
    danke4 = capth48.render("startet jetzt!",True,gold)
    
    screen.blit(danke1,center_text(danke1,screen,0,-180))
    screen.blit(danke2,center_text(danke2,screen,0,-80))
    screen.blit(danke3,center_text(danke3,screen,0,20))
    screen.blit(danke4,center_text(danke4,screen,0,120))
        
    pygame.display.update()

    waitfun(3000)

def pick_newgame_screen():
    global deutsch, gamenum, timescashedout, totalgamesplayed, startfresh, paid, currentbet
    
    loopmusic.stop()
    
    if startfresh and totalgamesplayed>0:
        perf_by_game_screen()
        #casinovisit_survey()

    of.write('Now picking a new game ' + repr(time.time()) + '\n')
    sof.write('Now picking a new game ' + repr(time.time()) + '\n')
    ae = u"ä"
    oe = u"ö"
    screen.fill(black)
    border = pygame.image.load('./images/border0.png').convert_alpha()
    screen.blit(border,(0,0))

    if startfresh: 
        betreten1 = capth65.render("Sie betreten",True,gold)
        betreten2 = capth65.render("nun zum",True,gold)
        betreten3 = capth65.render(repr(timescashedout+1)+". Mal",True,gold)
        betreten4 = capth65.render("das Kasino",True,gold)
        
        screen.blit(betreten1,center_text(betreten1,screen,0,-180))
        screen.blit(betreten2,center_text(betreten2,screen,0,-80))
        screen.blit(betreten3,center_text(betreten3,screen,0,20))
        screen.blit(betreten4,center_text(betreten4,screen,0,120))
        
        pygame.display.update()
        waitfun(1000)

    if startfresh:
        paid = 0
        currentbet = 0
        
        enter_casino()
        neuesspiel_neuesglueck()

    screen.fill(black)

    if startfresh:
        changegame1 = capth40.render("W"+ae+"hlen Sie",True,gold)
        changegame2 = capth40.render("einen Spielautomaten:",True,gold)
        screen.blit(changegame1,center_text(changegame1,screen,0,-300))
        screen.blit(changegame2,center_text(changegame2,screen,0,-250))
        of.write('New game after cashout at ' + repr(time.time()) + '\n')
        sof.write('New game after cashout at ' + repr(time.time()) + '\n')
    else:
        changebanner2a = capth30.render("W"+ae+"hlen Sie den Automaten",True,gold)
        changebanner2b = capth30.render("zu dem Sie wechseln m"+oe+"chten",True,gold)
        screen.blit(changebanner2a,center_text(changebanner2a,screen,0,-300))
        screen.blit(changebanner2b,center_text(changebanner2b,screen,0,-250))
        of.write('Switching machines at ' + repr(time.time()) + '\n')
        sof.write('Switching machines at ' + repr(time.time()) + '\n')

    backbutton = pygame.image.load(button4).convert_alpha()
    if not startfresh:
        screen.blit(backbutton, (210,690))
        
    if deutsch:
        takemeback = capth20.render("Zur"+ue+"ck",True,black)
    else:
        takemeback = capth20.render("BACK",True,black)     
            
    screen.blit(takemeback,center_text(takemeback,backbutton,210,690))        
    game0 = pygame.image.load('./images/game0_screenshot.png').convert_alpha()    
    game1 = pygame.image.load('./images/game1_screenshot.png').convert_alpha()    
    game2 = pygame.image.load('./images/game2_screenshot.png').convert_alpha()    
    game3 = pygame.image.load('./images/game3_screenshot.png').convert_alpha()    
    graygame = pygame.image.load('./images/graygame.png').convert_alpha()
        
    screen.blit(game0,(70,170))
    screen.blit(game1,(320,170))
    screen.blit(game2,(70,430))
    screen.blit(game3,(320,430))
    pygame.display.update()

    
    chosen = False
    while not chosen:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()

                if game0.get_rect(center=(170,295)).collidepoint(mouse[0],mouse[1]) and not chosen:
                    presssound.play()
                    gamenum = 0
                    totalgamesplayed += 1
                    game0.blit(graygame,(0,0))
                    screen.blit(game0,(70,170))
                    pygame.display.update()
                    waitfun(300)
                    of.write('Game 0 chosen ' + repr(time.time()) + '\n')
                    sof.write('Game 0 chosen ' + repr(time.time()) + '\n')
                    chosen = True
                    newgame_waitscreen()
                elif game1.get_rect(center=(420,295)).collidepoint(mouse[0],mouse[1]) and not chosen:
                    presssound.play()
                    gamenum = 1
                    game1.blit(graygame,(0,0))
                    screen.blit(game1,(320,170))
                    pygame.display.update()
                    waitfun(300)
                    totalgamesplayed += 1
                    of.write('Game 1 chosen ' + repr(time.time()) + '\n')
                    sof.write('Game 1 chosen ' + repr(time.time()) + '\n')
                    chosen = True
                    newgame_waitscreen()
                elif game2.get_rect(center=(170,555)).collidepoint(mouse[0],mouse[1]) and not chosen:
                    presssound.play()
                    gamenum = 2
                    game2.blit(graygame,(0,0))
                    screen.blit(game2,(70,430))
                    pygame.display.update()
                    waitfun(300)
                    totalgamesplayed += 1
                    of.write('Game 2 chosen ' + repr(time.time()) + '\n')
                    sof.write('Game 2 chosen ' + repr(time.time()) + '\n')
                    chosen = True
                    newgame_waitscreen()
                elif game3.get_rect(center=(420,555)).collidepoint(mouse[0],mouse[1]) and not chosen:
                    presssound.play()
                    game3.blit(graygame,(0,0))
                    screen.blit(game3,(320,430))
                    pygame.display.update()
                    waitfun(300)
                    gamenum = 3
                    totalgamesplayed += 1
                    of.write('Game 3 chosen ' + repr(time.time()) + '\n')
                    sof.write('Game 3 chosen ' + repr(time.time()) + '\n')
                    chosen = True
                    newgame_waitscreen()
                elif backbutton.get_rect(center=(300,710)).collidepoint(mouse[0],mouse[1]) and not startfresh:
                    of.write('Decided to continue current game ' + repr(time.time()) + '\n')
                    sof.write('Decided to continue current game ' + repr(time.time()) + '\n')
                    refresh_screen()
                    chosen = True    
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
    
    startfresh = False

def newgame_waitscreen():
    ue = u"ü"
    screen.fill(black)
    
    border = pygame.image.load('./images/border0.png').convert_alpha()
    screen.blit(border,(0,0))
    
    bitte = capth65.render("Bitte",True,gold)
    textpos = bitte.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 150
    screen.blit(bitte, textpos)

    wart = capth65.render("warten Sie",True,gold)
    textpos = wart.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 250
    screen.blit(wart, textpos)

    bis = capth65.render("bis Ihr",True,gold)
    textpos = bis.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 350
    screen.blit(bis, textpos)

    spielautomat = capth65.render("Spielautomat",True,gold)
    textpos = spielautomat.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 450
    screen.blit(spielautomat, textpos)
    
    bereit = capth65.render("bereit ist.",True,gold)
    textpos = bereit.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 550
    screen.blit(bereit, textpos)
          
    pygame.display.update()
    waitfun(2000)

def neuesspiel_neuesglueck():
    screen.fill(black)
    border = pygame.image.load('./images/border0.png').convert_alpha()
    screen.blit(border,(0,0))
    
    ns = capth65.render("Neuer Tag,",True,gold)
    textpos = ns.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 300
    screen.blit(ns, textpos)

    ng = capth65.render("neues Gl"+ue+"ck!",True,gold)
    textpos = ng.get_rect()
    textpos.centerx = background.get_rect().centerx
    textpos.centery = 400
    screen.blit(ng, textpos)
    
    pygame.display.update()
    waitfun(1500)

# Screen that prints updated money information to the main screen 
def refresh_money():
    global backcolor, banner2

    # Blit money numbers to the screen    
    scorewipeout.fill(backcolor)
    screen.blit(scorewipeout,(97,420))
  
    winnerpaid2 = capth20.render("Gewinn",True,eval(bannercolors[gamenum]))
    creditsstr2 = capth20.render("Cents",True,eval(bannercolors[gamenum]))
    bet2 = capth20.render("Einsatz",True,eval(bannercolors[gamenum]))
    screen.blit(banner2,center_text(banner2,screen,0,-280))
    screen.blit(creditsstr2,(100,420))
    screen.blit(bet2,(285,420))
    screen.blit(winnerpaid2,(390,420))
       
    screen.blit(scores,(90,410))    
    screen.blit(dsdgib35.render(str('%d' % credits), True, red),(100,440))
    screen.blit(dsdgib35.render(str(currentbet), True,red),(285,440))
    screen.blit(dsdgib35.render(str(paid), True, red),(390,440))
    of.write('RM: Cents: ' + repr(credits) + ' Cash: ' + repr(cash) + ' CurrentBet: ' + repr(currentbet) + ' Paid: ' + repr(paid) + ' ' + repr(time.time()) + '\n')
    
    screen.blit(onecent,(10,348))
    pygame.display.update()

# Function that refreshes the main screen, essentially beginning a new trial. This function is called by most other functions
def refresh_screen():
    global backcolor, backgroundcolors, bannercolors, gamenum, cancashout, banner2, buttondown1
    
    # Define colors
    backcolor = eval(backgroundcolors[gamenum])
    borderpic = './images/border' + repr(gamenum) + '.png'
    border = pygame.image.load(borderpic).convert_alpha()

    # Blit the buttons and button text
    screen.fill(backcolor)
    
    if buttondown1 == True:
        screen.blit(press1,(85,500))
    else:
        screen.blit(play1,(85,500))
    screen.blit(bet1,center_text(bet1,play1,75,510))
    screen.blit(betx,(145,540))
    
    if buttondown2 == True:
        screen.blit(press2,(215,500))
    else:
        screen.blit(play2,(215,500))
    screen.blit(betmax,center_text(betmax,play2,205,510))
    screen.blit(betx,(275,540))

    if deutsch:
        screen.blit(betbutton,center_text(betbutton,play1,85,485))
        screen.blit(betbutton,center_text(betbutton,play2,215,485))
    else:
        screen.blit(betbutton,(68,510))
        screen.blit(betbutton,(168,510))
        screen.blit(betbutton,(268,510))


    screen.blit(pull,(355,500))
    screen.blit(pullme,center_text(pullme,pull,355,500))

    screen.blit(clear,(50,590))
    screen.blit(clearme,center_text(clearme,clear,50,590))
    
    screen.blit(checkscores,(218,590))    
    screen.blit(scoreme,center_text(scoreme,checkscores,218,590))
        
    screen.blit(checkcash,(385, 589))
    screen.blit(checkmycash,center_text(checkmycash,checkcash,385,589))
    
    
    if cancashout:
        screen.blit(cashout, (50,640))
    else:
        screen.blit(nocashout, (50,640))
        
    screen.blit(cotext,center_text(cotext,cashout,50,640))
    
    screen.blit(chggamebutton,(220,640))
    screen.blit(changetext,center_text(changetext,chggamebutton,220,640))

    screen.blit(endgame,(525,635))
        
    # Blit borders and such
    screen.blit(border,(0,0))
   
    screen.blit(slot1,(30,150))
    screen.blit(slot2,(210,150))
    screen.blit(slot3,(390,150))
    screen.blit(scores,(90,410))

    if gamenum==0:
        banner2 = capth110.render("SLOTS!!!",True,eval(bannercolors[gamenum]))
    elif gamenum == 1:
        banner2 = fredericka92.render("LUCKY DAY!",True,eval(bannercolors[gamenum]))
    elif gamenum == 2:
        banner2 = capth90.render("BIG MONEY!",True,eval(bannercolors[gamenum]))
    elif gamenum == 3:
        banner2 = risque127.render("JACKPOT!",True,eval(bannercolors[gamenum]))
        
    screen.blit(banner2,center_text(banner2,screen,0,-280))
    screen.blit(onecent,(10,348))
    refresh_money()

# This is the main game loop function, that defines all of the mechanics of the player interacting with the screen
# It iterates over trials that it reads from the candidateTrace1.txt file (that is the input (f) to the function). 
# It then writes most dynamics out to the output file
def game_loop(f):
    global cash, credits, currentbet, paid, winsize, button1coords, cancashout, timescashedout, training, counter, buttondown1, buttondown2, totaltrialsplayed, startfresh, training
   
    # Start game loop
    finish = False
    of.write('Starting game loop ' + repr(time.time()) + '\n')
    refresh_screen()
    
    # Cue music
    loopmusic.play(100,0)

    # Start actual event pulling
    counter = 0
    cashoutcounter = 0
    for line in f:
        
        counter += 1
        cashoutcounter += 1
        
        if not training:
            totaltrialsplayed += 1
            
        # Alert the user if there are only 5 trials left
        if counter == 196:
            of.write('5 more trials ' + repr(time.time()) + '\n')
            if deutsch:
                nfs = capth65.render("Noch 5 spiele",True,green)
                screen.blit(nfs,center_text(nfs,screen,0,-110))                
            else:
                screen.blit(capth40.render("5 more chances!",True,green),center_text(mustaddmoney,screen,0,-110))

            pygame.display.update()
            waitfun(4000)
            refresh_screen()

        
        mouse = pygame.mouse.get_pos()
        of.write('Starting trial : ' + repr(counter) + ' at ' + repr(time.time()) + ' mouse1: ' +  repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + '\n')        
        of.write('Specifications for trial ' + repr(counter) + ' are: P: ' + line[0] + ' and the symbols are: ' + line[1:])
        sof.write('Starting trial : ' + repr(counter) + ' at ' + repr(time.time()) + ' mouse1: ' +  repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + '\n')
        sof.write('Trial ' + repr(counter) + ': P: ' + line[0] + ', symbols: ' + line[1:])
        
        buttondown1 = False
        buttondown2 = False
        buttondown = False
        done=False
        while not done:
          
            # Pull pygame events
            for event in pygame.event.get():           
                if event.type == QUIT:
                    of.write('quit ' + repr(time.time()))
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if pressed(mouse,play1,1) and buttondown==False:
                        screen.blit(press1,(85,500))
                        screen.blit(betbutton,center_text(betbutton,play1,85,485))
                        screen.blit(bet1,center_text(bet1,play1,75,510))
                        screen.blit(betx,(145,540))
                        pygame.display.update()
                        currentbet = betsize[0]
                        if credits<currentbet:
                            screen.blit(mustaddmoney,center_text(mustaddmoney,screen,0,-110))
                            pygame.display.update()
                            wohwah.play()
                            waitfun(1800)
                            currentbet = 0
                            refresh_screen()
                            break
                        presssound.play()
                        credits = credits - currentbet
                        winsize = winsize1
                        buttondown = True
                        buttondown1 = True
                        of.write('Bet started: b1 ' + repr(time.time()) + ' mouse1: ' +  repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + ' \n')
                        sof.write('Bet started: ' + repr(currentbet) + ' at ' + repr(time.time()) + ' mouse1: ' +  repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + ' \n')
                        paid = 0
                        refresh_money()
                    elif pressed(mouse,play2,3) and buttondown==False:
                        screen.blit(press2,(215,500))
                        screen.blit(betbutton,center_text(betbutton,play2,215,485))
                        screen.blit(betmax,center_text(betmax,play2,205,510))
                        screen.blit(betx,(275,540))
                         
                        pygame.display.update()
                        currentbet = betsize[1]
                        if credits<currentbet:
                            screen.blit(mustaddmoney,center_text(mustaddmoney,screen,0,-110))
                            pygame.display.update()
                            wohwah.play()
                            waitfun(1800)
                            currentbet = 0
                            refresh_screen()
                            break                        
                        presssound.play()
                        credits = credits - currentbet
                        winsize = winsize3
                        buttondown = True
                        buttondown2 = True
                        of.write('Bet started: b3 ' + repr(time.time())  + ' mouse1: ' + repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + ' \n')
                        sof.write('Bet started: ' + repr(currentbet) + ' at ' + repr(time.time())  + ' mouse1: ' + repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + ' \n')
                        paid = 0
                        refresh_money()
                    elif pressed(mouse,pull,4) and buttondown==True:    
                        of.write('Hit pull button at ' + repr(time.time()) + ' and mouse at mouse1: ' + repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + '\n')
                        sof.write('Hit pull button at ' + repr(time.time()) + ' and mouse at mouse1: ' + repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + '\n')
                        waitfun(30)
                        screen.blit(press9,(355,500))
                        screen.blit(pullme,center_text(pullme,press9,355,500))
                        pygame.display.update()
                    
                        leversound.play()
                        waitfun(100)
                        leversound.stop()

                        # Pull the probabilities
                        wl = int(line[0])
                        for roll in xrange(1):
                            if wl == 3: # jackpot
                                p = 10
                                q = 10
                                r = 10
                            elif wl == 2: # near miss
                                p = int(line[1])
                                q = p
                                r = int(line[2])
                            elif wl == 1: # win
                                t = int(line[1])
                                p = t
                                q = t
                                r = t
                                dg = int(line[2]) # do i gamble? 0 then no and 1 then yes
                                dgo = int(line[3]) # 1 in win and 2 is loss 0 is nothing
                            elif wl == 0: # loss - sprites still specified
                                p = int(line[1])
                                q = int(line[2])
                                r = int(line[3])
    
                        # Get a good roll
                        waitfun(500)
                        spinsound.play(100,0)
                        vertpos = 200                   
                        rollcounter = 1
                        pics = ['one', 'two', 'three', 'four', 'five', 'six','seven','eight','nine', 'jackpot']
                        
                        startroll = True
                        of.write('Starting wheel spin at ' + repr(time.time()) + '\n')
                        rollcounter = 1 
                        
                        # Start spinning!
                        while rollcounter < 40:
                            for roller in pics:
                                screen.blit(eval(roller),(45,vertpos))
                                screen.blit(eval(roller),(225,vertpos))
                                screen.blit(eval(roller),(405,vertpos))
                                pygame.display.update()
                                screen.blit(blackout,(40,180))
                                screen.blit(blackout,(220,180))
                                screen.blit(blackout,(400,180))
                                rollcounter += 1
                                waitfun(5)
                        
                        of.write('Wheel spin ended at ' + repr(time.time()) + '\n')
                        spinsound.stop()
                        
                        (picnum, screenpos) = sprite_disp(p,1)  
                        screen.blit(eval(picnum),(screenpos,vertpos))
                        pygame.display.update()
                        spinstopsound.play()
                        of.write('Sprite 1 shown at '+ repr(time.time()) + '\n')
                        waitfun(500)
                        
                        (picnum, screenpos) = sprite_disp(q,2)
                        screen.blit(eval(picnum),(screenpos,vertpos))
                        pygame.display.update()
                        spinstopsound.play()
                        of.write('Sprite 2 shown at '+ repr(time.time()) + '\n')
                        waitfun(500)
                        
                        (picnum, screenpos) = sprite_disp(r,3)
                        screen.blit(eval(picnum),(screenpos,vertpos))
                        pygame.display.update()
                        spinstopsound.play()
                        of.write('Sprite 3 shown at '+ repr(time.time()) + '\n')
                        waitfun(500)

                        # Check winner/loser and update cash
                        if p == q == r:
                            paid = winsize[p-1]
                            credits = credits + paid
                            currentbet = 0
                            
                            if p==8 or p==9:
                                numsparkle = 3
                                winwin = bigwinner
                            else:
                                numsparkle = 1
                                winwin=winner
                                                                
                            for i in range(numsparkle):
                                screen.blit(winwin,center_text(winwin,screen,10,-120))
                                pygame.display.update()
                                if p==8 or p==9:
                                    bigwinsound.play()
                                else:
                                    winsound.play()
                                waitfun(1100)
                                refresh_screen()
                                of.write('Winner image blit at ' + repr(time.time()) + '\n')
                            if p==8 or p==9:
                                bigwinsound.stop()
                            else:
                                winsound.play()

                            screen.blit(winbanner,(25,180))
                            if deutsch:
                                dugewinnst = capth30.render("Du gewinnst", True, black)
                                screen.blit(dugewinnst,center_text(dugewinnst,winbanner,20,120))
                            else:
                                screen.blit(capth30.render("You won:", True, black),(220,220))
                                
                            amtwon = capth30.render(str(paid) + " cents!!",True,black)
                            sof.write('Win of ' + str(paid) + ' cents\n')
                            of.write('Blit you won banner at ' + repr(time.time()) + '\n')
                            screen.blit(amtwon,center_text(amtwon,winbanner,20,175))
                            pygame.display.update()
                            waitfun(2000)
                            winsound.stop()
                            of.write('Outcome known at ' + repr(time.time()) + ' location: mouse1: ' + repr(mouse[0]) + ' and mouse2: ' + repr(mouse[1]) + '\n') 
                            sof.write('Outcome known at ' + repr(time.time()) + ' location: mouse1: ' + repr(mouse[0]) + ' and mouse2: ' + repr(mouse[1]) + '\n')
                            if dg == 1:
                                of.write('Extra gamble started at: ' + repr(time.time()) + '\n')
                                sof.write('Extra gamble started at: ' + repr(time.time()) + '\n')
                                # Double or nothing gamble
                                screen.blit(moregamble,center_text(moregamble, screen, 0,-50))
                                etbutton1 = pygame.image.load(etbutton).convert_alpha()
                                etbutton2 = pygame.image.load(etbutton).convert_alpha()
                                screen.blit(etbutton1, (100,400))
                                screen.blit(etbutton2, (320,400))                            
                                no = capth25.render("Nein",True,black)
                                thanks = capth25.render("Danke.",True,black)
                                yesgamble = capth25.render("Gamble!",True,black)
                                #timer = capth40.render("Timer:",True,green)
                                screen.blit(no, (140,410))
                                screen.blit(thanks,(130,435))
                                screen.blit(yesgamble,center_text(yesgamble,etbutton2,320,400))
                                screen.blit(cardback,(220,200))
                                #screen.blit(timer,(220,215))
                                pygame.display.update()
                               
                                decided = False
                                countdownstart = time.time()
                                countdownvec = [4,3,2,1]
                                while not decided:
                                    timepass = int(round(time.time()-countdownstart))
                                    if timepass in countdownvec:
                                        screen.blit(cardback,(220,200))
                                        timestr = capth150.render(repr(countdownvec[timepass-1]-1),True,green)
                                        screen.blit(timestr,center_text(timestr,cardback,220,190))
                                        pygame.display.update()
                                        if countdownvec[timepass-1]-1 == 0:
                                            failsound.play()
                                            decided = True

                                    for event in pygame.event.get():
                                        if event.type == MOUSEBUTTONDOWN:
                                            mouse = pygame.mouse.get_pos()
                                            
                                            if etbutton1.get_rect(center=(180,440)).collidepoint(mouse[0],mouse[1]):
                                                of.write('Did not gamble: ' + repr(time.time()) + '\n')
                                                sof.write('Did not gamble: ' + repr(time.time()) + '\n')
                                                decided = True
                                                
                                            elif etbutton2.get_rect(center=(400,440)).collidepoint(mouse[0],mouse[1]):
                                                of.write('Decided to gamble ' + repr(time.time()) + '\n')
                                                sof.write('Decided to gamble ' + repr(time.time()) + '\n')
                                                if dgo == 1:
                                                    screen.blit(wincard,(220,200))
                                                    pygame.display.update()
                                                    winsound.play()
                                                    credits = credits + paid
                                                    of.write('Won extra gamble ' + repr(time.time()) + '\n')
                                                    sof.write('Won extra gamble ' + repr(time.time()) + '\n')
                                                elif dgo == 2:
                                                    screen.blit(losscard,(220,200))
                                                    pygame.display.update()
                                                    failsound.play()
                                                    credits = credits - paid
                                                    of.write('Lost extra gamble ' + repr(time.time()) + '\n')
                                                    sof.write('Lost extra gamble ' + repr(time.time()) + '\n')
                                                    
                                                waitfun(1000)
                                                decided = True

                            
                            if dg != 1:
                                waitfun(2000)
                            of.write('Summary: In Machine: ' + repr(credits) + ' Cash: ' + repr(cash) + '\n')
                            sof.write('Summary: In Machine: ' + repr(credits) + ' Cash: ' + repr(cash) + '\n')
                            buttondown=False
                            buttondown1=False
                            buttondown2=False
                            startroll = False
                            refresh_screen()
                            of.write('Trial ' + repr(counter) + ' ended at: ' + repr(time.time()) + '\n')
                            sof.write('Trial ' + repr(counter) + ' ended at: ' + repr(time.time()) + '\n')
                            done = True
                        else:
                            sof.write('Lost\n')
                            paid = 0
                            credits = credits 
                            currentbet = 0
                            failsound.play()
                            waitfun(600)
                            failsound.stop()
                            mouse = pygame.mouse.get_pos()
                            of.write('Outcome known at ' + repr(time.time()) + ' location: mouse1: ' + repr(mouse[0]) + ' and mouse2: ' + repr(mouse[1]) + '\n') 
                            sof.write('Summary: In Machine: ' + repr(credits) + ' Cash: ' + repr(cash) + '\n')
                            sof.write('Outcome known at ' + repr(time.time()) + ' location: mouse1: ' + repr(mouse[0]) + ' and mouse2: ' + repr(mouse[1]) + '\n') 
                            of.write('Trial ' + repr(counter) + ' ended at: ' + repr(time.time()) + '\n')
                            buttondown=False
                            buttondown1=False
                            buttondown2=False
                            refresh_screen()
                            done = True
                            if cash+credits < 20:
                                wlpergame.append(credits-cashforgame)
                                lost_all_money()
                                final_exit_screen()

                    elif pressed(mouse,clear,5):
                        buttondown = False
                        buttondown1 = False
                        buttondown2 = False
                        credits = credits + currentbet
                        currentbet = 0
                        presssound.play()
                        refresh_screen()
                        of.write('clear ' + repr(time.time()) + ' mouse1: ' + repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + ' \n')
                    elif pressed(mouse,checkcash,6):
                        presssound.play()
                        of.write('Checking cash  at ' + repr(time.time()) + ' mouse1: ' +  repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + '\n')
                        top_up()
                    elif pressed(mouse,checkscores,7):
                        of.write('Checking scores at ' + repr(time.time()) + ' mouse1: ' + repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + '\n')
                        presssound.play()
                        score_screen()
                    elif pressed(mouse,endgame,8):
                        of.write('Ending game at ' + repr(time.time()) + ' mouse1: ' + repr(mouse[0]) + ' mouse2: ' + repr(mouse[1]) + '\n')
                        exit_screen()     
                    elif pressed(mouse,cashout,9) and cancashout:
                        of.write('Cashing out after trial ' + repr(counter-1) + ' at time ' + repr(time.time()) + '\n')
                        sof.write('Cashing out after trial ' + repr(counter-1) + ' at time ' + repr(time.time()) + '\n')
                        cashout_screen()
                        cashoutcounter = 0
                        refresh_screen()
                        loopmusic.play(100,0)
                    elif pressed(mouse,chggamebutton,10):
                        of.write('Switching machines after trial ' + repr(counter-1) + ' at time ' + repr(time.time()) + '\n')
                        sof.write('Switching machines after trial ' + repr(counter-1) + ' at time ' + repr(time.time()) + '\n')
                        pick_newgame_screen()
                        loopmusic.play(100,0)
                        refresh_screen()
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
          
        # Allow the user to cashout
        if cashoutcounter==1 and not training:
            cancashout = True                
            refresh_screen()

    wlpergame.append(credits-cashforgame)


##################################
## Game time!
##################################

# Get initial information from the player
# Blit the introduction screen
# Parse patient information from the user
(patientname, deutsch) = patient_information_screen()
patient = patientname.replace(" ","")


# Make a folder with the patients name and the trial number in the output files dir
filetochoose = 1
dirmade = False
foldernum = 0
while not dirmade:
    dirname = './outputfiles/' + patient + '_' + repr(foldernum)
    subdirname = dirname + '/' + repr(filetochoose)
    if not os.path.isdir(dirname):
        os.mkdir('./outputfiles/' + patient + '_' + repr(foldernum))
        os.mkdir(subdirname)
        dirmade = True
    elif os.path.isdir(dirname) and not os.path.isdir(subdirname):
        os.mkdir(subdirname)
        dirmade = True
    else:
        foldernum += 1

# Define output file
nowstr = strftime("%Y%m%d%H%M%S", localtime()) 

# Define the output file in the patient folder
outputfile = subdirname + '/output' + nowstr + '.txt'
shortoutputfile = subdirname + '/output' + nowstr + '_short.txt'
dgfile = subdirname + '/d2ganswers' + nowstr + '_short.txt'
qfile = subdirname + '/questionnaires' + nowstr + '.txt'
headerfile = subdirname + '/header' + nowstr + '.txt'

# Open file
starttime = time.time()
of = open(outputfile,'w')
sof = open(shortoutputfile,'w')
dof = open(dgfile,'w')
qof = open(qfile,'w')
header = open(headerfile,'w')

header.write('Patient name: ' + patient + '\n')

# Print start time to file
of.write('Start time is : ' + repr(starttime) + ' for subject ' + patient + '\n')

#################################
### Now set up the game
#################################

# Hardcoded reward values and bet sizes (this can be read from a file)
winsize1 = [5, 10, 15, 20, 40, 60, 90, 150, 200, 2000]
winsize2 = [10, 20, 30, 40, 80, 120, 180, 300, 400, 4000]
winsize3 = [15, 30, 45, 60, 120, 180, 270, 450, 600, 6000]

# changed by rike end
betsize = [20, 60]

from initial_gamevals import *

## Full sequence of events:
### 1. Intro screen
### 2. Enter casino
### 3. Wait while your game is being readied
### 4. Send them into the game loop
### 5. Let them cashout or switch games
### 6. Once they've finished the trace, ask if they want to play more trials
### 7. Present the final questionnaire
### 8. Exit

# Start introductory screen
#screen = pygame.display.set_mode((900,675))
#intro_screen()

# Change screensize
background = pygame.Surface(screen.get_size())
screen = pygame.display.set_mode((600,750))

# Set up training trials

of.write('Trainingbegin ' + repr(time.time()) + '\n')
sof.write('Trainingbegin ' + repr(time.time()) + '\n')
training = True
startfresh = False
trainingfile = './probtraces/trainingTrace.txt'
t = open(trainingfile,'r')
game_loop(t)
training_end_screen()

training = False
of.write('Trainingend ' + repr(time.time()) + '\n')
sof.write('Trainingend ' + repr(time.time()) + '\n')


# Reset these values
from initial_gamevals import *

# Set up the entrance and game pick
pick_newgame_screen()

# Predefined number of trials
tracefile = './probtraces/candidateTrace.txt'
f = open(tracefile,'r')

# Send the player into the game loop
game_loop(f)
done_screen()

# Now ask if the player wants to play moree trials
waitfun(100)
itnum = 1
num_extra_trials = extra_trials_screen()
while num_extra_trials>0 and itnum < 4:
    itnum += 1
    num_extra_trials = extra_trials_screen()
    
# Send the user to the exit screen
final_exit_screen()
