import pathlib
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
import components.shared
from components.SpritesManager import Controls, SpritesList



class SpriteSheetPreview(components.shared.VerticalBoxLayout):
    def __init__(self):
        super(SpriteSheetPreview, self).__init__()

        # SCROLL AREA
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(True)
        self.lyt.addWidget(scroll_area)

        # PREVIEW BUTTONS
        ssp_buttons = QtWidgets.QWidget(self) # overlay button container on top of scroll area (this works because the scroll area is a child widget of the SSP's layout, while the button container is a child widget of the SSP itself like the layout)
        ssp_buttons.setObjectName('SSPB') # id for styling
        ssp_buttons.setMinimumWidth(200)
        ssp_buttons.move(10,10) # move down diagonally right (i.e. increase space between buttons and menubar + left edge of window)

        sspb_lyt = QtWidgets.QHBoxLayout(ssp_buttons)
        sspb_lyt.setContentsMargins(0,0,0,0)

        ICONS_FOLDER_PATH = f'{pathlib.Path(__file__).parent.resolve()}/../../local/icons'

        preview_buttons = [
            QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_icon.png'), ''),
            QtWidgets.QPushButton('</>'),
            QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_zoom_out_icon.png'), ''),
            QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_zoom_in_icon.png'), '')
        ]

        preview_buttons[0].setToolTip('Preview Sprite Sheet')
        preview_buttons[1].setToolTip('Preview Data Sheet')
        preview_buttons[2].setToolTip('Zoom Out')
        preview_buttons[3].setToolTip('Zoom In')

        for i in range(len(preview_buttons)):
            b = preview_buttons[i]
            b.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
            b.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
            b.setToolTipDuration(1000 * 3)

            sspb_lyt.addWidget(b)

        # INITIALIZATION
        self.lyt.setContentsMargins(0,0,0,0)
        self.lyt.setSpacing(0)

        self.setStyleSheet(
            """
            QWidget {
                background-color: #242629;
            }

            QScrollArea {
                background-color: #242629;
                border: none;
            }

            #SSPB {
                background-color: none;
            }

            #SSPB QPushButton {
                border-radius: none;
                padding: 5px 10px;
                background-color: #656769;
            }

            #SSPB QPushButton:pressed {
                background-color: #55595d;
            }
            """
        )



class SpritesManager(components.shared.VerticalBoxLayout):
    def __init__(self):
        super(SpritesManager, self).__init__()

        self.addWidgets([
            Controls(),
            SpritesList()
        ])

        self.setStyleSheet(
            """
            QWidget {
                background-color: #292b2e;
            }
            """
        )

        self.lyt.setSpacing(0)
        self.lyt.setContentsMargins(0,0,0,0)

        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum))
        self.setMinimumWidth(400)