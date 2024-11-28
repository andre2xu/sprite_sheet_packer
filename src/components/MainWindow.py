from PySide6 import QtWidgets

### GUI COMPONENTS ###
import components.shared
from components.Workspace import SpriteSheetPreview, SpritesManager



class Menubar(QtWidgets.QMenuBar):
    def __init__(self):
        super(Menubar, self).__init__()

        self.addMenu('File')
        self.addMenu('Help')

        self.setStyleSheet(
            """
            QMenuBar {
                background-color: #2f3133;
                padding: 8px 10px;
            }

            QMenuBar::item {
                border: none;
                padding: 3px 10px;
            }

            QMenuBar::item:selected {
                background-color: #404244;
                border-radius: 5px;
            }
            """
        )



class Workspace(components.shared.HorizontalBoxLayout):
    def __init__(self):
        super(Workspace, self).__init__()

        self.lyt.setSpacing(0)
        self.lyt.setContentsMargins(0,0,0,0)

        self.addWidgets([
            SpriteSheetPreview(),
            SpritesManager()
        ])