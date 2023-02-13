import pygame
import time
import random


def head_movement(direction, x, y):
    x_add = 0
    y_add = 0
    if direction == "up" and y > 0:
        y_add = -20
    elif direction == "down" and y < 480:
        y_add = 20
    elif direction == "right" and x < 480:
        x_add = 20
    elif direction == "left" and x > 0:
        x_add = -20

    return (x + x_add), (y + y_add)


def module_key_check(key, direction):
    if key == 1073741904:
        direction = "left"
    if key == 1073741903:
        direction = "right"
    if key == 1073741906:
        direction = "up"
    if key == 1073741905:
        direction = "down"

    return direction


class Block(pygame.sprite.Sprite):

    def __init__(self, x, y, direction, number):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 20, 20)
        self.direction = direction
        self.rect.x = x
        self.rect.y = y
        self.number = number


class Food(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.rect.x = x
        self.rect.y = y

    def delete_food(self):
        self.kill()


class Game:

    def __init__(self):
        pygame.init()
        # pygame.font.init()
        self.snake = pygame.sprite.Group()
        self.snakeArray = []
        self.screen = pygame.display.set_mode((500, 500))
        self.head = Block(240, 240, "right", 0)
        self.food = Food((20 * random.randint(0, 24) + 5),
                         (20 * random.randint(0, 24) + 5))
        self.snake.add(self.head)
        self.snakeArray.append(self.head)
        self.font = pygame.font.Font(None, 36)
        self.number = 0
        # noinspection PyTypeChecker
        self.textImg = self.font.render("Loading...", 1, (0, 0, 0))

    def main(self):

        done = False
        clock = pygame.time.Clock()

        while not done:

            death_collisions = pygame.sprite.spritecollide(self.head, self.snake, False)
            #    print(death_collisions)
            if len(death_collisions) > 1:
                done = True

            eat_collisions = pygame.sprite.collide_rect(self.head, self.food)
            if eat_collisions:  # == True
                self.food.kill()
                self.food = Food((20 * random.randint(0, 24) + 5), (20 * random.randint(0, 24) + 5))
                new_block = Block(self.snakeArray[self.number].rect.x, self.snakeArray[self.number].rect.y,
                                  self.snake, self.number + 1)

                self.snakeArray.append(new_block)
                self.snake.add(new_block)  # potentially unneeded
                self.number += 1

            for event in pygame.event.get():  # Check for an event (mouse click, key press)

                if event.type == pygame.QUIT:  # If user clicked close window
                    done = True  # Flag that we are done so we exit this loop
                if event.type == pygame.KEYDOWN:

                    self.head.direction = module_key_check(event.key, self.head.direction)
                    print(self.head.direction)

            self.screen.fill((230, 230, 230))
            print(len(self.snakeArray))

            for index in range(len(self.snakeArray) - 1, 0, -1):

                self.snakeArray[index].rect.x = self.snakeArray[index - 1].rect.x
                self.snakeArray[index].rect.y = self.snakeArray[index - 1].rect.y

                # calculate new head coordinates after movement
            self.head.rect.x, self.head.rect.y = head_movement(self.head.direction, self.head.rect.x, self.head.rect.y)

            for blocks in self.snake:
                pygame.draw.rect(self.screen, (0, 0, 0), blocks)

            self.textImg = self.font.render(str(self.number), 1, (0, 0, 0))
            self.screen.blit(self.textImg, (10, 10))
            pygame.draw.rect(self.screen, (0, 0, 0), self.food.rect)
            pygame.display.flip()
            time.sleep(0.075)
            clock.tick(10)

    def post_game(self):
        #  clock = pygame.time.Clock()
        #  done = False

        #  while not done:
        self.screen.fill((230, 230, 230))

        pygame.display.flip()
        #   time.sleep(0.075)
        #   clock.tick(12)
        print("Score: " + str(self.number))
        name = input("Name: ")
        scores_file = open("scores.txt", "a")
        scores_file.write(str(name) + ", " + str(self.number) + "\n")
        scores_file.close()


game = Game()
game.main()
game.post_game()
