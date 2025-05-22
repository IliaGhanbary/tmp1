import pygame
import os
from os.path import join

#motaghayera sabet #Ilia
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 10
BULLET_COOLDOWN = 15

class Entity(pygame.sprite.Sprite):
    #class base bray hame mojoodat bazi #Ilia
    
    def __init__(self, x, y, width, height, color, name=None):
        #x , y mokhtasatan (x_pos,y_pos)
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)  # mostatil hitbox
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)  # namayesh
        self.image.fill(color)
        self.mask = pygame.mask.from_surface(self.image)  # masky ke bray collision bayad estefade beshe
        self.name = name
        self.hit = False 

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class NPC(Entity):#class npc bray bot ha ya kolan age npc doost ya doshman baadan dashtim felan faz 1 goft enemy sabet #Ilia
    COLOR = (0, 0, 0) #meshky
    
    def __init__(self, x, y, width, height, name=None):
        super().__init__(x, y, width, height, self.COLOR, name)
        self.hp = 100  #hp hamoon salamatiye

    def draw(self, window):
        if self.hp > 0:
            super().draw(window)
        else:
            self.kill()

class Gun(Entity): #class gun ro bra baad ke assetaro bedan neveshtam felan kari bash nadarim #Ilia
    COLOR = (0, 0, 0)
    
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, self.COLOR)

class Bullet(Entity):# class tir ke shelik mishe #Ilia
    COLOR = (255, 255, 0)  #zard
    
    def __init__(self, x, y, width, height, direction):
        super().__init__(x, y, width, height, self.COLOR)
        self.direction = direction
        self.speed = BULLET_SPEED
        self.lifetime = FPS * 3  # tir baad 3 saniye az bein mire 

    #def update(self):
        #Amir hossein
        #too oon samty ke player istade shelik kon va lifetime ham dar nazar begir
        

class Player(Entity):#Ilia
    COLOR = (255, 0, 0)  # ghermez
    #GRAVITY = 1
    #MAX_JUMP_COUNT = 1  bray baad age double jump dashtim

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, self.COLOR)
        self.hp = 200
        self.x_speed = 0
        self.y_speed = 0
        self.direction = "left"
        self.fall_count = 0
        self.jump_count = 0
        self.hit_count = 0
        self.bullets = pygame.sprite.Group()#tir hay faal ro donbal mikone
        self.shoot_cooldown = 0

    #def shoot(self):
    #Amirhossein
    #bar asas moghiet player shru harkat tiro hesab kon cooldown yadet nare

    #def jump(self):
     #Amirhossein   

    #def move(self, dx, dy):
        #Amirhossein

    #def move_left(self, speed):
        #Amirhossein

    #def move_right(self, speed):
        #Amirhossein

    #def landed(self):
        #Amirhossein
        #vizhegy ha paresh va oftadano reset kon   

    #def hit_head(self):
        #Amirhossein
        #vizhegy hayee ke bayad taghir bedy vaghty az bala barkhord darim

    #def loop(self, fps):
        #Amirhossein
        #vazeiat playero too har frame update kon 
        #ino ezafe kon tahesh
        #self.bullets.update()

    #def draw(self, window):
        #Amirhossein
        #ino ezafe kon tahesh
        #for bullet in self.bullets:
            #bullet.draw(window)

class Object(Entity):#class ashya #Ilia bray baad age bejoz platform chizi dashtim

    def __init__(self, x, y, width, height, name=None):
        super().__init__(x, y, width, height, (0, 0, 255), name)

class Platform(Object):#Ilia
    
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = Game().get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Game:#class asli bazi ke toosh main vojood dare #Ilia
    
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("brawlforge")
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()  #bray control frame rate
        
    def get_block(self, size):#bray vaghty ke assetaro midan bezarim too in file felan ye aks sade sabz gozashtam

        path = join("assets", "Terrain", "Terrain.jpg")
        image = pygame.image.load(path).convert_alpha()
        surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(96, 0, size, size)
        surface.blit(image, (0, 0), rect)
        return pygame.transform.scale2x(surface)

    def get_background(self, name):#inam mesl ghably
        image = pygame.image.load(join("assets", "background", name))
        _, _, width, height = image.get_rect()
        tiles = []

        for i in range(SCREEN_WIDTH // width + 1):
            for j in range(SCREEN_HEIGHT // height + 1):
                pos = (i * width, j * height)
                tiles.append(pos)

        return tiles, image

    def draw(self, background, background_image, player, objects, platforms, npcs):
        for tile in background:
            self.window.blit(background_image, tile)

        for obj in platforms:
            obj.draw(self.window)

        for obj in objects:
            obj.draw(self.window)

        for npc in npcs:
            if npc.hp > 0:
                npc.draw(self.window)

        player.draw(self.window)

        pygame.display.update()

    #def handle_vertical_collision(self, player, objects, platforms, npcs, dy):
        #Armita
        #dy meghdar taghirat amoodye
        
           
        # Check kon barkhord ba objecta 
        # Check kon barkhord ba platforma 
        # Check kon barkhord ba npc ha 

        #tahesh list obj hayee ke barkhord darano return kon
        #az barkhord mask ha estefade kon

    #def collide(self, player, objects, platforms, npcs, dx):
        #Armita
        #in bra check kardan barkhord ofoghie aval ja be ja kon bar asas dx baad collide mask ro check kon   
        #akharesh bayad ye object ro return kony oony ke bash barkhord dare
         
    #def handle_bullet_collisions(self, player, objects, platforms, npcs):
        #Armita
        #age be platform ya objecty bokhore serfan az bein mire age bokhore be npc bayad ye meghdary az joonesh kam she   

    #def handle_movement(self, player, objects, platforms, npcs):
        #Amirhossein
        #bar asas voroodya playero harkat bede
        #ino ezafe kon tahesh
        #self.handle_vertical_collision(player, objects, platforms, npcs, player.y_speed)

    def main(self):#Halghe asli bazi  #Ilia
        background, background_image = self.get_background("bg.jpg")

        player = Player(100, 100, 50, 50)
        block_size = 96
        #ina random hastan age khastin taghir bedin
        platforms = [
            Platform(300, 400, block_size),
            Platform(500, 300, block_size),
            Platform(200, 200, block_size),
            Platform(600, 400, block_size),
            Platform(100, 300, block_size)
        ]
        
        enemies = [NPC(500, 450, 50, 50, "demon")]
        
        floor = [Platform(i * block_size, SCREEN_HEIGHT - block_size, block_size) 
                 for i in range(-SCREEN_WIDTH // block_size, (SCREEN_WIDTH * 2) // block_size)]

        run = True
        while run:
            self.clock.tick(FPS)  # handle kardan fps
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and player.jump_count < 1:
                        player.jump()

            # update kardan vazeiat bazy
            player.loop(FPS)
            self.handle_movement(player, floor, platforms, enemies)
            self.handle_bullet_collisions(player, floor, platforms, enemies)
            
            #in bra ine age enemy ei mord dige too list hesab nashe
            enemies = [npc for npc in enemies if npc.hp > 0]
            
            self.draw(background, background_image, player, floor, platforms, enemies)
        
        pygame.quit()
        quit()

if __name__ == "__main__":
    game = Game()
    game.main()
