import pygame
import sys
import random






#================================================
pygame.init()
gravity=0.1
bird_movement=0
game_active=True
score=0
high_score=0
game_font=pygame.font.Font("04B_19.TTF",15)


screen=pygame.display.set_mode((288,512))
clock=pygame.time.Clock()
floor_x_position=0
bg_surface=pygame.image.load('assets/background-day.png').convert()
#--------------------------------------------------

def movefloor():
    screen.blit(floor_surface,(floor_x_position,400))
    screen.blit(floor_surface,(floor_x_position+288,400))

def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(400,random_pipe_pos))
    return bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -=3
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        screen.blit(pipe_surface,pipe)

def create_bird():
    random_red_bird_x=random.choice(red_bird_x)
    random_red_bird_y=random.choice(red_bird_y)
    red_bird=red_bird_surface.get_rect(midtop=(random_red_bird_x,random_red_bird_y))
    return red_bird

def move_red_birds(birds):
    for bird in birds:
        bird.centerx -=1
    return birds

def draw_red_birds(birds):
    for bird in birds:
        screen.blit(red_bird_surface,bird)

def check_collision(pipes,birds):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    for bird in birds:
        if bird_rect.colliderect(bird):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >=500:
        return False
    else:
        return True

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def score_display(game_state):
	if game_state == 'main_game':
		score_surface = game_font.render(f'Score: {int(score)}',True,(0,0,0))
		score_rect = score_surface.get_rect(center = (36,30))
		screen.blit(score_surface,score_rect)
		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(0,0,0))
		high_score_rect = high_score_surface.get_rect(center = (230,30))
		screen.blit(high_score_surface,high_score_rect)
	if game_state == 'game_over':
		score_surface = game_font.render(f'Score: {int(score)}' ,True,(0,0,0))
		score_rect = score_surface.get_rect(center = (36,30))
		screen.blit(score_surface,score_rect)

		high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(0,0,0))
		high_score_rect = high_score_surface.get_rect(center = (230,30))
		screen.blit(high_score_surface,high_score_rect)
		game_over_surface = game_font.render(f'GAME OVER',True,(0,0,0))
		game_over_rect = game_over_surface.get_rect(center = (145,200))
		screen.blit(game_over_surface,game_over_rect)
		hit_space_surface = game_font.render(f'Hit space to retry',True,(0,0,0))
		hit_space_rect = hit_space_surface.get_rect(center = (140,300))
		screen.blit(hit_space_surface,hit_space_rect)

#---------------------------------------------------

floor_surface= pygame.image.load('assets/base.png').convert()

#--------------------------------------------------

pipe_surface=pygame.image.load('assets/pipe-red.png').convert()
pipe_rect=pipe_surface.get_rect(center=(0,0))
pipe_list=[]
SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1500)
pipe_height=[340,420,280,300,370,200]
#--------------------------------------------------

bird_surface =pygame.image.load('assets/bluebird-midflap.png').convert()
bird_rect=bird_surface.get_rect(center=(90,387))

red_bird_surface=pygame.image.load('assets/redbird.png').convert()
red_bird_rect=red_bird_surface.get_rect(center=(0,0))
red_bird_list=[]
SPAWNbird=pygame.USEREVENT
pygame.time.set_timer(SPAWNbird,1200)
red_bird_x=[400,460,390,470,410,500]
red_bird_y=[10,100,250,170,105,150,190,90,110]


while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type== pygame.KEYDOWN:
            if event.key ==pygame.K_SPACE and game_active:
                bird_movement=5
            if event.key ==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                red_bird_list.clear()
                bird_rect.center=(90,387)
                bird_movement=0
        if event.type==SPAWNPIPE:
            pipe_list.append(create_pipe())
        if event.type==SPAWNbird:
            red_bird_list.append(create_bird())



    screen.blit(bg_surface,(0,0))

    pipe_list=move_pipes(pipe_list)
    draw_pipes(pipe_list)

    red_bird_list=move_red_birds(red_bird_list)
    draw_red_birds(red_bird_list)

    if game_active:

        if bird_rect.centery>=387:
            bird_rect.centery=383
            gravity=0
        else:
            gravity=0.1
            bird_movement-=gravity

        bird_rect.centery-=bird_movement
        screen.blit(bird_surface,bird_rect)
        game_active=check_collision(pipe_list,red_bird_list)
        score +=0.01

        score_display('main_game')
    else:
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        red_bird_list=move_red_birds(red_bird_list)
        draw_red_birds(red_bird_list)
        high_score = update_score(score,high_score)
        score=0
        score_display('game_over')


    floor_x_position-=1
    if floor_x_position<=-288:
        floor_x_position=0
    movefloor()


    pygame.display.update()
    clock.tick(120)
