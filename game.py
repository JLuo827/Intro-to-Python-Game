# Jiahao Luo (jl2yt) and Tyler Kling (tk9md)

import pygame
import gamebox
import random

# The game will be a multiplayer game where the two players are trying to get the highest score/popularity in a
# set amount of time. Whoever reaches a score of 100, or has the highest score after time is up wins.
# The features included in this game will be
# 1. Timer - After time is up, player with highest score wins
# 2. Enemies - Will lower the players' score if they touch and could also lead to game over if score is 0
# 3. Health - Sort of. If one of the player's scores falls to 0, they lose
# 4. Collectibles - Tweets falling from the sky that will increase a player's score
# 5. Multiplayer - One plays as Hillary Clinton, other as Donald Trump

camera = gamebox.Camera(800, 600)
opening_text = [
    gamebox.from_text(400, 100, "Battle for Popularity", 50, 'white'),
    gamebox.from_text(400, 150, "By Jiahao Luo(jl2yt) and Tyler Kling(tk9md)", 50, 'white'),
    gamebox.from_text(400, 200, "Move Trump using wad", 50, 'white'),
    gamebox.from_text(400, 250, "Move Clinton using arrow keys", 50, 'white'),
    gamebox.from_text(400, 300, "Score = Popularity", 50, 'white'),
    gamebox.from_text(400, 350, "Collect tweets(+10 popularity) from the sky", 50, 'white'),
    gamebox.from_text(400, 400, "Avoid logic(-10 popularity) from the sides", 50, 'white'),
    gamebox.from_text(400, 450, "Highest score after 30s wins", 50, 'white'),
    gamebox.from_text(400, 500, "If popularity drops to 0, you lose", 50, 'white'),
    gamebox.from_text(400, 550, "Press space to start", 50, 'white')
]

background = gamebox.from_image(400, 300, 'capitol_hill.jpg')
background.size = 800, 600
ground = gamebox.from_color(400, 650, 'white', 1500, 100)
donald_trump = gamebox.from_image(250, 550, 'Donald Trump.png')
donald_trump.size = 75, 85
trump_score = 50
hillary_clinton = gamebox.from_image(550, 550, 'hilary clinton.png')
hillary_clinton.size = 75, 85
hillary_score = 50
dumb_tweets = gamebox.from_image(random.randrange(50, 750), 0, "dumb tweets.png")
dumb_tweets.size = 30, 30
dumb_tweets.speedy = 10
enemy = gamebox.from_image(800, 530, "logic.png")
enemy.size = 100, 60
enemy.speedx = -10
game_on = False
timer = 900

def tick(keys):
    global game_on
    global trump_score
    global hillary_score
    global timer
    if pygame.K_SPACE in keys:
        game_on = True
    if game_on:
        camera.draw(ground)
        camera.draw(background)
        camera.draw(donald_trump)
        camera.draw(hillary_clinton)
        camera.draw(enemy)
        enemy.move_speed()
        timer -= 1
        camera.draw(dumb_tweets)
        dumb_tweets.move_speed()
        if enemy.touches(donald_trump, -20, -20):
            position = random.randrange(0, 2)
            if position == 0:
                enemy.x = -40
            if position == 1:
                enemy.x = 840
            trump_score -= 10
        if enemy.touches(hillary_clinton, -20, -20):
            position = random.randrange(0, 2)
            if position == 0:
                enemy.x = -40
            if position == 1:
                enemy.x = 840
            hillary_score -= 10
        if enemy.right < camera.left or enemy.left > camera.right:
            enemy.speedx *= -1
        if pygame.K_w in keys or pygame.K_a in keys or pygame.K_d in keys or not donald_trump.bottom_touches(ground):
            donald_trump.speedx = 0
            if pygame.K_w in keys and donald_trump.bottom_touches(ground):
                donald_trump.speedy = -50
            if pygame.K_a in keys:
                donald_trump.speedx = -8
            if pygame.K_d in keys:
                donald_trump.speedx = 8
            if not donald_trump.bottom_touches(ground):
                donald_trump.speedy += 8
            donald_trump.move_speed()
        if pygame.K_UP in keys or pygame.K_LEFT in keys or pygame.K_RIGHT in keys or not hillary_clinton.bottom_touches(ground):
            hillary_clinton.speedx = 0
            if pygame.K_UP in keys and hillary_clinton.bottom_touches(ground):
                hillary_clinton.speedy = -50
            if pygame.K_LEFT in keys:
                hillary_clinton.speedx = -8
            if pygame.K_RIGHT in keys:
                hillary_clinton.speedx = 8
            if not hillary_clinton.bottom_touches(ground):
                hillary_clinton.speedy += 8
            hillary_clinton.move_speed()
        hillary_clinton.move_to_stop_overlapping(ground)
        donald_trump.move_to_stop_overlapping(ground)
        if dumb_tweets.top > camera.bottom:
            dumb_tweets.y = 0
            dumb_tweets.x = random.randrange(50, 750)
        if dumb_tweets.touches(hillary_clinton, -10, -10):
            dumb_tweets.y = 0
            dumb_tweets.x = random.randrange(50, 750)
            hillary_score += 10
        if dumb_tweets.touches(donald_trump, -10, -10):
            dumb_tweets.y = 0
            dumb_tweets.x = random.randrange(50, 750)
            trump_score += 10
        trump_scoreboard = gamebox.from_text(200, 100, "Trump Popularity: "+str(trump_score), 50, 'black')
        hillary_scoreboard = gamebox.from_text(600, 100, "Hillary Popularity: "+str(hillary_score), 50, 'black')
        timer_box = gamebox.from_text(400, 50, "Timer: "+str(timer//30), 50, 'black')
        camera.draw(timer_box)
        camera.draw(trump_scoreboard)
        camera.draw(hillary_scoreboard)
        if trump_score == 100 or hillary_score <= 0:
            gamebox.pause()
            camera.draw(gamebox.from_text(400, 300, "TRUMP WINS", 100, 'black'))
        if hillary_score == 100 or trump_score <= 0:
            gamebox.pause()
            camera.draw(gamebox.from_text(400, 300, "HILLARY WINS", 100, 'black'))
        if timer == 0:
            gamebox.pause()
            if trump_score > hillary_score:
                camera.draw(gamebox.from_text(400, 300, "TRUMP WINS", 100, 'black'))
            if hillary_score > trump_score:
                camera.draw(gamebox.from_text(400, 300, "HILLARY WINS", 100, 'black'))
            if trump_score == hillary_score:
                camera.draw(gamebox.from_text(400, 300, "SOCIETY WINS", 100, 'black'))
    if not game_on:
        for line in opening_text:
            camera.draw(line)
    camera.display()

gamebox.timer_loop(30, tick)
