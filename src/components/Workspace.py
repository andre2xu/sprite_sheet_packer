import pathlib
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
import components.shared
from components.SpritesManager import Controls, SpritesList



class SpriteSheetPreview(components.shared.VerticalBoxLayout):
    def __init__(self):
        super(SpriteSheetPreview, self).__init__()

        # PREVIEW BUTTONS
        ssp_buttons = components.shared.HorizontalBoxLayout()

        ICONS_FOLDER_PATH = f'{pathlib.Path(__file__).parent.resolve()}/../../local/icons'

        preview_buttons = [
            QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_icon.png'), ''),
            QtWidgets.QPushButton('</>'),
            QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_zoom_out_icon.png'), ''),
            QtWidgets.QPushButton(QtGui.QIcon(f'{ICONS_FOLDER_PATH}/sprite_sheet_preview_zoom_in_icon.png'), '')
        ]

        for i in range(len(preview_buttons)):
            b = preview_buttons[i]
            b.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
            b.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        ssp_buttons.addWidgets(preview_buttons)
        ssp_buttons.lyt.addStretch(0)

        ssp_buttons.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        ssp_buttons.setObjectName('SSPB')

        # INITIALIZATION
        self.addWidgets([
            ssp_buttons,
            QtWidgets.QLabel('Sprite Sheet')
        ])

        self.lyt.setContentsMargins(0,0,0,0)
        self.lyt.setSpacing(0)

        self.setStyleSheet(
            """
            QWidget {
                background-color: #242629;
            }

            #SSPB QPushButton {
                border-radius: none;
                padding: 5px 10px;
                background-color: #656769;
                margin-left: 5px;
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