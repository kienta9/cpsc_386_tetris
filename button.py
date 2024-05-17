import pygame as pg


class Button:
    def __init__(self, surface, x, y, width, height, text, default_color=(255, 255, 0), hover_color=(0, 255, 0), font=None, font_size=48, text_color=(0, 0, 0)):
        self.surface = surface
        self.rect = pg.Rect(x, y, width, height)
        self.default_color = default_color
        self.hover_color = hover_color
        self.color = default_color
        self.text = text
        self.font = pg.font.Font(font, font_size) if font else pg.font.SysFont(None, font_size)
        self.text_color = text_color
        self.is_hovered = False

    def draw(self):
        if self.is_hovered:
            color = self.hover_color
        else:
            color = self.default_color

        pg.draw.rect(self.surface, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        self.surface.blit(text_surface, text_rect)

    def is_clicked(self):
        mouse_pos = pg.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)
    
    def update(self):
        mouse_pos = pg.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        if self.is_hovered:
            pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        else:
            pg.mouse.set_cursor(*pg.cursors.arrow)

if __name__ == '__main__':
  print("\nERROR: button.py is the wrong file! Run play from game.py\n")