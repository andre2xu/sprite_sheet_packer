import components.shared
from PySide6 import QtWidgets
from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
from components.SpritesManager import Controls, SpritesList



class SpriteSheetPreview(components.shared.VerticalBoxLayout):
    def __init__(self):
        super(SpriteSheetPreview, self).__init__()

        self.addWidgets([QtWidgets.QLabel('Sprite Sheet Preview')])

        self.setStyleSheet(
            """
            QWidget {
                background-color: #242629;
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