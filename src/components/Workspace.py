import pathlib
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
import components.shared
from components.SpritesManager import Controls, SpritesList



class SpriteSheetPreview(components.shared.VerticalBoxLayout):
    def __init__(self, parent=None):
        super(SpriteSheetPreview, self).__init__(parent)

        # SCROLL AREA
        scroll_area = QtWidgets.QScrollArea()
        self.lyt.addWidget(scroll_area)

        scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll_area.setWidgetResizable(False) # make the scroll area resize according to its widget (the scroll area body), not the other way around

        scroll_area_body = QtWidgets.QWidget()
        scroll_area_body.setStyleSheet('background-color: red;')
        scroll_area_body.resize(scroll_area.width() * 2, scroll_area.height() * 2) # make the scroll area widget larger than the scroll area so that the scrollbar's appear
        scroll_area.setWidget(scroll_area_body)

        sprite_sheet = QtWidgets.QLabel(scroll_area_body)
        sprite_sheet.setPixmap(QtGui.QPixmap(f'{pathlib.Path(__file__).parent.resolve()}/../../local/packed.png'))
        sprite_sheet.setScaledContents(True)

        # move sprite sheet to the center of the scroll area body & scroll to it
        sab_center_distanceX = scroll_area_body.width() // 2
        sab_center_distanceY = scroll_area_body.height() // 2
        sprite_sheet.move(sab_center_distanceX - (sprite_sheet.width() * 2), sab_center_distanceY - (sprite_sheet.height() * 2))

        sa_hscrollbar = scroll_area.horizontalScrollBar()
        sa_vscrollbar = scroll_area.verticalScrollBar()
        sa_hscrollbar.setValue(sa_hscrollbar.maximum() // 2)
        sa_vscrollbar.setValue(sa_vscrollbar.maximum() // 2)

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
    def __init__(self, parent=None):
        super(SpritesManager, self).__init__(parent)

        self.addWidgets([
            Controls(self),
            SpritesList(self)
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