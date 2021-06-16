import pygame, pygame.surface
import pygame_gui
import globe
from pygame_gui import UIManager
from pygame_gui.elements import UIButton
from pygame_gui.elements import UIWindow
from pygame_gui.elements import UILabel
from pygame_gui.elements import UITextEntryLine
from pygame_gui.elements import UIDropDownMenu
from Emulation.main_Emulation import Emulation
Vector2 = pygame.math.Vector2

SET_FLAG = 0


class Emulation_GUI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Swarm Emulation")
        self.screen = pygame.display.set_mode([840, 765], pygame.DOUBLEBUF)
        self.gui_surface = pygame.surface.Surface([840, 765])
        self.emu_surface = pygame.surface.Surface(globe.RESOLUTION)
        self.emulation = Emulation(self.emu_surface)  # initialize the Emulation object
        self.isInitialized = False
        self.isRunning = True
        self.toBeTerminated = False
        self.settingsWindow = None
        self.manager = UIManager((840, 765))

    def init(self):

        self.start_pause_button = UIButton(pygame.Rect((19, 712), (100, 35)), text="Start/Pause", manager=self.manager)
        self.terminate_button = UIButton(pygame.Rect((129, 712), (100, 35)), text="Terminate", manager=self.manager)
        self.settings_button = UIButton(pygame.Rect((239, 712), (100, 35)), text="Settings", manager=self.manager)
        self.static_label = UILabel(pygame.Rect(590,714,230,31), "Boids Emulator Ver 0.1.2", self.manager)

    def handleScreenUpdate(self):
        if self.isRunning:
            if self.isInitialized:
                self.emulation.update()
                self.screen.blit(self.emu_surface, [20, 20])
            else:
                self.emu_surface.fill((230, 230, 230))
                self.screen.blit(self.emu_surface, [20, 20])
        else:
            self.screen.blit(self.emu_surface, [20, 20])

    def handleParaModification(self):
        pass

    def handleEventProcessing(self, event):
        global SET_FLAG
        if event.type == pygame.QUIT:
            self.isRunning = False
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_pause_button:
                    if not self.isInitialized:
                        self.isInitialized = True
                        self.isRunning = True
                    else:
                        self.isRunning = not self.isRunning
                if event.ui_element == self.terminate_button:
                    self.toBeTerminated = True
                if event.ui_element == self.settings_button:
                    self.settingsWindow = SettingsWindow(pygame.Rect((10, 10), (600, 420)), self.manager)
                    self.isRunning = False
                    self.settings_button.disable()
                if self.settingsWindow and event.ui_element == self.settingsWindow.apply_button:
                    self.settingsWindow.kill()
                    self.handleParaModification()
                    self.emulation.initGroup()

            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                if event.text == "Enemy Group 0":
                    SET_FLAG = 2
                    self.settingsWindow.label_neibRange.set_text("Prey detection range     ")
                    self.settingsWindow.entry_enemRange.disable()
                    self.settingsWindow.label_enemRange.disable()
                else:
                    self.settingsWindow.label_neibRange.set_text("Neighbour detection range")
                    self.settingsWindow.entry_enemRange.enable()
                    self.settingsWindow.label_enemRange.enable()
                if event.text == "Boid Group 0":
                    SET_FLAG = 0
                if event.text == "Boid Group 1":
                    SET_FLAG = 1

            if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                self.isRunning = True
                if event.ui_element == self.settingsWindow:
                    self.settings_button.enable()

        self.manager.process_events(event)

    def run(self):
        self.emulation.initGroup()
        while not self.toBeTerminated:
            time_delta = pygame.time.Clock().tick(60) / 1000.0
            self.gui_surface.fill((128, 128, 128))
            self.screen.blit(self.gui_surface, [0, 0])
            self.handleScreenUpdate()
            for event in pygame.event.get():
                self.handleEventProcessing(event)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)
            pygame.display.update()  # apply the changes and re-render the screen context


class SettingsWindow(UIWindow):
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Settings',
                         object_id='#everything_window',
                         resizable=False)

        self.label_agent = UILabel(pygame.Rect((12, 38), (200, 25)), "Select agent groups", ui_manager, container=self)

        current_resolution_string = "Boid Group 0"
        self.agentMenu = UIDropDownMenu(["Boid Group 0",
                                                   "Boid Group 1",
                                                   "Enemy Group 0",
                                                   ],
                                                  current_resolution_string,
                                                  pygame.Rect((352, 38), (200, 25)),
                                                  ui_manager, container=self)

        self.label_groupSize = UILabel(pygame.Rect((32, 96), (200, 25)), "Size of the agent group  ", ui_manager, container=self)
        self.entry_groupSize = UITextEntryLine(pygame.Rect((352, 96), (200, -1)), self.ui_manager, container=self)

        self.label_maxSpeed = UILabel(pygame.Rect((32, 139), (200, 25)), "Maximum velocity         ", ui_manager, container=self)
        self.entry_maxSpeed = UITextEntryLine(pygame.Rect((352, 139), (200, -1)), self.ui_manager, container=self)

        self.label_maxAcc = UILabel(pygame.Rect((32, 182), (200, 25)), "Maximum acceleration rate", ui_manager, container=self)
        self.entry_maxAcc = UITextEntryLine(pygame.Rect((352, 182), (200, -1)), self.ui_manager, container=self)

        self.label_neibRange = UILabel(pygame.Rect((32, 225), (200, 25)), "Neighbour detection range", ui_manager, container=self)
        self.entry_neibRange = UITextEntryLine(pygame.Rect((352, 225), (200, -1)), self.ui_manager, container=self)

        self.label_enemRange = UILabel(pygame.Rect((32, 268), (200, 25)), "Preditor detection range ", ui_manager, container=self)
        self.entry_enemRange = UITextEntryLine(pygame.Rect((352, 268), (200, -1)), self.ui_manager, container=self)

        self.apply_button = UIButton(pygame.Rect((352, 306), (200, 35)), text="Apply changes", manager=ui_manager, container=self)

    def update(self, time_delta):
        super().update(time_delta)

gui = Emulation_GUI()
gui.init()
gui.run()