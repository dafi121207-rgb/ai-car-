import pygame

# Warna UI
PANEL_BG = (20, 24, 33)
CARD_BG = (30, 36, 48)
TEXT_COLOR = (220, 220, 220)
NODE_COLOR = (100, 200, 255)
LINE_POS = (255, 80, 80)    # Garis merah untuk bobot positif
LINE_NEG = (80, 255, 120)   # Garis hijau untuk bobot negatif

def draw_sidebar(surface, population, generation, active_track_name, sim_speed, start_x=800, width=300, height=600):
    # 1. Gambar Background Panel Kanan
    pygame.draw.rect(surface, PANEL_BG, (start_x, 0, width, height))
    pygame.draw.line(surface, (50, 60, 80), (start_x, 0), (start_x, height), 2)

    font_title = pygame.font.SysFont("Arial", 18, bold=True)
    font_body = pygame.font.SysFont("Arial", 14)

    # 2. Kotak Telemetri / Stats
    pygame.draw.rect(surface, CARD_BG, (start_x + 15, 15, width - 30, 110), border_radius=8)
    
    best_car = max(population, key=lambda c: c.time_alive)
    alive_count = sum(1 for c in population if c.alive)

    stats = [
        f"GENERASI: {generation}",
        f"Track: {active_track_name}",
        f"Mobil Hidup: {alive_count}/{len(population)}",
        f"Speed: {sim_speed}x | Score Terbaik: {best_car.time_alive}"
    ]
    for i, txt in enumerate(stats):
        color = (255, 200, 80) if i == 0 else TEXT_COLOR
        font = font_title if i == 0 else font_body
        txt_surf = font.render(txt, True, color)
        surface.blit(txt_surf, (start_x + 25, 25 + i * 22))

    # 3. Visualisasi Otak AI (Neural Network Diagram)
    pygame.draw.rect(surface, CARD_BG, (start_x + 15, 145, width - 30, 435), border_radius=8)
    txt_nn = font_title.render("NEURAL NETWORK (BEST)", True, TEXT_COLOR)
    surface.blit(txt_nn, (start_x + 25, 155))

    # Gambar diagram node & garis weights jika ada mobil jagoan
    draw_network_diagram(surface, best_car.brain, start_x + 30, 200, width - 60, 360)


def draw_network_diagram(surface, brain, x, y, w, h):
    # Posisi Layer: Input (7 node), Hidden 1 (12 node), Hidden 2 (12 node), Output (1 node)
    layers = [7, 12, 12, 1]
    layer_x = [x + int(i * (w / (len(layers) - 1))) for i in range(len(layers))]

    act_inputs = getattr(brain, 'last_inputs', [0.5]*7)
    act_hidden1 = getattr(brain, 'last_h1', [0.0]*12)
    act_hidden2 = getattr(brain, 'last_h2', [0.0]*12)
    act_output = getattr(brain, 'last_output', [0.0]*1)
    activations = [act_inputs, act_hidden1, act_hidden2, act_output]
    
    # Hitung koordinat (X,Y) tiap node
    node_positions = []
    for layer_idx, num_nodes in enumerate(layers):
        pts = []
        spacing = h / (num_nodes + 1)
        for n_idx in range(num_nodes):
            ny = y + int((n_idx + 1) * spacing)
            pts.append((layer_x[layer_idx], ny))
        node_positions.append(pts)

    # A. Garis Koneksi Weights (w1: Input -> Hidden 1)
    for i, p_in in enumerate(node_positions[0]):
        a_in = act_inputs[i] if i < len(act_inputs) else 0.5
        for h1_idx, p_h1 in enumerate(node_positions[1]):
            weight = brain.w1[i][h1_idx]
            signal = abs(a_in * weight)
            brightness = min(255, max(30, int(signal * 220)))
            color = (brightness, 80, 80) if weight > 0 else (80, brightness, 120)
            pygame.draw.line(surface, color, p_in, p_h1, 1)

    # B. Garis Koneksi Weights (w2: Hidden 1 -> Hidden 2)
    for h1_idx, p_h1 in enumerate(node_positions[1]):
        a_h1 = act_hidden1[h1_idx] if h1_idx < len(act_hidden1) else 0.0
        for h2_idx, p_h2 in enumerate(node_positions[2]):
            weight = brain.w2[h1_idx][h2_idx]
            signal = abs(a_h1 * weight)
            brightness = min(255, max(30, int(signal * 220)))
            color = (brightness, 80, 80) if weight > 0 else (80, brightness, 120)
            pygame.draw.line(surface, color, p_h1, p_h2, 1)

    # C. Garis Koneksi Weights (w3: Hidden 2 -> Output)
    for h2_idx, p_h2 in enumerate(node_positions[2]):
        a_h2 = act_hidden2[h2_idx] if h2_idx < len(act_hidden2) else 0.0
        for o_idx, p_out in enumerate(node_positions[3]):
            weight = brain.w3[h2_idx][o_idx]
            signal = abs(a_h2 * weight)
            brightness = min(255, max(30, int(signal * 220)))
            color = (brightness, 80, 80) if weight > 0 else (80, brightness, 120)
            pygame.draw.line(surface, color, p_h2, p_out, 1 if signal < 0.5 else 2)

    # D. Gambar Node Lingkaran
    for layer_idx, layer_pts in enumerate(node_positions):
        for node_idx, pt in enumerate(layer_pts):
            val = activations[layer_idx][node_idx] if node_idx < len(activations[layer_idx]) else 0
            
            # Skala intensitas cahaya (0.1 sampai 1.0)
            intensity = max(0.15, min(1.0, (val + 1.0) / 2.0 if layer_idx > 0 else val))

            # Warna Cyan menyala jika sinyal tinggi, redup jika sinyal rendah
            glow_color = (int(50 * intensity), int(200 * intensity + 55), int(255 * intensity))
            core_color = (255, 255, 255) if intensity > 0.7 else glow_color

            # Render efek pendaran
            pygame.draw.circle(surface, (15, 20, 30), pt, 6)          # Pinggiran hitam
            pygame.draw.circle(surface, glow_color, pt, 5)           # Pendaran luar
            pygame.draw.circle(surface, core_color, pt, max(1, int(3 * intensity))) # Inti cahaya