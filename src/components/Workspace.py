import components.shared
from PySide6 import QtWidgets



class SpriteSheetPreview(components.shared.VerticalBoxLayout):
    def __init__(self):
        super(SpriteSheetPreview, self).__init__()

        self.addWidgets([QtWidgets.QLabel('Sprite Sheet Preview')])



class SpritesManager(components.shared.VerticalBoxLayout):
    def __init__(self):
        super(SpritesManager, self).__init__()

        self.addWidgets([QtWidgets.QLabel('Sprites Manager')])