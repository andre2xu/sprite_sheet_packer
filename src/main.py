import sys, pathlib, os, shutil, PIL, mimetypes
import PIL.Image
from PySide6 import QtWidgets, QtCore

### GUI COMPONENTS ###
import components.shared
from components.MainWindow import Menubar, Workspace



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app, parent=None):
        super(MainWindow, self).__init__(parent)

        self.app = app

        self.project_folder_path = None

        central_widget = components.shared.VerticalBoxLayout()
        central_widget.lyt.setSpacing(0)
        central_widget.lyt.setContentsMargins(0,0,0,0)

        self.workspace = Workspace(self)
        self.workspace.sprites_manager.controls.sprite_input_choice_dialog.selection_option.clicked.connect(self.uploadSprites)
        self.workspace.sprite_sheet_preview.scrollable_area.displayImage(f'{pathlib.Path(__file__).parent.resolve()}/../local/packed.png')

        central_widget.addWidgets([
            self.workspace
        ])
        self.setCentralWidget(central_widget)

        self.menubar = Menubar(self)
        self.menubar.file_menu_new_project_dialog.submit_button.clicked.connect(self.createProjectFolder)
        self.menubar.file_menu_open_project.triggered.connect(self.openProjectFolder)
        self.setMenuBar(self.menubar)

        self.setMinimumSize(QtCore.QSize(800, 500))

        self.window_title_base = 'Sprite Sheet Packer'
        self.setWindowTitle(self.window_title_base)

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

        # load the folder's contents
        self.loadProjectFolder(path)

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

    def loadProjectFolder(self, path):
        # check if the given folder exists
        if os.path.exists(path) == False:
            QtWidgets.QMessageBox.critical(
                self,
                'Not Found',
                "The project folder you specified either does not exist or it may have been moved.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )

            return

        # check if the given folder is a valid project folder
        invalid_project_folder_message = "Failed to load the contents of the project folder."
        sprites_folder = f'{path}/sprites'

        if os.path.exists(sprites_folder) == False:
            QtWidgets.QMessageBox.critical(
                self,
                'Invalid Project Folder',
                f"{invalid_project_folder_message} The 'sprites' subfolder could not be found.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )

            return

        # save the path to the project folder
        self.project_folder_path = path

        # display folder name in window title
        self.setWindowTitle(f'{self.window_title_base}  |  {pathlib.Path(path).name}')

        # populate sprites list
        sprites_folder_contents = os.listdir(sprites_folder)
        sprite_sources = []

        for content in sprites_folder_contents:
            if content.endswith('.png') and mimetypes.guess_type(content)[0] == 'image/png':
                sprite_sources.append(f'{sprites_folder}/{content}')
            else:
                QtWidgets.QMessageBox.critical(
                    self,
                    'Invalid Sprite Found',
                    f"The sprites folder contains an invalid sprite. \"{content}\" is not a png image. Only png sprites are supported.",
                    QtWidgets.QMessageBox.StandardButton.Ok
                )

                return

        self.workspace.sprites_manager.sprites_list.loadSprites(sprite_sources)

    def openProjectFolder(self):
        home_folder_paths = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.StandardLocation.DesktopLocation)
        home_folder = ''

        if len(home_folder_paths) > 0:
            home_folder = home_folder_paths[0]

        project_folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            'Select a project folder',
            home_folder, # default directory
            QtWidgets.QFileDialog.Option.ShowDirsOnly | QtWidgets.QFileDialog.Option.ReadOnly
        )

        if len(project_folder_path) > 0:
            self.loadProjectFolder(project_folder_path)

    def uploadSprites(self):
        sprites = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            'Select sprites',
            '',
            'Images (*.png)'
        )[0]

        if len(sprites) > 0:
            # make a copy of each sprite and put them in the sprites subfolder of the project folder
            sprites_folder_paths = []

            for i in range(len(sprites)):
                sprite_src = sprites[i]

                with PIL.Image.open(sprite_src) as sprite:
                    file_name = os.path.basename(sprite_src)
                    file_path = f'{self.project_folder_path}/sprites/{file_name}'

                    sprite.save(file_path, 'png')

                    sprites_folder_paths.append(file_path)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(app)
    main_window.show()

    sys.exit(app.exec())