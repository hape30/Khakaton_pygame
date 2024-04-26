import pygame
import random
import csv
# инициализация Pygame
# инициализация Pygame
pygame.init()

# константы-параметры окна
WIDTH = 800
HEIGHT = 600
# константы-цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)
BLACK = (0, 0, 0)

# класс для игрока
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):  # добавляем новый параметр image_path
        super().__init__()

        # загружаем изображение для спрайта
        self.image = pygame.image.load(image_path).convert_alpha()

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # компоненты скорости по оси X и Y
        self.x_velocity = 0
        self.y_velocity = 0

        # переменная-флаг для отслеживания в прыжке ли спрайт
        self.on_ground = False

        # здоровье игрока
        self.health = 100

    def update(self):
        # Обновление позиции игрока
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

        # применение гравитации
        self.y_velocity += 0.3

        # Проверка, находится ли игрок на земле
        if self.rect.y >= HEIGHT - self.rect.height:
            self.on_ground = True
            self.rect.y = HEIGHT - self.rect.height
            self.y_velocity = 0
        else:
            self.on_ground = False

# класс для платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        # создание изображения для спрайта
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# класс для врагов
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path):
        super().__init__()

        # загружаем изображение для спрайта
        self.image = pygame.image.load(image_path).convert_alpha()

        # создание хитбокса для спрайта
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # компоненты скорости по оси X и Y
        self.x_velocity = 1
        self.y_velocity = 0

    def update(self):
        # Обновление позиции врага
        self.rect.x += self.x_velocity
        self.rect.y += self.y_velocity

# функция для проверки коллизий c платформой
def check_collision_platforms(object, platform_list):
    # перебираем все платформы из списка (не группы спрайтов)
    for platform in platform_list:
        if object.rect.colliderect(platform.rect):
            if object.y_velocity > 0:  # Если спрайт падает
                # меняем переменную-флаг
                object.on_ground = True
                # ставим его поверх платформы и сбрасываем скорость по оси Y
                object.rect.bottom = platform.rect.top
                object.y_velocity = 0
            elif object.y_velocity < 0:  # Если спрайт движется вверх
                # ставим спрайт снизу платформы
                object.rect.top = platform.rect.bottom
                object.y_velocity = 0
            elif object.x_velocity > 0:  # Если спрайт движется вправо
                # ставим спрайт слева от платформы
                object.rect.right = platform.rect.left
            elif object.x_velocity < 0:  # Если спрайт движется влево
                # ставим спрайт справа от платформы
                object.rect.left = platform.rect.right

# функция для проверки коллизий между игроком и врагами
def check_collision_enemies(player, enemies_group):
    # перебираем всех врагов в группе
    for enemy in enemies_group:
        if player.rect.colliderect(enemy.rect):
            player.health -= 10  # уменьшаем здоровье игрока при столкновении с врагом
            enemies_group.remove(enemy)  # удаляем врага при столкновении

# создаем экран, счетчик частоты кадров и очков
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
score = 0

# Чтение уровня из CSV
# функция для чтения уровня из CSV
def read_level_from_csv(file_path):
    level_data = []
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            level_data.append(row)
    return level_data

level_data = read_level_from_csv("level0.csv")

# Создание платформ на основе данных из CSV
platforms_list = []
for row_index, row in enumerate(level_data):
    for col_index, item in enumerate(row):
        if item == '1':  # Платформа есть (можно выбрать любой символ для обозначения платформ)
            platform = Platform(col_index * 50, row_index * 50, 50, 20)  # Размеры платформы могут быть изменены
            platforms_list.append(platform)

# создаем группу спрайтов для платформ
player_and_platforms = pygame.sprite.Group()

# в трех циклах добавляем объекты в соответствующие группы
for i in platforms_list:
    player_and_platforms.add(i)

# отдельно добавляем игрока
player_instance = Player(50, 50, "image/gg.png")  # Создание экземпляра игрока
player_and_platforms.add(player_instance)  # Добавление игрока в группу спрайтов

# создаем врагов
enemies_list = [Enemy(120, 315, "image/enemi.png"), Enemy(500, 200, "image/enemi.png")]

# создаем группу спрайтов для врагов
enemies_group = pygame.sprite.Group()

# добавляем врагов в группу спрайтов
for enemy in enemies_list:
    enemies_group.add(enemy)

# игровой цикл
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обработка прыжка
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player_instance.on_ground:
                player_instance.y_velocity = -9  # Задаем вертикальную скорость при прыжке
                player_instance.on_ground = False  # Сбрасываем флаг "на земле"

    # проверяем нажатие на клавиши для перемещения
    keys = pygame.key.get_pressed()
    player_instance.x_velocity = 0
    if keys[pygame.K_LEFT]:
        player_instance.x_velocity = -5
    if keys[pygame.K_RIGHT]:
        player_instance.x_velocity = 5

    # обновляем значения атрибутов игрока
    player_instance.update()

    # проверяем все возможные коллизии
    check_collision_platforms(player_instance, platforms_list)
    check_collision_enemies(player_instance, enemies_group)  # добавляем проверку коллизий с врагами

    # отрисовываем фон и платформы
    screen.fill(WHITE)
    player_and_platforms.draw(screen)

    # отрисовываем здоровье игрока
    pygame.draw.rect(screen, RED, (10, 10, player_instance.health * 2, 20))

    # обновляем и отрисовываем врагов
    enemies_group.update()
    enemies_group.draw(screen)

    # обновление экрана и установка частоты кадров
    pygame.display.update()
    clock.tick(60)

    # завершение игры, если здоровье игрока меньше или равно 0
    if player_instance.health <= 0:
        running = False

pygame.quit()
