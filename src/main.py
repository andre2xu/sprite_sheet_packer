import sys, pathlib, os, shutil, mimetypes, re, hashlib, datetime
import PIL.Image
from PySide6 import QtWidgets, QtCore, QtGui

### GUI COMPONENTS ###
import components.shared
import components.dialogs
from components.MainWindow import Menubar, Workspace



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, app: QtWidgets.QApplication, parent: QtWidgets.QWidget | None = None):
        super(MainWindow, self).__init__(parent)

        self.app = app

        self.project_folder_path = None
        self.sprites_folder_path = None
        self.temp_folder_path = None

        central_widget = components.shared.VerticalBoxLayout()
        central_widget.lyt.setSpacing(0)
        central_widget.lyt.setContentsMargins(0,0,0,0)

        self.workspace = Workspace(self)
        self.workspace.sprites_manager.controls.sprite_input_choice_dialog.selection_option.clicked.connect(self.uploadSprites)
        self.workspace.sprites_manager.controls.sprite_input_choice_dialog.sprite_sheet_option.clicked.connect(self.uploadSpriteSheet)

        central_widget.addWidgets([
            self.workspace
        ])
        self.setCentralWidget(central_widget)

        self.menubar = Menubar(self)
        self.menubar.file_menu_new_project_dialog.submit_button.clicked.connect(self.createProjectFolder)
        self.menubar.file_menu_open_project.triggered.connect(self.openProjectFolder)
        self.menubar.file_menu_close_project.triggered.connect(self.closeProjectFolder)
        self.setMenuBar(self.menubar)

        self.setMinimumSize(QtCore.QSize(800, 500))

        self.window_title_base = 'Sprite Sheet Packer'
        self.setWindowTitle(self.window_title_base)
        self.setWindowIcon(QtGui.QIcon(os.path.join(pathlib.Path(__file__).parent.resolve(), './icons/app_icon.png')))

        self.sprite_sheet_info_dialog = components.dialogs.SpriteSheetInfoDialog(self, QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.FramelessWindowHint)

    def resizeEvent(self, event: QtGui.QResizeEvent):
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

    def generateProjectFolder(self, path: str, enableOverwrite: bool = False):
        if enableOverwrite:
            # delete existing folder
            shutil.rmtree(path)

        # make root folder
        os.makedirs(path)

        # make sprites folder
        os.makedirs(os.path.join(path, 'sprites'))

        # make folder for temporary files
        os.makedirs(os.path.join(path, 'tmp'))

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

    def loadProjectFolder(self, path: str):
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

        sprites_folder = os.path.join(path, 'sprites')
        temp_folder = os.path.join(path, 'tmp')

        if os.path.exists(sprites_folder) == False:
            QtWidgets.QMessageBox.critical(
                self,
                'Invalid Project Folder',
                f"{invalid_project_folder_message} The 'sprites' subfolder could not be found.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )
            return
        elif os.path.exists(temp_folder) == False:
            QtWidgets.QMessageBox.critical(
                self,
                'Invalid Project Folder',
                f"{invalid_project_folder_message} The 'tmp' subfolder could not be found.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )
            return

        # close project folder first (if one is opened)
        self.closeProjectFolder()

        # save the path to the project folder
        self.project_folder_path = path
        self.sprites_folder_path = sprites_folder
        self.temp_folder_path = temp_folder

        # empty temp folder
        temp_files = os.listdir(self.temp_folder_path)

        for i in range(len(temp_files)):
            pathlib.Path.unlink(os.path.join(self.temp_folder_path, temp_files[i]), missing_ok=True)

        # display folder name in window title
        self.setWindowTitle(f'{self.window_title_base}  |  {pathlib.Path(path).name}')

        # populate sprites list
        sprites_folder_contents = os.listdir(sprites_folder)
        sprite_sources = []

        for content in sprites_folder_contents:
            if content.endswith('.png') and mimetypes.guess_type(content)[0] == 'image/png':
                sprite_sources.append(os.path.join(sprites_folder, content))
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

    def closeProjectFolder(self):
        # empty sprites list
        self.workspace.sprites_manager.sprites_list.vertical_list.clear()

        # clear sprite sheet preview
        self.workspace.sprite_sheet_preview.scrollable_area.clearImage()

        # clear sprite sheet data preview
        self.workspace.sprite_sheet_preview.sprite_sheet_data_preview.clearData()

        # reset window title
        self.setWindowTitle(self.window_title_base)

        # clear paths
        self.project_folder_path = None
        self.sprites_folder_path = None
        self.temp_folder_path = None

    def uploadSprites(self):
        sprites = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            'Select sprites',
            '',
            'Images (*.png)'
        )[0]

        if len(sprites) > 0:
            # check if all uploads are valid
            valid_extension = re.compile(r'\.png$')

            for i in range(len(sprites)):
                uploaded_sprite = sprites[i]

                if (valid_extension.search(uploaded_sprite) != None and mimetypes.guess_type(uploaded_sprite)[0] == 'image/png') == False:
                    QtWidgets.QMessageBox.critical(
                        self,
                        'Invalid Upload',
                        f"Only png images are allowed. \"{os.path.basename(uploaded_sprite)}\" is not a png sprite.",
                        QtWidgets.QMessageBox.StandardButton.Ok,
                    )

                    return

            # make a copy of each sprite and put them in the sprites subfolder of the project folder
            sprites_folder_paths = []

            try:
                for i in range(len(sprites)):
                    sprite_src = sprites[i]

                    file_name = os.path.basename(sprite_src)
                    file_path = os.path.join(self.sprites_folder_path, file_name)

                    if os.path.exists(file_path) == False:
                        with PIL.Image.open(sprite_src) as sprite:
                            sprite.save(file_path, 'png')
                            sprites_folder_paths.append(file_path)
                    else:
                        # sprite already exists, request permission to replace it
                        answer = QtWidgets.QMessageBox.warning(
                            self,
                            'Sprite Already Exists',
                            f"\"{file_name}\" already exists in the sprites folder. Would you like to replace it?",
                            QtWidgets.QMessageBox.StandardButton.No,
                            QtWidgets.QMessageBox.StandardButton.Yes
                        )

                        if answer == QtWidgets.QMessageBox.StandardButton.Yes:
                            with PIL.Image.open(sprite_src) as sprite:
                                sprite.save(file_path, 'png')

                # update sprites list
                if len(sprites_folder_paths) > 0:
                    self.workspace.sprites_manager.sprites_list.addSprites(sprites_folder_paths)

                # close sprite input choice dialog
                self.workspace.sprites_manager.controls.sprite_input_choice_dialog.accept()
            except:
                if os.path.exists(self.project_folder_path) == False:
                    QtWidgets.QMessageBox.critical(
                        self,
                        'Missing Project Folder',
                        "The project folder could not be found. It may have been moved or deleted. Please close the current project and either create a new one or re-open the project from its new location.",
                        QtWidgets.QMessageBox.StandardButton.Ok,
                    )

                    return
                elif os.path.exists(self.sprites_folder_path) == False:
                    QtWidgets.QMessageBox.critical(
                        self,
                        'Missing Sprites Folder',
                        "The sprites folder could not be found. It may have been moved or deleted.",
                        QtWidgets.QMessageBox.StandardButton.Ok,
                    )

                    return

    def uploadSpriteSheet(self):
        sprite_sheet = QtWidgets.QFileDialog.getOpenFileName(
            self,
            'Select sprite sheet',
            '',
            '*.png'
        )

        file_path = sprite_sheet[0]
        format = sprite_sheet[1]

        if os.path.exists(self.project_folder_path) == False:
            QtWidgets.QMessageBox.critical(
                self,
                'Missing Project Folder',
                "The project folder could not be found. It may have been moved or deleted. Please close the current project and either create a new one or re-open the project from its new location.",
                QtWidgets.QMessageBox.StandardButton.Ok,
            )

            return
        elif os.path.exists(self.temp_folder_path) == False:
            QtWidgets.QMessageBox.critical(
                self,
                'Missing Temp Folder',
                "The folder for temporary files could not be found. It may have been moved or deleted.",
                QtWidgets.QMessageBox.StandardButton.Ok,
            )

            return

        if len(file_path) > 0 and len(format) > 0:
            file_name, extension = os.path.splitext(file_path)
            iso_timestamp = datetime.datetime.isoformat(datetime.datetime.today())

            new_file_name = hashlib.sha1((file_name + iso_timestamp).encode('utf-8')).hexdigest() + extension

            save_path = os.path.join(self.temp_folder_path, new_file_name)

            # save a copy of the sprite sheet in the temp folder
            with PIL.Image.open(file_path) as sprite_sheet_file:
                sprite_sheet_file.save(save_path)

            # close sprite input choice dialog
            self.workspace.sprites_manager.controls.sprite_input_choice_dialog.accept()

            # open sprite sheet info dialog
            self.sprite_sheet_info_dialog.open(save_path)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow(app)
    main_window.show()

    sys.exit(app.exec())