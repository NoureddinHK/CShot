

































































































































































































































































































































































































































































































































































































































































































































































import pygame

class Menu:
    def __init__(self, screen, title, options, parent=None):
        self.screen = screen
        self.title = title
        self.options = options
        self.selected = 0
        self.running = True
        self.font = pygame.font.Font(None, 50)
        self.title_font = pygame.font.Font(None, 70)
        self.parent = parent  # Reference to the previous menu

    def draw_menu(self):
        self.screen.fill((255, 255, 255))
        title_text = self.title_font.render(self.title, True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(400, 100))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected else (0, 0, 0)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(400, 200 + i * 60))
            self.screen.blit(text, rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    return self.options[self.selected]
                
    def back(self):
        if self.menu_history:
            self.menu_history.pop()
            if self.menu_history:
                self.menu_history[-1]()
            else:
                self.initial_menu()

    def run(self):
        while self.running:
            action = self.handle_events()
            if action:
                return action  # Return selected option
            self.draw_menu()
            pygame.display.flip()
        return None

class InputMenu(Menu):
    def __init__(self, screen, title, parent=None):
        super().__init__(screen, title, ["Submit", "Back"], parent)
        self.input_text = ""
    
    def draw_menu(self):
        super().draw_menu()
        pygame.draw.rect(self.screen, (200, 200, 200), (250, 350, 300, 50), 2)
        text_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (260, 360))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.selected = (self.selected + 1) % len(self.options)
                elif event.key == pygame.K_UP:
                    self.selected = (self.selected - 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    if self.options[self.selected] == "Submit":
                        return self.input_text  # Return input value
                    return self.options[self.selected]
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Create menus
main_menu = Menu(screen, "Main Menu", ["Register", "Login", "Leaderboard", "Quit"])
register_menu = InputMenu(screen, "Register Menu", parent=main_menu)
login_menu = InputMenu(screen, "Login Menu", parent=main_menu)
leaderboard_menu = Menu(screen, "Leaderboard Menu", ["Back"], parent=main_menu)

# Menu navigation
current_menu = main_menu

menu_history = []

while current_menu:
    menu_history.append(current_menu)  # Track menu history
    choice = current_menu.run()

    if choice == "Quit":
        current_menu = None  # Exit program
    elif choice == "Register":
        current_menu = register_menu
    elif choice == "Login":
        current_menu = login_menu
    elif choice == "Leaderboard":
        current_menu = leaderboard_menu
    elif choice == "Back":
        menu_history.pop()  # Remove the current menu
        current_menu = menu_history[-1] if menu_history else main_menu  # Go back
    elif isinstance(choice, str):  
        print(f"Input received: {choice}")  # Display input text
        menu_history.pop()  # Remove input menu from history
        current_menu = menu_history[-1] if menu_history else main_menu  


pygame.quit()
