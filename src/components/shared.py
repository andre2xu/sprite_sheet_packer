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
    class GridSquare():
        def __init__(self, spriteSheetClass, topX: int, topY: int, width: int, height: int):
            self.sprite_sheet_class = spriteSheetClass

            self.grid_top_x = topX
            self.grid_top_y = topY
            self.grid_width = width
            self.grid_height = height

        def getPixel(self, x: int, y: int):
            index = (self.sprite_sheet_class.sprite_sheet.width * y) + x

            return self.sprite_sheet_class.pixels[index]

        def getSpriteTopX(self):
            sprite_top_x = None

            x = self.grid_top_x
            last_x = self.grid_top_x + (self.grid_width - 1)
            last_y = self.grid_top_y + (self.grid_height - 1)

            # scan the grid square column by column (left to right) until the first non-background pixel is found
            while x != last_x:
                y1 = self.grid_top_y
                y2 = last_y

                while y1 <= y2:
                    top_column_pixel = self.getPixel(x, y1)

                    if top_column_pixel != self.sprite_sheet_class.background_color:
                        sprite_top_x = x
                        break

                    if y1 != y2:
                        bottom_column_pixel = self.getPixel(x, y2)

                        if bottom_column_pixel != self.sprite_sheet_class.background_color:
                            sprite_top_x = x
                            break

                    y1 += 1
                    y2 -= 1

                if sprite_top_x != None:
                    break

                x += 1

            return sprite_top_x

        def getSpriteTopY(self):
            sprite_top_y = None

            y = self.grid_top_y
            last_x = self.grid_top_x + (self.grid_width - 1)
            last_y = self.grid_top_y + (self.grid_height - 1)

            # scan the grid square row by row (top to bottom) until the first non-background pixel is found
            while y != last_y:
                x1 = self.grid_top_x
                x2 = last_x

                while x1 <= x2:
                    left_row_pixel = self.getPixel(x1, y)

                    if left_row_pixel != self.sprite_sheet_class.background_color:
                        sprite_top_y = y
                        break

                    if x1 != x2:
                        right_row_pixel = self.getPixel(x2, y)

                        if right_row_pixel != self.sprite_sheet_class.background_color:
                            sprite_top_y = y
                            break

                    x1 += 1
                    x2 -= 1

                if sprite_top_y != None:
                    break

                y += 1

            return sprite_top_y

        def getSpriteBottomX(self):
            sprite_bottom_x = None

            x = self.grid_top_x + (self.grid_width - 1)
            last_x = self.grid_top_x
            last_y = self.grid_top_y + (self.grid_height - 1)

            # scan the grid square column by column (right to left) until the first non-background pixel is found
            while x != last_x:
                y1 = self.grid_top_y
                y2 = last_y

                while y1 <= y2:
                    top_column_pixel = self.getPixel(x, y1)

                    if top_column_pixel != self.sprite_sheet_class.background_color:
                        sprite_bottom_x = x
                        break

                    if y1 != y2:
                        bottom_column_pixel = self.getPixel(x, y2)

                        if bottom_column_pixel != self.sprite_sheet_class.background_color:
                            sprite_bottom_x = x
                            break

                    y1 += 1
                    y2 -= 1

                if sprite_bottom_x != None:
                    break

                x -= 1

            return sprite_bottom_x

        def getSpriteBottomY(self):
            sprite_bottom_y = None

            y = self.grid_top_y + (self.grid_height - 1)
            last_x = self.grid_top_x + (self.grid_width - 1)
            last_y = self.grid_top_y

            # scan the grid square row by row (bottom to top) until the first non-background pixel is found
            while y != last_y:
                x1 = self.grid_top_x
                x2 = last_x

                while x1 <= x2:
                    left_row_pixel = self.getPixel(x1, y)

                    if left_row_pixel != self.sprite_sheet_class.background_color:
                        sprite_bottom_y = y
                        break

                    if x1 != x2:
                        right_row_pixel = self.getPixel(x2, y)

                        if right_row_pixel != self.sprite_sheet_class.background_color:
                            sprite_bottom_y = y
                            break

                    x1 += 1
                    x2 -= 1

                if sprite_bottom_y != None:
                    break

                y -= 1

            return sprite_bottom_y

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

        if self.sprite_sheet != None and type(self.pixels) == list and len(self.pixels) > 0 and self.background_color != None:
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

            # iterate over each grid square and extract its sprite
            num_of_grid_squares_per_row = areaToScanWidth // gridSquareWidth
            num_of_grid_squares_per_column = areaToScanHeight // gridSquareHeight

            total_grid_squares = num_of_grid_squares_per_row * num_of_grid_squares_per_column

            pixel_x = 0
            pixel_y = 0

            for _ in range(total_grid_squares):
                grid_square = self.GridSquare(
                    self,
                    pixel_x,
                    pixel_y,
                    gridSquareWidth,
                    gridSquareHeight
                )

                # move to the next grid square in the row
                pixel_x += gridSquareWidth

                # move to the next row
                if pixel_x >= areaToScanWidth:
                    pixel_x = 0
                    pixel_y += gridSquareHeight

        return sprites

    def close(self):
        if self.sprite_sheet != None:
            self.sprite_sheet.close()
