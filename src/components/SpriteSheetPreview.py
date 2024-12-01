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

        preview_buttons = [
            QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_icon.png'), ''),
            QtWidgets.QPushButton('</>'),
            QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_zoom_out_icon.png'), ''),
            QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_zoom_in_icon.png'), '')
        ]

        # add a tooltip to each of the buttons
        preview_buttons[0].setToolTip('Preview Sprite Sheet')
        preview_buttons[1].setToolTip('Preview Data Sheet')
        preview_buttons[2].setToolTip('Zoom Out')
        preview_buttons[3].setToolTip('Zoom In')

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
        self.scroll_area_body.setStyleSheet('background-color: red;')
        self.setWidget(self.scroll_area_body)

        self.image_widget = QtWidgets.QLabel(' ', self.scroll_area_body)

    def rescaleScrollableAreaBody(self):
        self.scroll_area_body.resize(self.width() * 2, self.height() * 2) # make the scrollable area's body widget twice its size so that the scrollbars appear

        centerX = self.scroll_area_body.width() // 2
        centerY = self.scroll_area_body.height() // 2
        self.image_widget.move(centerX - (self.image_widget.width() // 2), centerY - (self.image_widget.height() // 2))

        horizontal_scrollbar = self.horizontalScrollBar()
        vertical_scrollbar = self.verticalScrollBar()

        horizontal_scrollbar.setValue(horizontal_scrollbar.maximum() // 2)
        vertical_scrollbar.setValue(vertical_scrollbar.maximum() // 2)

    def displayImage(self, imagePath: str):
        self.image_widget.clear()
        self.image_widget.setText('') # remove placeholder text
        self.image_widget.setPixmap(QtGui.QPixmap(imagePath))
