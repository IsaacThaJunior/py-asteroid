import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
import sys
from shot import Shot


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    new_time = pygame.time.Clock()
    dt = 0
    score = 0
    lives = 3
    font = pygame.font.Font(None, 36)

    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    asteroid_field = AsteroidField()
    # asteroid_field.spawn(20, pygame.Vector2(0, 0), pygame.Vector2(0, 0))

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    while True:
        log_state()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill("black")
        updatable.update(dt)
        for object in asteroids:
            for shot in shots:
                if shot.collides_with(object):
                    log_event("asteroid_hit")
                    object.split()
                    shot.kill()
                    score += 1
            if object.collides_with(player):
                log_event("player_hit")
                lives -= 1
                if lives == 0:
                    print("Game Over!")
                    score = 0
                    sys.exit()

                if lives > 0:
                    asteroids.empty()

                    # optionally respawn a fresh field
                    asteroid_field = AsteroidField()

                    # respawn player
                    player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.velocity = pygame.Vector2(0, 0)
                    shots.empty()
                    print(f"Lives left: {lives}")

        for sprite in drawable:
            sprite.draw(screen)
        for shot in shots:
            shot.draw(screen)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(score_text, text_rect)

        pygame.display.flip()

        new_time.tick(60)
        dt = new_time.get_time() / 1000  # Convert to seconds


if __name__ == "__main__":
    main()
