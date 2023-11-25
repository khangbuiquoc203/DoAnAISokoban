import pygame

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
class TextBox:
    def __init__(self, x, y, width, height, font_size=32):
        self.width = width
        self.rect = pygame.Rect(x, y, width, height)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = 'asdasdasdasd'
        self.font = pygame.font.Font(None, font_size)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.color_active if self.active else self.color_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self):
        width = max(200, self.font.size(self.text)[0]+10)
        self.rect.w = width

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, self.color)
        width = self.width
        self.rect.w = width
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(screen, self.color, self.rect, 2)