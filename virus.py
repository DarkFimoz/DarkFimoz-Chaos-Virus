import os
import sys
import time
import random
import ctypes
import threading
from pathlib import Path
from pygame import mixer
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import win32gui
import win32con
import win32api
import win32ui
from ctypes import windll

mixer.init()

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02

class ChaosVirus:
    def __init__(self):
        self.original_wallpaper = self.get_wallpaper()
        self.is_running = True
        self.root = None
        self.windows = []
        self.screen_width = win32api.GetSystemMetrics(0)
        self.screen_height = win32api.GetSystemMetrics(1)
        self.effect_canvas = None
        self.music_loaded = False
        self.music_length = 0
        
    def get_wallpaper(self):
        try:
            ubuf = ctypes.create_unicode_buffer(512)
            ctypes.windll.user32.SystemParametersInfoW(0x0073, 512, ubuf, 0)
            return ubuf.value
        except:
            return None
    
    def set_wallpaper(self, path):
        try:
            ctypes.windll.user32.SystemParametersInfoW(
                SPI_SETDESKWALLPAPER, 0, path, 
                SPIF_UPDATEINIFILE | SPIF_SENDCHANGE
            )
        except:
            pass
    
    def create_matrix_wallpaper(self):
        try:
            width, height = 1920, 1080
            img = Image.new('RGB', (width, height), color='black')
            draw = ImageDraw.Draw(img)
            
            try:
                font = ImageFont.truetype("consola.ttf", 20)
            except:
                font = None
            
            chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
            
            for x in range(0, width, 20):
                for y in range(0, height, 30):
                    char = random.choice(chars)
                    brightness = random.randint(50, 255)
                    if font:
                        draw.text((x, y), char, fill=(0, brightness, 0), font=font)
                    else:
                        draw.text((x, y), char, fill=(0, brightness, 0))
            
            wallpaper_path = os.path.join(os.getcwd(), 'matrix_wallpaper.bmp')
            img.save(wallpaper_path, 'BMP')
            return wallpaper_path
        except Exception as e:
            print(f"Ошибка создания обоев: {e}")
            return None
    
    def create_screen_melt_effect(self):
        """Эффект утекания экрана"""
        try:
            win = tk.Toplevel(self.root)
            win.attributes('-fullscreen', True)
            win.attributes('-topmost', True)
            win.attributes('-alpha', 0.8)
            win.overrideredirect(True)
            
            canvas = tk.Canvas(win, bg='black', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            # Создаём эффект утекания
            colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff']
            
            def melt_animation(frame=0):
                if frame < 50 and self.is_running:
                    try:
                        canvas.delete('all')
                        
                        # Вертикальные полосы стекают вниз
                        for x in range(0, self.screen_width, 20):
                            height = random.randint(100, 400)
                            y_offset = frame * 10
                            color = random.choice(colors)
                            canvas.create_rectangle(
                                x, y_offset, x + 15, y_offset + height,
                                fill=color, outline=''
                            )
                        
                        # Горизонтальные искажения
                        for y in range(0, self.screen_height, 50):
                            offset = random.randint(-30, 30)
                            canvas.create_line(
                                0, y, self.screen_width, y + offset,
                                fill=random.choice(colors), width=5
                            )
                        
                        self.root.after(50, lambda: melt_animation(frame + 1))
                    except:
                        pass
                else:
                    try:
                        win.destroy()
                    except:
                        pass
            
            melt_animation()
            self.windows.append(win)
            
        except Exception as e:
            print(f"Ошибка melt эффекта: {e}")
    
    def create_screen_shift_effect(self):
        """Эффект сдвига экрана влево/вправо"""
        try:
            win = tk.Toplevel(self.root)
            win.attributes('-fullscreen', True)
            win.attributes('-topmost', True)
            win.attributes('-alpha', 0.6)
            win.overrideredirect(True)
            
            canvas = tk.Canvas(win, bg='black', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            def shift_animation(frame=0):
                if frame < 30 and self.is_running:
                    try:
                        canvas.delete('all')
                        
                        # RGB разделение
                        offset = int(30 * (1 - frame / 30))
                        
                        # Красный канал
                        canvas.create_rectangle(
                            offset, 0, self.screen_width + offset, self.screen_height,
                            fill='', outline='red', width=3
                        )
                        
                        # Синий канал
                        canvas.create_rectangle(
                            -offset, 0, self.screen_width - offset, self.screen_height,
                            fill='', outline='blue', width=3
                        )
                        
                        # Случайные блоки
                        for _ in range(10):
                            x = random.randint(0, self.screen_width - 200)
                            y = random.randint(0, self.screen_height - 100)
                            w = random.randint(100, 300)
                            h = random.randint(50, 150)
                            shift = random.randint(-50, 50)
                            canvas.create_rectangle(
                                x + shift, y, x + w + shift, y + h,
                                fill='', outline=random.choice(['red', 'green', 'blue']),
                                width=2
                            )
                        
                        self.root.after(50, lambda: shift_animation(frame + 1))
                    except:
                        pass
                else:
                    try:
                        win.destroy()
                    except:
                        pass
            
            shift_animation()
            self.windows.append(win)
            
        except Exception as e:
            print(f"Ошибка shift эффекта: {e}")
    
    def create_cpu_death_effect(self):
        """Эффект умирающего процессора"""
        try:
            win = tk.Toplevel(self.root)
            win.attributes('-fullscreen', True)
            win.attributes('-topmost', True)
            win.attributes('-alpha', 0.7)
            win.overrideredirect(True)
            win.configure(bg='black')
            
            canvas = tk.Canvas(win, bg='black', highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            # Текст предупреждения
            canvas.create_text(
                self.screen_width // 2, 100,
                text="⚠ CPU OVERHEATING ⚠",
                fill='red', font=('Courier', 40, 'bold')
            )
            
            canvas.create_text(
                self.screen_width // 2, 200,
                text=f"TEMPERATURE: {random.randint(95, 125)}°C",
                fill='orange', font=('Courier', 30)
            )
            
            def death_animation(frame=0):
                if frame < 40 and self.is_running:
                    try:
                        # Случайные пиксели "выгорают"
                        for _ in range(100):
                            x = random.randint(0, self.screen_width)
                            y = random.randint(0, self.screen_height)
                            size = random.randint(2, 10)
                            color = random.choice(['red', 'orange', 'yellow', 'white'])
                            canvas.create_rectangle(
                                x, y, x + size, y + size,
                                fill=color, outline=''
                            )
                        
                        # Горизонтальные линии помех
                        if frame % 3 == 0:
                            y = random.randint(0, self.screen_height)
                            canvas.create_line(
                                0, y, self.screen_width, y,
                                fill='white', width=random.randint(1, 5)
                            )
                        
                        self.root.after(100, lambda: death_animation(frame + 1))
                    except:
                        pass
                else:
                    try:
                        win.destroy()
                    except:
                        pass
            
            death_animation()
            self.windows.append(win)
            
        except Exception as e:
            print(f"Ошибка CPU эффекта: {e}")

    def shake_all_windows(self):
        """Трясти все окна"""
        def enum_callback(hwnd, _):
            if win32gui.IsWindowVisible(hwnd):
                try:
                    rect = win32gui.GetWindowRect(hwnd)
                    x, y = rect[0], rect[1]
                    offset_x = random.randint(-15, 15)
                    offset_y = random.randint(-15, 15)
                    win32gui.SetWindowPos(hwnd, 0, x + offset_x, y + offset_y, 0, 0, 0x0001)
                except:
                    pass
            return True
        
        try:
            for _ in range(3):
                if not self.is_running:
                    break
                win32gui.EnumWindows(enum_callback, None)
                time.sleep(0.05)
        except:
            pass
    
    def move_mouse_crazy(self):
        """Двигать мышь"""
        try:
            import math
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            radius = 150
            
            for angle in range(0, 360, 20):
                if not self.is_running:
                    break
                x = int(center_x + radius * math.cos(math.radians(angle)))
                y = int(center_y + radius * math.sin(math.radians(angle)))
                win32api.SetCursorPos(x, y)
                time.sleep(0.03)
        except:
            pass
    
    def spam_programs(self):
        """Открыть программы"""
        try:
            programs = ['notepad', 'calc']
            for _ in range(2):
                os.system(f'start {random.choice(programs)}')
                time.sleep(0.3)
        except:
            pass
    
    def create_chaos_window(self):
        """Создать случайное окно"""
        try:
            win = tk.Toplevel(self.root)
            
            window_types = ['error', 'matrix', 'glitch', 'warning', 'terminal']
            wtype = random.choice(window_types)
            
            if wtype == 'error':
                self._create_error(win)
            elif wtype == 'matrix':
                self._create_matrix(win)
            elif wtype == 'glitch':
                self._create_glitch(win)
            elif wtype == 'warning':
                self._create_warning(win)
            else:
                self._create_terminal(win)
            
            self.windows.append(win)
            
            # Автоудаление
            self.root.after(random.randint(3000, 6000), lambda: self._safe_destroy(win))
        except Exception as e:
            print(f"Ошибка создания окна: {e}")
    
    def _safe_destroy(self, win):
        """Безопасно удалить окно"""
        try:
            if win in self.windows:
                self.windows.remove(win)
            win.destroy()
        except:
            pass
    
    def _create_error(self, win):
        try:
            win.title(f"ERROR {random.randint(1000, 9999)}")
            win.configure(bg='red')
            win.attributes('-topmost', True)
            
            width, height = 400, 200
            x = random.randint(0, max(0, self.screen_width - width))
            y = random.randint(0, max(0, self.screen_height - height))
            win.geometry(f"{width}x{height}+{x}+{y}")
            
            messages = [
                "⚠ CRITICAL ERROR ⚠",
                "SYSTEM FAILURE",
                "VIRUS DETECTED",
                "ALL FILES ENCRYPTED",
                "HACKED BY DARKFIMOZ",
                "YOUR PC IS MINE",
                "NO ESCAPE"
            ]
            
            label = tk.Label(win, text=random.choice(messages), 
                           bg='red', fg='white', 
                           font=('Courier', 18, 'bold'))
            label.pack(expand=True)
            
            self._animate_shake(win, x, y, width, height)
        except:
            pass
    
    def _create_matrix(self, win):
        try:
            win.title("MATRIX")
            win.configure(bg='black')
            win.attributes('-topmost', True)
            
            width, height = 300, 400
            x = random.randint(0, max(0, self.screen_width - width))
            y = random.randint(0, max(0, self.screen_height - height))
            win.geometry(f"{width}x{height}+{x}+{y}")
            
            text = tk.Text(win, bg='black', fg='#00ff00', 
                          font=('Courier', 10), bd=0)
            text.pack(fill='both', expand=True)
            
            self._animate_matrix(text)
        except:
            pass
    
    def _create_glitch(self, win):
        try:
            win.title("GLITCH")
            win.attributes('-topmost', True)
            win.overrideredirect(True)
            win.attributes('-alpha', 0.7)
            
            width = random.randint(200, 500)
            height = random.randint(200, 500)
            x = random.randint(0, max(0, self.screen_width - width))
            y = random.randint(0, max(0, self.screen_height - height))
            win.geometry(f"{width}x{height}+{x}+{y}")
            
            colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
            canvas = tk.Canvas(win, bg=random.choice(colors), highlightthickness=0)
            canvas.pack(fill='both', expand=True)
            
            for _ in range(30):
                x1, y1 = random.randint(0, width), random.randint(0, height)
                x2, y2 = random.randint(0, width), random.randint(0, height)
                canvas.create_line(x1, y1, x2, y2, fill=random.choice(colors), width=3)
        except:
            pass
    
    def _create_warning(self, win):
        try:
            win.title("⚠ WARNING ⚠")
            win.configure(bg='yellow')
            win.attributes('-topmost', True)
            
            width, height = 350, 150
            x = random.randint(0, max(0, self.screen_width - width))
            y = random.randint(0, max(0, self.screen_height - height))
            win.geometry(f"{width}x{height}+{x}+{y}")
            
            warnings = [
                "FILES ENCRYPTED!",
                "SEND 1000 BTC",
                "VIRUS: DARKFIMOZ.EXE",
                "FIREWALL DISABLED",
                "BACKDOOR ACTIVE",
            ]
            
            label = tk.Label(win, text=random.choice(warnings),
                           bg='yellow', fg='red',
                           font=('Arial', 16, 'bold'),
                           wraplength=300)
            label.pack(expand=True, pady=20)
            
            self._animate_blink(win, label)
        except:
            pass
    
    def _create_terminal(self, win):
        try:
            win.title("ROOT@DARKFIMOZ")
            win.configure(bg='black')
            win.attributes('-topmost', True)
            
            width, height = 600, 400
            x = random.randint(0, max(0, self.screen_width - width))
            y = random.randint(0, max(0, self.screen_height - height))
            win.geometry(f"{width}x{height}+{x}+{y}")
            
            text = tk.Text(win, bg='black', fg='#00ff00',
                          font=('Courier', 11), bd=0)
            text.pack(fill='both', expand=True)
            
            commands = [
                "root@darkfimoz:~# whoami\nSYSTEM",
                "root@darkfimoz:~# exploit.py\nPayload injected!",
                "root@darkfimoz:~# ransomware\nEncrypting...",
                "root@darkfimoz:~# bitcoin-miner\nMining: 1337 MH/s",
            ]
            
            for cmd in commands[:2]:
                text.insert('end', cmd + '\n')
        except:
            pass
    
    def _animate_shake(self, win, orig_x, orig_y, width, height):
        def shake(count=0):
            if count < 15 and self.is_running:
                try:
                    new_x = orig_x + random.randint(-8, 8)
                    new_y = orig_y + random.randint(-8, 8)
                    win.geometry(f"{width}x{height}+{new_x}+{new_y}")
                    self.root.after(50, lambda: shake(count + 1))
                except:
                    pass
        shake()
    
    def _animate_blink(self, win, label):
        def blink(count=0):
            if count < 8 and self.is_running:
                try:
                    if count % 2 == 0:
                        win.configure(bg='red')
                        label.configure(bg='red', fg='yellow')
                    else:
                        win.configure(bg='yellow')
                        label.configure(bg='yellow', fg='red')
                    self.root.after(300, lambda: blink(count + 1))
                except:
                    pass
        blink()
    
    def _animate_matrix(self, text):
        chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*"
        
        def update(count=0):
            if count < 25 and self.is_running:
                try:
                    line = ''.join(random.choice(chars) for _ in range(30))
                    text.insert('end', line + '\n')
                    text.see('end')
                    self.root.after(100, lambda: update(count + 1))
                except:
                    pass
        update()

    def create_fullscreen_bsod(self):
        """Фейковый BSOD"""
        try:
            win = tk.Toplevel(self.root)
            win.title("CRITICAL ERROR")
            win.configure(bg='#0000aa')
            win.attributes('-topmost', True)
            
            width = self.screen_width - 100
            height = self.screen_height - 100
            win.geometry(f"{width}x{height}+50+50")
            
            text = f"""


            A problem has been detected and Windows has been shut down
            to prevent damage to your computer.

            KERNEL_DATA_INPAGE_ERROR

            Technical information:

            *** STOP: 0x{random.randint(10000000, 99999999):08X}

            Collecting data for crash dump...
            
            Hacked by DarkFimoz
            """
            
            label = tk.Label(win, text=text, bg='#0000aa', fg='white',
                           font=('Courier', 12), justify='left')
            label.pack(expand=True)
            
            self.windows.append(win)
            self.root.after(5000, lambda: self._safe_destroy(win))
        except:
            pass
    
    def chaos_loop(self):
        """Основной цикл хаоса"""
        if not self.is_running:
            return
        
        try:
            # Случайный эффект
            effects = [
                ('windows', self.shake_all_windows),
                ('mouse', self.move_mouse_crazy),
                ('programs', self.spam_programs),
                ('chaos_window', lambda: [self.create_chaos_window() for _ in range(random.randint(2, 4))]),
                ('screen_melt', self.create_screen_melt_effect),
                ('screen_shift', self.create_screen_shift_effect),
                ('cpu_death', self.create_cpu_death_effect),
            ]
            
            effect_name, effect_func = random.choice(effects)
            
            if effect_name in ['windows', 'mouse', 'programs']:
                threading.Thread(target=effect_func, daemon=True).start()
            else:
                effect_func()
            
        except Exception as e:
            print(f"Ошибка в chaos_loop: {e}")
        
        # Следующий цикл
        delay = random.randint(1000, 2500)
        self.root.after(delay, self.chaos_loop)
    
    def mega_event(self):
        """Мега событие"""
        if not self.is_running:
            return
        
        try:
            print("\n💀💀💀 MEGA EVENT 💀💀💀")
            
            # BSOD
            self.create_fullscreen_bsod()
            
            # Эффекты экрана
            self.create_screen_melt_effect()
            self.root.after(1000, self.create_screen_shift_effect)
            self.root.after(2000, self.create_cpu_death_effect)
            
            # Куча окон
            for i in range(8):
                self.root.after(i * 150, self.create_chaos_window)
            
        except Exception as e:
            print(f"Ошибка в mega_event: {e}")
        
        # Следующее мега событие
        self.root.after(20000, self.mega_event)
    
    def check_music_status(self):
        """Проверка статуса музыки"""
        if not self.is_running:
            return
        
        try:
            # Проверяем играет ли музыка
            if self.music_loaded and not mixer.music.get_busy():
                print("\n🎵 Трек закончился - автоматическая остановка...")
                self.stop()
                return
        except Exception as e:
            print(f"Ошибка проверки музыки: {e}")
        
        # Проверяем каждую секунду
        if self.root:
            self.root.after(1000, self.check_music_status)
    
    def start(self):
        """Запуск вируса"""
        print("="*60)
        print(" "*15 + "⚠ CHAOS VIRUS ACTIVATED ⚠")
        print("="*60)
        print("\nЗакрой окно или Ctrl+C для остановки\n")
        
        # Музыка - исправлено для EXE
        try:
            # Для PyInstaller - путь к временной папке
            if getattr(sys, 'frozen', False):
                # Запущено как EXE
                base_path = sys._MEIPASS
            else:
                # Запущено как скрипт
                base_path = os.path.dirname(os.path.abspath(__file__))
            
            music_path = os.path.join(base_path, 'sounds.mp3')
            
            if os.path.exists(music_path):
                mixer.music.load(music_path)
                mixer.music.play(0)  # Играть один раз (не зацикливать)
                self.music_loaded = True
                
                # Получаем длину трека
                try:
                    from mutagen.mp3 import MP3
                    audio = MP3(music_path)
                    self.music_length = int(audio.info.length * 1000)  # в миллисекундах
                    print(f"🎵 Музыка запущена (длина: {int(audio.info.length)}с)\n")
                except:
                    print("🎵 Музыка запущена\n")
            else:
                print(f"⚠ sounds.mp3 не найден по пути: {music_path}\n")
        except Exception as e:
            print(f"⚠ Ошибка музыки: {e}\n")
        
        # Обои
        matrix_wall = self.create_matrix_wallpaper()
        if matrix_wall:
            self.set_wallpaper(matrix_wall)
            print("🖼 Обои изменены\n")
        
        # Главное окно (минимизированное)
        self.root = tk.Tk()
        self.root.title("DarkFimoz Virus - Закрой для остановки")
        self.root.geometry("300x100")
        
        label = tk.Label(self.root, text="VIRUS ACTIVE\n\nЗакрой это окно\nдля остановки", 
                        font=('Courier', 12, 'bold'), fg='red')
        label.pack(expand=True)
        
        # Запуск хаоса
        self.root.after(1000, self.chaos_loop)
        self.root.after(10000, self.mega_event)
        
        # Запуск проверки музыки
        if self.music_loaded:
            self.root.after(1000, self.check_music_status)
        
        # Обработка закрытия
        self.root.protocol("WM_DELETE_WINDOW", self.stop)
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.stop()
    
    def stop(self):
        """Остановка вируса"""
        print("\n\n🛑 Остановка...")
        self.is_running = False
        
        # Закрыть все окна
        for win in self.windows[:]:
            try:
                win.destroy()
            except:
                pass
        
        # Остановить музыку
        try:
            mixer.music.stop()
        except:
            pass
        
        # Восстановить обои
        if self.original_wallpaper:
            try:
                self.set_wallpaper(self.original_wallpaper)
                print("✅ Обои восстановлены")
            except:
                pass
        
        # Удалить временные файлы
        try:
            if os.path.exists('matrix_wallpaper.bmp'):
                time.sleep(1)
                os.remove('matrix_wallpaper.bmp')
        except:
            pass
        
        print("\n" + "="*60)
        print(" "*20 + "СИСТЕМА ВОССТАНОВЛЕНА")
        print("="*60)
        
        if self.root:
            try:
                self.root.quit()
                self.root.destroy()
            except:
                pass
        
        sys.exit(0)

if __name__ == "__main__":
    virus = ChaosVirus()
    try:
        virus.start()
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        virus.stop()
