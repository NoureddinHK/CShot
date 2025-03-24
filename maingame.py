import pygame
import random
import math

pygame.init() # اجرای پای گیم

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
            random.randint(PLAY_AREA.left + 10, PLAY_AREA.right - 20), # محدوده تصادفی هدف با فاصله کم از لبه های محدوده بازی
            random.randint(PLAY_AREA.top + 10, PLAY_AREA.bottom - 20),
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
            random.randint(PLAY_AREA.left + 10, PLAY_AREA.right - 20), # محدوده تصادفی هدف با فاصله کم از لبه های محدوده بازی
            random.randint(PLAY_AREA.top + 10, PLAY_AREA.bottom - 20),
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


while True:
    """کلیدهای حرکت پوینتر"""
    players = [
        Player(RED, {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d, "shoot": pygame.K_f}, "Player 1"),
        Player(BLUE, {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "shoot": pygame.K_RETURN}, "Player 2"),
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

        new_traces = []
        for trace in traces:
            hit_target = None
            for target in targets:
                if target.is_hit(trace):
                    hit_target = target
                    break

            if hit_target:
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
