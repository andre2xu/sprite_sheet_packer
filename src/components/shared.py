import os, mimetypes, PIL
import PIL.Image
from PySide6 import QtWidgets, QtGui



### LAYOUTS ###
class Layout(QtWidgets.QWidget):
    def __init__(self, layout: QtWidgets.QLayout, parent=None):
        super(Layout, self).__init__(parent)

        self.lyt = layout
        self.setLayout(layout)

    def addWidgets(self, widgets: list):
        for i in range(len(widgets)):
            self.lyt.addWidget(widgets[i])

    def paintEvent(self, _):
        # NOTE: this method is needed for stylesheets to work when inheriting QWidget (source: https://stackoverflow.com/questions/18344135/why-do-stylesheets-not-work-when-subclassing-qwidget-and-using-q-object)

        style_option = QtWidgets.QStyleOption()
        style_option.initFrom(self)

        painter = QtGui.QPainter(self)

        self.style().drawPrimitive(
            QtWidgets.QStyle.PrimitiveElement.PE_Widget,
            style_option,
            painter,
            self
        )

class HorizontalBoxLayout(Layout):
    def __init__(self, parent=None):
        super(HorizontalBoxLayout, self).__init__(QtWidgets.QHBoxLayout(), parent)

class VerticalBoxLayout(Layout):
    def __init__(self, parent=None):
        super(VerticalBoxLayout, self).__init__(QtWidgets.QVBoxLayout(), parent)



### MISCELLANEOUS ###
class SpriteSheet():
    def __init__(self, spriteSheetPath: str, backgroundColor: tuple):
        self.sprite_sheet = None
        self.pixels = [] # each pixel will be 4 elements long (RGBA)
        self.background_color = None # (R,G,B,A)

        if os.path.exists(spriteSheetPath):
            # validate the sprite sheet file
            file_name = os.path.basename(spriteSheetPath)
            extension = os.path.splitext(file_name)[1]
            mime_type = mimetypes.guess_type(file_name)[0]

            if (extension == '.png' or extension == '.jpg' or extension == '.jpeg') and (mime_type == 'image/png' or mime_type == 'image/jpg' or mime_type == 'image/jpeg'):
                self.sprite_sheet = PIL.Image.open(spriteSheetPath)
                self.sprite_sheet.convert('RGBA')
                self.pixels = list(self.sprite_sheet.getdata())
            else:
                raise Exception("Invalid sprite sheet. Must be a png or jpeg image.")

            # validate the background color data
            if type(backgroundColor) == tuple and len(backgroundColor) == 4 and all(type(backgroundColor[i]) == int and backgroundColor[i] >= 0 and backgroundColor[i] <= 255 for i in range(len(backgroundColor))):
                self.background_color = backgroundColor
            else:
                raise Exception("Invalid background color. Must be a tuple with RGBA values between 0 and 255.")
        else:
            raise FileNotFoundError("The sprite sheet could not be found. Please make sure you're passing a valid path to an existing file.")

    def getSprites(self, areaToScanWidth: int, areaToScanHeight: int, gridSquareWidth: int, gridSquareHeight: int) -> list:
        sprites = []

        if self.sprite_sheet != None:
            # validate area to scan dimensions
            if areaToScanWidth < 1 or areaToScanHeight < 1:
                raise ValueError("The width and height of the area to scan cannot be less than 1.")
            elif areaToScanWidth > self.sprite_sheet.width:
                raise IndexError("The area to scan width cannot exceed the sprite sheet's width.")
            elif areaToScanHeight > self.sprite_sheet.height:
                raise IndexError("The area to scan height cannot exceed the sprite sheet's height.")

            # validate grid square dimensions
            if gridSquareWidth < 1 or gridSquareHeight < 1:
                raise ValueError("The grid square width and height cannot be less than 1.")
            elif areaToScanWidth % gridSquareWidth != 0:
                raise IndexError("The grid square width does not divide evenly into the width of the area to scan. This means that there are either too many horizontal pixels, in one or more of the squares, or too few.")
            elif areaToScanHeight % gridSquareHeight != 0:
                raise IndexError("The grid square height does not divide evenly into the height of the area to scan. This means that there are either too many vertical pixels, in one or more of the squares, or too few.")

        return sprites

    def close(self):
        if self.sprite_sheet != None:
            self.sprite_sheet.close()
