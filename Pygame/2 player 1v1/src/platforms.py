from config import *


class Platform(p.sprite.Sprite):

    def __init__(self, x, y, width, height, game):
        super(Platform, self).__init__()

        self.image = game.loader.get_image("default_platform_1")

        # self.image = p.Surface((width, height))
        # self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)


class Jump_platform(Platform):

    def __init__(self, x, y, width, height, game):
        super(Jump_platform, self).__init__(x, y, width, height, game)

        self.image = game.loader.get_image("jump_platform_1")

        #self.image = p.Surface((width, height))
        # self.image.fill((0, 0, 255))


class Weak_platform(Platform):

    def __init__(self, x, y, width, height, game):
        super(Weak_platform, self).__init__(x, y, width, height, game)

        self.image = game.loader.get_image("weak_platform_s0")
        # self.image = p.Surface((width, height))
        # self.image.fill((0, 255, 255))
        self.health = 5
        self.game = game

    def update(self, dt):
        bullet_collision = p.sprite.spritecollide(self, self.game.bullet, dokill=True)

        for bullet in bullet_collision:
            self.health -= 1

            if self.health == 4:
                self.image = self.game.loader.get_image('weak_platform_s1')
            elif self.health == 3:
                self.image = self.game.loader.get_image('weak_platform_s2')
            elif self.health == 2:
                self.image = self.game.loader.get_image('weak_platform_s3')
            elif self.health == 1:
                self.image = self.game.loader.get_image('weak_platform_s4')
            elif self.health <= 0:
                self.game.all_sprites.remove(self)
                self.game.all_platforms.remove(self)


class Lava_platform(Platform):
    def __init__(self, x, y, width, height, game):
        super(Lava_platform, self).__init__(x, y, width, height, game)

        self.image = p.Surface((192, 64))
        self.image.fill((255, 0, 0))
        self.game = game


