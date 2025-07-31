import pygame

class Button:
    def __init__(self, text, x, y, w, h, color, hover_color, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.color = color
        self.hover_color = hover_color
        self.action = action

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        current_color = self.color
        if self.rect.collidepoint(mouse):
            current_color = self.hover_color
            if click[0] and self.action:
                self.action()
        pygame.draw.rect(screen, current_color, self.rect, border_radius=8)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
