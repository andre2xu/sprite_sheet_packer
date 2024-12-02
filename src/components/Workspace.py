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

        self.preview_buttons = PreviewButtons(self)

        self.image_zoom = 1
        self.preview_buttons.zoom_out_button.clicked.connect(self.zoomOut)
        self.preview_buttons.zoom_in_button.clicked.connect(self.zoomIn)

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

    def zoomOut(self):
        new_zoom_value = round(self.image_zoom - 0.25, 2)

        if new_zoom_value >= 0.1:
            self.image_zoom = new_zoom_value
            self.scrollable_area.setZoom(self.image_zoom)
            self.scrollable_area.scrollToCenter()

            self.preview_buttons.zoomValueDisplay.setText(f'{round(new_zoom_value * 100)}%')

    def zoomIn(self):
        new_zoom_value = round(self.image_zoom + 0.25, 2)

        if new_zoom_value < 8.1:
            self.image_zoom = new_zoom_value
            self.scrollable_area.setZoom(self.image_zoom)
            self.scrollable_area.scrollToCenter()

            self.preview_buttons.zoomValueDisplay.setText(f'{round(new_zoom_value * 100)}%')



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