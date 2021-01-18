import pygame
import random
import math

class Entity():
    def updatePosition():
        pass

    def getInformation():
        pass

    def render(window):
        pass

class Avatar(Entity):
    colour = (235, 52, 52)
    radius = 20

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def updatePosition(self, move):
        self.y += move
        if self.y + self.radius < 0:
            self.y = 0

    def getInformation(self):
        return [self.x, self.y, self.radius]

    def render(self, window):
        pygame.draw.circle(window, self.colour, (self.x, self.y)
                                                    , self.radius, 0) 

class Obstacle(Entity):
    colour = (30, 179, 53)
    width = 50

    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

    def updatePosition(self, move):
        self.x -= move

    def getInformation(self):
        return [self.x, self.y, self.height, self.width, 
                                    self.height + 200]

    def render(self, win):
        w, h = pygame.display.get_surface().get_size()

        pygame.draw.rect(win, self.colour, (self.x, self.y,
                                     self.width, self.height), 0)

        pygame.draw.rect(win, self.colour, (self.x, 
        self.y + self.height + 200, self.width, h - self.height - 200), 0) 

class Button():
    def __init__(self, colour, function, x, y, width, height, text):
        self.colour = colour
        self.function = function
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def show(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y,
                                     self.width, self.height), 0)

        if self.text:
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                             self.y + (self.height/2 - text.get_height()/2))) 

    def isOver(self, pos, x):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.function(x)

class Listner():
    def change():
        pass

class EventMenager():
    def __init__(self):
        self.listeners = []

    def addSubscriber(self, subscriber, types):
        self.listeners.append([types, subscriber])

    def unsubscribe(self, subscriber, types):
        self.listeners.remove([types, subscriber])

    def notify(self, types):
        for i in self.listeners:
            if i[0] == types:
                if types == "new":
                    i[1].new()
                elif types == "end":
                    i[1].end()
                else:
                    i[1].change()

class Event():
    def __init__(self):
        self.events = EventMenager()

    def collision(self, a, o):
        if a[1] + a[2] >= 800:
            self.events.notify("collision")
            return 1
        if a[1] < o[2] + (200/2):
            if a[1] < o[2]:
                if abs(a[0] - o[0]) <= a[2]:
                    self.events.notify("collision")
                    return 1
            elif a[0] > o[0] and a[0] < o[0] + o[3]:
                if abs(a[1] - o[2]) <= a[2]:
                    self.events.notify("collision")
                    return 1
            else:
                if math.sqrt((a[0] - o[0])**2 + (a[1] - o[2])**2) <= a[2]:
                    self.events.notify("collision")
                    return 1
        else:
            if a[1] > o[2] + 200:
                if abs(a[0] - o[0]) <= a[2]:
                    self.events.notify("collision")
                    return 1
            elif a[0] > o[0] and a[0] < o[0] + o[3]:
                if abs(a[1] - (o[2] + 200)) <= a[2]:
                    self.events.notify("collision")
                    return 1
            else:
                if math.sqrt((a[0] - o[0])**2 + (a[1] - o[2] - 200)**2) <= a[2]:
                    self.events.notify("collision")
                    return 1
        return 0

    def score(self, a, o):
        if a[0] >= o[0] + (o[3] / 2):
            self.events.notify("score")
            return 1
        return 0

    def newGame(self):
        self.events.notify("new")

    def endGame(self):
        self.events.notify("end")

class Score(Listner):
    def __init__(self, x, y):
        self.score = 0
        self.x = x
        self.y = y
        self.got = True

    def change(self):
        self.score += 1
        self.got = True

    def show(self, win):
        font = pygame.font.SysFont('comicsans', 60)
        text = font.render(str(self.score), 1, (0,0,0))
        win.blit(text, (self.x, self.y))

class Game(Listner):
    def __init__(self, width, height):
        pygame.init()
        self.window = pygame.display.set_mode((width, height))
        self.gameOver = False
        self.endGame = False

    def loop(self, e):
        best = 0
        while not self.endGame:
            avatar = Avatar(50, 400)
            score = Score(0, 0)
            e.events.addSubscriber(score, "score")
            obstacles = []
            apart = 300
            current = 0
            scurrent = 0
            move = False
            sign = Button((159, 245, 242), lambda x: None,
                                    75, 380, 300, 60, "Wciśnij spację") 

            while not self.gameOver:
                if move:
                    avatar.updatePosition(0.75)

                    current += 0.5
                    if current >= apart:
                        r = random.randint(100, 500)
                        obstacles.append(Obstacle(400, 0, r))
                        current = 0

                for i in obstacles:
                    i.updatePosition(0.5)               

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    pressed = pygame.key.get_pressed()
                    if pressed[pygame.K_SPACE]:
                        move = True
                        avatar.updatePosition(-75)
                        
                
                self.window.fill((159, 245, 242))

                avatar.render(self.window)

                for i in obstacles:
                    i.render(self.window)

                score.show(self.window)

                if not move:
                    sign.show(self.window)

                pygame.display.update()

                if obstacles:
                    o = obstacles[0].getInformation()
                    if o[0] + 50 <= 0:
                        del obstacles[0]
                    ob = obstacles[0]
                    w = e.collision(avatar.getInformation(), ob.getInformation())

                    if not score.got:
                        w = e.score(avatar.getInformation(), ob.getInformation())
                    elif scurrent == apart:
                        scurrent = 0
                        score.got = False
                    else:
                        scurrent += 1

            now = score.score
            if now > best:
                best = now

            
            elements = [Button((255, 108, 3), lambda x: None,
                                    80, 50, 240, 60, "Koniec gry"),
                        Button((255, 108, 3), lambda x: None,
                                    20, 120, 140, 60, "Punkty"),
                        Button((255, 108, 3), lambda x: None,
                                    180, 120, 210, 60, "Najlepszy"),
                        Button((255, 108, 3), lambda x: None,
                                    55, 190, 70, 60, str(now)),
                        Button((255, 108, 3), lambda x: None,
                                    255, 190, 70, 60, str(best)),
                        Button((194, 21, 21), lambda x: x.newGame(),
                                    30, 300, 340, 100, "Zagraj ponownie"),
                        Button((194, 21, 21), lambda x: x.endGame(),
                                    70, 430, 260, 100, "Zakończ grę")]

            while self.gameOver:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for i in elements:
                            i.isOver(pos, e)

                self.window.fill((255, 137, 3))

                for i in elements:
                    i.show(self.window)

                pygame.display.update()
            
            elements.clear()
            e.events.unsubscribe(score, "score")

        pygame.quit()
        quit()

    def change(self):
        self.gameOver = True

    def end(self):
        self.endGame = True
        self.gameOver = False

    def new(self):
        self.gameOver = False