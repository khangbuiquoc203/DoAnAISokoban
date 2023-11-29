import pygame
import time

# button class
class Button():
	def __init__(self, image, image_rect, text, text_rect, image_hover):
		self.image = image
		self.image_rect = image_rect
		self.text = text
		self.text_rect = text_rect
		self.image_hover = image_hover
		self.clicked = False

	def is_clicked(self):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.image_rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		return action

	def is_hover():
		return True

	def draw(self, surface):
		surface.blit(self.image, self.image_rect)
		surface.blit(self.text, self.text_rect)


# label class
class Label():
    def __init__(self, font_path, str, size, color, location_topleft):
        font = pygame.font.Font(font_path, size)
        self.text = font.render(str, True, color)
        self.text_rect = self.text.get_rect(topleft=location_topleft)
        
    def draw(self, surface):
        surface.blit(self.text, self.text_rect)

# textbox class
class TextScroll:
    def __init__(self, area, font, fg_color, bk_color, text, ms_per_line=800):

        super().__init__()
        self.rect = area.copy()
        self.fg_color = fg_color
        self.bk_color = bk_color
        self.size = area.size
        self.surface = pygame.Surface(self.size, flags=pygame.SRCALPHA)
        self.surface.fill(bk_color)
        self.font = font
        self.lines = text.split('\n')
        self.ms_per_line = ms_per_line
        self.y = 0
        self.y_delta = self.font.size("M")[1]
        self.next_time = None
        self.dirty = False

    def _update_line(self, line):  # render next line if it's time
        if self.y + self.y_delta > self.size[1]:  # line does not fit in remaining space
            self.surface.blit(self.surface, (0, -self.y_delta))  # scroll up
            self.y += -self.y_delta  # backup a line
            pygame.draw.rect(self.surface, self.bk_color,
                             (0, self.y, self.size[0], self.size[1] - self.y))

        text = self.font.render(line, True, self.fg_color)
        # pygame.draw.rect(text, GREY, text.get_rect(), 1)  # for demo show render area
        self.surface.blit(text, (0, self.y))

        self.y += self.y_delta

    # call update from pygame main loop
    def update(self):

        time_now = time.time()
        if (self.next_time is None or self.next_time < time_now) and self.lines:
            self.next_time = time_now + self.ms_per_line / 1000
            line = self.lines.pop(0)
            self._update_line(line)
            self.dirty = True
            self.update()  # do it again to catch more than one event per tick

    # call draw from pygam main loop after update
    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        self.dirty = False
            
    def add_line(self, new_line):
        """Add a new line to the text."""
        self.lines.append(new_line)
        self.dirty = True