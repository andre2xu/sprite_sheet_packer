import os
import PIL.Image
from PySide6 import QtWidgets, QtCore

### GUI COMPONENTS ###
import components.shared, components.dialogs
from components.Workspace import SpriteSheetPreview, SpritesManager



class Menubar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super(Menubar, self).__init__(parent)

        main_window = self.parent()

        # FILE MENU
        file_menu = self.addMenu('File')
        file_menu.setMinimumWidth(250)

        file_menu_new_project = file_menu.addAction('New project...')
        file_menu_new_project.setShortcut('Ctrl+N')
        self.file_menu_open_project = file_menu.addAction('Open project...')
        self.file_menu_open_project.setShortcut('Ctrl+O')
        self.file_menu_close_project = file_menu.addAction('Close project')
        self.file_menu_close_project.setShortcut('Ctrl+Q')
        file_menu.addSeparator()
        file_menu_export_sprite_sheet = file_menu.addAction('Export sprite sheet...')
        file_menu_export_data_sheet = file_menu.addAction('Export data sheet...')
        file_menu.addSeparator()
        file_menu_exit = file_menu.addAction('Exit')
        file_menu_exit.triggered.connect(lambda: main_window.app.quit())

        self.addMenu(file_menu)

        # HELP MENU
        help_menu = self.addMenu('Help')
        help_menu.setMinimumWidth(180)

        help_menu_tutorial = help_menu.addAction('Tutorial')
        help_menu.addSeparator()
        help_menu_my_channel = help_menu.addAction('My YouTube channel')
        help_menu_source_code = help_menu.addAction('Project repository')

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

            QMenu {
                background-color: #53585a;
                padding: 5px;
            }

            QMenu::separator {
                height: 1px;
                background-color: #3f4344;
                margin: 4px 0px;
            }

            QMenu::item {
                color: #fff;
                padding: 10px 15px;
            }

            QMenu::item:selected {
                background-color: #484c4e;
            }
            """
        )

        # FILE MENU > NEW PROJECT ACTION
        self.file_menu_new_project_dialog = components.dialogs.FileMenuNewProjectDialog(main_window, QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.FramelessWindowHint)

        file_menu_new_project.triggered.connect(lambda: self.file_menu_new_project_dialog.open())

        # FILE MENU > EXPORT SPRITE SHEET ACTION
        file_menu_export_sprite_sheet.triggered.connect(self.exportSpriteSheet)

    def exportSpriteSheet(self):
        main_window = self.parent()

        sprite_sheet_file = 'spritesheet.png'

        if main_window.temp_folder_path != None and os.path.exists(os.path.join(main_window.temp_folder_path, sprite_sheet_file)):
            save_data = QtWidgets.QFileDialog.getSaveFileName(
                main_window,
                'Choose a destination and file name',
                main_window.project_folder_path,
                'Images (*.png)'
            )

            save_path = save_data[0]

            if len(save_path) > 0:
                destination = os.path.dirname(save_path)

                # validate save folder
                if os.path.exists(destination) == False:
                    QtWidgets.QMessageBox.critical(
                        main_window,
                        'Invalid Destination',
                        "The folder you specified does not exist. Please make sure you are providing a valid path to an existing directory in your machine.",
                        QtWidgets.QMessageBox.StandardButton.Ok
                    )

                    return

                # save sprite sheet
                with PIL.Image.open(os.path.join(main_window.temp_folder_path, sprite_sheet_file)) as sprite_sheet:
                    sprite_sheet.save(save_path)
        else:
            QtWidgets.QMessageBox.critical(
                main_window,
                'No Sprite Sheet',
                "Please create a sprite sheet first by adding sprites and then packing them.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )



class Workspace(components.shared.HorizontalBoxLayout):
    def __init__(self, parent=None):
        super(Workspace, self).__init__(parent)

        self.lyt.setSpacing(0)
        self.lyt.setContentsMargins(0,0,0,0)

        self.sprite_sheet_preview = SpriteSheetPreview(self)
        self.sprites_manager = SpritesManager(self)

        self.addWidgets([
            self.sprite_sheet_preview,
            self.sprites_manager
        ])