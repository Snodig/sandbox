
'''
 * Date: 17-02-28
 * Desc: The entry-point of our program
 * Author: Collaboration
'''

import time
import pygame
from pygame.locals import *
from os import environ
import Drawables


class Game:
    '''
     * A class is an idea in object-oriented programming, and is a construct which encapsulates functions and variables.
     * Functions and variables that belong to a class are often called methods and members.
    '''

    # This is python's concept of a constructor; a function automatically called when creating an instance of a class.
    # The job of a class' constructor is to initialize all members to their default values and make the class ready for use.
    # The opposite of a constructor is a destructor (mandatory in C++) or a finalizer (in java, which has both).
    def __init__(self):
        self.fullscreen = True
        self.running = False

        # Python has no concept of member visibility (public, private, protected), but naming-conventions dictate
        # that members whose names start with '_' are private (and '__' are super-private, for some reason).
        # Member visibility is big in languages like C++, C#, and java, and are there to ensure no-one messes with
        # variables (or calls functions) they are not supposed to be messing with. Such members are dubbed 'private' to the class.
        self._screen = None
        self._start_time = time.mktime(time.localtime())
        self._loop_start = time.time()
        self._fps = 0
        self.drawables = list()

    # The on_setup function is an addition to the constructor, and will initialize any members that depend on the class
    # being memory-stable and well-defined before being set. In our case, we use it to set up the game-window.
    def on_setup(self):

        # Note that 'self' is passed to all member-functions in python.
        # This is how python handles object-orienting in general.
        # Other languages may use 'this', which always refers to the object that owns the function, or, like C++,
        # many languages will let you interact with members simply by their unique name within the class-'scope'.
        self._running = True

        environ['SDL_VIDEO_CENTERED'] = '1'

        # pygame is a simple game-framework that uses SDL to draw it's graphics.
        pygame.init()
        pygame.display.set_caption("Yuge Game")
        pygame.mouse.set_visible(False)

        self.size = self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.background = Drawables.Drawable("Resources/background.jpg")
        self.mousePointer = Drawables.MousePointer()

        self.toggleFullScreen()

        # Python will let you return just about anything from a function call, while most other languages
        # will only allow you to return one pre-declared type as return-values.
        # Python uses what's known as 'dynamic typing' (aka duck-typing), like javascript.
        return self._running

    # start is our 'run'-function for the game class.
    # It owns the main game-loop and game timers.
    def start(self):

        oneSecond = 0
        numFrames = 0

        if not self.on_setup():
            self._running = False

        # Unlike some languages, python doesn't surround conditions (while, for, if) with parentheses.
        # It's syntactically legal, but neither necessary nor encouraged in python.
        while self._running:

            # I honestly can't remember why this check is here, but could be to prevent CPU-burn.
            if self.getLoopTime() > 0.003:  # Should probably be replaced with pygame.Clock

                # print("Current loop took " + str(self.getLoopTime()) + " seconds")
                oneSecond += self.getLoopTime()
                if oneSecond > 1:
                    self._fps = numFrames
                    oneSecond = 0
                    numFrames = 0

                self._loop_start = time.time()
                # The sequencing here is important!
                # We must first see if there is user-input or other events, since they influence our updates to acceleration etc.
                # Then we need to move objects around, speed them up or start an animation.
                # Finally we can draw our entire screen, including all our events and updates since the last frame.
                for event in pygame.event.get():
                    self.on_event(event)
                self.on_update()
                self.on_render()
                numFrames += 1  # We've successfully completed one frame

    # This style of function/variable naming is called 'lowerCamelCasing'.
    def addDrawable(self, drawable):
        self.drawables.append(drawable)

    # This function returns how long this loop has taken so far.
    def getLoopTime(self):
        return time.time() - self._loop_start

    # Returns the total running-time of the game, in seconds.
    def getRunningTime(self):
        localSeconds = time.mktime(time.localtime())
        elapsed = localSeconds - self.__start_time
        return elapsed

    # Event-handler, called whenever an event is available from pygame.
    def on_event(self, event):

        if event.type == QUIT:
            self._running = False

        # A key has been pressed (but no released)
        elif event.type == KEYDOWN:
            print("Key dn: " + pygame.key.name(event.key))

            if event.key == K_ESCAPE:
                self._running = False

            if pygame.key.get_mods() & KMOD_ALT and event.key == K_RETURN:
                self.toggleFullScreen()

        # A key has been released
        elif event.type == KEYUP:
            print("Key up: " + pygame.key.name(event.key))

        elif event.type == MOUSEMOTION:
            self.mousePointer.move(event.pos, event.rel)

        # LMouse down
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            for drawable in self.drawables:
                if drawable.rect.collidepoint(event.pos):
                    self.mousePointer.grab(drawable)
                    break

        # LMouse up
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            self.mousePointer.drop()

        # Middle mouse down
        elif event.type == MOUSEBUTTONDOWN and event.button == 2:
            # 'pass' is a python-exclusive keyword used to tell the interpreter that this scope has no code (yet?).
            # Simply ignore this case and keep executing.
            pass

        # RMouse down
        elif event.type == MOUSEBUTTONDOWN and event.button == 3:
            pass

    # Instruct our actors to update themselves.
    # It's common to pass the elapsed time to each actor, so they move synchronously.
    def on_update(self):
        # This type of for-loop is also called a 'for-each' loop.
        for drawable in self.drawables:
            drawable.update()

    # Use pygame to draw sprites onto the screen
    def on_render(self):
        # Draw the background
        self.background.draw(self.screen)

        # Draw other actors
        for drawable in self.drawables:
            drawable.draw(self.screen)

        # Draw the fps-counter
        font = pygame.font.SysFont("copperplate gothic", 35)
        fpsLabel = font.render("FPS: " + str(self._fps), 1, (255, 255, 0))
        self.screen.blit(fpsLabel, (10, 10))  # 'Blit' is a term meaning to draw onto the current inactive buffer

        # Draw our custom mouse-pointer
        self.mousePointer.draw(self.screen)

        # We switch between one active and one inactive buffer (double-buffering)
        pygame.display.flip()

    # Switch between windowed and frameless fullscreen, and reinitialize our background.
    def toggleFullScreen(self):

        self.fullscreen = not self.fullscreen
        print("ToggleFullScreen: " + str(self.fullscreen))

        if self.fullscreen:
            self.size = self.width, self.height = 1920, 1080
            self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.NOFRAME)
        else:
            self.size = (800, 600)
            # self.size = self.width, self.height = 800, 600
            self.screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        # We draw a blank (black) canvas first, to avoid issues with alpha-channels.
        # Our actual background will be self.background painted on top of self.bg.
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg = self.bg.convert()
        self.bg.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))

        self.background.rect = self.screen.get_rect()
        self.background.rescale(size=self.size)

    # I'm not sure we actually need this
    def on_cleanup(self):
        self._running = False
        pygame.quit()
