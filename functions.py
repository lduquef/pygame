import pygame
import random

# Inicializa todos los módulos de Pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.font.init()  # Inicializa el módulo de fuentes de Pygame
font = pygame.font.Font('freesansbold.ttf', 32)  # Fuente para el texto de los botones
objects = []  # Lista para almacenar todos los botones y objetos

class Button:
    """
    Clase para representar un botón en Pygame.
    """
    
    def __init__(self, x, y, width, height, buttonText='Button', onePress=False):
        """
        Constructor para inicializar el botón.

        Parámetros:
        - x: posición x del botón
        - y: posición y del botón
        - width: ancho del botón
        - height: alto del botón
        - buttonText: texto que se muestra en el botón
        - onePress: si es True, el botón solo puede ser presionado una vez
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onePress = onePress
        self.alreadyPressed = False

        # Colores para los diferentes estados del botón
        self.fillColors = {
            'normal': '#eb8209',
            'hover': '#d9971c',
            'pressed': '#a85b03',
            'hide': (0, 0, 0),
        }
        # Superficie y rectángulo del botón
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        # Superficie del texto del botón
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        # Añadir el botón a la lista de objetos
        objects.append(self)

    def process(self):
        """
        Método para procesar el estado del botón en función de la interacción del usuario.
        Cambia el color del botón según el estado del mouse y si se ha presionado.
        """
        mousePos = pygame.mouse.get_pos()  # Obtiene la posición actual del mouse
        self.buttonSurface.fill(self.fillColors['normal'])  # Color normal del botón
        
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])  # Cambia color si el mouse está sobre el botón
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])  # Cambia color si el botón está presionado
                if self.onePress:
                    self.alreadyPressed = True  # Marca el botón como presionado una vez
                    self.buttonSurface.fill(self.fillColors['hide'])  # Oculta el botón después de presionarlo
                elif not self.alreadyPressed:
                    self.alreadyPressed = True  # Marca el botón como presionado
            else:
                self.alreadyPressed = False  # Resetea el estado del botón si no está presionado

        # Centra el texto en el botón
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        # Dibuja el botón en la pantalla
        screen.blit(self.buttonSurface, self.buttonRect)

class Player:
    """
    Clase para representar al jugador en el juego.
    """
    
    def __init__(self):
        self.position = [50, 100]
        self.size = [20, 20]
        self.speed = 30

    def up(self):
        self.position[1] -= self.speed*1.5

    def down(self):
        self.position[1] += self.speed

    def gravity(self):
        self.position[1] += 1

    def draw(self, screen, image):
        """
        Método para dibujar al jugador en la pantalla.

        Parámetros:
        - screen: superficie de la pantalla donde dibujar
        - image: imagen del jugador a dibujar
        """
        screen.blit(image, self.position)

class Bullet:
    """
    Clase para representar una bala en el juego.
    """
    
    def __init__(self, x, y, img):
        self.position = [x, y]
        self.size = [10, 5]  # Tamaño del bullet
        self.speed = 10  # Velocidad de movimiento hacia la izquierda
        self.image = img

    def move(self):
        """
        Método para mover la bala hacia la izquierda.
        """
        self.position[0] += self.speed

    def draw(self, screen):
        """
        Método para dibujar la bala en la pantalla.

        Parámetros:
        - screen: superficie de la pantalla donde dibujar
        """
        screen.blit(self.image, self.position)

class Enemy:
    """
    Clase para representar a un enemigo en el juego.
    """
    
    def __init__(self):
        self.position = [600, 250]
        self.size = [30, 30]  # Tamaño del enemigo
        self.speed = 3  # Velocidad de movimiento hacia la izquierda
        self.health  =100
    def move(self):
        """
        Método para mover al enemigo hacia arriba y abajo lentamente.
        """

        self.position[1] += self.speed  # Movimiento hacia abajo
        if self.position[1] <= 20 or self.position[1] >= 600:
            self.speed = -self.speed  # Cambiar dirección al llegar a los límites de la pantalla

    def draw(self, screen, img):
        """
        Método para dibujar al enemigo en la pantalla.

        Parámetros:
        - screen: superficie de la pantalla donde dibujar
        - img: imagen del enemigo a dibujar
        """
        screen.blit(img, self.position)
    def hit(self):
        """
        Método para reducir la vida del enemigo cuando es impactado por una bala.
        """
        self.health -= 10  # Reducir la vida del enemigo

# Bucle principal del juego