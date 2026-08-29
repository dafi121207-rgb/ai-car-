import os
import pygame
from car import Car
from tracks import TRACKS
from genetic import next_generation

HEADLESS = False  # Set True jika ingin latihan tanpa window GUI
POP_SIZE = 50
MUTATION_RATE = 0.1
WIDTH, HEIGHT = 800, 600

if HEADLESS:
    os.environ["SDL_VIDEODRIVER"] = "dummy"

pygame.init()
pygame.font.init()

screen = pygame.Surface((WIDTH, HEIGHT)) if HEADLESS else pygame.display.set_mode((WIDTH, HEIGHT))
if not HEADLESS:
    pygame.display.set_caption("AI Car Evolution - Modular Edition")

clock = pygame.time.Clock()
FONT = pygame.font.SysFont("Arial", 16)

def main():
    current_track_idx = 0
    active_track = TRACKS[current_track_idx]
    
    population = [Car(active_track["start"][0], active_track["start"][1], active_track["angle"]) for _ in range(POP_SIZE)]
    generation = 1
    sim_speed = 1
    running = True

    while running:
        if not HEADLESS:
            clock.tick(60)

        active_track["draw_func"](screen, WIDTH, HEIGHT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and not HEADLESS:
                if event.key == pygame.K_1: sim_speed = 1
                if event.key == pygame.K_2: sim_speed = 5
                if event.key == pygame.K_3: sim_speed = 10
                if event.key == pygame.K_4: sim_speed = 50

                if event.key == pygame.K_s:
                    best_car = max(population, key=lambda c: c.time_alive)
                    best_car.brain.save_to_file("best_brain.json")

                if event.key == pygame.K_l:
                    for car in population:
                        car.brain.load_from_file("best_brain.json")

                if event.key == pygame.K_t:
                    current_track_idx = (current_track_idx + 1) % len(TRACKS)
                    active_track = TRACKS[current_track_idx]
                    for car in population:
                        car.reset_for_track(active_track["start"], active_track["angle"])

        for _ in range(sim_speed):
            alive_count = 0
            for car in population:
                if car.alive:
                    car.think_and_drive(screen, WIDTH, HEIGHT, active_track.get("wall_type", "black"))
                    alive_count += 1
            if alive_count == 0:
                break

        if not HEADLESS:
            for car in population:
                car.draw(screen)

        if alive_count == 0:
            population = next_generation(population, POP_SIZE, MUTATION_RATE, active_track["start"], active_track["angle"])
            generation += 1

        if not HEADLESS:
            info_text = [
                f"Generasi: {generation} | Track: {active_track['name']}",
                f"Mobil Hidup: {alive_count}/{POP_SIZE} | Speed: {sim_speed}x",
                "[1-4] Speed  [T] Ganti Track  [S] Save AI  [L] Load AI"
            ]
            for i, text in enumerate(info_text):
                txt_surface = FONT.render(text, True, (255, 255, 255))
                screen.blit(txt_surface, (15, 15 + i * 20))

            pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()