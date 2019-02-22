#!/usr/bin/env python3
'''
	Name: Space Invaders
	Module: PyArcade
'''
import arcade, os, sys, random, time

#Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Space Invaders"
PLAYER_SCALING = 0.7
BULLET_SCALING = 1
ENEMY_SCALING = 0.3
MOVEMENT_SPEED = 3.5
BULLET_SPEED = 5
CLOCK_TIME = 30
GAME_RUNNING = 1
GAME_OVER = 2
GAME_WIN = 3

class MyGame(arcade.Window):
	def __init__(self, width, height, title):
		#Standard declarations and working folder
		super().__init__(width, height, title)
		file_path = os.path.dirname(os.path.abspath(__file__))
		os.chdir(file_path)
		
		#Inizialize Variables
		self.player_list = None
		self.enemy_list = None
		self.bullet_list = None
		self.enemy_bullet_list = None
		self.background = None
		self.player_sprite = None
		self.enemy_sprite = None

		#Set of current state and score
		self.current_state = GAME_RUNNING
		self.score = 0	

		#Movement variables
		self.left_pressed = False
		self.right_pressed = False
		self.down_pressed = False
		self.up_pressed = False	

		arcade.set_background_color(arcade.color.BLACK)

	def setup(self):
		#Declarations of Sprite lists
		self.player_list = arcade.SpriteList()
		self.enemy_list = arcade.SpriteList()
		self.bullet_list = arcade.SpriteList()
		self.enemy_bullet_list = arcade.SpriteList()

		#Player score
		self.score = 0

		#Player spawn
		self.player_sprite = Player("sprites/ship.png", PLAYER_SCALING)
		self.player_sprite.center_x = (SCREEN_WIDTH/2)
		self.player_sprite.center_y = 50
		self.player_list.append(self.player_sprite)
		
		#Spacing for spawning enemies
		X_SPACING = 0
		Y_SPACING = 0

		#Enemy Spawn
		for col in range(3):
			for row in range(16):
				self.enemy_sprite = Enemy("sprites/enemy1_1.png", ENEMY_SCALING)
				self.enemy_sprite.center_x = 25 + X_SPACING
				self.enemy_sprite.center_y = 570 - Y_SPACING
				self.enemy_list.append(self.enemy_sprite)
				X_SPACING += 50
			Y_SPACING += 50
			X_SPACING = 0
	
		self.background = arcade.load_texture("sprites/background.jpg")

	def draw_game_win(self):
		output = "YOU WON"
		arcade.draw_text(output, 200, SCREEN_HEIGHT / 2, arcade.color.GREEN, 50)
		
		output = "Press R to restart"
		arcade.draw_text(output, 200, (SCREEN_HEIGHT / 2) - 35, arcade.color.WHITE, 18)

		output = "Press ESC to exit"
		arcade.draw_text(output, 200, (SCREEN_HEIGHT /2 )- 70, arcade.color.WHITE, 18)

	def draw_game_over(self):
		output = "GAME OVER"
		arcade.draw_text(output, 200, SCREEN_HEIGHT / 2, arcade.color.RED, 50)
		
		output = "Press R to restart"
		arcade.draw_text(output, 200, (SCREEN_HEIGHT / 2) - 35, arcade.color.WHITE, 18)

		output = "Press ESC to exit"
		arcade.draw_text(output, 200, (SCREEN_HEIGHT /2 )- 70, arcade.color.WHITE, 18)

	def draw_game(self):
		self.player_list.draw()
		self.enemy_list.draw()
		self.bullet_list.draw()
		self.enemy_bullet_list.draw()

		output = f"Score: {self.score}"
		arcade.draw_text(output, 10 , 20, arcade.color.WHITE, 14)

	def on_draw(self):
		arcade.start_render()
		arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

		if self.current_state == GAME_RUNNING:
			self.draw_game()
		elif self.current_state == GAME_OVER:
			self.draw_game_over()
		elif self.current_state == GAME_WIN:
			self.draw_game_win()
	
	def update(self, delta_time):
		if self.current_state == GAME_RUNNING:
			self.player_list.update()
			self.enemy_list.update()
			self.bullet_list.update()
			self.enemy_bullet_list.update()

			for enemy in self.enemy_list:
				if random.randrange(500) == 0:
					enemy_bullet = arcade.Sprite("sprites/enemylaser.png")
					enemy_bullet.center_x = enemy.center_x
					enemy_bullet.top = enemy.bottom
					enemy_bullet.change_y = -2
					self.enemy_bullet_list.append(enemy_bullet)

			if arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list):
				self.player_sprite.kill()
				self.current_state = GAME_OVER

			for enemy_bullet in self.enemy_bullet_list:
				enemy_hit_list = arcade.check_for_collision_with_list(enemy_bullet, self.player_list)
				if len(enemy_hit_list) > 0:
					enemy_bullet.kill()
				for player in enemy_hit_list:
					player.kill()
					self.current_state = GAME_OVER
				if enemy_bullet.bottom > SCREEN_HEIGHT:
					enemy_bullet.kill()	

			for bullet in self.bullet_list:
				hit_list = arcade.check_for_collision_with_list(bullet, self.enemy_list)
				if len(hit_list) > 0:
					bullet.kill()
				for enemy in hit_list:
					enemy.kill()
					self.score += 10
				if bullet.bottom > SCREEN_HEIGHT:
					bullet.kill()

			self.player_sprite.change_x = 0
			self.player_sprite.change_y = 0

			if self.up_pressed and not self.down_pressed:
				self.player_sprite.change_y = MOVEMENT_SPEED
			elif self.down_pressed and not self.up_pressed:
				self.player_sprite.change_y = -MOVEMENT_SPEED
			if self.left_pressed and not self.right_pressed:
				self.player_sprite.change_x = -MOVEMENT_SPEED
			elif self.right_pressed and not self.left_pressed:
				self.player_sprite.change_x = MOVEMENT_SPEED

			if self.enemy_sprite.center_y < 50:
				self.current_state = GAME_OVER

			if len(self.enemy_list) == 0:
				self.current_state == GAME_WIN

	def on_key_press(self, key, modifiers):
		if self.current_state == GAME_RUNNING:
			if key == arcade.key.UP or key == arcade.key.W:
				self.up_pressed = True
			elif key == arcade.key.DOWN or key == arcade.key.S:
				self.down_pressed = True
			if key == arcade.key.LEFT or key == arcade.key.A:
				self.left_pressed = True
			elif key == arcade.key.RIGHT or key == arcade.key.D:
				self.right_pressed = True
			if key == arcade.key.SPACE:
				bullet = arcade.Sprite("sprites/laser.png", BULLET_SCALING)
				bullet.change_y = BULLET_SPEED
				bullet.center_x = self.player_sprite.center_x
				bullet.bottom = self.player_sprite.top
				self.bullet_list.append(bullet)
		if self.current_state == GAME_OVER:
			if key == arcade.key.R:
				self.setup()
				self.current_state = GAME_RUNNING

		if key == arcade.key.ESCAPE:
			sys.exit()	

	def on_key_release(self, key, modifiers):
		if self.current_state == GAME_RUNNING:
			if key == arcade.key.UP or key == arcade.key.W:
				self.up_pressed = False
			elif key == arcade.key.DOWN or key == arcade.key.S:
				self.down_pressed = False
			if key == arcade.key.LEFT or key == arcade.key.A:
				self.left_pressed = False
			elif key == arcade.key.RIGHT or key == arcade.key.D:
				self.right_pressed = False

class Player(arcade.Sprite):
	def update(self):
		self.center_x += self.change_x
		self.center_y += self.change_y

		if self.left < 0:
			self.left = 0
		elif self.right > SCREEN_WIDTH - 1:
			self.right = SCREEN_WIDTH - 1

		if self.bottom < 0:
			self.bottom = 0
		elif self.top > SCREEN_HEIGHT - 1:
			self.top = SCREEN_HEIGHT - 1

class Enemy(arcade.Sprite):
	def update(self):
		self.center_x += self.change_x
		self.center_y += self.change_y 
	
		self.center_y -= 1

		if self.left < 0:
			self.left = 0
		elif self.right > SCREEN_WIDTH - 1:
			self.right = SCREEN_WIDTH - 1

		if self.bottom < 0:
			self.bottom = 0
		elif self.top > SCREEN_HEIGHT - 1:
			self.top = SCREEN_HEIGHT - 1

def main():
	game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
	game.setup()
	arcade.run()

if __name__ == "__main__":
	main()