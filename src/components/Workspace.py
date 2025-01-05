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
        self.preview_buttons.zoom_reset_button.clicked.connect(self.zoomReset)

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

            QScrollBar {
                background-color: #212124;
            }

            QScrollBar::handle {
                background-color: #656769;
                border: 1px solid gray;
                border-radius: 2px;
            }

            QScrollBar::add-line, QScrollBar::sub-line {
                width: 0px;
                height: 0px;
            }

            QScrollBar::add-page, QScrollBar::sub-page {
                background-color: #242629;
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

            self.preview_buttons.zoom_value_display.setText(f'{round(new_zoom_value * 100)}%')

    def zoomIn(self):
        new_zoom_value = round(self.image_zoom + 0.25, 2)

        if new_zoom_value < 8.1:
            self.image_zoom = new_zoom_value
            self.scrollable_area.setZoom(self.image_zoom)
            self.scrollable_area.scrollToCenter()

            self.preview_buttons.zoom_value_display.setText(f'{round(new_zoom_value * 100)}%')

    def zoomReset(self):
        self.image_zoom = 1
        self.scrollable_area.setZoom(self.image_zoom)
        self.scrollable_area.scrollToCenter()

        self.preview_buttons.zoom_value_display.setText('100%')



class SpritesManager(components.shared.VerticalBoxLayout):
    def __init__(self, parent=None):
        super(SpritesManager, self).__init__(parent)

        self.controls = Controls(self)
        self.sprites_list = SpritesList(self)

        self.controls.clear_all_sprites_btn.clicked.connect(lambda: self.sprites_list.deleteAllSprites())

        self.addWidgets([
            self.controls,
            self.sprites_list
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