class BaseWeapon:
    def __init__(self, fire_rate, ammo, damage):
        self.fire_rate = fire_rate
        self.ammo = ammo  # ammo means ammunition
        self.damage = damage
        # self.bullet_speed = bullet_speed  Use this if custom bullet speed is wanted
        # self.icon =   If images are wanted they can be added here using this


class Smg(BaseWeapon):
    def __init__(self):
        super().__init__(0.1, 30000000000, 1)


class Pistol(BaseWeapon):
    def __init__(self):
        super().__init__(2, 4, 5)


class Mp4(BaseWeapon):
    def __init__(self):
        super().__init__(0.05, 60, 0.2)


class GrenadeLauncher(BaseWeapon):
    def __init__(self):
        super().__init__(5, 1, 20)


class Railgun(BaseWeapon):
    def __init__(self):
        super().__init__(6, 4, 15)


class ____(BaseWeapon):
    def __init__(self):
        super().__init__(1.5, 4, 5)
