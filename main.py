import pygame
import sys

# Inicia Pygame
pygame.init()

# Configuracion ventana 
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Zorro Aventurero - Acertijos Celestiales")

# Fondos
background = pygame.image.load("fondo.jpg").convert()
background2 = pygame.image.load("fondo2.jpg").convert()
bg_width = background.get_width()

#lista de fondos y posiciones
backgrounds = [background, background2]
bg_positions = [0, bg_width]

# Control FPS
clock = pygame.time.Clock()
FPS = 60

# Cargar imagen del personaje
fox_image = pygame.image.load("zorroAventurero.png").convert_alpha()
fox_image = pygame.transform.scale(fox_image, (200, 200))  # ajusta el tamaño del personaje
fox_rect = fox_image.get_rect()
fox_rect.topleft = (100, 400)  # Posición inicial


# Variables de movimiento
vel_x = 5
vel_y = 0
jump_force = -15
gravity = 1
on_ground = True

#Bucle principal que mantiene la ventana activa
def main():
    global vel_y, on_ground
    while True:
    
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Movimiento con teclas
        if keys[pygame.K_LEFT]:
            fox_rect.x -= vel_x
            for i in range(len(bg_positions)):
                bg_positions[i] += vel_x

        if keys[pygame.K_RIGHT]:
            fox_rect.x += vel_x
            for i in range(len(bg_positions)):
                bg_positions[i] -= vel_x
            

        #Salto    
        if keys[pygame.K_UP] and on_ground:
            vel_y = jump_force
            on_ground = False

        # Aplicar gravedad
        vel_y += gravity
        fox_rect.y += vel_y

        # Colisión con el suelo
        if fox_rect.bottom >= 500:
            fox_rect.bottom = 500
            vel_y = 0
            on_ground = True

        #colisiones laterales para zorro y fondo
        if fox_rect.right >= 600:
            fox_rect.right = 600

        if fox_rect.left <= 50:
            fox_rect.left = 50

        # Reposicionar fondos cuando salen de pantalla
        for i in range(len(bg_positions)):
            if bg_positions[i] <= -bg_width:
                bg_positions[i] += bg_width * len(bg_positions)
            elif bg_positions[i] >= bg_width * (len(bg_positions) - 1):
                bg_positions[i] -= bg_width * len(bg_positions)

        # Dibujar fondos
        for i, bg in enumerate(backgrounds):
            screen.blit(bg, (bg_positions[i], 0))

        # Aqui inicia la logica del juego
        screen.blit(fox_image, fox_rect)


        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()