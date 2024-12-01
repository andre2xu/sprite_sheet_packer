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

        scroll_area_body = QtWidgets.QWidget()
        scroll_area_body.setStyleSheet('background-color: red;')
        scroll_area_body.resize(self.width() * 2, self.height() * 2) # make the scrollable area's body widget twice its size so that the scrollbars appear
        self.setWidget(scroll_area_body)

        # create a placeholder sprite sheet
        self.sprite_sheet = QtWidgets.QLabel(scroll_area_body)
        self.sprite_sheet.setPixmap(QtGui.QPixmap(f'{pathlib.Path(__file__).parent.resolve()}/../../local/packed.png'))
        self.sprite_sheet.setScaledContents(True)

        # move sprite sheet to the center of the scrollable area body & scroll to it
        sab_center_distanceX = scroll_area_body.width() // 2
        sab_center_distanceY = scroll_area_body.height() // 2
        self.sprite_sheet.move(sab_center_distanceX - (self.sprite_sheet.width() * 2), sab_center_distanceY - (self.sprite_sheet.height() * 2))

        sa_hscrollbar = self.horizontalScrollBar()
        sa_vscrollbar = self.verticalScrollBar()
        sa_hscrollbar.setValue(sa_hscrollbar.maximum() // 2)
        sa_vscrollbar.setValue(sa_vscrollbar.maximum() // 2)