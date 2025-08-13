import pygame
class InputBox:
    def __init__(self, x, y, w, h, text='', font=None, color_active=(0, 255, 0), color_inactive=(200, 200, 200)):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = color_inactive
        self.color_active = color_active
        self.color = color_inactive
        self.text = text
        self.font = font
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Click trong box thì active, ngoài thì inactive
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = self.color_inactive
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.unicode.isdigit() or event.unicode == '.':
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))

    def draw(self, screen):
        # Vẽ text
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Vẽ khung
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self, default=0):
        try:
            return float(self.text) if '.' in self.text else int(self.text)
        except ValueError:
            return default
