import pathlib
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy



class PreviewButtons(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PreviewButtons, self).__init__(parent)

        self.setObjectName('SSPB') # id for styling
        self.setMinimumWidth(200)
        self.move(10,10) # move down diagonally right (i.e. increase space between buttons and the menubar as well as the left edge of window)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        ICONS_FOLDER_PATH = f'{pathlib.Path(__file__).parent.resolve()}/../../local/icons'

        self.preview_sprite_sheet_button = QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_icon.png'), '')
        self.preview_data_sheet_button = QtWidgets.QPushButton('</>')
        self.zoom_out_button = QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_zoom_out_icon.png'), '')
        self.zoom_in_button = QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_zoom_in_icon.png'), '')

        preview_buttons = [
            self.preview_sprite_sheet_button,
            self.preview_data_sheet_button,
            self.zoom_out_button,
            self.zoom_in_button
        ]

        # add a tooltip to each of the buttons
        self.preview_sprite_sheet_button.setToolTip('Preview Sprite Sheet')
        self.preview_data_sheet_button.setToolTip('Preview Data Sheet')
        self.zoom_out_button.setToolTip('Zoom Out')
        self.zoom_in_button.setToolTip('Zoom In')

        # configure the buttons & add them to the container
        for i in range(len(preview_buttons)):
            button = preview_buttons[i]
            button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
            button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            button.setToolTipDuration(1000 * 3)

            layout.addWidget(button)



class ScrollableArea(QtWidgets.QScrollArea):
    def __init__(self, parent=None):
        super(ScrollableArea, self).__init__(parent)

        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.setWidgetResizable(False) # make the scrollable area resize according to its body widget, not the other way around

        self.scroll_area_body = QtWidgets.QWidget()
        self.scroll_area_body.setMinimumSize(self.width() * 2, self.height() * 2)
        self.setWidget(self.scroll_area_body)

        self.image_widget = QtWidgets.QLabel(' ', self.scroll_area_body)

        # re-scroll to the center if the scrollable distances change (e.g. when image is changed)
        self.horizontalScrollRangeChanged = False
        self.verticalScrollRangeChanged = False
        self.horizontalScrollBar().rangeChanged.connect(lambda: self.scrollRangeChangedHorizontally())
        self.verticalScrollBar().rangeChanged.connect(lambda: self.scrollRangeChangedVertically())

    def rescaleScrollableAreaBody(self):
        self.scroll_area_body.resize(self.width() * 2, self.height() * 2) # make the scrollable area's body widget twice its size so that the scrollbars appear

        centerX = self.scroll_area_body.width() // 2
        centerY = self.scroll_area_body.height() // 2
        self.image_widget.move(centerX - (self.image_widget.width() // 2), centerY - (self.image_widget.height() // 2))

        self.scrollToCenter()

    def displayImage(self, imagePath: str):
        self.image_widget.clear()
        self.image_widget.setText('') # remove placeholder text
        self.image_widget.setPixmap(QtGui.QPixmap(imagePath))
        self.image_widget.adjustSize() # ensure the widget's size data matches the dimensions of the rendered image
        self.image_widget.setScaledContents(True) # scale pixmap with image

        self.horizontalScrollRangeChanged = True
        self.verticalScrollRangeChanged = True

    def setZoom(self, zoomFactor):
        """
        HOW ZOOM WORKS:
        Zoom is given as a decimal not a percentage, e.g. 50% = 0.5, 125% = 1.25, etc.

        Zoom=200%, img * 2, sab * 2
        Zoom=175%, img * 1.75, sab * 1.75
        Zoom=150%, img * 1.5, sab * 1.5
        Zoom=125%, img * 1.25, sab * 1.25
        Zoom=100%, img * 1, sab * 1
        Zoom=75%, img * 0.75
        Zoom=50%, img * 0.5
        Zoom=25%, img * 0.25

        Note that the scroll area body only scales with the image when the zoom factor is over 1 (i.e. over 100%). This is a minimum threshold that prevents it from getting smaller than the scroll area.

        Also, the zoom factor is not limited to the values shown. These are just the values commonly seen in other software.
        """

        scaled_size = self.image_widget.size()
        scaled_size.scale(self.image_widget.width() * zoomFactor, self.image_widget.height() * zoomFactor, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        self.image_widget.resize(scaled_size)

        if zoomFactor > 1:
            # set a fixed size to resize the scrollbars as well
            self.scroll_area_body.setFixedSize(
                self.scroll_area_body.width() * zoomFactor,
                self.scroll_area_body.height() * zoomFactor
            )

    def scrollRangeChangedHorizontally(self):
        if self.horizontalScrollRangeChanged:
            self.scrollToHorizontalCenter()
            self.horizontalScrollRangeChanged = False

    def scrollRangeChangedVertically(self):
        if self.verticalScrollRangeChanged:
            self.scrollToVerticalCenter()
            self.verticalScrollRangeChanged = False

    def scrollToCenter(self):
        self.scrollToHorizontalCenter()
        self.scrollToVerticalCenter()

    def scrollToHorizontalCenter(self):
        horizontal_scrollbar = self.horizontalScrollBar()
        horizontal_scrollbar.setValue(horizontal_scrollbar.maximum() // 2)

    def scrollToVerticalCenter(self):
        vertical_scrollbar = self.verticalScrollBar()
        vertical_scrollbar.setValue(vertical_scrollbar.maximum() // 2)