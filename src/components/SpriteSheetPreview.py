import pathlib, os
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy



class PreviewButtons(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(PreviewButtons, self).__init__(parent)

        self.setObjectName('SSPB') # id for styling
        self.setMinimumWidth(300)
        self.move(10,10) # move down diagonally right (i.e. increase space between buttons and the menubar as well as the left edge of window)

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)

        ICONS_FOLDER_PATH = os.path.join(pathlib.Path(__file__).parent.resolve(), '../../local/icons')

        self.preview_sprite_sheet_button = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(ICONS_FOLDER_PATH, 'sprite_sheet_preview_icon.png')), '')
        self.preview_data_sheet_button = QtWidgets.QPushButton('</>')
        self.zoom_reset_button = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(ICONS_FOLDER_PATH, 'sprite_sheet_preview_zoom_reset_icon.png')), '')
        self.zoom_out_button = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(ICONS_FOLDER_PATH, 'sprite_sheet_preview_zoom_out_icon.png')), '')
        self.zoom_in_button = QtWidgets.QPushButton(QtGui.QIcon(os.path.join(ICONS_FOLDER_PATH, 'sprite_sheet_preview_zoom_in_icon.png')), '')
        self.zoom_value_display = QtWidgets.QLabel('100%')

        preview_buttons = [
            self.preview_sprite_sheet_button,
            self.preview_data_sheet_button,
            self.zoom_reset_button,
            self.zoom_out_button,
            self.zoom_in_button,
            self.zoom_value_display
        ]

        # add a tooltip to each of the buttons
        self.preview_sprite_sheet_button.setToolTip('Preview Sprite Sheet')
        self.preview_data_sheet_button.setToolTip('Preview Data Sheet')
        self.zoom_reset_button.setToolTip('Reset Zoom')
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

        self.original_sab_width = self.scroll_area_body.width()
        self.original_sab_height = self.scroll_area_body.height()

        self.image_widget = QtWidgets.QLabel(' ', self.scroll_area_body)
        self.original_image_width = None
        self.original_image_height = None

        # re-scroll to the center if the scrollable distances change (e.g. when image is changed)
        self.horizontal_scroll_range_changed = False
        self.vertical_scroll_range_changed = False
        self.horizontalScrollBar().rangeChanged.connect(lambda: self.scrollRangeChangedHorizontally())
        self.verticalScrollBar().rangeChanged.connect(lambda: self.scrollRangeChangedVertically())

    def rescaleScrollableAreaBody(self):
        self.scroll_area_body.resize(self.width() * 2, self.height() * 2) # make the scrollable area's body widget twice its size so that the scrollbars appear

        self.centerImage()

        self.scrollToCenter()

    def displayImage(self, imagePath: str):
        pixmap = QtGui.QPixmap(imagePath)

        self.image_widget.clear()
        self.image_widget.setText('') # remove placeholder text
        self.image_widget.setPixmap(pixmap)
        self.image_widget.setFixedSize(pixmap.size()) # make the label widget match the pixmap's dimensions
        self.image_widget.adjustSize() # ensure the widget's size data matches the dimensions of the rendered image
        self.image_widget.setScaledContents(True) # scale pixmap with image

        # update saved dimensions
        self.original_image_width = self.image_widget.width()
        self.original_image_height = self.image_widget.height()

        # allow the 'QScrollBar.rangeChanged' slots to fire
        self.horizontal_scroll_range_changed = True
        self.vertical_scroll_range_changed = True

        # reset zoom
        self.setZoom(1)

    def centerImage(self):
        centerX = self.scroll_area_body.width() // 2
        centerY = self.scroll_area_body.height() // 2
        self.image_widget.move(centerX - (self.image_widget.width() // 2), centerY - (self.image_widget.height() // 2))

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

        if self.original_image_width != None and self.original_image_height != None:
            new_size = QtCore.QSize(self.original_image_width * zoomFactor, self.original_image_height * zoomFactor)

            self.image_widget.setFixedSize(new_size)

            if zoomFactor > 1:
                # set a fixed size to resize the scrollbars as well
                self.scroll_area_body.setFixedSize(
                    self.original_sab_width * zoomFactor,
                    self.original_sab_height * zoomFactor
                )

            # re-position image in the center (I didn't scroll to center here because I consider it a non-zoom effect)
            self.centerImage()

    def scrollRangeChangedHorizontally(self):
        if self.horizontal_scroll_range_changed:
            self.scrollToHorizontalCenter()
            self.horizontal_scroll_range_changed = False

    def scrollRangeChangedVertically(self):
        if self.vertical_scroll_range_changed:
            self.scrollToVerticalCenter()
            self.vertical_scroll_range_changed = False

    def scrollToCenter(self):
        self.scrollToHorizontalCenter()
        self.scrollToVerticalCenter()

    def scrollToHorizontalCenter(self):
        horizontal_scrollbar = self.horizontalScrollBar()
        horizontal_scrollbar.setValue(horizontal_scrollbar.maximum() // 2)

    def scrollToVerticalCenter(self):
        vertical_scrollbar = self.verticalScrollBar()
        vertical_scrollbar.setValue(vertical_scrollbar.maximum() // 2)