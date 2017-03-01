
'''
 * Date: 14-12-16
 * Desc: All Surface-holding objects
 * Comments: Obviously, this is snatched from my vtes-client, and needs to be tidied.
 * Author: H. Skjevling
'''
import pygame


def loadImage(fileName):
    try:
        image = pygame.image.load(fileName)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error:
        print("Could not load image: " + fileName)
        raise

    return image, image.get_bounding_rect()


class Drawable(pygame.sprite.Sprite):  # Should we just use Surface?

    def __init__(self, imageFile):
        pygame.sprite.Sprite.__init__(self)
        self.imageFile = imageFile
        # print("Loading: " + self.imageFile)
        self.image, self.rect = loadImage(self.imageFile)
        self.originalImage = self.image.copy()
        self.rotation = 0.0
        self.highlit = False

    def move(self, rel):
        self.rect.move_ip(rel)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        pygame.event.pump()

    def resetScale(self):
        self.rescale(size=self.originalImage.get_bounding_rect().size)

    # Size overrides ratio
    # Sets absolute size or multiplies current size by ratio
    def rescale(self, size: tuple=None, scaleRatio: float=None):
        center = self.rect.center
        if size is not None:
            self.rect.size = size
        elif scaleRatio is not None:
            # print("Rescaling " + self.imageFile + " by a ratio of " + str(scaleRatio))
            size = (self.rect.size[0] * scaleRatio, self.rect.size[1] * scaleRatio)

            # This is totally fucked and needs to be fixed
            if type(self) == Card:
                if self.is_tapped:
                    size = (self.rect.size[1] * scaleRatio, self.rect.size[0] * scaleRatio)

            self.rect.size = size
        else:
            self.resetScale()
            return

        self.recalcDimensions()
        self.rect.center = center

    def rotate(self, angle):
        center = self.rect.center
        self.rotation += angle
        self.recalcDimensions()
        self.rect.center = center

    # Image rect is stretched to orthogonally fit the new surface
    # In other words, this only works perfectly for rectangular images!
    def recalcDimensions(self):
        self.image = pygame.transform.scale(self.originalImage, self.rect.size)
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_bounding_rect()

    def highlight(self, highlight_onOff):
        if self.highlit == highlight_onOff:
            highlight_onOff = False

        if highlight_onOff:
            self.rescale(scaleRatio=2.0)
        else:
            self.resetScale()
        self.highlit = highlight_onOff


s_orignalCardSize = (363, 513)
s_defaultCardSize = (int(363 / 2), int(513 / 2))


class Card(Drawable):

    def __init__(self, file_name):
        Drawable.__init__(self, file_name)
        self.is_tapped = False
        self.resetScale()

    def resetScale(self):
        Drawable.resetScale(self)
        self.rescale(size=s_defaultCardSize)

    def tap(self):  # Bug: When tapped, collision is still done on the original rect for some reason
        if not self.is_tapped:
            self.rotate(-90)
            self.is_tapped = True

    def untap(self):
        if self.is_tapped:
            center = self.rect.center
            self.rotate(90)
            self.resetScale()
            self.rect.center = center
            self.is_tapped = False

    def toggleTap(self):
        if self.is_tapped:
            self.untap()
        else:
            self.tap()

    def flip(self):
        pass


class MousePointer(Drawable):

    def __init__(self):
        Drawable.__init__(self, "Resources/blooddrop.png")
        self.rotate(-135.0)
        self.rescale(scaleRatio=0.1)
        self.grabbed = None
        self.highlit = None

    def grab(self, item):
        if type(item) == Card:
            self.grabbed = item
            if self.grabbed == self.highlit:
                self.highlight(None)
            # print("Mousepointer grabbed: " + str(self.imageFile))
            item.rescale(scaleRatio=1.1)

    def drop(self):
        if self.grabbed is not None:
            # print("Mousepointer dropped: " + str(self.imageFile))

            if type(self.grabbed) == Card:
                self.grabbed.resetScale()  # Should probably be moved to the Card class (drop())
            self.grabbed = None

    def move(self, pos, rel):
        self.rect.topleft = (pos[0] - 10, pos[1] - 10)

        if self.grabbed is not None:
            self.grabbed.move(rel)

    def highlight(self, item):
        if self.highlit is not None and item is None:
            self.highlit.highlight(False)

        self.highlit = item
        if item is not None:
            item.highlight(True)

    def recalcDimensions(self):
        self.image = pygame.transform.scale(self.originalImage, self.rect.size)
        self.image = pygame.transform.rotate(self.image, self.rotation)


class InfoPanel(Drawable):

    def __init__(self, infoDict: dict):
        self.dict = infoDict


class CardPreview(InfoPanel):

    def __init__(self, card: Card):
        InfoPanel.__init__(self)
