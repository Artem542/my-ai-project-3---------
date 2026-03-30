import pygame
import sys

from game.constants import *
from game.snake import Snake
from game.food import Food


def draw_grid(screen):
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))


def draw_snake(screen, snake: Snake):
    for pos in snake.positions:
        rect = pygame.Rect(
            pos.x * GRID_SIZE, pos.y * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2
        )
        pygame.draw.rect(screen, GREEN, rect)


def draw_food(screen, food: Food):
    rect = pygame.Rect(
        food.position.x * GRID_SIZE,
        food.position.y * GRID_SIZE,
        GRID_SIZE - 2,
        GRID_SIZE - 2,
    )
    pygame.draw.rect(screen, RED, rect)


def draw_score(screen, score: int):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def draw_game_over(screen, score: int):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font(None, 72)
    text = font.render("GAME OVER", True, RED)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
    screen.blit(score_text, score_rect)

    restart_text = font.render("Press R to restart, Q to quit", True, WHITE)
    restart_rect = restart_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
    )
    screen.blit(restart_text, restart_rect)


def main():
    pygame.init()
    SCREEN_WIDTH = GRID_WIDTH * GRID_SIZE
    SCREEN_HEIGHT = GRID_HEIGHT * GRID_SIZE
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()

    snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
    food = Food()
    food.respawn(snake.positions, GRID_WIDTH, GRID_HEIGHT)

    score = 0
    game_over = False
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        snake.change_direction(pygame.Vector2(0, -1))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        snake.change_direction(pygame.Vector2(0, 1))
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        snake.change_direction(pygame.Vector2(-1, 0))
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        snake.change_direction(pygame.Vector2(1, 0))
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        snake = Snake(GRID_WIDTH // 2, GRID_HEIGHT // 2)
                        food.respawn(snake.positions, GRID_WIDTH, GRID_HEIGHT)
                        score = 0
                        game_over = False
                    elif event.key == pygame.K_q:
                        running = False

        if not game_over:
            snake.move()

            if snake.head == food.position:
                snake.grow()
                score += 1
                food.respawn(snake.positions, GRID_WIDTH, GRID_HEIGHT)

            if snake.check_collision(GRID_WIDTH, GRID_HEIGHT):
                game_over = True

        screen.fill(BLACK)
        draw_grid(screen)
        draw_food(screen, food)
        draw_snake(screen, snake)
        draw_score(screen, score)

        if game_over:
            draw_game_over(screen, score)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()