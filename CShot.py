


















































































































































































































































































































































































































































































































































































































































































import pygame
import mysql.connector



class SaveData():
    def __init__(self, host = "127.0.0.1", user = "root", password = "123456789", database = "rank_player_cshot"):
        self.host = host 
        self.user = user
        self.password = password
        self.database = database
        self.conn = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database=self.database
        )
        self.cursor = self.conn.cursor()
    def Table(self):                      #ساخت جدول برای ثبت اطلاعات
        self.cursor.execute('''
    CREATE TABLE IF NOT EXISTS leaderboard (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        point BIGINT
    )
    ''')
    def Register(self, name, point=0):     #ثبت کردن اطلاعات بازیکن
        self.cursor.execute('''
            INSERT INTO leaderboard (name, point)
            VALUES (%s, %s)
        ''', (name, point))
        self.conn.commit()
    def repeatName(self, name, point=0):    #اگر اسم تکراری باشد امتیاز گرفته شده را اضافه میکند به امتیاز قبلی
        self.cursor.execute('SELECT * FROM leaderboard')
        users = self.cursor.fetchall()
        for user in users:
            if user[1] == name:
                CurrentScore = user[2]
                newScore = CurrentScore + point
                self.cursor.execute('''
                UPDATE leaderboard
                SET point = %s
                WHERE name = %s '''
                , (newScore, name))
                self.conn.commit()
                return
        self.Register(name, point)
    def sortAndPrint(self):
        self.cursor.execute("SELECT * FROM leaderboard ORDER BY point DESC")
        sortPoint = self.cursor.fetchall()
        return sortPoint    




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
        title_rect = title_text.get_rect(center=(600, 100))
        self.screen.blit(title_text, title_rect)

        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected else (0, 0, 0)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(600, 240 + i * 60))
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

class LoginMenu(Menu):
    def __init__(self, screen, title, parent=None):
        super().__init__(screen, title, ["Submit", "Back"], parent)
        self.input_text = ""
    
    def draw_menu(self):
        super().draw_menu()
        pygame.draw.rect(self.screen, (200, 200, 200), (490, 355, 300, 50), 2)
        text_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (500, 360))

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
                        SaveData().repeatName(str(self.input_text))
                        return self.input_text  # Return input value
                    return self.options[self.selected]
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode


class ExtraInputMenu(Menu):
    def __init__(self, screen, title, parent=None):
        super().__init__(screen, title, ["Submit", "Back"], parent)
        self.input_text = ""

    def draw_menu(self):
        super().draw_menu()
        pygame.draw.rect(self.screen, (200, 200, 200), (450, 350, 300, 50), 2)
        text_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(text_surface, (460, 360))

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
                        return self.input_text  # Return user input
                    return self.options[self.selected]
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode


class LeaderboardMenu(Menu):
    def __init__(self, screen, title, leaderboard_data, parent=None):
        super().__init__(screen, title, ["Back"], parent)
        self.leaderboard_data = leaderboard_data  # List of (name, score) tuples

    def draw_menu(self):
        self.screen.fill((255, 255, 255))
        
        # Draw Title
        title_text = self.title_font.render(self.title, True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(600, 50))
        self.screen.blit(title_text, title_rect)

        # Draw Leaderboard Entries
        for i, (id,name, score) in enumerate(self.leaderboard_data):
            # Set colors for top 3 players
            if i == 0:
                color = (255, 215, 0)  # Gold
                font_size = 60
            elif i == 1:
                color = (192, 192, 192)  # Silver
                font_size = 60
            elif i == 2:
                color = (205, 127, 50)  # Bronze
                font_size = 60
            else:
                color = (0, 0, 0)  # Black for others
                font_size = 40

            font = pygame.font.Font(None, font_size)
            name_text = font.render(name, True, color)
            score_text = font.render(str(score), True, color)

            # Align names to the left and scores to the right
            self.screen.blit(name_text, (350, 150 + i * 50))
            self.screen.blit(score_text, (750, 150 + i * 50))

        # Draw Back Option
        back_text = self.font.render("Back", True, (255, 0, 0) if self.selected == 0 else (0, 0, 0))
        back_rect = back_text.get_rect(center=(600, 550))
        self.screen.blit(back_text, back_rect)
        
        



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
screen = pygame.display.set_mode((1200, 700))

#  temporary leaderboard data
leaderboard_data = SaveData().sortAndPrint()

# Create menus
# Create menus
main_menu = Menu(screen, "Main Menu", ["New Game", "Leaderboard", "Quit"])
login_menu = LoginMenu(screen, "Login Menu", parent=main_menu)
extra_input_menu = ExtraInputMenu(screen, "Extra Step", parent=main_menu)  # New step
leaderboard_menu = LeaderboardMenu(screen, "Leaderboard", leaderboard_data, parent=main_menu)

# Menu navigation
current_menu = main_menu

menu_history = []
pygame.display.set_caption("CSHOT GAME")
while current_menu:
    menu_history.append(current_menu)  # Track menu history
    choice = current_menu.run()

    if choice == "Quit":
        current_menu = None  # Exit program
    elif choice == "New Game":
        current_menu = login_menu
    elif choice == "Leaderboard":
        current_menu = leaderboard_menu
    elif choice == "Back":
        menu_history.pop()  # Remove the current menu
        current_menu = menu_history[-1] if menu_history else main_menu  # Go back
    elif isinstance(choice, tuple):  # Username & Password entered
        print(f"Credentials received: {choice}")  
        current_menu = extra_input_menu  # Move to extra input
    elif isinstance(choice, str):  
        print(f"Input received: {choice}")  
        menu_history.pop()  
        current_menu = menu_history[-1] if menu_history else main_menu  
  


pygame.quit()
