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
fox_rectemp = fox_image.get_rect().inflate(-110,0)
fox_rect = fox_rectemp.copy()
fox_rect.x = fox_rect.x + 50


# Cargar bloques continuos del juego
blockC = pygame.image.load("bloqueContinuo.png").convert_alpha()
blockC = pygame.transform.scale(blockC, (300,150))


# Lista de muros (puedes tener muchas)
walls = [
    pygame.Rect(100, 500, 300, 50),
    pygame.Rect(350, 500, 300, 50),
    pygame.Rect(600, 500, 300, 50),
]


#Cargar bloques flotantes
block_1 = pygame.image.load("bloque1.png").convert_alpha()
block_1 = pygame.transform.scale(block_1, (200,200))
block1_rect = block_1.get_rect()
block1_rect.topleft = (10, 400)  # Posición inicial


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
            fox_rect.x -= vel_x  #movimiento zorro
            fox_rectemp.x -= vel_x #movimiento rect colision
            for i in range(len(bg_positions)): #movimiento fondo
                bg_positions[i] += vel_x

        if keys[pygame.K_RIGHT]:
            fox_rect.x += vel_x 
            fox_rectemp.x += vel_x
            for i in range(len(bg_positions)):
                bg_positions[i] -= vel_x


        #Salto    
        if keys[pygame.K_UP] and on_ground:
            vel_y = jump_force
            on_ground = False

        # Aplicar gravedad
        vel_y += gravity
        fox_rect.y += vel_y
        fox_rectemp.y += vel_y


        # Colisiones con bloques (suelo)
        for i, wall in enumerate(walls):
            wall_screen_x = wall.x + bg_positions[i % len(bg_positions)]
            wall_moved = wall.move(bg_positions[i % len(bg_positions)], 0)

            if fox_rect.colliderect(wall_moved):
                if vel_y > 0 and fox_rect.bottom <= wall_moved.bottom:
                    fox_rect.bottom = wall_moved.top
                    fox_rectemp.bottom = wall_moved.top
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
            
            
        # Dibujar muros con su desplazamiento
        for i, wall in enumerate(walls):
            wall_screen_x = wall.x + bg_positions[i % len(bg_positions)]
            #pygame.draw.rect(screen, (0, 0, 0), (wall_screen_x, wall.y, wall.width, wall.height))
            screen.blit(blockC, (wall_screen_x, wall.y))

        # Dibujar personaje 

        screen.blit(fox_image, fox_rectemp)
        pygame.draw.rect(screen, (0, 255, 255), fox_rect, 2)


        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()