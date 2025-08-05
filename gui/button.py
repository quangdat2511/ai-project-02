import pygame

class Button:
    def __init__(self, pos, width, height, text, color, text_color=(255, 255, 255), font=None, border_radius=0):
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = font or pygame.font.SysFont('comicsans', 20)
        self.border_radius = border_radius
        self.is_hovered = False
    
    def draw(self, surface):
        # Draw button with hover effect
        color = tuple(min(255, c + 30) for c in self.color) if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=self.border_radius)
        
        # Draw centered text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            return True
        return False