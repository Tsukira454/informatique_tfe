import cv2
import pygame

# --- Initialisation Pygame ---
pygame.init()

# --- Charger la vidéo avec OpenCV ---
video_path = "C:/Users/Tsuki/Desktop/informatique_tfe/github/video.mp4"
cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    raise Exception(f"Impossible d'ouvrir la vidéo : {video_path}")

fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# --- Créer la fenêtre Pygame ---
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Vidéo en Background")
clock = pygame.time.Clock()

running = True
while running:
    ret, frame = cap.read()

    # Reboucler la vidéo si elle se termine
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    # Convertir BGR (OpenCV) → RGB (Pygame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convertir la frame en surface Pygame
    surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    # Afficher la frame
    screen.blit(surface, (0, 0))

    # Événements Pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(fps)  # Respecter le FPS de la vidéo

# --- Libérer les ressources ---
cap.release()
pygame.quit()
