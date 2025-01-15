import os, json
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
import components.shared, components.dialogs
from components.SpriteSheetPreview import PreviewButtons, ScrollableArea, SpriteSheetDataPreview
from components.SpritesManager import Controls, SpritesList



class SpriteSheetPreview(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SpriteSheetPreview, self).__init__(parent)

        self.stacked_layout = QtWidgets.QStackedLayout()
        self.setLayout(self.stacked_layout)

        self.scrollable_area = ScrollableArea()
        self.sprite_sheet_data_preview = SpriteSheetDataPreview()

        self.stacked_layout.addWidget(self.scrollable_area)
        self.stacked_layout.addWidget(self.sprite_sheet_data_preview)

        self.preview_buttons = PreviewButtons(self)
        self.preview_buttons.preview_sprite_sheet_button.clicked.connect(self.previewSpriteSheet)
        self.preview_buttons.preview_data_sheet_button.clicked.connect(self.previewDataSheet)

        self.previewDataSheet() # temp

        self.image_zoom = 1
        self.preview_buttons.zoom_out_button.clicked.connect(self.zoomOut)
        self.preview_buttons.zoom_in_button.clicked.connect(self.zoomIn)
        self.preview_buttons.zoom_reset_button.clicked.connect(self.zoomReset)

        self.stacked_layout.setContentsMargins(0,0,0,0)
        self.stacked_layout.setSpacing(0)

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

        # make the buttons, and the zoom value, still take up space even when they are invisible
        new_size_policy = self.preview_buttons.zoom_reset_button.sizePolicy()
        new_size_policy.setRetainSizeWhenHidden(True)
        self.preview_buttons.zoom_reset_button.setSizePolicy(new_size_policy)

        new_size_policy = self.preview_buttons.zoom_out_button.sizePolicy()
        new_size_policy.setRetainSizeWhenHidden(True)
        self.preview_buttons.zoom_out_button.setSizePolicy(new_size_policy)

        new_size_policy = self.preview_buttons.zoom_in_button.sizePolicy()
        new_size_policy.setRetainSizeWhenHidden(True)
        self.preview_buttons.zoom_in_button.setSizePolicy(new_size_policy)

        new_size_policy = self.preview_buttons.zoom_value_display.sizePolicy()
        new_size_policy.setRetainSizeWhenHidden(True)
        self.preview_buttons.zoom_value_display.setSizePolicy(new_size_policy)

    def previewSpriteSheet(self):
        self.stacked_layout.setCurrentIndex(0)
        self.preview_buttons.raise_() # keep the preview buttons on top

        # show zoom buttons
        self.preview_buttons.zoom_out_button.setVisible(True)
        self.preview_buttons.zoom_in_button.setVisible(True)
        self.preview_buttons.zoom_reset_button.setVisible(True)

        # show zoom value
        self.preview_buttons.zoom_value_display.setVisible(True)

    def previewDataSheet(self):
        self.stacked_layout.setCurrentIndex(1)
        self.preview_buttons.raise_() # keep the preview buttons on top

        # hide zoom buttons
        self.preview_buttons.zoom_out_button.setVisible(False)
        self.preview_buttons.zoom_in_button.setVisible(False)
        self.preview_buttons.zoom_reset_button.setVisible(False)

        # hide zoom value
        self.preview_buttons.zoom_value_display.setVisible(False)

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

        self.controls.clear_all_sprites_btn.clicked.connect(self.clearAllSprites)
        self.controls.pack_sprites_btn.clicked.connect(self.packSprites)

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

    def clearAllSprites(self):
        main_window = self.parent().parent().parent()

        if main_window.sprites_folder_path != None and self.sprites_list.vertical_list.count() > 0:
            answer = QtWidgets.QMessageBox.warning(
                main_window,
                'Confirmation',
                "Clearing all will delete all your sprites. Are you sure you want to proceed with this action?",
                QtWidgets.QMessageBox.StandardButton.No,
                QtWidgets.QMessageBox.StandardButton.Yes
            )

            if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                self.sprites_list.deleteAllSprites()
        else:
            QtWidgets.QMessageBox.critical(
                main_window,
                'Empty Sprites List',
                "You need to open an existing project folder with sprites before you can do this. If you already have a project folder open, be sure to add sprites first.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )

    def packSprites(self):
        main_window = self.parent().parent().parent()

        if self.sprites_list.vertical_list.count() > 0:
            sprite_sheet_layout_dialog = components.dialogs.SpriteSheetLayoutDialog(main_window, QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.FramelessWindowHint)

            # display packed sprite sheet (if one was created)
            sprite_sheet_layout_dialog.accepted.connect(self.loadSheets)

            sprite_sheet_layout_dialog.open()
        else:
            QtWidgets.QMessageBox.critical(
                main_window,
                'Empty Sprites List',
                "You need to open an existing project folder with sprites before you can do this. If you already have a project folder open, be sure to add sprites first.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )

    def loadSheets(self):
        main_window = self.parent().parent().parent()

        if main_window.temp_folder_path != None:
            sprite_sheet_file = os.path.join(main_window.temp_folder_path, 'spritesheet.png')
            data_sheet_file = os.path.join(main_window.temp_folder_path, 'datasheet.json')

            if os.path.exists(sprite_sheet_file) and os.path.exists(data_sheet_file):
                # sprite sheet
                main_window.workspace.sprite_sheet_preview.scrollable_area.displayImage(sprite_sheet_file)

                # data sheet
                with open(data_sheet_file) as json_file:
                    data = json.load(json_file)

                    main_window.workspace.sprite_sheet_preview.sprite_sheet_data_preview.displayData(data)