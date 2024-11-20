import components.shared
from PySide6 import QtWidgets



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

        self.addWidgets([QtWidgets.QLabel('Sprites Manager')])