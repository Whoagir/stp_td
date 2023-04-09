import pygame as pg
from collections import defaultdict

from constant import menu_font, menu_hover_font, menu_hover_font_weight


class Button(object):
    def __init__(self, text, callback, status, center=(100, 100)):
        self.text = text
        self.status = status
        self.color = [(0, 0, 0), (0, 0, 200)][self.status]
        self.callback = callback
        self.center = center
        self.surface_text = None
        self.rect = None

    def set_status(self, status):
        self.status = status

    def update(self):
        pass

    def click(self):
        self.callback()

    def draw(self, surface):
        if self.status:
            self.color = (0, 0,  200)
            self.surface_text = menu_hover_font.render(self.text, True, self.color)
        else:
            self.color = (0, 0, 0)
            self.surface_text = menu_font.render(self.text, True, self.color)
        self.rect = self.surface_text.get_rect(center=self.center)
        surface.blit(self.surface_text, self.rect)


class Menu(object):
    def __init__(self, surface, game, running=False):
        self.running = running
        self.surface = surface
        self.game = game
        self.objects = []
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)

        self.current_menu_item = 0
        self.menu_list = [
            ('start', self.start_game),
            ('settings', self.open_settings),
            ('quit', self.exit_game)
        ]

        self.create_menu()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game.quit()
            if event.type == pg.KEYDOWN:
                for handler in self.keydown_handlers[event.key]:
                    handler(event.key)

    def start_game(self):
        self.running = False
        self.game.start()

    def exit_game(self):
        self.running = False
        self.game.quit()

    def open_settings(self):
        pass

    def change_menu_item(self, key):
        if key == pg.K_UP or key == pg.K_w:
            di = -1
        else:
            di = 1
        self.current_menu_item = (self.current_menu_item + di) % len(self.menu_list)
        for i, obj in enumerate(self.objects):
            if i == self.current_menu_item:
                obj.set_status(1)
            else:
                obj.set_status(0)

    def call_menu_item(self, key):
        if key == pg.K_SPACE:
            for i, obj in enumerate(self.objects):
                if i == self.current_menu_item:
                    obj.click()

    def update(self):
        for obj in self.objects:
            obj.update()

    def create_menu(self):
        for i, menu_item in enumerate(self.menu_list):
            self.objects.append(Button(
                text=menu_item[0],
                callback=menu_item[1],
                status=i == self.current_menu_item,
                center=(self.game.screen_width//2, self.game.screen_height//2 + i * menu_hover_font_weight)))
        self.keydown_handlers[pg.K_DOWN].append(self.change_menu_item)
        self.keydown_handlers[pg.K_UP].append(self.change_menu_item)
        self.keydown_handlers[pg.K_w].append(self.change_menu_item)
        self.keydown_handlers[pg.K_s].append(self.change_menu_item)
        self.keydown_handlers[pg.K_SPACE].append(self.call_menu_item)

    def draw(self):
        self.game.screen.fill((255, 255, 255))
        for obj in self.objects:
            obj.draw(self.surface)

        pg.display.flip()