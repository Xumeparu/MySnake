import pygame
import sys
import random
import time


class Game:
    def __init__(self):
        self.screenWidth = 600
        self.screenHeight = 400

        self.white = pygame.Color(255, 255, 255)
        self.black = pygame.Color(0, 0, 0)
        self.red = pygame.Color(157, 32, 67)
        self.orange = pygame.Color(214, 99, 48)
        self.yellow = pygame.Color(216, 183, 46)
        self.green = pygame.Color(23, 135, 77)
        self.foodColor = self.FoodColor()

        self.clock = pygame.time.Clock()

        self.score = 0

    def SetDisplayAndTitle(self):
        # Задаем игровое поле и заголовок окна
        self.playingDisplay = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        pygame.display.set_caption('Snake')

    @staticmethod
    def EventsLoop(changeTo):
        # Отслеживание клавиш
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    changeTo = "RIGHT"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    changeTo = "LEFT"
                elif event.key == pygame.K_UP or event.key == ord('w'):
                    changeTo = "UP"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    changeTo = "DOWN"
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        return changeTo

    @staticmethod
    def UpdateDisplay():
        pygame.display.flip()
        game.clock.tick(20)

    def ShowScore(self, show=1):
        scoreFont = pygame.font.Font('fonts/contra.ttf', 20)
        scoreOnDisplay = scoreFont.render('Your score: {0}'.format(self.score), True, self.white)
        showScore = scoreOnDisplay.get_rect()

        if show == 1:
            showScore.midtop = (150, 10)
        else:
            showScore.midtop = (300, 220)

        self.playingDisplay.blit(scoreOnDisplay, showScore)

    def GameOver(self):
        # Функция для вывода надписи Game Over, результата и выход из игры
        gameoverFont = pygame.font.Font('fonts/contra.ttf', 50)
        gameoverDraw = gameoverFont.render('Game over', True, self.white)
        gameoverShow = gameoverDraw.get_rect()
        gameoverShow.midtop = (300, 130)
        self.playingDisplay.blit(gameoverDraw, gameoverShow)
        self.ShowScore(0)
        pygame.display.flip()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    def FoodColor(self):
        self.count = random.randint(0, 2)

        if self.count == 0:
            self.foodColor = pygame.Color(157, 32, 67)
        elif self.count == 1:
            self.foodColor = pygame.Color(216, 183, 46)
        else:
            self.foodColor = pygame.Color(216, 183, 46)

        return self.foodColor


class Snake:
    def __init__(self):
        self.snakeHeadPosition = [300, 200]
        self.snakeBody = [[300, 200]]
        self.snakeColor = game.green
        self.direction = "0"
        self.changeTo = self.direction

    def ChangeDirection(self):
        if any((self.changeTo == "RIGHT" and not self.direction == "LEFT",
                self.changeTo == "LEFT" and not self.direction == "RIGHT",
                self.changeTo == "UP" and not self.direction == "DOWN",
                self.changeTo == "DOWN" and not self.direction == "UP")):
            self.direction = self.changeTo

    def ChangeSnakeHeadPosition(self):
        if self.direction == "RIGHT":
            self.snakeHeadPosition[0] += 10
        elif self.direction == "LEFT":
            self.snakeHeadPosition[0] -= 10
        elif self.direction == "UP":
            self.snakeHeadPosition[1] -= 10
        elif self.direction == "DOWN":
            self.snakeHeadPosition[1] += 10

    def SnakeBodyMechanism(self):
        self.snakeBody.insert(0, list(self.snakeHeadPosition))

        if self.snakeHeadPosition[0] == food.foodPosition[0] and self.snakeHeadPosition[1] == food.foodPosition[1]:
            food.foodPosition = [random.randrange(1, game.screenWidth / 10) * 10,
                                 random.randrange(1, game.screenHeight / 10) * 10]
            game.score += 1
        else:
            self.snakeBody.pop()
        return game.score, food.foodPosition

    def DrawSnake(self):
        # Отображение всех сегментов змеи
        self.back = pygame.image.load('images/background.png').convert()
        self.back = pygame.transform.scale(self.back, (game.screenWidth, game.screenHeight))
        self.backRect = self.back.get_rect()

        game.playingDisplay.blit(self.back, self.backRect)
        for position in self.snakeBody:
            pygame.draw.rect(
                game.playingDisplay, self.snakeColor, pygame.Rect(
                    position[0], position[1], 10, 10))

    def CollisionsChecking(self):
        # Проверка на столкновение змеи с полями или со своими сегментами
        if any((self.snakeHeadPosition[0] > game.screenWidth - 10
                or self.snakeHeadPosition[0] < 0,
                self.snakeHeadPosition[1] > game.screenHeight - 10
                or self.snakeHeadPosition[1] < 0)):
            game.GameOver()

        for block in self.snakeBody[1:]:
            if block[0] == self.snakeHeadPosition[0] and block[1] == self.snakeHeadPosition[1]:
                game.GameOver()


class Food:
    def __init__(self):
        self.foodColor = game.FoodColor()
        self.foodSizeByX = 10
        self.foodSizeByY = 10
        self.foodPosition = [random.randrange(1, game.screenWidth / 10) * 10,
                             random.randrange(1, game.screenHeight / 10) * 10]

    def DrawFood(self):
        pygame.draw.rect(
            game.playingDisplay, self.foodColor, pygame.Rect(
                self.foodPosition[0], self.foodPosition[1],
                self.foodSizeByX, self.foodSizeByY))


pygame.init()

game = Game()
snake = Snake()
food = Food()

game.SetDisplayAndTitle()

while True:
    snake.changeTo = game.EventsLoop(snake.changeTo)

    snake.ChangeDirection()
    snake.ChangeSnakeHeadPosition()
    game.score, food.foodPosition = snake.SnakeBodyMechanism()
    snake.DrawSnake()

    food.DrawFood()

    snake.CollisionsChecking()

    game.ShowScore()
    game.UpdateDisplay()
