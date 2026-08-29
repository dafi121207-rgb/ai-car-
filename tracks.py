import pygame

# Pastikan warna WALL_COLOR di sini sama persis dengan warna dinding di gambar PNG
WALL_COLOR = (50, 50, 50) 

# Load gambar track (Pastikan file PNG ada di folder yang sama)
def load_track_image(filename, width=800, height=600):
    try:
        img = pygame.image.load(filename)
        return pygame.transform.scale(img, (width, height))
    except FileNotFoundError:
        print(f"[WARNING] File {filename} tidak ditemukan, menggunakan fallback.")
        return None

# Load gambar sirkuit
track_img_1 = load_track_image("track1.png")
track_img_2 = load_track_image("track2.png")

# Fungsi Render Menggunakan Gambar
def draw_png_track_1(surface, width=800, height=600):
    if track_img_1:
        surface.blit(track_img_1, (0, 0))
    else:
        surface.fill(WALL_COLOR) # Fallback jika gambar hilang

def draw_png_track_2(surface, width=800, height=600):
    if track_img_2:
        surface.blit(track_img_2, (0, 0))
    else:
        surface.fill(WALL_COLOR)

# Daftar Track dengan koordinat START khusus per sirkuit
TRACKS = [
    {"name": "PNG Track 1", "draw_func": draw_png_track_1, "start": (47, 497), "angle": 270, "wall_type": "red_black"},
    {"name": "PNG Track 2", "draw_func": draw_png_track_2, "start": (100, 500), "angle": -90, "wall_color": "black"}
]