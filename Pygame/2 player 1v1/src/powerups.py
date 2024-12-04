from config import *
#from sprites import AnimatedSprite

POWERUP_COOLDOWN_TYPE = 0


class BasePowerup(p.sprite.Sprite):
    def __init__(self, x, y, game):
        super(BasePowerup, self).__init__()  #FIXME

        self.image = game.loader.get_image('fastshoot_1')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.game = game
        self.type = None
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= POWERUP_TIME:
            return True

        return False


class Fastshoot(BasePowerup):
    def __init__(self, x, y, game):
        super(Fastshoot, self).__init__(x, y, game)

        self.cooldown_multiplier = 0.5
        self.type = POWERUP_COOLDOWN_TYPE
