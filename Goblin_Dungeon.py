import pygame
pygame.init()
print(Start)

win = pygame.display.set_mode((600,390))

pygame.display.set_caption("First Game")

walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('dungeon.jpg')
char = pygame.image.load('standing.png')

clock = pygame.time.Clock()

bulletSound=pygame.mixer.Sound('bullet.wav')
hitSound=pygame.mixer.Sound('hit.wav')
music=pygame.mixer.Sound('music.wav')
music.set_volume(0.3)
music.play(-1)

class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.standing = True
        self.hitbox=(self.x+20,self.y+12,24,50)
        self.alive=True

    def draw(self, win):
        if self.walkCount== 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount +=1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        self.hitbox=(self.x+20,self.y+12,24,50)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def hit(self):
        self.alive=False
        Font=pygame.font.SysFont('comicsans',100,True)
        Font2=pygame.font.SysFont('comicsans',40)
        text2=Font2.render('Press Enter to restart', 1 , (255,0,0))
        text=Font.render('GAME OVER', 1, (255,255,255))
        win.blit(text,(250-(text.get_width()/2),100))
        win.blit(text2,(250-(text.get_width()/2),200))
        pygame.display.update()
        while not self.alive:
            pygame.time.delay(10)
            key=pygame.key.get_pressed()
            if key[pygame.K_RETURN]:
                restart()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    dead=False
                    pygame.quit()



class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing

    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    def __init__(self,x,y,height,width,end):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.end=end
        self.path=[0,self.end]
        self.walkCount=0
        self.vel=3 
        self.hitbox=(self.x+17,self.y+2,28,57)
        self.hitNumber=0
        self.levelupScore = 10

    def draw(self,win):
        self.move()
        if self.walkCount==33:
            self.walkCount=0
        if self.vel > 0:
            win.blit(self.walkRight[self.walkCount//3],(self.x,self.y))
            self.walkCount += 1
        else:
             win.blit(self.walkLeft[self.walkCount//3],(self.x,self.y))
             self.walkCount += 1
        if self.vel > 0:
            self.hitbox=(self.x+15,self.y+2,25,57)
        else:
            self.hitbox=(self.x+25,self.y+2,25,57)

        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

    def move(self):
        if self.vel>0:
            if (self.x+self.vel)<self.path[1]:
                self.x+=self.vel
            else:
                self.vel=self.vel * -1
                self.walkcount=0
        else:
            if self.x-self.vel>self.path[0]:
                self.x += self.vel
            else:
                self.vel=self.vel * -1
                self.walkcount=0

    def hit(self):
        self.hitNumber+=1
        if self.hitNumber==self.levelupScore:
            self.levelupScore += 10
            if self.vel > 0:   
                self.vel += 2
            else:
                self.vel -= 2   
                             
def start():
    global run
    start=True
    while start:
        clock.tick(27)
        win.blit(bg,(0,0))
        font=pygame.font.SysFont('comicsans',80)
        text=font.render('Goblin Dungeon', 1, (255,255,255))
        win.blit(text,(100,20))
        font2=pygame.font.SysFont('comicsans',40)
        text2=font2.render('Press Enter to start', 1, (255,0,0))  
        win.blit(text2,(200,350)) 
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                break
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            run=True
            return
            
def redrawGameWindow():
    score=goblin.hitNumber + goblin2.hitNumber
    Font=pygame.font.SysFont('comicsans',30,True)
    text=Font.render("Score: "+ str(score),1,(255,255,255))
    win.blit(bg, (0,0))
    win.blit(text,(450,10))
    man.draw(win)
    goblin.draw(win)
    goblin2.draw(win)

    for bullet in bullets:
        bullet.draw(win)
    
    pygame.display.update()

def restart():
    man.alive = True
    man.x = 250
    goblin.x, goblin.vel, goblin.hitNumber = 0, 3 , 0
    goblin2.x, goblin2.vel, goblin2.hitNumber = 400, 3, 0



#mainloop
man = player(250, 230, 64,64)
goblin=enemy(0,230,64,64,550)
goblin2=enemy(400,230,64,64,550)
shootDelay=0
bullets = []
run = False
start()
while run:
    clock.tick(27)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    if man.hitbox[1]<goblin.hitbox[1]+goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3]>goblin.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
            man.hit()

    if man.hitbox[1]<goblin2.hitbox[1]+goblin2.hitbox[3] and man.hitbox[1] + man.hitbox[3]>goblin2.hitbox[1]:
        if man.hitbox[0] + man.hitbox[2] > goblin2.hitbox[0] and man.hitbox[0] < goblin2.hitbox[0] + goblin2.hitbox[2]:
            man.hit()

    for bullet in bullets:
        if bullet.y-bullet.radius>=goblin.hitbox[1] and bullet.y+bullet.radius<goblin.hitbox[1]+goblin.hitbox[3]:
            if bullet.x+bullet.radius>goblin.hitbox[0] and bullet.x-bullet.radius<goblin.hitbox[0]+goblin.hitbox[2]:
                goblin.hit()
                hitSound.play()
                bullets.remove(bullet)
                print("Goblin1- ",goblin.hitNumber, "vel = ", goblin.vel)


            elif bullet.y-bullet.radius>=goblin2.hitbox[1] and bullet.y+bullet.radius<goblin2.hitbox[1]+goblin2.hitbox[3]:
                if bullet.x+bullet.radius>goblin2.hitbox[0] and bullet.x-bullet.radius<goblin2.hitbox[0]+goblin2.hitbox[2]:
                    goblin2.hit()
                    hitSound.play()
                    bullets.remove(bullet)
                    print("Goblin2- ",goblin2.hitNumber, " vel = ", goblin2.vel)

        if bullet.x < 600 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.remove(bullet)
    
    keys = pygame.key.get_pressed()
    
    if man.alive:
        if shootDelay>0:
            shootDelay+=1
        if shootDelay==5:
            shootDelay=0

        if keys[pygame.K_SPACE] and shootDelay==0:
            bulletSound.play()
        
            if man.left:
                facing = -1
            else:
                facing = 1
            
            if len(bullets) < 5:
                bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height//2), 5, (0,0,255), facing))
                shootDelay+=1
    
        if keys[pygame.K_LEFT] and man.x > man.vel:
            man.x -= man.vel
            man.left = True
            man.right = False
            man.standing = False
        elif keys[pygame.K_RIGHT] and man.x < 620 - man.width - man.vel:
            man.x += man.vel
            man.right = True
            man.left = False
            man.standing = False
        else:
            man.standing = True
            man.walkCount = 0
            
        if not(man.isJump):
            if keys[pygame.K_UP]:
                man.isJump = True
                
                man.walkCount = 0
        else:
            if man.jumpCount >= -10:
                neg = 1
                if man.jumpCount < 0:
                    neg = -1
                man.y -= (man.jumpCount ** 2) * 0.3 * neg
                man.jumpCount -= 1
            else:
                man.isJump = False
                man.jumpCount = 10
    if not man.alive:
        man.standing=True
        

    redrawGameWindow()

pygame.quit()


