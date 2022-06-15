import os
import platform
import ctypes
from ctypes import wintypes


try:
    import PIL
except ImportError:
    os.system("pip install Pillow")

try:
    import pyautogui
except ImportError:
    os.system("pip install pyautogui")

try:
    from pynput import keyboard
    from pynput.keyboard import Key, Controller
except ImportError:
    os.system("pip install pynput")

import pygame

def take_screenshot(name="screenshot.png"):
    pyautogui.screenshot(name)

class Game:
    def __init__(self):
        self.movelimit = 30
        self.delay = 30

        self.inf = pygame.display.Info()
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.sprites = pygame.sprite.Group()

        self.hwnd = pygame.display.get_wm_info()['window']
        self.user32 = ctypes.WinDLL("user32")

        self.font = pygame.font.SysFont("Calibri", 110)

        self.showtime = True

        self.keyboard = Controller()

    def on_press(self, key):
        if key == Key.ctrl_l or key == Key.ctrl_r:
            self.keyboard.release(key)

    def on_release(self, key):
        pass

    def run(self):
        Image("screenshot.png", (0, 0), self.size(), self.allsprites())
        self.screen = pygame.display.set_mode((0, 35), pygame.NOFRAME)
        self.done = False
        self.keylistener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.keylistener.start()
        while not self.done:
            self.ontop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.done = True
            self.screen.fill((0, 0, 0))
            self.sprites.draw(self.screen)
            pygame.display.flip()
        pygame.quit()
        self.keylistener.stop()
        self.keylistener.join()

    def allsprites(self):
        return self.sprites

    def size(self):
        return (self.inf.current_w, self.inf.current_h)

    def ontop(self):
        self.user32.SetWindowPos.restype = wintypes.HWND
        self.user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
        self.user32.SetWindowPos(self.hwnd, -1, 0, 0, 0, 0, 0x0001)

class Image(pygame.sprite.Sprite):
    def __init__(self, image, position, size, *groups):
        super().__init__(*groups)
        self.image = pygame.transform.scale(pygame.image.load(image), size)
        self.rect = self.image.get_rect()
        self.rect.topleft = position

class PressedKeys:
    def __init__(self):
        self.keyboard = Controller()
    def on_press(self, key, *args):        
        if key == Key.insert:
            take_screenshot()
            pygame.init()
            game = Game()
            game.run()
            if os.path.exists("screenshot.png"):
                os.remove("screenshot.png")

    def on_release(self, key):
        pass

    

if __name__ == "__main__":
    if platform.system() == "Windows":
        pressed = PressedKeys()
        keylistener = keyboard.Listener(
            on_press=pressed.on_press,
            on_release=pressed.on_release)
        keylistener.start()
        keylistener.join()
