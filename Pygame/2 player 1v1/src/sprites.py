from config import *
from powerups import POWERUP_COOLDOWN_TYPE
from weapons import *
from platforms import *


class AnimatedSprite(p.sprite.Sprite):
    def __init__(self, x, y, images: list):
        super().__init__()

        self.delay = 1
        self.images = images
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.current = 0

    def update(self, dt):
        self.current += dt

        if self.current > self.delay:
            self.index += 1
            self.index %= len(self.images)
            self.image = self.images[self.index]
            self.current = 0


class Bullet(p.sprite.Sprite):

    def __init__(self, x, y, velocity, game, origin, weapon):
        super(Bullet, self).__init__()

        # Gives size of rectangle
        # self.image = p.Surface((20, 20))
        # self.image.fill((255, 255, 255))

        # Gives colour of rectangle
        self.image = game.loader.get_image('bullet')

        width, height = self.image.get_size()

        # gets the rectangle dimensions
        self.rect = self.image.get_rect()
        self.rect.topleft = (x - width // 2, y - height // 2)

        # This makes the velocity
        self.velocity = velocity

        self.bullet_life = 0

        self.game = game

        self.origin = origin

        self.shoot_cooldown = 0.2

        self.weapon = weapon

    def update(self, dt):
        # This is the x velocity
        self.rect.x += self.velocity.x * dt
        # This is the y velocity
        self.rect.y += self.velocity.y * dt

        # Put everything above this
        self.bullet_life += dt
        if self.bullet_life >= BULLET_LIFESPAN:
            # This removes the bullet from all sprites and stops updating
            self.game.all_sprites.remove(self)


class Player(p.sprite.Sprite):

    def __init__(self, x, y, is_player_one, game, player_direction=NORTH, current_num=0, can_jump=True, health=20):
        super(Player, self).__init__()

        # Gives image of rectangle
        self.image = game.loader.get_image("purple_player")

        # self.image = p.Surface((64, 64))
        # self.image.fill((255, 0, 0))

        # gets the rectangle dimensions
        self.rect = self.image.get_rect()

        # Tells us that the (x, y) is in the center
        self.rect.center = (x, y)

        # Movement attributes
        self.position = p.math.Vector2(self.rect.centerx, self.rect.centery)
        self.velocity = p.math.Vector2(0, 0)
        self.acceleration = p.math.Vector2(0, GRAVITY)

        self.is_player_one = is_player_one
        self.player_direction = p.math.Vector2(0, -1)

        self.current_num = current_num
        self.health = health

        self.game = game

        self.can_jump = can_jump
        self.jumps = 0
        self.jump_time = 0

        self.can_shoot = True
        self.shoot_time = 0
        self.weapon = Smg()

        self.can_dash = True
        self.dash_time = 0

        self.on_platform = False  # New flag
        self.powerups = {}

    def update(self, dt):
        if self.game.death:
            if self.game.timer < 2:
                self.game.timer += dt
            else:
                self.game.all_sprites.empty()
                self.game.all_sprites.add(self.game.player, self.game.player2)

            return
        self.inputs(dt)
        self.movement(dt)

        # When the player simply walks off the platform (without jumping) gravity does not occur. As it still thinks
        # it is on the platform So we need to tell it, it is not on the platform anymore.
        # Check if player is still on a platform

        # if self.on_platform:
        #     # Check if there's a platform directly below the player
        #     rect_below = self.rect.move(0, 1)  # Move the rect down by 1 pixel
        #     if not any(platform.rect.colliderect(rect_below) for platform in self.game.all_platforms):
        #         self.on_platform = False  # No platform below, so set on_platform to False

        self.object_collision(dt)
        self.clipping(dt)
        self.handle_flags(dt)

    def object_collision(self, dt):
        # Handle Bullet Collisions
        collided_bullets = p.sprite.spritecollide(self, self.game.bullet, False)

        for bullet in collided_bullets:
            if (self.is_player_one and not bullet.origin) or (not self.is_player_one and bullet.origin):
                self.health -= bullet.weapon.damage
                self.game.bullet.remove(bullet)
                self.game.all_sprites.remove(bullet)

            # Handle player death here
            if self.health <= 0:
                self.death(dt)

        # Handle powerup collisions
        collided_powerups = p.sprite.spritecollide(self, self.game.all_powerups, True)

        for powerup in collided_powerups:
            self.powerups[powerup.type] = powerup

    def clipping(self, dt):
        # Handle Screen Clipping
        if self.rect.right >= WIDTH:
            self.rect.left = 0
        elif self.rect.left < 0:
            self.rect.right = WIDTH

        if self.rect.top < 0:
            self.rect.top = 0

        self.position = self.rect.topleft

    def handle_flags(self, dt):
        # Manage Cooldowns and Flags
        if not self.can_jump:
            self.jump_time += dt
            if self.jump_time >= JUMP_COOLDOWN:
                self.can_jump = True
                self.jump_time = 0
                if self.jumps > MAX_JUMPS - 1:
                    self.can_jump = False

        if not self.can_shoot:
            self.shoot_time += dt
            powerup = self.powerups.get(POWERUP_COOLDOWN_TYPE)
            if powerup is None:
                x = 1
            else:
                x = powerup.cooldown_multiplier
            if self.shoot_time >= self.weapon.fire_rate * x:
                self.can_shoot = True
                self.shoot_time = 0

        # if not self.can_dash:
        #     self.dash_time += dt
        #     if self.dash_time >= DASH_COOLDOWN:
        #         self.can_dash = True
        #         self.dash_time = 0

        # This controls the powerup timer and removes the powerup once over
        for key, value in list(self.powerups.items()):
            if value.update(dt):
                self.powerups.pop(key)

    def inputs(self, dt):
        self.velocity += self.acceleration * dt

        # Apply Friction
        self.velocity.x *= FRICTION


        # Player Controls
        keys = p.key.get_pressed()
        mouse = p.mouse.get_pressed()

        # Handle Horizontal Movement
        self.player_direction.x = 0
        if (keys[p.K_d] and self.is_player_one) or (keys[p.K_RIGHT] and not self.is_player_one):
            self.velocity.x = PLAYER_SPEED
            self.player_direction.x = 1
            self.image = self.game.loader.get_image('purple_player_right')

        if (keys[p.K_a] and self.is_player_one) or (keys[p.K_LEFT] and not self.is_player_one):
            self.velocity.x = -PLAYER_SPEED
            self.player_direction.x = -1
            self.image = self.game.loader.get_image('purple_player_left')

        # Handle Vertical Movement (Jumping)
        self.player_direction.y = 0
        if self.can_jump and ((keys[p.K_w] and self.is_player_one) or (keys[p.K_UP] and not self.is_player_one)):
            self.can_jump = False
            self.velocity.y = -1400
            self.jumps += 1
            self.on_platform = False
            self.player_direction.y = 1

        # Handle Downward Movement
        if (keys[p.K_s] and self.is_player_one) or (keys[p.K_DOWN] and not self.is_player_one):
            self.velocity.y = 1400
            self.player_direction.y = - 1

        # Handle Shooting
        if self.can_shoot and ((keys[p.K_SPACE] and self.is_player_one) or (
                mouse[0] and not self.is_player_one)) and self.weapon.ammo > 0:
            self.can_shoot = False
            # If the player stays still they shoot up
            if self.player_direction.magnitude() == 0:
                self.player_direction.y = -1

            bullet_velocity = self.player_direction * BULLET_SPEED

            bullet = Bullet(self.rect.centerx, self.rect.centery, game=self.game, velocity=bullet_velocity,
                            origin=self.is_player_one, weapon=self.weapon)
            self.weapon.ammo -= 1

            self.game.all_sprites.add(bullet)
            self.game.bullet.add(bullet)

        if abs(self.velocity.x) < VELOCITY_THRESHOLD:
            self.velocity.x = 0

    def movement(self, dt):
        # Update Direction Based on Velocity

        self.collisions(dt)

        self.rect.topleft = self.position

    def collisions(self, dt):

        # Update Y position and handle vertical collisions
        self.position += self.velocity * dt + (0.5 * self.acceleration * (dt ** 2))

        self.rect.x = self.position.x
        collided_platform = p.sprite.spritecollide(self, self.game.all_platforms, dokill=False)

        for platform in collided_platform:
            if isinstance(platform, Lava_platform):
                self.health -= 0.001
                self.velocity.x /= 2

                break
            if self.velocity.x > 0:
                self.rect.right = platform.rect.left
                self.position.x = self.rect.left
                self.velocity.x = -1000 if isinstance(platform, Jump_platform) else 0

            elif self.velocity.x < 0:
                self.rect.left = platform.rect.right
                self.position.x = self.rect.left
                self.velocity.x = 1000 if isinstance(platform, Jump_platform) else 0
            break

        self.rect.y = self.position.y
        collided_platform = p.sprite.spritecollide(self, self.game.all_platforms, dokill=False)

        for platform in collided_platform:
            if isinstance(platform, Lava_platform):
                self.health -= 0.001
                self.velocity.y /= 2.5
                self.on_platform = False
                self.jumps = 0

                break

            else:
                if self.velocity.y > 0:
                    self.rect.bottom = platform.rect.top
                    self.position.y = self.rect.top

                    if isinstance(platform, Jump_platform):
                        self.can_jump = False
                        self.jumps = 2
                        self.jump_time = 0
                        self.velocity.y = -JUMP_AMOUNT_PLATFORM
                        self.on_platform = False

                    else:
                        self.can_jump = True
                        self.jumps = 0
                        self.jump_time = 0
                        self.velocity.y = 0
                        self.on_platform = True

                elif self.velocity.y < 0:
                    self.rect.top = platform.rect.bottom
                    self.position.y = self.rect.top
                    self.velocity.y = JUMP_AMOUNT_PLATFORM if isinstance(platform, Jump_platform) else 0
            break

    def death(self, dt):

        self.game.death = True

        self.image.fill((255, 0, 0))
