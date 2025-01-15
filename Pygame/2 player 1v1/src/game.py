from platforms import *
from sprites import *
from weapons import *
from powerups import *
from config import *
import os

# rect stays at 976 then sometimes changes to 977 presumably since the acceleration and velocity is accumulating
#  and when the ut + 0.5xat^2 for the y axis is greater than 0.5 pygame rounds it to 977.

# WHEN ON TOP OF A PLATFORM STOP ADDING TO ACCELERATION

# for image in resources:
#     pygame.image.load(image)


# add time based movement
# add collision
# add sprites
# add ending
# other player collision -
# add gravity
# add border - teleportation
#  add double jumping
# add delay in shots
# TODO add gui - pygame_menu -- loadout -- main
# TODO maybe add a level editor - save levels to pc - destroy platform if shot too much - lava insta kill - crumbling platform over time
# TODO add coop mode - players vs ai
# add a way to go down quicker
# TODO add powerups and different guns. maybe loadout screen
# TODO Animated textures
# TODO sort out MESS of files
# add friction
# - RESEARCH (pygame.sprite.spritecollide(self, group, dokill)


RES_DIR = "..\\res"


class ResourceLoader:
    def __init__(self):
        self.resources = {}

        self._load()

    def _load(self):
        files = os.listdir(RES_DIR)
        files.sort()
        current = files[0]
        current_split_file = current.split('.')[0].split('_')
        current_res_type = '_'.join(current_split_file[:-1])  # Bullet empty as join has only 1 element
        temp = []
        for i, file in enumerate(files):  # Getcwd means get current working directory
            if i == 0:
                continue

            temp.append(current)

            split_file = file.split('_')
            res_type = '_'.join(split_file[:-1])

            if current_res_type != res_type:
                if len(temp) == 1:
                    self.resources[current_res_type] = p.image.load(os.path.join(RES_DIR, temp[0])).convert_alpha()
                    temp = []
                else:
                    self.resources[current_res_type] = [p.image.load(os.path.join(RES_DIR, x)).convert_alpha() for x in temp]
                    temp = []

            current_res_type = res_type
            current = file
            print(self.resources)

        temp.append(current)
        self.resources[current_res_type] = temp
        print(current, current_res_type)

        # exit()
        # if file.endswith('.png') or file.endswith('.gif'):
        # print(file.replace('.png', ''))   #OTHERS
        # print(file.split('.')[0])         #OTHERS
        # file_path = os.path.join(RES_DIR, file)
        # self.resources[file[:-4]] = p.image.load(file_path).convert_alpha()

    def get_resource(self, key):
        return self.resources.get(key)


class State:
    def __init__(self):
        self.prev_state = None
        self.current_state = None

    def add(self, new):
        self.prev_state = self.current_state

        self.current_state = new

    def update(self, dt):
        self.current_state.update(dt)

    def events(self):
        self.current_state.events()

    def draw(self, screen):
        self.current_state.draw(screen)


class Manager:
    def __init__(self, game):
        # Set up the display
        self.screen = SCREEN

        self.loader = ResourceLoader()

        # These are all the groups
        self.all_sprites = p.sprite.Group()
        self.all_platforms = p.sprite.Group()
        self.bullet = p.sprite.Group()
        self.all_powerups = p.sprite.Group()

        self._create_level_one()

        self.death = False

        self.game = game

    def _create_level_one(self):
        # These are the players
        # True is because boolean is being used up there, so we are using it here too
        self.player = Player(300, 1000, True, self)
        self.player2 = Player(1600, 1000, False, self)

        # These are the other objects
        platform = GrassPlatform(0, 1040, 192, 64, self)
        platform1 = GrassPlatform(190, 1040, 192, 64, self)
        platform2 = GrassPlatform(380, 1040, 192, 64, self)
        platform3 = GrassPlatform(570, 1040, 192, 64, self)
        #platform4 = GrassPlatform(760, 1040, 192, 64, self)
        platform5 = GrassPlatform(950, 1040, 192, 64, self)
        platform6 = GrassPlatform(1140, 1040, 192, 64, self)
        platform7 = GrassPlatform(1330, 1040, 192, 64, self)
        platform8 = GrassPlatform(1520, 1040, 192, 64, self)
        platform9 = GrassPlatform(1710, 1040, 192, 64, self)
        platform10 = GrassPlatform(1900, 1040, 192, 64, self)

        # bouncy platforms
        jump_platform = Jump_platform(1000, 600, self)

        # weak platforms
        weak_platform = Weak_platform(1500, 300, 192, 64, self)
        weak_platform1 = Weak_platform(1310, 300, 192, 64, self)
        weak_platform2 = Weak_platform(1120, 300, 192, 64, self)

        # Lava platforms
        lava_platform = Lava_platform(760, 1040, 192, 64, self)

        # Powerups
        fastershoot = Fastshoot(1000, 300, self)
        print(type(fastershoot))

        # END OF LEVEL 1
        #####################################

        # These add the sprites to the groups
        self.all_sprites.add(self.player, self.player2, platform, platform1, platform2, platform3, platform5,
                             platform6, platform7, platform8, platform9, platform10, jump_platform, weak_platform,
                             weak_platform1, weak_platform2, lava_platform, fastershoot)

        self.all_platforms.add(platform, platform1, platform2, platform3, platform5, platform6, platform7,
                               platform8, platform9, platform10, jump_platform, weak_platform, weak_platform1,
                               weak_platform2, lava_platform)

        self.all_powerups.add(fastershoot)

    def update(self, dt):
        self.all_sprites.update(dt)

        if self.death:
            self.game.state.add(GameOver())

    def draw(self, screen):
        self.all_sprites.draw(screen)

    def events(self):
        pass


class Game:
    def __init__(self):

        # This creates the clock
        self.clock = p.time.Clock()

        # This is dt
        self.accumulator = 0.0
        self.time_step = 1 / TARGET_FPS

        self.state = State()
        self.state.add(Manager(self))

        self.timer = 0

    def run(self):
        # This makes the below continuously repeat until quit
        running = True
        while running:
            # This limits the computer's fps to 60
            dt = self.clock.tick() / 1000

            self.events()

            # This lets you close the screen when x is pressed
            for event in p.event.get():
                if event.type == p.QUIT:
                    running = False
                # This lets you close the screen when ESCAPE is pressed
                if event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        running = False

            self.accumulator += dt
            while self.accumulator >= self.time_step:
                self.update(self.time_step)
                self.accumulator -= self.time_step

            self.draw(SCREEN)

    def update(self, dt):
        self.state.update(dt)

    def events(self):
        self.state.events()

    def draw(self, screen):
        screen.fill((0, 0, 0))
        self.state.draw(screen)
        p.display.update()


class GameOver:
    @staticmethod
    def draw(screen):
        font = p.font.SysFont('Arial', 50, True)
        text_surface = font.render('Game Over LOLOLOLOL!!!!', True, (155, 0, 0))

        screen.blit(text_surface, (WIDTH / 2, HEIGHT / 2))

    @staticmethod
    def events():
        if p.key.get_pressed()[p.K_q]:
            exit()

    def update(self, dt):
        pass


if __name__ == "__main__":
    g = Game()
    g.run()
