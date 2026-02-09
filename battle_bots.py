#!/usr/bin/env python3
"""
Battle Bots - A pygame-based battle bot video game
Control your bot and defeat enemy bots in arena combat!
"""

import pygame
import sys
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_RED = (150, 0, 0)
DARK_GREEN = (0, 150, 0)

# Game settings
PLAYER_SPEED = 5
ENEMY_SPEED = 3
BULLET_SPEED = 10
FIRE_COOLDOWN = 500  # milliseconds
BOT_SIZE = 40
BULLET_DAMAGE = 20
RETREAT_HEALTH_THRESHOLD = 30
CHASE_MIN_DISTANCE = 200


class Bullet:
    """Represents a bullet fired by a bot"""
    
    def __init__(self, x, y, angle, owner):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = BULLET_SPEED
        self.radius = 5
        self.owner = owner
        self.active = True
        
    def update(self):
        """Update bullet position"""
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        
        # Check if bullet is off screen
        if (self.x < 0 or self.x > WINDOW_WIDTH or 
            self.y < 0 or self.y > WINDOW_HEIGHT):
            self.active = False
            
    def draw(self, screen):
        """Draw the bullet"""
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)


class BattleBot:
    """Base class for battle bots"""
    
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.size = BOT_SIZE
        self.health = 100
        self.max_health = 100
        self.angle = 0
        self.last_fire_time = 0
        self.bullets = []
        
    def take_damage(self, damage):
        """Reduce health when hit"""
        self.health -= damage
        if self.health < 0:
            self.health = 0
            
    def is_alive(self):
        """Check if bot is still alive"""
        return self.health > 0
        
    def fire(self, current_time):
        """Fire a bullet if cooldown has passed"""
        if current_time - self.last_fire_time >= FIRE_COOLDOWN:
            # Calculate bullet spawn position at front of bot
            bullet_x = self.x + math.cos(self.angle) * (self.size / 2)
            bullet_y = self.y + math.sin(self.angle) * (self.size / 2)
            
            bullet = Bullet(bullet_x, bullet_y, self.angle, self)
            self.bullets.append(bullet)
            self.last_fire_time = current_time
            return True
        return False
        
    def update_bullets(self):
        """Update all bullets fired by this bot"""
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.active:
                self.bullets.remove(bullet)
                
    def draw(self, screen):
        """Draw the bot and its components"""
        # Draw bot body (circle)
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)
        
        # Draw direction indicator (line showing where bot is facing)
        end_x = self.x + math.cos(self.angle) * (self.size // 2)
        end_y = self.y + math.sin(self.angle) * (self.size // 2)
        pygame.draw.line(screen, WHITE, (int(self.x), int(self.y)), 
                        (int(end_x), int(end_y)), 3)
        
        # Draw health bar
        self.draw_health_bar(screen)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)
            
    def draw_health_bar(self, screen):
        """Draw health bar above the bot"""
        bar_width = self.size
        bar_height = 5
        bar_x = self.x - bar_width // 2
        bar_y = self.y - self.size // 2 - 15
        
        # Background (red)
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)


class PlayerBot(BattleBot):
    """Player-controlled battle bot"""
    
    def __init__(self, x, y):
        super().__init__(x, y, BLUE, "Player")
        self.speed = PLAYER_SPEED
        
    def handle_input(self, keys, mouse_pos, current_time):
        """Handle player input for movement and aiming"""
        # Movement with WASD or arrow keys
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.y += self.speed
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.x += self.speed
            
        # Keep player in bounds
        self.x = max(self.size // 2, min(WINDOW_WIDTH - self.size // 2, self.x))
        self.y = max(self.size // 2, min(WINDOW_HEIGHT - self.size // 2, self.y))
        
        # Aim toward mouse cursor
        dx = mouse_pos[0] - self.x
        dy = mouse_pos[1] - self.y
        self.angle = math.atan2(dy, dx)


class EnemyBot(BattleBot):
    """AI-controlled enemy battle bot"""
    
    def __init__(self, x, y):
        super().__init__(x, y, RED, "Enemy")
        self.speed = ENEMY_SPEED
        self.target = None
        self.state = "chase"  # chase or retreat
        self.retreat_distance = 150
        self.fire_distance = 300
        
    def update_ai(self, target, current_time):
        """Update AI behavior"""
        self.target = target
        
        if not target.is_alive():
            return
            
        # Calculate distance to target
        dx = target.x - self.x
        dy = target.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Aim at target
        self.angle = math.atan2(dy, dx)
        
        # Decide behavior based on distance and health
        if self.health < RETREAT_HEALTH_THRESHOLD and distance < self.retreat_distance:
            # Retreat if low health and too close
            self.state = "retreat"
            self.x -= math.cos(self.angle) * self.speed
            self.y -= math.sin(self.angle) * self.speed
        else:
            # Chase player
            self.state = "chase"
            if distance > CHASE_MIN_DISTANCE:  # Stay at medium range
                self.x += math.cos(self.angle) * self.speed
                self.y += math.sin(self.angle) * self.speed
                
        # Keep enemy in bounds
        self.x = max(self.size // 2, min(WINDOW_WIDTH - self.size // 2, self.x))
        self.y = max(self.size // 2, min(WINDOW_HEIGHT - self.size // 2, self.y))
        
        # Fire at player if in range
        if distance < self.fire_distance:
            self.fire(current_time)


class BattleBotsGame:
    """Main game class"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Battle Bots")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.running = True
        self.game_state = "playing"  # playing, won, lost
        
        # Create player
        self.player = PlayerBot(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        
        # Create enemies
        self.enemies = []
        self.spawn_enemies(3)
        
        self.all_bots = [self.player] + self.enemies
        
    def spawn_enemies(self, count):
        """Spawn enemy bots at random positions"""
        for _ in range(count):
            # Spawn enemies away from center
            x = random.choice([random.randint(50, 200), 
                             random.randint(WINDOW_WIDTH - 200, WINDOW_WIDTH - 50)])
            y = random.choice([random.randint(50, 200), 
                             random.randint(WINDOW_HEIGHT - 200, WINDOW_HEIGHT - 50)])
            self.enemies.append(EnemyBot(x, y))
            
    def check_collisions(self):
        """Check for bullet collisions with bots"""
        for bot in self.all_bots:
            if not bot.is_alive():
                continue
                
            for other_bot in self.all_bots:
                if bot == other_bot or not other_bot.is_alive():
                    continue
                    
                for bullet in bot.bullets[:]:
                    # Check if bullet hits other bot
                    dx = bullet.x - other_bot.x
                    dy = bullet.y - other_bot.y
                    distance = math.sqrt(dx**2 + dy**2)
                    
                    if distance < other_bot.size // 2:
                        other_bot.take_damage(BULLET_DAMAGE)
                        bullet.active = False
                        bot.bullets.remove(bullet)
                        break
                        
    def update(self):
        """Update game state"""
        if self.game_state != "playing":
            return
            
        current_time = pygame.time.get_ticks()
        
        # Handle player input
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        
        self.player.handle_input(keys, mouse_pos, current_time)
        
        # Fire with mouse click or space
        if mouse_buttons[0] or keys[pygame.K_SPACE]:
            self.player.fire(current_time)
            
        # Update enemies
        for enemy in self.enemies:
            if enemy.is_alive():
                enemy.update_ai(self.player, current_time)
                
        # Update all bullets
        for bot in self.all_bots:
            bot.update_bullets()
            
        # Check collisions
        self.check_collisions()
        
        # Check win/loss conditions
        if not self.player.is_alive():
            self.game_state = "lost"
        elif all(not enemy.is_alive() for enemy in self.enemies):
            self.game_state = "won"
            
    def draw(self):
        """Draw everything"""
        self.screen.fill(GRAY)
        
        # Draw grid
        for x in range(0, WINDOW_WIDTH, 50):
            pygame.draw.line(self.screen, (100, 100, 100), (x, 0), (x, WINDOW_HEIGHT), 1)
        for y in range(0, WINDOW_HEIGHT, 50):
            pygame.draw.line(self.screen, (100, 100, 100), (0, y), (WINDOW_WIDTH, y), 1)
            
        # Draw all bots
        for bot in self.all_bots:
            if bot.is_alive():
                bot.draw(self.screen)
                
        # Draw UI
        self.draw_ui()
        
        # Draw game over screen
        if self.game_state == "won":
            self.draw_victory_screen()
        elif self.game_state == "lost":
            self.draw_defeat_screen()
            
        pygame.display.flip()
        
    def draw_ui(self):
        """Draw game UI"""
        # Player health
        health_text = self.small_font.render(f"Health: {self.player.health}", True, WHITE)
        self.screen.blit(health_text, (10, 10))
        
        # Enemy count
        enemies_alive = sum(1 for enemy in self.enemies if enemy.is_alive())
        enemy_text = self.small_font.render(f"Enemies: {enemies_alive}/{len(self.enemies)}", 
                                           True, WHITE)
        self.screen.blit(enemy_text, (10, 40))
        
        # Controls hint
        controls = self.small_font.render("WASD/Arrows: Move | Mouse/Space: Shoot", 
                                         True, WHITE)
        self.screen.blit(controls, (10, WINDOW_HEIGHT - 30))
        
    def draw_victory_screen(self):
        """Draw victory screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(DARK_GREEN)
        self.screen.blit(overlay, (0, 0))
        
        text = self.font.render("VICTORY!", True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(text, text_rect)
        
        restart_text = self.small_font.render("Press R to Restart or ESC to Quit", 
                                             True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_defeat_screen(self):
        """Draw defeat screen"""
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(DARK_RED)
        self.screen.blit(overlay, (0, 0))
        
        text = self.font.render("DEFEAT!", True, WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30))
        self.screen.blit(text, text_rect)
        
        restart_text = self.small_font.render("Press R to Restart or ESC to Quit", 
                                             True, WHITE)
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(restart_text, restart_rect)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_state in ["won", "lost"]:
                    self.restart()
                    
    def restart(self):
        """Restart the game"""
        self.player = PlayerBot(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        self.enemies = []
        self.spawn_enemies(3)
        self.all_bots = [self.player] + self.enemies
        self.game_state = "playing"
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    game = BattleBotsGame()
    game.run()


if __name__ == "__main__":
    main()
