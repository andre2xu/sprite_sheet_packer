from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
import components.shared
from components.SpriteSheetPreview import PreviewButtons, ScrollableArea
from components.SpritesManager import Controls, SpritesList



class SpriteSheetPreview(components.shared.VerticalBoxLayout):
    def __init__(self, parent=None):
        super(SpriteSheetPreview, self).__init__(parent)

        self.scrollable_area = ScrollableArea()
        self.lyt.addWidget(self.scrollable_area)

        PreviewButtons(self)

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