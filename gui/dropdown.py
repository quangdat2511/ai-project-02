import pygame

class Dropdown:
    def __init__(self, title, options, pos, font, width=150, height=40):
        self.title = title
        self.options = options
        self.pos = pos
        self.font = font
        self.width = width
        self.height = height
        self.selected_index = 0
        self.open = False
        self.rect = pygame.Rect(pos[0], pos[1] + 25, width, height)

    def draw(self, screen):
        # Draw title
        title_surf = self.font.render(self.title, True, (0, 0, 0))
        screen.blit(title_surf, self.pos)

        # Draw main box
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)
        
        # Draw selected text
        text = self.font.render(self.options[self.selected_index], True, (0, 0, 0))
        screen.blit(text, (self.rect.x + 10, self.rect.y + 10))
        
        # Draw arrow
        arrow_x = self.rect.right - 15
        arrow_y = self.rect.centery
        pygame.draw.polygon(screen, (0, 0, 0), [
            (arrow_x - 5, arrow_y - 5),
            (arrow_x + 5, arrow_y - 5),
            (arrow_x, arrow_y + 5)
        ])

        # Draw options if open
        if self.open:
            y = self.rect.bottom
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, y, self.width, self.height)
                color = (180, 180, 255) if option_rect.collidepoint(pygame.mouse.get_pos()) else (220, 220, 220)
                pygame.draw.rect(screen, color, option_rect)
                pygame.draw.rect(screen, (0, 0, 0), option_rect, 1)
                text = self.font.render(option, True, (0, 0, 0))
                screen.blit(text, (option_rect.x + 10, option_rect.y + 10))
                y += self.height

    def handle_event(self, event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if self.rect.collidepoint(mouse_pos):
                self.open = not self.open

                return True
            
            elif self.open:
                y = self.rect.bottom
                for i in range(len(self.options)):
                    option_rect = pygame.Rect(self.rect.x, y, self.width, self.height)
                    if option_rect.collidepoint(mouse_pos):
                        self.selected_index = i
                        self.open = False
                        break
                    y += self.height
                else:
                    self.open = False
                
                return True
                
        return False

    def get_value(self):
        return self.options[self.selected_index]