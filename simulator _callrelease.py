import pygame
import random
import os
import math

pygame.init()
WIDTH = 1210
HEIGHT = 610
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Call_Release")
prob_amplifier=10000
poisson_lambda=1/720
poisson_prob=float(((math.e)**(-poisson_lambda))*(poisson_lambda))
running = True
clock = pygame.time.Clock()
FPS = 24
V = 1
Pt = 200
# V/= FPS
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
BLOCK_SIZE=50
switch_nearest = 0
switch_threshold = 0
switch_entropy = 0
switch_direction = 0
# temp = 0
class Car(pygame.sprite.Sprite):
	def __init__(self,x,y,direction):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10,10))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		self.spy = 0
		self.spx = 0
		self.oncall = 0
		self.callend = 0

		self.dB = 0
		self.dB_entropy = 0
		self.dB_threshold = 0
		self.dB_direction = 0
		self.connet_nearest = -1
		self.change_nearest = 0
		self.connet_direction = -1
		self.change_direction = 0
		self.connet_threshold = -1
		self.change_threshold = 0
		self.connet_entropy = -1
		self.change_entropy = 0
		if direction == 0:
			self.spy = V
		elif direction == 1:
			self.spy = -1*V
		elif direction == 2:
			self.spx = V
		elif direction == 3:
			self.spx = -V
		for i in range(len(BS_sprites)):
			dis = calculate_Distance(self.rect.centerx, self.rect.centery,BS_sprites[i].rect.centerx,BS_sprites[i].rect.centery)
			if self.dB < calculate_DB(dis,BS_sprites[i].freq):
				self.dB = calculate_DB(dis,BS_sprites[i].freq)
				self.connet_nearest = i
				self.dB_threshold = calculate_DB(dis,BS_sprites[i].freq)
				self.connet_threshold = i
				self.dB_entropy = calculate_DB(dis,BS_sprites[i].freq)
				self.connet_entropy = i
				self.dB_direction = calculate_DB(dis,BS_sprites[i].freq)
				self.connet_direction = i
	def update(self):
		#if call
		if self.callend < round((pygame.time.get_ticks())/1000):
			self.oncall = 0
			self.callend = 0
		iscall = 3600
		if self.oncall == 0:
			iscall = random.randrange(0,30*FPS)
		if iscall == 0:
			self.oncall = 1
			self.callend = round((pygame.time.get_ticks())/1000) + 5
		#move
		self.rect.x += self.spx
		self.rect.y += self.spy
		if self.rect.x%60 == 0 and self.rect.y%60 == 0:
			next_direct=random.randrange(0,32)
			if next_direct < 2:
				self.spx *= -1
				self.spy *= -1
			elif next_direct >= 2 and next_direct <= 8:
				tempx = self.spx
				tempy = self.spy
				self.spx = tempy 
				self.spy = tempx 
			elif next_direct >= 9 and next_direct <= 15:
				tempx = self.spx
				tempy = self.spy
				self.spx = tempy * -1
				self.spy = tempx * -1
		#dB count
		direct = 0
		if self.spx > 0:
			direct = 1#R
		elif self.spx<0:
			direct = 2#L
		elif self.spy > 0:
			direct = 3#D
		elif self.spy > 0:
			direct = 4#U
		self.change_nearest = 0
		self.change_threshold = 0
		self.change_entropy = 0
		self.change_direction = 0
		t_nearest = self.connet_nearest
		t_threshold = self.connet_threshold
		t_entropy = self.connet_entropy
		t_direction = self.connet_direction
		for i in range(len(BS_sprites)):
			dis = calculate_Distance(self.rect.centerx, self.rect.centery,BS_sprites[i].rect.centerx,BS_sprites[i].rect.centery)
			dis_threshold = calculate_Distance(self.rect.centerx, self.rect.centery,BS_sprites[i].rect.centerx,BS_sprites[i].rect.centery)
			dis_entropy = calculate_Distance(self.rect.centerx, self.rect.centery,BS_sprites[i].rect.centerx,BS_sprites[i].rect.centery)
			dis_direction = calculate_Distance(self.rect.centerx, self.rect.centery,BS_sprites[i].rect.centerx,BS_sprites[i].rect.centery)

			if self.dB < calculate_DB(dis,BS_sprites[i].freq) and self.oncall ==1:#and self.dB < 90:
				self.dB = calculate_DB(dis,BS_sprites[i].freq)
				self.connet_nearest = i
			if self.dB_threshold  < calculate_DB(dis_threshold,BS_sprites[i].freq) and self.dB_threshold < 90 and self.oncall ==1:#and self.dB < 90:
				self.dB_threshold = calculate_DB(dis_threshold,BS_sprites[i].freq)
				self.connet_threshold = i
			if self.dB_entropy  + 15 < calculate_DB(dis_entropy,BS_sprites[i].freq) and self.oncall ==1:#and self.dB < 90:
				self.dB_entropy = calculate_DB(dis_entropy,BS_sprites[i].freq)
				self.connet_entropy = i
			if self.dB_direction < calculate_DB(dis_direction,BS_sprites[i].freq) and self.dB_direction < 85 and self.rect.x > 120 and self.rect.y > 120 and self.rect.x < 480 and self.rect.y < 480 and self.oncall ==1:#and self.dB < 90:
				# if self.rect.x > 120 and self.rect.y > 120 and self.rect.x < 480 and self.rect.y < 480:
				self.dB_direction = calculate_DB(dis_direction,BS_sprites[i].freq)
				self.connet_direction = i
		if self.connet_nearest != t_nearest:
				self.change_nearest = 1
		if self.connet_threshold != t_threshold:
				self.change_threshold = 1
		if self.connet_entropy != t_entropy:
				self.change_entropy = 1
		if self.connet_direction != t_direction:
				self.change_direction = 1
		#out of map
		if self.rect.x >= 600 or self.rect.y >= 600 or self.rect.x <= 0 or self.rect.y <= 0:
			all_sprites.remove(self)
			car_sprites.remove(self)
			self.kill()
def calculate_Distance(Carx,Cary,BSx,BSy):
	tem = ((Carx-BSx)**2+(Cary-BSy)**2)**(1/2)
	return (tem *0.5)
def calculate_DB(freq,dis):
	return Pt - (32.45+20*math.log(freq,10)+20*math.log(dis,10))
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y,color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    surf.blit(text_surface, text_rect)
class Block(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((BLOCK_SIZE,BLOCK_SIZE))
		self.image.fill(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y	
class BS(pygame.sprite.Sprite):
	def __init__(self,x,y):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.Surface((10,10))
		self.image.fill(RED)
		self.rect = self.image.get_rect()
		self.rect.x=x+((BLOCK_SIZE-10)/2)
		self.rect.y=y+((BLOCK_SIZE-10)/2)
		self.DBpower=0
		self.load_car=0
		bias=random.randrange(0,4)
		if bias==0:
			self.rect.y-=(BLOCK_SIZE/25)
		elif bias==1:
			self.rect.y+=(BLOCK_SIZE/25)
		elif bias==2:
			self.rect.x-=(BLOCK_SIZE/25)
		elif bias==3:
			self.rect.x+=(BLOCK_SIZE/25)
		self.freq = random.randrange(1,10)
		self.freq *= 100

all_sprites = pygame.sprite.Group()
# newcar = Car()
# all_sprites.add(newcar)
car_sprites = []
block_sprite = []
BS_sprites=[]
for i in range(10):
	for j in range(10):
		bsrand = random.randrange(0, 10000)
		block = Block((((BLOCK_SIZE+10)*i)+10),(((BLOCK_SIZE+10)*j)+10))
		all_sprites.add(block)
		if bsrand%10==0:
			bs = BS((((BLOCK_SIZE+10)*i)+10),(((BLOCK_SIZE+10)*j)+10))
			all_sprites.add(bs)
			bs.DBpower=random.randrange(1,11)*100
			bs.load_car=0
			BS_sprites.append(bs)

while running:
	clock.tick(FPS)#執行FPS次/SEC
	#輸入
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
	for i in range(1,10):
		if random.randrange(0,prob_amplifier)<=poisson_prob*prob_amplifier:
			newcar = Car((BLOCK_SIZE+10)*i,0,0)
			all_sprites.add(newcar)
			car_sprites.append(newcar)
		if random.randrange(0,prob_amplifier)<=poisson_prob*prob_amplifier:
			newcar = Car((BLOCK_SIZE+10)*i,600,1)
			all_sprites.add(newcar)
			car_sprites.append(newcar)
		if random.randrange(0,prob_amplifier)<=poisson_prob*prob_amplifier:
			newcar = Car(0,(BLOCK_SIZE+10)*i,2)
			all_sprites.add(newcar)
			car_sprites.append(newcar)
		if random.randrange(0,prob_amplifier)<=poisson_prob*prob_amplifier:
			newcar = Car(600,(BLOCK_SIZE+10)*i,3)
			all_sprites.add(newcar)
			car_sprites.append(newcar)

	#更新

	#顯示
	screen.fill(BLACK)#背景顏色
	all_sprites.update()
	for i in range(len(car_sprites)):
		if car_sprites[i].change_nearest != 0:
			switch_nearest += 1
		if car_sprites[i].change_entropy != 0:
			switch_entropy += 1
		if car_sprites[i].change_threshold != 0:
			switch_threshold += 1
		if car_sprites[i].change_direction != 0:
			switch_direction += 1
	nowtime = round((pygame.time.get_ticks())/1000)
	all_sprites.draw(screen)
	draw_text(screen,"Time(min):"+str(round((pygame.time.get_ticks())/1000)),30,(BLOCK_SIZE+10)*10+170,20,WHITE)
	draw_text(screen,"Best Effort Algorithm Switch Times:"+str(switch_nearest),30,850,100,WHITE)
	draw_text(screen,"Per Second:"+str(switch_nearest/(round((pygame.time.get_ticks())/1000))),30,850,130,WHITE)
	draw_text(screen,"Entropy Algorithm Switch Times:"+str(switch_entropy),30,850,200,WHITE)
	draw_text(screen,"Per Second:"+str(switch_entropy/(round((pygame.time.get_ticks())/1000))),30,850,230,WHITE)
	draw_text(screen,"Threshold Switch Times:"+str(switch_threshold),30,850,300,WHITE)
	draw_text(screen,"Per Second:"+str(switch_threshold/(round((pygame.time.get_ticks())/1000))),30,850,330,WHITE)
	draw_text(screen,"Threshold Central Switch Times:"+str(switch_direction),30,850,400,WHITE)
	draw_text(screen,"Per Second:"+str(switch_direction/(round((pygame.time.get_ticks())/1000))),30,850,430,WHITE)
	draw_text(screen,"Car Num:"+str(len(car_sprites)),30,750,500,WHITE)
	# print(switch_nearest)
	# if len(car_sprites) != 0: 
	# 	print(car_sprites[0].dB)
	pygame.display.update()#更新畫面
pygame.quit()