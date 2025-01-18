import os, mimetypes, numpy
import PIL.Image
from PySide6 import QtWidgets, QtGui, QtCore



### LAYOUTS ###
class Layout(QtWidgets.QWidget):
    def __init__(self, layout: QtWidgets.QLayout, parent: QtWidgets.QWidget | None = None):
        super(Layout, self).__init__(parent)

        self.lyt = layout
        self.setLayout(layout)

    def addWidgets(self, widgets: list[QtWidgets.QWidget]):
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
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super(HorizontalBoxLayout, self).__init__(QtWidgets.QHBoxLayout(), parent)

class VerticalBoxLayout(Layout):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
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

        def extractSprite(self):
            sprite_top_x = self.getSpriteTopX()
            sprite_top_y = self.getSpriteTopY()
            sprite_bottom_x = self.getSpriteBottomX()
            sprite_bottom_y = self.getSpriteBottomY()

            if sprite_top_x != None and sprite_top_y != None and sprite_bottom_x != None and sprite_bottom_y != None:
                pixels = []

                # get all the sprite's pixels row by row
                y = sprite_top_y

                while y != sprite_bottom_y:
                    row = []

                    x = sprite_top_x

                    while x != sprite_bottom_x:
                        row.append(self.getPixel(x, y))

                        x += 1

                    pixels.append(row)

                    y += 1

                # recreate the sprite using its pixels
                if len(pixels) > 0:
                    pixels = numpy.array(pixels, dtype=numpy.uint8)

                    return PIL.Image.fromarray(pixels)
                else:
                    return None
            else:
                raise IndexError("The bounding box of a sprite in one of the grid squares could not be determined. This could mean that either one or more of the grid squares is empty or the background color provided is incorrect (i.e. a pixel with a color different to the background wasn't found in a grid square).")

    def __init__(self, spriteSheetPath: str, backgroundColor: tuple, progressDialogParent: QtWidgets.QWidget):
        self.sprite_sheet = None
        self.pixels = [] # each pixel will be 4 elements long (RGBA)
        self.background_color = None # (R,G,B,A)

        self.progress_bar_dialog = QtWidgets.QProgressDialog('Scanning Completed', 'Cancel', 0, 100, progressDialogParent, QtCore.Qt.WindowType.FramelessWindowHint)
        self.progress_bar_dialog.setValue(0)

        self.cancel_scan = False
        self.progress_bar_dialog.canceled.connect(self.cancelScan)

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

    def cancelScan(self):
        self.cancel_scan = True

    def getSprites(self, areaToScanStartX: int, areaToScanStartY: int, areaToScanWidth: int, areaToScanHeight: int, gridSquareWidth: int, gridSquareHeight: int) -> list:
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

            # display progress bar dialog
            self.progress_bar_dialog.open()

            # iterate over each grid square and extract its sprite
            num_of_grid_squares_per_row = areaToScanWidth // gridSquareWidth
            num_of_grid_squares_per_column = areaToScanHeight // gridSquareHeight

            total_grid_squares = num_of_grid_squares_per_row * num_of_grid_squares_per_column

            pixel_x = areaToScanStartX
            pixel_y = areaToScanStartY

            right_edge_of_sprite_sheet = areaToScanStartX + areaToScanWidth

            for i in range(total_grid_squares):
                if self.cancel_scan:
                    # stop scanning and end the function abruptly by returning no sprites
                    return []

                grid_square = self.GridSquare(
                    self,
                    pixel_x,
                    pixel_y,
                    gridSquareWidth,
                    gridSquareHeight
                )

                sprite_in_grid_square = grid_square.extractSprite()

                if sprite_in_grid_square != None:
                    sprites.append(sprite_in_grid_square)

                # move to the next grid square in the row
                pixel_x += gridSquareWidth

                # move to the next row
                if pixel_x >= right_edge_of_sprite_sheet:
                    pixel_x = areaToScanStartX
                    pixel_y += gridSquareHeight

                # update progress
                self.progress_bar_dialog.setValue(((i+1) / total_grid_squares) * 100)

            # close progress bar dialog
            self.progress_bar_dialog.accept()

        return sprites

    def close(self):
        if self.sprite_sheet != None:
            self.sprite_sheet.close()

class TutorialWindow(VerticalBoxLayout):
    def __init__(self, parent: QtWidgets.QWidget | None = None):
        super(TutorialWindow, self).__init__(parent)

        self.setFixedWidth(500)
        self.setMinimumHeight(600)
        self.setWindowTitle('Sprite Sheet Packer Tutorial')

        self.setContentsMargins(0,0,0,0)
        self.lyt.setSpacing(0)
        self.lyt.setContentsMargins(0,0,0,0)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)

        scroll_area.setStyleSheet(
            """
            QScrollArea {
                border-radius: 0px;
            }

            QScrollBar {
                width: 4px;
                background-color: transparent;
            }

            QScrollBar::handle {
                background-color: #5f656a;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #383b3f;
            }
            """
        )

        scroll_area_body = VerticalBoxLayout()
        scroll_area_body.setStyleSheet(
            """
                background-color: #383b3f;
                padding-left: 10px;
                padding-right: 30px;
            """
        )

        # TUTORIAL: How to create a packed sprite sheet
        tutorial1 = QtWidgets.QLabel()
        tutorial1.setTextFormat(QtCore.Qt.TextFormat.RichText)
        tutorial1.setWordWrap(True)
        tutorial1.setStyleSheet("""margin-top: 20px;""")

        tutorial1.setText(
            """
            <h2>How to create a packed sprite sheet</h2>

            <ol style="font-size:14px;">
                <li style="margin-bottom:10px;">First create a new project or open an existing one. Click on [File] > [New project] or [File] > [Open project].</li>

                <li style="margin-bottom:10px;">Add sprites to the project by clicking the [Add Sprites] button. Choose whether you want to use sprites from an existing sprite sheet, or prefer to select them individually from your machine.</li>

                <li style="margin-bottom:10px;">Once the sprites list is populated, click the [Pack Sprites] icon button to the right of the [Add Sprites] button.</li>

                <li style="margin-bottom:10px;">Choose the layout for your sprite sheet.</li>

                <li style="margin-bottom:10px;">Wait for the packing to finish after selecting a layout. Either the sprite sheet or its data will appear in the preview (this depends on which preview you have toggled) when it's done.</li>

                <li style="margin-bottom:10px;">To save your new sprite sheet, click on [File] > [Export sprite sheet]. Provide a name for the file and hit save.</li>

                <li>To save its data sheet, click on [File] > [Export data sheet]. Provide a name for the file and hit save.</li>
            </ol>
            """
        )

        # TUTORIAL:
        tutorial2 = QtWidgets.QLabel()
        tutorial2.setTextFormat(QtCore.Qt.TextFormat.RichText)
        tutorial2.setWordWrap(True)
        tutorial2.setStyleSheet("""margin-top: 40px;""")

        tutorial2.setText(
            """
            <h2>How to add sprites using an existing sprite sheet</h2>

            <ol style="font-size:14px;">
                <li style="margin-bottom:10px;">First create a new project or open an existing one. Click on [File] > [New project] or [File] > [Open project].</li>

                <li style="margin-bottom:10px;">Click on the [Add Sprites] button and select the [Sheet] input type.</li>

                <li style="margin-bottom:10px;">Find your sprite sheet and double click on it. This will open up a dialog that asks you for information about your sheet.</li>

                <li style="margin-bottom:10px;">Specify the area to scan. This area determines which part of the sprite sheet to check for sprites. By default, it is set to the entire sprite sheet. The width and height refers to an invisible box on your sprite sheet (i.e. the area to scan). The 'StartX' and the 'StartY' fields is how you move the box in the sprite sheet; the movement is relative to the top left corner of the sheet and is in pixels. Make sure that the box stays within the sheet's edges. If it doesn't, you will either have to resize it or change its position.</li>

                <li style="margin-bottom:10px;">Specify the dimensions of the grid squares on your sprite sheet. It's expected that every grid square has the same dimension and are divided evenly in the sheet (vertically & horizontally).</li>

                <li style="margin-bottom:10px;">Specify the background color of the sprite sheet. This can be done manually by entering an RGB or hex code in the field, or by clicking on the [Auto Find] button which will get the most common color (transparent pixels included).</li>

                <li style="margin-bottom:10px;">Specify the background color's opacity in percentage. Note that the [Auto Find] button will fill this in.</li>

                <li>Click the [Start Scan] button and wait for the sprites list to be populated.</li>
            </ol>
            """
        )

        scroll_area_body.addWidgets([
            tutorial1,
            tutorial2
        ])

        scroll_area.setWidget(scroll_area_body)

        self.lyt.addWidget(scroll_area)