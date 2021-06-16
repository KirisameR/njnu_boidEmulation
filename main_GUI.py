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
    """
    DESCRIPTION:
        @author  Yi Lu
        @version 0.2.1
        @desc    A class responsible for holding the fundamental context of the entire GUI

        Method 'handleScreenUpdate': A helper responsible for updating the Emulation sub-surface based on the specified current state
        Method 'handleparaModification': A helper responsible for decompose the user input from the text entry lines of the settings sub-window, and generate some generalized
                                         properties for each agent groups
        Method 'handleEventProcessing': A helper responsible for controling the behaviour based on the corresponding event

    """
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Swarm Emulation")
        self.screen = pygame.display.set_mode([840, 765], pygame.DOUBLEBUF)
        self.gui_surface = pygame.surface.Surface([840, 765])
        self.emu_surface = pygame.surface.Surface(globe.RESOLUTION)
        globe.init()
        self.backup_settings = {"Boids": globe.boids_property, "Enemy": globe.enemy_property}
        self.settings = self.backup_settings
        self.emulation = Emulation(self.emu_surface, self.settings)  # initialize the Emulation object
        self.isInitialized = False
        self.isRunning = True
        self.toBeTerminated = False
        self.settingsWindow = None
        self.manager = UIManager((840, 765))


        # build basic UX controls
        self.start_pause_button = UIButton(pygame.Rect((19, 712), (100, 35)), text="Start/Pause", manager=self.manager)
        self.terminate_button = UIButton(pygame.Rect((129, 712), (100, 35)), text="Terminate", manager=self.manager)
        self.settings_button = UIButton(pygame.Rect((239, 712), (100, 35)), text="Settings", manager=self.manager)
        self.static_label = UILabel(pygame.Rect(590, 714, 230, 31), "Boids Emulator Ver 0.1.2", self.manager)

    def handleScreenUpdate(self):
        """
        A helper responsible for updating the Emulation sub-surface based on the specified current state
        """
        # only update the sub-screen when the emulation is running (not paused)
        if self.isRunning:
            if self.isInitialized:  # we render the sub-screen by calling its own update method if the emulation has been initialized
                self.emulation.update()
                self.screen.blit(self.emu_surface, [20, 20])
            else:                   # if the emulation is not initialized yet, we render an empty screen
                self.emu_surface.fill((230, 230, 230))
                self.screen.blit(self.emu_surface, [20, 20])
        else:
            self.screen.blit(self.emu_surface, [20, 20])

    def handleParaModification(self):
        """
        A helper responsible for decompose the user input from the text entry lines of the settings sub-window, and generate some generalized
        properties for each agent groups
        """
        globe.boids_property = self.settings["Boids"]
        globe.enemies_property = [self.settings["Enemy"]]

    def handleEventProcessing(self, event):
        """
        A helper responsible for controling the behaviour based on the corresponding event
        It interprets: 1. button-pressing behaviour either in the main window or the settings sub-window
                       2. drop-down menu changes in the settings sub-window
                       3. the different closing ways of the settings sub-window
        :param event: the event received to be justified
        """
        global SET_FLAG     # declare the usage of the global flag
        if event.type == pygame.QUIT:       # case: the GUI stop running
            self.isRunning = False
        if event.type == pygame.USEREVENT:  # consider userevents
            # take care of button-pressings
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.start_pause_button:     # start/pause button
                    if not self.isInitialized:          # check whether the emulation has been initialized or not
                        self.isInitialized = True
                        self.isRunning = True
                    else:
                        self.isRunning = not self.isRunning
                if event.ui_element == self.terminate_button:       # terminate button
                    self.toBeTerminated = True
                if event.ui_element == self.settings_button:        # settings button
                    self.settingsWindow = SettingsWindow(pygame.Rect((10, 10), (600, 420)), self.manager)
                    # and intialize entry context
                    self.settingsWindow.entry_groupSize.set_text(str(self.settings["Boids"][SET_FLAG]["GROUP_SIZE"]))
                    self.settingsWindow.entry_maxSpeed.set_text(str(self.settings["Boids"][SET_FLAG]["MAX_SPEED"]))
                    self.settingsWindow.entry_maxAcc.set_text(str(self.settings["Boids"][SET_FLAG]["MAX_ACC"]))
                    self.settingsWindow.entry_neibRange.set_text(str(float(self.settings["Boids"][SET_FLAG]["NEIGHBOR_DIST"])))
                    self.settingsWindow.entry_enemRange.set_text(str(float(self.settings["Boids"][SET_FLAG]["ENEMY_DIST"])))
                    self.isRunning = False                          # pause emulation running when open settings
                    self.settings_button.disable()
                if self.settingsWindow and event.ui_element == self.settingsWindow.apply_button:
                    self.settingsWindow.kill()                      # save any modified params if the user close the window using 'save' button
                    self.handleParaModification()
                    globe.init()
                    self.emulation = Emulation(self.emu_surface, self.settings)
                    self.emulation.initGroup(self.settings)  # initialize the emulation at the very beginning
                if self.settingsWindow and event.ui_element == self.settingsWindow.save_button:
                    if SET_FLAG == 0 or SET_FLAG == 1:
                        tmp_properties = self.settings["Boids"][SET_FLAG]
                        tmp_properties["GROUP_SIZE"] = int(self.settingsWindow.entry_groupSize.get_text())
                        tmp_properties["MAX_SPEED"] = float(self.settingsWindow.entry_maxSpeed.get_text())
                        tmp_properties["MAX_ACC"] = float(self.settingsWindow.entry_maxAcc.get_text())
                        tmp_properties["NEIGHBOR_DIST"] = float(self.settingsWindow.entry_neibRange.get_text())
                        tmp_properties["ENEMY_DIST"] = float(self.settingsWindow.entry_enemRange.get_text())
                        self.settings["Boids"][SET_FLAG] = tmp_properties
                    else:
                        tmp_properties = self.settings["Enemy"]
                        tmp_properties["GROUP_SIZE"] = int(self.settingsWindow.entry_groupSize.get_text())
                        tmp_properties["MAX_SPEED"] = float(self.settingsWindow.entry_maxSpeed.get_text())
                        tmp_properties["MAX_ACC"] = float(self.settingsWindow.entry_maxAcc.get_text())
                        tmp_properties["DETECT_DIST"] = float(self.settingsWindow.entry_neibRange.get_text())
                        self.settings["Enemy"] = tmp_properties

            # take care of the changing of drop-down menus
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
                # we need to: 1. save changes in the entry lines 2. initialize the context of the entry lines
                if event.text == "Enemy Group 0":
                    SET_FLAG = 2
                    self.settingsWindow.label_neibRange.set_text("Prey detection range     ")
                    self.settingsWindow.entry_enemRange.disable()
                    self.settingsWindow.label_enemRange.disable()
                    self.settingsWindow.entry_groupSize.set_text(str(self.settings["Enemy"]["GROUP_SIZE"]))
                    self.settingsWindow.entry_maxSpeed.set_text(str(self.settings["Enemy"]["MAX_SPEED"]))
                    self.settingsWindow.entry_maxAcc.set_text(str(self.settings["Enemy"]["MAX_ACC"]))
                    self.settingsWindow.entry_neibRange.set_text(str(self.settings["Enemy"]["DETECT_DIST"]))
                else:
                    if event.text == "Boid Group 0":
                        SET_FLAG = 0
                    if event.text == "Boid Group 1":
                        SET_FLAG = 1
                    self.settingsWindow.label_neibRange.set_text("Neighbour detection range")
                    self.settingsWindow.entry_enemRange.enable()
                    self.settingsWindow.label_enemRange.enable()

                    self.settingsWindow.entry_groupSize.set_text(str(self.settings["Boids"][SET_FLAG]["GROUP_SIZE"]))
                    self.settingsWindow.entry_maxSpeed.set_text(str(self.settings["Boids"][SET_FLAG]["MAX_SPEED"]))
                    self.settingsWindow.entry_maxAcc.set_text(str(self.settings["Boids"][SET_FLAG]["MAX_ACC"]))
                    self.settingsWindow.entry_neibRange.set_text(str(float(self.settings["Boids"][SET_FLAG]["NEIGHBOR_DIST"])))
                    self.settingsWindow.entry_enemRange.set_text(str(float(self.settings["Boids"][SET_FLAG]["ENEMY_DIST"])))

            if event.user_type == pygame_gui.UI_WINDOW_CLOSE:
                self.isRunning = True
                if event.ui_element == self.settingsWindow:
                    self.settings_button.enable()

        self.manager.process_events(event)

    def run(self):
        """
        responsible for refreshing the screen and keep the GUI interact with the user
        """

        self.emulation.initGroup(self.settings)      # initialize the emulation at the very beginning
        while not self.toBeTerminated:  # keep refreshing the screen in 60fps when not terminated
            time_delta = pygame.time.Clock().tick(60) / 1000.0
            self.gui_surface.fill((128, 128, 128))      # fill the background surface with a grey color
            self.screen.blit(self.gui_surface, [0, 0])  # and render it
            self.handleScreenUpdate()   # call the helper for rendering the emulation sub-screen
            for event in pygame.event.get():    # and perform event-handlings
                self.handleEventProcessing(event)
            self.manager.update(time_delta)
            self.manager.draw_ui(self.screen)   # render the settings window or buttons related to GUI controls
            pygame.display.update()  # apply the changes and re-render the screen context


class SettingsWindow(UIWindow):
    """
    DESCRIPTION:
        @author  Yi Lu
        @desc    A class responsible for constructing the settings sub-window
    """
    def __init__(self, rect, ui_manager):
        super().__init__(rect, ui_manager,
                         window_display_title='Settings',
                         object_id='#everything_window',
                         resizable=False)

        self.label_agent = UILabel(pygame.Rect((12, 38), (200, 25)), "Select agent groups", ui_manager, container=self)

        current_resolution_string = "Boid Group 0"
        self.agentMenu = UIDropDownMenu(["Boid Group 0", "Boid Group 1", "Enemy Group 0"], current_resolution_string, pygame.Rect((352, 38), (200, 25)), ui_manager, container=self)

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

        self.save_button = UIButton(pygame.Rect((352, 315), (100, 35)), text="Save", manager=ui_manager, container=self)
        self.apply_button = UIButton(pygame.Rect((452, 315), (100, 35)), text="Apply All", manager=ui_manager, container=self)

        # make sure only valid user inputs will be accepted by the entries
        self.entry_groupSize.set_allowed_characters("numbers")
        self.entry_maxSpeed.set_allowed_characters(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])
        self.entry_maxAcc.set_allowed_characters(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])
        self.entry_neibRange.set_allowed_characters(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])
        self.entry_enemRange.set_allowed_characters(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."])

    def update(self, time_delta):
        super().update(time_delta)


if __name__ == '__main__':
    gui = Emulation_GUI()
    gui.run()