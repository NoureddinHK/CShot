import pygame
import mysql.connector
import random
import math

namePlayers = []
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
    active_input = 1
    def __init__(self, screen, title, parent=None):
        super().__init__(screen, title, ["Submit", "Back"], parent)
        self.input_text1 = ""
        self.input_text2 = ""
    
    def draw_menu(self):
        super().draw_menu()
        p1 = self.font.render("Player1:", True, (0,0,0))
        p2 = self.font.render("Player2:", True, (0,0,0))
        self.screen.blit(p1, (340, 360))
        self.screen.blit(p2, (340, 455))
        pygame.draw.rect(self.screen, (200, 200, 200), (490, 355, 300, 50), 2)
        pygame.draw.rect(self.screen, (200, 200, 200), (490, 450, 300, 50), 2)
        text_surface = self.font.render(self.input_text1, True, (0, 0, 0))
        text_surface2 = self.font.render(self.input_text2, True, (0, 0, 0))
        self.screen.blit(text_surface, (500, 360))
        self.screen.blit(text_surface2, (500, 455))
        if LoginMenu.active_input == 1:
            pygame.draw.rect(self.screen, (0,0,0), (490, 355, 300, 50), 2)
        else:
            pygame.draw.rect(self.screen, (0,0,0), (490, 450, 300, 50), 2)

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
                        SaveData().Table()
                        SaveData().repeatName(str(self.input_text1))
                        SaveData().repeatName(str(self.input_text2))
                        namePlayers.append(self.input_text1)
                        namePlayers.append(self.input_text2)
                        return self.input_text1# Return input value
                    return self.options[self.selected]
                elif event.key == pygame.K_TAB:
                    if LoginMenu.active_input == 1:
                        LoginMenu.active_input = 2
                    else : 
                        LoginMenu.active_input = 1
                elif LoginMenu.active_input == 1:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text1 = self.input_text1[:-1]
                    elif event.key == pygame.K_RETURN and self.input_text1 and self.input_text2:
                        self.input_text1 = ""
                        self.input_text2 = ""
                    else:
                        self.input_text1 += event.unicode
                
                elif LoginMenu.active_input == 2:
                    if event.key == pygame.K_BACKSPACE:
                        self.input_text2 = self.input_text2[:-1]
                    elif event.key == pygame.K_RETURN and self.input_text1 and self.input_text2:
                        self.input_text1 = ""
                        self.input_text2 = ""
                    else:
                        self.input_text2 += event.unicode


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
        self.leaderboard_data = leaderboard_data  # List of (id, name, score) tuples
        self.scrolly = 0  # مکان اسکرول
        self.visible_entries = 7  

    def draw_menu(self):
        self.screen.fill((255, 255, 255))
        
        # Draw Title
        title_text = self.title_font.render(self.title, True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(600, 50))
        self.screen.blit(title_text, title_rect)

        # Draw Leaderboard Entries (only visible ones)
        for i in range(self.visible_entries):
            if i + self.scrolly >= len(self.leaderboard_data):
                break
                
            id, name, score = self.leaderboard_data[i + self.scrolly]
            
            # Set colors for top 3 players (global ranking, not visible ones)
            original_index = i + self.scrolly
            if original_index == 0:
                color = (255, 215, 0)  # Gold
                font_size = 60
            elif original_index == 1:
                color = (192, 192, 192)  # Silver
                font_size = 60
            elif original_index == 2:
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
                        return self.input_text
                    return self.options[self.selected]
                elif event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:  # Scroll up
                    self.scrolly = max(0, self.scrolly - 1)
                elif event.button == 5:  # Scroll down
                    self.scrolly = min(len(self.leaderboard_data) - self.visible_entries, self.scrolly + 1)




# کلاس بازیکن(پوینتر)
class Player:
    def __init__(self, color, controls, name):
        self.position = [
            random.randint(PLAY_AREA.left + 100, PLAY_AREA.right - 100), # محدوده تصادفی پوینتر با فاصله کم از لبه های محدوده بازی
            random.randint(PLAY_AREA.top + 50, PLAY_AREA.bottom - 50),
        ]
        self.color = color
        self.controls = controls
        self.bullets = 30
        self.score = 0
        self.last_hit_position = None # برای امتیازدهی برحسب فاصله بین دو هدف
        self.name = name
        self.double_points_active = False
        self.double_points_timer = 0

# تابع حرکت بازیکن
    def move(self, keys):
        if keys[self.controls["up"]] and self.position[1] - 8 > PLAY_AREA.top: # پوینتر از خط بالا خارج نشود
            self.position[1] -= 7 # سرعت بالارفتن پوینتر
        if keys[self.controls["down"]] and self.position[1] + 8 < PLAY_AREA.bottom: # پوینتر از خط پایین خارج نشود
            self.position[1] += 7 # سرعت پایین آمدن پوینتر
        if keys[self.controls["left"]] and self.position[0] - 8 > PLAY_AREA.left: # پوینتر از خط چپ خارج نشود
            self.position[0] -= 7 # سرعت چپ رفتن پوینتر
        if keys[self.controls["right"]] and self.position[0] + 8 < PLAY_AREA.right: # پوینتر از خط راست خارج نشود
            self.position[0] += 7 # سرعت راست رفتن پوینتر

# تابع تیراندازی
    def shoot(self, traces):
        """برای مشخص کردن محل پوینتر بعد از شلیک و کم شدن گلوله بعد هربار شلیک"""
        if self.bullets > 0:
            traces.append((self.position[0], self.position[1], self.color))
            self.bullets -= 1

# تابع مدیریت دابل پوینت(چون این آیتم تایمر دارد این تابع لازم است)
    def update(self):
        """اگر دابل پوینت فعال بود یک ثانیه کم کن و اگر تایمر صفر شد غیرفعال کن"""
        if self.double_points_active:
            if self.double_points_timer > 0:
                self.double_points_timer -= 1
            else:
                self.double_points_active = False
                self.double_points_timer = 0

# تابع امتیازدهی
    def update_score(self, target):
        """اولین هدف ۳۰ امتیاز دارد و بعد از آن برحسب فاصله امتیاز داده میشود"""
        current_hit_position = target.position
        if self.last_hit_position:
            distance = math.dist(self.last_hit_position, current_hit_position) # محاسبه فاصله با کتابخانه math
            points = max(int(distance / 5), 30) # حداقل امتیاز دریافت شده همیشه ۳۰ امتیاز است
        else:
            points = 30  # اولین هدف

        if self.double_points_active:
            points *= 2  # اثر آیتم دابل پوینت
        self.score += points
        self.last_hit_position = current_hit_position

# (والد)کلاس هدف
class Target:
    def __init__(self):
        self.position = [
            random.randint(PLAY_AREA.left + 40, PLAY_AREA.right - 40), # محدوده تصادفی هدف با فاصله کم از لبه های محدوده بازی
            random.randint(PLAY_AREA.top + 20, PLAY_AREA.bottom - 20),
        ]
        target_image = pygame.image.load("target.png") # تصویر هدف
        target_image = pygame.transform.scale(target_image, (45, 45)) # ابعاد هدف
        self.image = target_image
        self.width, self.height = self.image.get_size()

    def draw(self, screen):
        screen.blit(self.image, (self.position[0], self.position[1])) # نمایش هدف

    def is_hit(self, trace):
        """بررسی اینکه آیا تیر به هدف خورده است؟ با استفاده از مختصات تیر وهدف"""
        x, y = trace[0], trace[1]
        return (
            self.position[0] <= x <= self.position[0] + self.width
            and self.position[1] <= y <= self.position[1] + self.height
        )

    def respawn(self):
        """اسپاون شدن هدف بعدی"""
        self.position = [
            random.randint(PLAY_AREA.left + 40, PLAY_AREA.right - 40), # محدوده تصادفی هدف با فاصله کم از لبه های محدوده بازی
            random.randint(PLAY_AREA.top + 20, PLAY_AREA.bottom - 20),
        ]

# کلاس هدف امتیازی تایمر 
class TimerTarget(Target):
    def __init__(self):
        super().__init__()
        timer_image = pygame.image.load("timer.png")
        self.image = pygame.transform.scale(timer_image, (55, 55))  # تغییر ابعاد هدف

    def grant_time(self, player_index):
        """عملکرد آیتم امتیازی"""
        player_timers[player_index] += 20 # ۲۰ ثانیه اضافه شود


# کلاس هدف امتیازی تیر اضافه
class AmmoTarget(Target):
    def __init__(self):
        super().__init__()
        ammo_image = pygame.image.load("ammo.png")
        self.image = pygame.transform.scale(ammo_image, (50, 50))

    def grant_ammo(self, player):
        player.bullets += 8  # ۸ تا گلوله اضافه شود


# کلاس هدف امتیازی دابل پوینت
class DoublePointsTarget(Target):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("double_points.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

    def grant_double_points(self, player):
        player.double_points_active = True # فعال کردن دابل پوینت
        player.double_points_timer = 360  # مدت زمان دابل پوینت که ۳۶۰فریم معادل ۱۲ثانیه است


# تابع صفحه پایان بازی
def game_over_screen():
    screen.fill(WHITE) # بک گراند

    # مشخص شدن برنده
    if players[0].score > players[1].score:
        winner_text = f"{players[0].name} Wins!"
        winner_color = RED
    elif players[1].score > players[0].score:
        winner_text = f"{players[1].name} Wins!"
        winner_color = BLUE
    else:
        winner_text = "It's a Tie!"
        winner_color = BLACK

    # متون نمایش داده شده در صفحه پایان بازی
    text = large_font.render("Game Over", True, BLACK)
    winner_display = large_font.render(winner_text, True, winner_color) # برای لود کردن متون از تابع قبلی
    score_text1 = font.render(f"{players[0].name}: {players[0].score} points", True, RED)
    score_text2 = font.render(f"{players[1].name}: {players[1].score} points", True, BLUE)
    restart_text = font.render("Press 'R' to Restart or 'ESC' to Exit", True, BLACK)

    # پوزیشن متن ها
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))
    screen.blit(winner_display, (WIDTH // 2 - winner_display.get_width() // 2, HEIGHT // 3))
    screen.blit(score_text1, (WIDTH // 2 - score_text1.get_width() // 2, HEIGHT // 2))
    screen.blit(score_text2, (WIDTH // 2 - score_text2.get_width() // 2, HEIGHT // 1.8))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))

    SaveData().repeatName(players[0].name, players[0].score)
    SaveData().repeatName(players[1].name, players[1].score)
    # برای آپدیت شدن صفحه بازی به صفحه پایان بعد از اتمام بازی
    pygame.display.flip()


    waiting = True # برای اجرای حلقه بازی تا زمانی که خودمان مشخص کنیم
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((1200, 700))

#  temporary leaderboard data
SaveData().Table()
leaderboard_data = SaveData().sortAndPrint()

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

    if choice == "Back":
        menu_history.pop()  # Remove the current menu
        current_menu = menu_history[-1] if menu_history else main_menu  # Go back
    if current_menu == login_menu:
        break
    if choice == "Quit":
        current_menu = None  # Exit program
        exit()
    elif choice == "New Game":
        current_menu = login_menu
    elif choice == "Leaderboard":
        current_menu = leaderboard_menu
    elif isinstance(choice, tuple):  # Username & Password entered
        print(f"Credentials received: {choice}")  
        current_menu = extra_input_menu  # Move to extra input
    elif isinstance(choice, str):  
        print(f"Input received: {choice}")  
        menu_history.pop()  
        current_menu = menu_history[-1] if menu_history else main_menu  
  


pygame.quit()

pygame.init() 

WIDTH, HEIGHT = 1200, 700 # طول و عرض صفحه
screen = pygame.display.set_mode((WIDTH, HEIGHT)) # نامگذاری بجای استفاده از اعداد
pygame.display.set_caption("CShot") # تایتل بالای صفحه بازی

# نامگذاری رنگ ها
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# محدوده بازی
PLAY_AREA = pygame.Rect(100, 100, 1000, 500)

font = pygame.font.Font(None, 36) # فونت سایز کوچک
large_font = pygame.font.Font(None, 72)  # فونت سایز بزرگ

# تایم هر بازیکن برحسب ثانیه
TIMER_DURATION = 60

while True:
    """کلیدهای حرکت پوینتر"""
    players = [
        Player(RED, {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "shoot": pygame.K_f}, namePlayers[0]),
        Player(BLUE, {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "shoot": pygame.K_RETURN}, namePlayers[1]),
    ]

    # لیست برای ذخیره اثر شلیک ها
    traces = []
    targets = [Target() for _ in range(5)] # ایجاد ۵ هدف


    player_timers = [TIMER_DURATION, TIMER_DURATION] # TIMER_DURATION = 60
    clock = pygame.time.Clock() # برای محدودیت fps

    last_special_spawn = pygame.time.get_ticks()  # برای مدیریت فاصله زمانی اسپاون شدن آیتم امتیازی


    """حلقه اجرای توابع اصلی بازی"""

    running = True
    while running:
        screen.fill(WHITE)
        """ظاهر محدوده بازی"""
        pygame.draw.rect(screen, BLACK, PLAY_AREA, 3) # مستطیل سیاه با ضخامت ۳

        dt = clock.tick(30) / 1000  # زمان بین فریم ها برحسب میلی ثانیه

        """مدیریت تایمر بازیکن"""
        for i in range(2):
            if player_timers[i] > 0:
                player_timers[i] -= dt
            else:
                player_timers[i] = 0  # برای منفی نشدن تایمر

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit() # خروج از پای گیم و برنامه
            elif event.type == pygame.KEYDOWN:
                for i, player in enumerate(players):
                    if event.key == player.controls["shoot"] and player_timers[i] > 0:
                        player.shoot(traces) # تیراندازی درصورت مثبت بودن تایمر

        keys = pygame.key.get_pressed()
        for player in players:
            player.move(keys)

        for x, y, color in traces:
            pygame.draw.circle(screen, color, (x, y), 5)  # ظاهر پوینتر

        for target in targets:
            target.draw(screen)

        new_traces = [] # لیست جدید برای تیرهایی که به هدف نخوردند
        for trace in traces:
            hit_target = None
            for target in targets:
                if target.is_hit(trace):
                    hit_target = target
                    break

            if hit_target: # اگر تیر به هدف خورد هدف و جای تیر حذف شوند و وضعیت اثرگذاری هدف اینجا بررسی شود
                for player in players:
                    if trace[2] == player.color:
                        if isinstance(hit_target, TimerTarget):
                            hit_target.grant_time(players.index(player))
                        elif isinstance(hit_target, AmmoTarget):
                            hit_target.grant_ammo(player)
                        elif isinstance(hit_target, DoublePointsTarget):
                            hit_target.grant_double_points(player)
                        else:
                            player.update_score(hit_target)

                    if isinstance(hit_target, (TimerTarget, AmmoTarget, DoublePointsTarget)):
                        if hit_target in targets:
                            targets.remove(hit_target)
                    else:
                        hit_target.respawn()
            else:
                new_traces.append(trace)

        traces = new_traces

        # آپدیت کردن تایمر دابل پوینت
        for player in players:
            player.update()


        """نمایش اطلاعات بازیکن"""
        name_text1 = font.render(f"{players[0].name} | Time: {int(player_timers[0])}s", True, RED)
        name_text2 = font.render(f"{players[1].name} | Time: {int(player_timers[1])}s", True, BLUE)
        bullet_text1 = font.render(f"Bullets: {players[0].bullets} | Score: {players[0].score}", True, RED)
        bullet_text2 = font.render(f"Bullets: {players[1].bullets} | Score: {players[1].score}", True, BLUE)

        screen.blit(name_text1, (20, 20))
        screen.blit(bullet_text1, (20, 50))
        screen.blit(name_text2, (WIDTH - 300, 20))
        screen.blit(bullet_text2, (WIDTH - 300, 50))

          # نمایش تایمر دابل پوینت و پوزیشن
        if players[0].double_points_active:
            dp_timer_text1 = font.render(f"Double Points: {players[0].double_points_timer // 30}s", True, RED)
            screen.blit(dp_timer_text1, (20, HEIGHT - 40))  # قرمز
        if players[1].double_points_active:
            dp_timer_text2 = font.render(f"Double Points: {players[1].double_points_timer // 30}s", True, BLUE)
            screen.blit(dp_timer_text2, (WIDTH - 300, HEIGHT - 40))  # آبی

        # هر ۱۰ ثانیه یک آیتم امتیازی اسپاون شود(در لیست تارگت که آیتم های نمایش داده شده بودند اپ اند شود)
        if pygame.time.get_ticks() - last_special_spawn >= 10000:
            special_item = random.choice([TimerTarget(), AmmoTarget(), DoublePointsTarget()])
            targets.append(special_item)
            last_special_spawn = pygame.time.get_ticks()

        pygame.display.flip()


        """اگر تیر یا تایم هردوبازیکن تمام شد یا تیر یکی و تایم دیگری تمام شد حلقه بازی تمام شود"""
        if (players[0].bullets == 0 and players[1].bullets == 0) or (player_timers[0] == 0 and player_timers[1] == 0) or (players[0].bullets == 0 and player_timers[1] == 0) or (players[1].bullets == 0 and player_timers[0] == 0):
            running = False


    game_over_screen() # پایان بازی بعد از اتمام حلقه اصلی
