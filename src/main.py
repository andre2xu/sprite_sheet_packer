import sys, pathlib, os, shutil
from PySide6 import QtWidgets, QtCore

### GUI COMPONENTS ###
import components.shared
from components.MainWindow import Menubar, Workspace



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app, parent=None):
        super(MainWindow, self).__init__(parent)

        self.app = app

        central_widget = components.shared.VerticalBoxLayout()
        central_widget.lyt.setSpacing(0)
        central_widget.lyt.setContentsMargins(0,0,0,0)

        self.workspace = Workspace(self)
        self.workspace.sprite_sheet_preview.scrollable_area.displayImage(f'{pathlib.Path(__file__).parent.resolve()}/../local/packed.png')

        central_widget.addWidgets([
            self.workspace
        ])
        self.setCentralWidget(central_widget)

        self.menubar = Menubar(self)
        self.menubar.file_menu_new_project_dialog.submit_button.clicked.connect(self.createProjectFolder)
        self.setMenuBar(self.menubar)

        self.setMinimumSize(QtCore.QSize(800, 500))
        self.setWindowTitle('Sprite Sheet Packer')

    def resizeEvent(self, event):
        super().resizeEvent(event)

        main_window_width = self.width()
        main_window_height = self.height()

        # re-scale the sprite sheet preview's scrollable area body
        self.workspace.sprite_sheet_preview.scrollable_area.rescaleScrollableAreaBody()

        # re-scale the sprite input choice dialog
        sprite_input_choice_dialog = self.workspace.sprites_manager.controls.sprite_input_choice_dialog

        if main_window_width > 1300 and main_window_height > 750:
            sprite_input_choice_dialog.setFixedSize(sprite_input_choice_dialog.original_width * 1.3, sprite_input_choice_dialog.original_height * 1.3)

            new_sprite_input_option_image_size = QtCore.QSize(130, 130)
            sprite_input_choice_dialog.sprite_sheet_option_image.setFixedSize(new_sprite_input_option_image_size)
            sprite_input_choice_dialog.selection_option_image.setFixedSize(new_sprite_input_option_image_size)
        else:
            sprite_input_choice_dialog.setFixedSize(sprite_input_choice_dialog.original_width, sprite_input_choice_dialog.original_height)

            sprite_input_choice_dialog.sprite_sheet_option_image.setFixedSize(sprite_input_choice_dialog.sprite_sheet_option_image.pixmap().size())
            sprite_input_choice_dialog.selection_option_image.setFixedSize(sprite_input_choice_dialog.selection_option_image.pixmap().size())

    def generateProjectFolder(self, path, enableOverwrite=False):
        if enableOverwrite:
            # delete existing folder
            shutil.rmtree(path)

        # make root folder
        os.makedirs(path)

        # make sprites folder
        os.makedirs(f'{path}/sprites')

    def createProjectFolder(self):
        project_folder_name = self.menubar.file_menu_new_project_dialog.folder_name_field.text()

        if len(project_folder_name) == 0:
            # no project folder name provided
            QtWidgets.QMessageBox.critical(
                self,
                'Invalid Name',
                "Please provide a name for the project folder.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )

            return

        project_folder_location = self.menubar.file_menu_new_project_dialog.folder_location_field.text()

        if os.path.isdir(project_folder_location):
            project_folder_path = os.path.join(project_folder_location, project_folder_name)

            try:
                if os.access(os.path.dirname(project_folder_path), os.W_OK):
                    if os.path.exists(project_folder_path):
                        # folder already exists with the same name as the project, ask user to confirm overwrite
                        user_response = QtWidgets.QMessageBox.warning(
                            self,
                            'Please Confirm',
                            "A folder with the same name as the project already exists in that location. Do you want to overwrite it?",
                            QtWidgets.QMessageBox.StandardButton.Yes,
                            QtWidgets.QMessageBox.StandardButton.Cancel
                        )

                        if user_response == QtWidgets.QMessageBox.StandardButton.Yes:
                            # create project folder
                            self.generateProjectFolder(project_folder_path, True)

                            # close dialog
                            self.menubar.file_menu_new_project_dialog.accept()
                    else:
                        # create project folder
                        self.generateProjectFolder(project_folder_path)

                        # close dialog
                        self.menubar.file_menu_new_project_dialog.accept()
            except:
                # invalid project folder name
                QtWidgets.QMessageBox.critical(
                    self,
                    'Invalid Name',
                    "Please make sure to provide a folder name that is valid for your machine.",
                    QtWidgets.QMessageBox.StandardButton.Ok
                )
        else:
            # invalid project folder location
            QtWidgets.QMessageBox.critical(
                self,
                'Invalid Location',
                "The given location for the project folder could not be found. Please specify a folder that exists on your machine.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(app)
    main_window.show()

    sys.exit(app.exec())