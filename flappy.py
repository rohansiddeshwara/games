import pygame
import sys
import random

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >=500:
        return False
    else:
        return True

def drawfloor():
    screen.blit(floor_surface,(floor_x_position,450))
    screen.blit(floor_surface,(floor_x_position+288,450))


def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(400,random_pipe_pos))
    top_pipe=pipe_surface.get_rect(midbottom=(400,random_pipe_pos-150))
    return bottom_pipe,top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -=2
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >=512:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe =pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)

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
		hit_space_rect = hit_space_surface.get_rect(center = (140,400))
		screen.blit(hit_space_surface,hit_space_rect)




def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score
pygame.init()
screen=pygame.display.set_mode((288,512))
clock=pygame.time.Clock()

game_font=pygame.font.Font("04B_19.TTF",13)
#Game variables
gravity=0.25
bird_movement=0
game_active=True
score=0
high_score=0

bg_surface=pygame.image.load('assets/background-day.png').convert()
# bg_surface=pygame.transform.scale2x(bg_surface)
floor_surface= pygame.image.load('assets/base.png').convert()
floor_x_position=0

pipe_surface=pygame.image.load('assets/pipe-red.png').convert()
pipe_list=[]
SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1500)
pipe_height=[400,340,280,250,420]

bird_surface =pygame.image.load('assets/bluebird-midflap.png').convert()
bird_rect=bird_surface.get_rect(center=(90,256))
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type== pygame.KEYDOWN:
            if event.key ==pygame.K_SPACE and game_active:
                bird_movement=0
                bird_movement-=5
            if event.key ==pygame.K_SPACE and game_active==False:
                game_active=True
                pipe_list.clear()
                bird_rect.center=(90,256)
                bird_movement=0
        if event.type==SPAWNPIPE:
            pipe_list.extend(create_pipe())

    screen.blit(bg_surface,(0,0))

    if game_active:
        bird_movement+=gravity
        bird_rect.centery+=bird_movement
        screen.blit(bird_surface,bird_rect)

        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        game_active=check_collision(pipe_list)
        score +=0.01

        score_display('main_game')
    else:
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)
        high_score = update_score(score,high_score)
        score=0
        score_display('game_over')


    floor_x_position -=1
    drawfloor()

    if floor_x_position<=-288:
        floor_x_position=0


    pygame.display.update()
    clock.tick(120)
