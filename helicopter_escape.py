# INTIALISATION
import random
import pygame, math, sys
from pygame.locals import *
import os

building_color = [(163,158,155),(104,73,71),(243,146,75),(234,62,122),(84,22,180),(25,25,112),(141,236,120),(255,226,0),(255,130,1),(255,0,0)]

screen = pygame.display.set_mode((1200, 600))
helicopter_height = 35
helicopter_width= 83
building_gap_mininum = 50
gap_between_building = 200
helicopter_y = 10
window_side = 10
building_width = 5 * window_side
floor_height = window_side*2.5
fuel_height = 30
fuel_width = 33
doublepoints_width = 39
doublepoints_height = 33
slower_width = 33
slower_height = 33
nodamage_width = 28
nodamage_height = 30
helicopter_x_init = 2

screen = pygame.display.set_mode((1200, 600))
clock = pygame.time.Clock()
pygame.font.init()
font1 = pygame.font.SysFont("cambria",24)
font2 = pygame.font.SysFont("arialblack",64)
font3 = pygame.font.SysFont("cambria",38)
font4 = pygame.font.SysFont("vt323",40)


def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
      return event.key
    else:
      pass


def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()


def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  display_box(screen, question + ": " + "".join(current_string))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      current_string.append("_")
    elif inkey <= 127:
      current_string.append(chr(inkey))
    display_box(screen, question + ": " + "".join(current_string))
  return "".join(current_string)


def load_image(name, colorkey=None):
    path = os.path.join('',  name)
    try:
        image = pygame.image.load(path)
    except pygame.error:
        print('Cannot load image: {}'.format(path))
        raise SystemExit
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at( (0, 0) )
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()



class Buildingpair(object):
	def __init__(self,location_x, floor,not_passed):
		self.location_x = location_x
		self.floor = floor
		self.not_passed = not_passed

	def draw(self,floor_sum,building_gap_size,level):
		pygame.draw.rect(screen,building_color[level-1], (self.location_x,0,building_width, self.floor*floor_height), 0)
		
		for i in range(self.floor):
			pygame.draw.rect(screen,(255,255,255), (self.location_x+window_side,i*floor_height+window_side//2,window_side,window_side), 0)
			pygame.draw.rect(screen,(255,255,255), (self.location_x+window_side*3,i*floor_height+window_side//2,window_side,window_side), 0)
		pygame.draw.rect(screen,building_color[level-1], (self.location_x,self.floor*floor_height+building_gap_size,building_width, (floor_sum-self.floor)*floor_height), 0)
		for i in range(floor_sum-self.floor):
			pygame.draw.rect(screen,(255,255,255), (self.location_x+window_side,(self.floor+i)*floor_height+window_side//2+building_gap_size,window_side,window_side), 0)
			pygame.draw.rect(screen,(255,255,255), (self.location_x+window_side*3,(self.floor+i)*floor_height+window_side//2+building_gap_size,window_side,window_side), 0)

	def is_helicopter_collision(self, helicopter,building_gap_size,floor_sum):
		rect1 = pygame.Rect(self.location_x,0,building_width,self.floor*floor_height)
		rect2 = pygame.Rect(self.location_x,self.floor*floor_height+building_gap_size,building_width, (floor_sum-self.floor)*floor_height)
		return rect1.colliderect(helicopter.get_rectangle_obj()) or rect2.colliderect(helicopter.get_rectangle_obj()) or helicopter.pos_y<=0 or helicopter.pos_y>= 600-helicopter_height

	def check_new_point(self, helicopter,building_gap_size):
		rect3 = pygame.Rect(self.location_x,self.floor*floor_height,building_width,building_gap_size)
		return rect3.colliderect(helicopter.get_rectangle_obj()) 



class Helicopter(object):
	def __init__(self,pos_x,pos_y,image):
		self.speed_x = helicopter_x_init
		self.speed_y = helicopter_y 
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image

	def draw(self):
		screen.blit(self.image,(self.pos_x,self.pos_y))

	def move(self,up_down):
		self.pos_x += self.speed_x
		self.pos_y += self.speed_y * up_down
		self.draw()

	def get_rectangle_obj(self):
		return pygame.Rect(self.pos_x, self.pos_y, helicopter_width, helicopter_height)


class Fuel(object):
	def __init__(self,pos_x,pos_y,image,not_passed):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		self.not_passed = not_passed

	def draw(self):
		screen.blit(self.image,(self.pos_x,self.pos_y))

	def get_rectangle_obj(self):
		return pygame.Rect(self.pos_x, self.pos_y, fuel_width, fuel_height)

	def check_get_fuel(self, helicopter):
		rect4 = pygame.Rect(self.pos_x,self.pos_y,fuel_width,fuel_height)
		return rect4.colliderect(helicopter.get_rectangle_obj()) 



class Doublepoints(object):
	def __init__(self,pos_x,pos_y,image,not_passed):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		self.not_passed = not_passed

	def draw(self):
		screen.blit(self.image,(self.pos_x,self.pos_y))

	def get_rectangle_obj(self):
		return pygame.Rect(self.pos_x, self.pos_y, doublepoints_width, doublepoints_height)

	def check_doublepoints(self, helicopter):
		rect4 = pygame.Rect(self.pos_x,self.pos_y,doublepoints_width,doublepoints_height)
		return rect4.colliderect(helicopter.get_rectangle_obj()) 


class Slower(object):
	def __init__(self,pos_x,pos_y,image,not_passed):
		self.pos_x = pos_x
		self.pos_y = pos_y
		self.image = image
		self.not_passed = not_passed

	def draw(self):
		screen.blit(self.image,(self.pos_x,self.pos_y))

	def get_rectangle_obj(self):
		return pygame.Rect(self.pos_x, self.pos_y, slower_width, slower_height)

	def check_slower(self, helicopter):
		rect4 = pygame.Rect(self.pos_x,self.pos_y,slower_width,slower_height)
		return rect4.colliderect(helicopter.get_rectangle_obj()) 


class User(object):

	def __init__(self,name, score):
		self.name = name
		self.score = score
		self.not_ranked = True


class myGame:

	def __init__(self):
		pygame.init()		
		self.level = 1
		self.building_gap_size = 150
		self.floor_sum = int((600- self.building_gap_size) // floor_height)
		self.building_sets = []
		self.pos_empty = [True] * 600

		for i in range(6):
			building1 = Buildingpair(300,random.randint(1,self.floor_sum-1),True)
			building2 = Buildingpair(600,random.randint(1,self.floor_sum-1),True)
			building3 = Buildingpair(900,random.randint(1,self.floor_sum-1),True)
			self.building_sets.append([building1,building2,building3])
		self.fuel_sets = [None,None,None]
		self.doublepoints_sets = [None,None,None]
		self.slower_sets = [None,None,None]
		

	def get_fuel_sets(self):		
		for i in range(3):
			num = random.randint(0,1)
			if num==0:
				show_or_not = False
			else:
				show_or_not = True
			
			if show_or_not:
				x = (i+1)*300+200-fuel_width
				y = random.randint(100,500)
				for j in range(y-2*fuel_height,y+2*fuel_height+1):
					self.pos_empty[j]=False
				fuel_image = load_image('fuelcan.png')
				fuel = Fuel(x,y,fuel_image[0],True)
				self.fuel_sets[i] = fuel


	def get_doublepoints_sets(self):		
		for i in range(3):
			num = random.randint(0,10)
			if num==0:
				show_or_not = True
			else:
				show_or_not = False
			
			if show_or_not:
				x = (i+1)*300+200-doublepoints_width
				y = random.randint(100,500)
				while self.pos_empty[y]:
					y = random.randint(100,500)
				for j in range(y-2*doublepoints_height,y+2*doublepoints_height+1):
					self.pos_empty[j]=False
				doublepoints_image = load_image('doublepoints.png')
				doublepoints = Doublepoints(x,y,doublepoints_image[0],True)
				self.doublepoints_sets[i] = doublepoints


	def get_slower_sets(self):		
		for i in range(3):
			num = random.randint(0,10)
			if num==0:
				show_or_not = True
			else:
				show_or_not = False
			
			if show_or_not:
				x = (i+1)*300+200-doublepoints_width/2
				y = random.randint(100,500)
				while self.pos_empty[y]:
					y = random.randint(100,500)
				for j in range(y-slower_height, y+2*slower_height+1):
					self.pos_empty[j]=False
				slower_image = load_image('slower.png')
				slower = Slower(x,y,slower_image[0],True)
				self.slower_sets[i] = slower


	def get_building_bg(self,i,level):
		background = load_image('background.png')
		screen.blit(background[0],(0,0))
		temp = self.building_sets[i]
		for j in range(3):
			temp[j].draw(self.floor_sum,self.building_gap_size,level)


	def show_fuel(self):		
		for i in range(3):
			if self.fuel_sets[i]!=None:
				self.fuel_sets[i].draw()


	def show_doublepoints(self):		
		for i in range(3):
			if self.doublepoints_sets[i]!=None:
				self.doublepoints_sets[i].draw()


	def show_slower(self):		
		for i in range(3):
			if self.slower_sets[i]!=None:
				self.slower_sets[i].draw()


	def start_screen(self):
		background = load_image('background.png')
		screen.blit(background[0],(0,0))
		helicopter_image = load_image('Helicopter2.png')
		screen.blit(helicopter_image[0],(25,200))
		helicopter_sound = pygame.mixer.Sound("Helicopter_sound.wav")	
		channel_helicopter = pygame.mixer.Channel(0)
		channel_helicopter.play(helicopter_sound)
		text = font2.render("HELICOPTER ESCAPE",1,(255,255,255))
		screen.blit(text,(200,50))
		text0 = font4.render("By:Nicholas Rahardja",1,(255,255,255))
		screen.blit(text0,(850,200))
		text1= font3.render("Press ANY KEY to start",1,(255,255,255))
		screen.blit(text1,(400,550))
		pygame.display.flip()
		pygame.time.delay(600)


	def show_rules(self):
		rule = load_image('instruction-1.png')
		screen.blit(rule[0],(0,0))
		pygame.display.flip()
				
	
	def run(self):
		# show the start screen
		helicopter_image = load_image('helicopter.png')
		helicopter = Helicopter(59,300,helicopter_image[0])
		self.start_screen()		
		# wait until the user is ready for the game
		event = pygame.event.wait()	
		while event.type!=KEYDOWN: 
			event = pygame.event.wait() 
		# show up the instruction page 1 
		self.show_rules()
		# ask for user input to decide with which level they would like to start
		self.level = 1
		if hasattr(event,"key"):

			while event.key!=K_1 and event.key!=K_2 and event.key!=K_3:
				event = pygame.event.wait() 			
			
			if event.key == K_1:
				self.level = 1

			elif event.key == K_2:
				self.level = 4
				self.building_gap_size = 100
				self.floor_sum = int((600- self.building_gap_size) // floor_height)
				helicopter.speed_x = 4

			else:
				self.level = 7
				self.building_gap_size = 75
				self.floor_sum = int((600- self.building_gap_size) // floor_height)
				helicopter.speed_x = 5
	
		# initializing the variables	
		point = 0		
		count_level_up = 0		
		count_doublepoints = 0
		count_slower = 0		
		power_doublepoints = False
		power_slower = False
		running = True
		
		# initializing the sounds
		pygame.mixer.init(channels=3)
		# play the helicopter background sound
		helicopter_sound = pygame.mixer.Sound("Helicopter_sound.wav")	
		channel_helicopter = pygame.mixer.Channel(0)
		channel_helicopter.play(helicopter_sound,loops=-1)
		#initializing the sound effect for getting fuelcans
		fuelsound = pygame.mixer.Sound("fuelsound.wav")	
		channel_fuel = pygame.mixer.Channel(1)
		#initialing the sound effect for level up
		levelup = pygame.mixer.Sound("levelup.wav")		
		channel_level = pygame.mixer.Channel(2)

		#set the initial movement of the helicopter to be horizontal to the right
		up_down = 0

		#draw the helicopter 
		helicopter.draw()
		pos = 0
		# get random building pairs, fuelcans, double-points powerups, half-speed powerups
		# and show these on the screen
		self.get_building_bg(pos,self.level)
		self.get_fuel_sets()		
		self.get_doublepoints_sets()
		self.get_slower_sets()		
		self.show_fuel()		
		self.show_doublepoints()
		self.show_slower()
		self.pos_empty = [True]*700
		pygame.display.flip()



		while running:
			clock.tick(100)		
			# after helicopter moves out of the screen
			if helicopter.pos_x >= 1200:
				# check if the user gets level up (successfully passing 6 building pairs)
				if count_level_up == 6:
					self.level += 1
					channel_level.play(levelup)
					# building gap sizes decreases by 25 for moving from every even level to an odd level
					if self.level % 2 ==1:
						self.building_gap_size -= 25
						self.floor_sum = int((600- self.building_gap_size) // floor_height)
					#speed increases by 1 for moving from moving from every odd level to an even level
					else:
						helicopter.speed_x += 1
					#the building gap size and the speed do not change for level larger than 10
					if self.level >= 10:
						self.building_gap_size = 50
						helicopter.speed_x = 7
						self.floor_sum = int((600- self.building_gap_size) // floor_height)
					count_level_up = 0
				#moving to the next random building pair
				pos = (pos+1) % 6
				# reset the helicopter position to the left of the screen
				helicopter.pos_x = 20
				for j in range(3):
					self.building_sets[pos][j].not_passed = True
				# get new fuelcans, double-points icons, half-speed icons for the new screen
				self.get_fuel_sets()				
				self.get_doublepoints_sets()
				self.get_slower_sets()
				self.pos_empty = [True]*700

			# show the new screen
			self.get_building_bg(pos,self.level)
			self.show_fuel()			
			self.show_doublepoints()
			self.show_slower()
			# move the helicopter up or down according to the user input
			helicopter.move(up_down)

			#show point
			show_point = font1.render("point:"+str(point),1,(255,255,255))
			screen.blit(show_point,(10,10))
			pygame.display.flip()

			#show level
			show_level = font1.render("level:"+str(self.level),1,(255,255,255))
			screen.blit(show_level,(140,10))
			pygame.display.flip()
			
			# check through each building pair
			for i in range(3):
				# check get fuel
				if self.fuel_sets[i]!=None and self.fuel_sets[i].check_get_fuel(helicopter) and self.fuel_sets[i].not_passed :
					point += 2
					channel_fuel.play(fuelsound)
					self.fuel_sets[i].not_passed = False
					self.fuel_sets[i] = None
					self.get_building_bg(pos,self.level)
					helicopter.draw()
				# check get double points
				if self.doublepoints_sets[i]!=None and self.doublepoints_sets[i].check_doublepoints(helicopter) and self.doublepoints_sets[i].not_passed :
					channel_fuel.play(fuelsound)
					self.doublepoints_sets[i].not_passed = False
					self.doublepoints_sets[i] = None
					power_doublepoints = True
					count_doublepoints = 0
					tex = font3.render("DOUBLE POINTS",1,(0,255,0))
					screen.blit(tex,(10,50))
					pygame.display.flip()
					pygame.time.delay(400)
					self.get_building_bg(pos,self.level)
					helicopter.draw()
				
				# check get slower
				if self.slower_sets[i]!=None and self.slower_sets[i].check_slower(helicopter) and self.slower_sets[i].not_passed :
					channel_fuel.play(fuelsound)
					self.slower_sets[i].not_passed = False
					self.slower_sets[i] = None
					power_slower = True
					count_slower = 0
					helicopter.speed_x  = helicopter.speed_x / 2
					tex = font3.render("HALF SPEED",1,(0,255,0))
					screen.blit(tex,(10,50))
					pygame.display.flip()
					pygame.time.delay(400)
					self.get_building_bg(pos,self.level)
					helicopter.draw()

				# check new point
				if self.building_sets[pos][i].check_new_point(helicopter,self.building_gap_size) and self.building_sets[pos][i].not_passed :
					point += self.level

					if power_doublepoints:
						point += self.level 

					count_level_up += 1	

					# expire doublepoints after passing 3 buildings
					if power_doublepoints:
						count_doublepoints += 1	
						if count_doublepoints == 3:
							count_doublepoints = 0
							power_doublepoints = False
							tex = font1.render("DOUBLE POINTS EXPIRES",1,(0,255,0))
							screen.blit(tex,(10,50))
							pygame.display.flip()
							pygame.time.delay(400)
					# expire slower after passing 3 buildings
					if power_slower :
						count_slower += 1	
						if count_slower == 3:
							count_slower = 0
							power_slower = False
							tex = font1.render("HALF SPEED EXPIRES",1,(0,255,0))
							screen.blit(tex,(10,50))
							pygame.display.flip()
							pygame.time.delay(400)
							helicopter.speed_x = 2 + self.level // 2
							multiplier = 1		

					self.building_sets[pos][i].not_passed = False


				# check collision
				if self.building_sets[pos][i].is_helicopter_collision(helicopter,self.building_gap_size,self.floor_sum):
					
					#show the collision image on the helicopter
					collision_image = load_image('collision.png')
					screen.blit(collision_image[0],(helicopter.pos_x-18,helicopter.pos_y-18))
					pygame.display.flip()
					pygame.mixer.init()

			
					#show the game over screen with the new score
					game_over_image = load_image('game over.png')
					screen.blit(game_over_image[0],(0,0))
					score = font2.render("Your Score: "+str(point),1,(255,255,255))
					screen.blit(score,(330,400))
					pygame.display.flip()

					####show enter or escape to replay or quit
					text1= font1.render("Press ANY KEY to replay",1,(255,255,255))
					text2= font1.render("Press ESCAPE to quit",1,(255,255,255))
					screen.blit(text1,(300,550))
					screen.blit(text2,(700,550))
					pygame.display.flip()
					pygame.time.delay(4000)

					#ask for user input to decide to play again or quit
					event = pygame.event.wait()		
					if hasattr(event,"key"):
						while event.type!=KEYDOWN: 
							event = pygame.event.wait()								
						if event.key == K_ESCAPE:
							sys.exit(0)
						else:
							#ask for username
							screen.fill((0,0,0))
							username = ask(screen, "Name") 
							
							#read the previous top 5 scores 
							file_handler = open('leader_board.txt', 'r')
							file_handler.seek(0)
							scores = file_handler.readlines()
							file_handler.close()
							scores.append(str(point))
							#scores = [int(x) for x in scores]							
							# read the previous top 5 users' name
							file_handler = open('username.txt','r')
							file_handler.seek(0)
							names = []
							for i in range(len(scores)-1):
								line = file_handler.readline()
								line = line.strip()
								names.append(line)
							file_handler.close()
							names.append(username)

							# get a userlist(name,score)
							userlist = []
							for i in range(len(scores)):
								temp_user = User(names[i],scores[i])
								userlist.append(temp_user)
							#sort the scores and corresponds the users' names to their scores
							scores.sort(reverse = True)
							for i in range(len(scores)):
								for j in userlist:
									if j.score == scores[i] and j.not_ranked:
										j.not_ranked = False
										names[i]=j.name
										break
							#get only top 5
							scores = scores[0:5]
							names = names[0:5]						
							scores = [str(x) for x in scores]
							
							#show new leaderboard on the screen
							screen.fill((0,0,0))
							texxt = font2.render("LEADERBOARD",1, (255,255,255))
							screen.blit(texxt,(330,30))
							for i in range(len(scores)):
								textt= font3.render(names[i]+': '+scores[i],1,(255,255,255))
								screen.blit(textt,(540,130+80*i))
							pygame.display.flip()
							pygame.time.delay(4000)
							#save the info to the file
							with open('leader_board.txt', 'w') as f:
								f.write('\n'.join(scores))
							with open('username.txt','w') as f:
								f.write('\n'.join(names))
					

							# go back to the instruction page
							self.show_rules()

							# reset all the variables to replay
							self.level = 1
							event = pygame.event.wait()
							if hasattr(event,"key"):
								while event.key!=K_1 and event.key!=K_2 and event.key!=K_3:
									event = pygame.event.wait() 									
								if event.key == K_1:
									self.level = 1
									helicopter.speed_x = 2
									self.building_gap_size = 150
								elif event.key == K_2:
									self.level = 4
									self.building_gap_size = 100									
									helicopter.speed_x = 4
								else:
									self.level = 7
									self.building_gap_size = 75
									helicopter.speed_x = 5
								self.floor_sum = int((600- self.building_gap_size) // floor_height)
								helicopter.pos_x = 59
								helicopter.pos_y = 300

							point = 0		
							count_level_up = 0
							running = True
							count_doublepoints = 0
							count_slower = 0
							power_doublepoints = False
							power_slower = False													
							pygame.mixer.init(channels=3)
							up_down = 0
							helicopter.draw()
							pos = 0							
							for i in range(3):
								self.building_sets[pos][i].not_passed = True							
							self.get_building_bg(pos,self.level)
							self.get_fuel_sets()
							self.get_doublepoints_sets()
							self.get_slower_sets()		
							self.show_fuel()
							self.show_doublepoints()
							self.show_slower()
							self.pos_empty = [True]*700

							pygame.display.flip()
							helicopter_sound = pygame.mixer.Sound("Helicopter_sound.wav")	
							channel_helicopter = pygame.mixer.Channel(0)
							channel_helicopter.play(helicopter_sound,loops=-1)

							fuelsound = pygame.mixer.Sound("fuelsound.wav")	
							channel_fuel = pygame.mixer.Channel(1)

							levelup = pygame.mixer.Sound("levelup.wav")		
							channel_level = pygame.mixer.Channel(2)									
							

			# constantly getting input from the user		
			for event in pygame.event.get():
				if not hasattr(event,"key"): continue									
				if event.key ==K_UP and event.type == KEYDOWN:
					up_down = -1
				elif event.key ==K_DOWN and event.type == KEYDOWN:
					up_down = 1
				elif event.key == K_ESCAPE:
					sys.exit(0)
				elif event.type ==KEYUP:
					up_down = 0
						
			pygame.display.flip()



if __name__ == "__main__":
    myGame().run()
