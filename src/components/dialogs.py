import pathlib, os, PIL, ast, re, hashlib, datetime
import PIL.Image
import PIL.ImageColor
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
import components.shared



class SpriteInputChoiceDialog(QtWidgets.QDialog):
    class Option(components.shared.VerticalBoxLayout, QtCore.QObject):
        clicked = QtCore.Signal(QtGui.QMouseEvent)

        def __init__(self, parent=None):
            super().__init__(parent)

            self.setMouseTracking(True)

        def enterEvent(self, event):
            # change the text color when the mouse is hovering over
            self.children()[1].setStyleSheet(
                """
                    margin-top: 10px;
                    color: yellow;
                """
            )

            return super().enterEvent(event)

        def leaveEvent(self, event):
            # reset the text color when the mouse is no longer hovering over the option
            self.children()[1].setStyleSheet(
                """
                    margin-top: 10px;
                    color: white;
                """
            )

            return super().leaveEvent(event)

        def mouseReleaseEvent(self, event):
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.clicked.emit(event)

            return super().mouseReleaseEvent(event)

    def __init__(self, parent = ..., f = ...):
        super().__init__(parent, f)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.original_width = 350
        self.original_height = 230
        self.setFixedSize(self.original_width, self.original_height)

        self.setStyleSheet(
            """
            QDialog {
                background-color: transparent;
            }

            #DialogTitleBar {
                background-color: #2f2f36;
            }

            #DialogTitleBar QLabel {
                font-weight: bold;
                margin-left: 8px;
            }

            #DialogTitleBar QPushButton {
                color: #fff;
                padding: 3px 10px;
                border-radius: 0px;
                font-size: 15px;
            }

            #DialogTitleBar QPushButton:hover {
                background-color: red;
            }

            #DialogBody {
                background-color: #36363c;
            }

            #DialogBody QLabel {
                background-position: top center;
                background-repeat: none;
            }
            """
        )

        # dialog title bar
        title_bar = QtWidgets.QWidget()
        title_bar.setObjectName('DialogTitleBar')
        title_bar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))

        self.close_button = QtWidgets.QPushButton('X')
        self.close_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.close)

        tb_lyt = QtWidgets.QHBoxLayout(title_bar)
        tb_lyt.addWidget(QtWidgets.QLabel('Choose Your Input Type'))
        tb_lyt.addStretch(0)
        tb_lyt.addWidget(self.close_button)

        layout.addWidget(title_bar)

        # dialog body
        body = QtWidgets.QWidget()
        body.setObjectName('DialogBody')

        icons_folder = os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), 'local/icons')

        self.sprite_sheet_option = self.Option()
        self.sprite_sheet_option.lyt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sprite_sheet_option_image = QtWidgets.QLabel('')
        self.sprite_sheet_option_image.setPixmap(QtGui.QPixmap(os.path.join(icons_folder, 'sprite_input_sheet_option.png')))
        self.sprite_sheet_option_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sprite_sheet_option_image.setScaledContents(True)
        self.sprite_sheet_option_text = QtWidgets.QLabel('Sheet', self.sprite_sheet_option)
        self.sprite_sheet_option_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sprite_sheet_option_text.setStyleSheet("""margin-top: 10px;""")
        self.sprite_sheet_option.addWidgets([
            self.sprite_sheet_option_image,
            self.sprite_sheet_option_text
        ])

        self.selection_option = self.Option()
        self.selection_option.lyt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.selection_option_image = QtWidgets.QLabel('')
        self.selection_option_image.setPixmap(QtGui.QPixmap(os.path.join(icons_folder, 'sprite_input_selection_option.png')))
        self.selection_option_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.selection_option_image.setScaledContents(True)
        self.selection_option_text = QtWidgets.QLabel('Selection', self.selection_option)
        self.selection_option_text.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.selection_option_text.setStyleSheet("""margin-top: 10px;""")
        self.selection_option.addWidgets([
            self.selection_option_image,
            self.selection_option_text
        ])

        body_lyt = QtWidgets.QHBoxLayout(body)
        body_lyt.addWidget(self.sprite_sheet_option)
        body_lyt.addWidget(self.selection_option)

        layout.addWidget(body)



class FileMenuNewProjectDialog(QtWidgets.QDialog):
    def __init__(self, parent = ..., f = ...):
        super().__init__(parent, f)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.original_width = 310
        self.original_height = 300
        self.setFixedSize(self.original_width, self.original_height)

        self.setStyleSheet(
                """
                QDialog {
                    background-color: transparent;
                }

                #DialogTitleBar {
                    background-color: #2f2f36;
                }

                #DialogTitleBar QLabel {
                    font-weight: bold;
                    margin-left: 8px;
                }

                #DialogTitleBar QPushButton {
                    color: #fff;
                    padding: 3px 10px;
                    border-radius: 0px;
                    font-size: 15px;
                }

                #DialogTitleBar QPushButton:hover {
                    background-color: red;
                }

                #DialogBody {
                    background-color: #36363c;
                }
                """
            )

        # dialog title bar
        title_bar = QtWidgets.QWidget()
        title_bar.setObjectName('DialogTitleBar')
        title_bar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))

        self.close_button = QtWidgets.QPushButton('X')
        self.close_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.close)

        tb_lyt = QtWidgets.QHBoxLayout(title_bar)
        tb_lyt.addWidget(QtWidgets.QLabel('Create a new project folder'))
        tb_lyt.addStretch(0)
        tb_lyt.addWidget(self.close_button)

        layout.addWidget(title_bar)

        # dialog body
        body = QtWidgets.QWidget()
        body.setObjectName('DialogBody')

        body_lyt = QtWidgets.QVBoxLayout(body)
        body_lyt.setSpacing(0)
        body_lyt.setContentsMargins(0,0,0,0)

        self.DEFAULT_PROJECT_NAME = 'New project'
        self.PROJECT_FOLDER_LOCATION_PLACEHOLDER = '/path/to/project'

        folder_name_field_container = components.shared.VerticalBoxLayout()
        folder_name_field_container.setObjectName('FolderNameFieldContainer')
        folder_name_field_container.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        folder_name_field_container.lyt.setSpacing(0)
        folder_name_field_container.lyt.setContentsMargins(0,0,0,0)
        folder_name_field_label = QtWidgets.QLabel('Project Name')
        folder_name_field_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        self.folder_name_field = QtWidgets.QLineEdit(self.DEFAULT_PROJECT_NAME)

        folder_name_field_container.lyt.addStretch(0)

        folder_name_field_container.addWidgets([
            folder_name_field_label,
            self.folder_name_field
        ])

        folder_name_field_container.lyt.addStretch(0)

        folder_name_field_container.setStyleSheet(
            """
            #FolderNameFieldContainer QLabel {
                margin: 15px 15px 10px;
            }

            #FolderNameFieldContainer QLineEdit {
                border-radius: 5px;
                border: 1px solid #545458;
                color: #a6a6ad;
                margin: 0px 15px 15px;
                padding: 3px;
                background-color: transparent;
            }
            """
        )

        folder_location_field_container = components.shared.VerticalBoxLayout()
        folder_location_field_container.setObjectName('FolderLocationFieldContainer')
        folder_location_field_container.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        folder_location_field_container.lyt.setSpacing(0)
        folder_location_field_container.lyt.setContentsMargins(0,0,0,0)
        folder_location_field_label = QtWidgets.QLabel('Project Location')

        folder_location_field_subcontainer = components.shared.HorizontalBoxLayout()
        folder_location_field_subcontainer.setObjectName('FolderLocationFieldSubContainer')
        folder_location_field_subcontainer.lyt.setSpacing(0)
        folder_location_field_subcontainer.lyt.setContentsMargins(0,0,0,0)
        folder_location_field_subcontainer.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        self.folder_location_field = QtWidgets.QLabel(self.PROJECT_FOLDER_LOCATION_PLACEHOLDER)
        self.folder_location_field.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        self.folder_location_field.setToolTip(self.folder_location_field.text())
        file_dialog_button = QtWidgets.QPushButton('Search')
        file_dialog_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum))
        file_dialog_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        file_dialog_button.clicked.connect(self.getFolderLocationFromUser)

        folder_location_field_subcontainer.addWidgets([
            self.folder_location_field,
            file_dialog_button
        ])

        folder_location_field_container.addWidgets([
            folder_location_field_label,
            folder_location_field_subcontainer
        ])

        folder_location_field_container.setStyleSheet(
            """
            #FolderLocationFieldContainer QLabel {
                margin: 15px 15px 10px;
            }

            #FolderLocationFieldSubContainer {
                margin: 0px 15px;
            }

            #FolderLocationFieldSubContainer QLabel {
                margin: 0px;
                margin-left: 15px;
                margin-right: 5px;
                border: 1px solid #545458;
                color: #a6a6ad;
                padding: 3px;
            }

            #FolderLocationFieldSubContainer QPushButton {
                margin: 0px;
                margin-right: 15px;
                border-radius: 0px;
                background-color: #2b2b35;
                padding: 0 8px;
            }
            """
        )

        self.submit_button = QtWidgets.QPushButton('Create')
        self.submit_button.setObjectName('SubmitButton')
        self.submit_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.submit_button.setStyleSheet(
            """
            QPushButton {
                margin: 0px 10px 20px;
                padding: 6px;
                border-radius: 6px;
                background-color: #47474e;
            }

            QPushButton:hover {
                border: 1px solid gray;
            }
            """
        )

        body_lyt.addWidget(folder_name_field_container)
        body_lyt.addWidget(folder_location_field_container)
        body_lyt.addStretch(0)
        body_lyt.addWidget(self.submit_button)

        layout.addWidget(body)

    def open(self):
        # reset the default values of the fields
        self.folder_name_field.setText(self.DEFAULT_PROJECT_NAME)
        self.folder_location_field.setText(self.PROJECT_FOLDER_LOCATION_PLACEHOLDER)
        self.folder_location_field.setToolTip(self.PROJECT_FOLDER_LOCATION_PLACEHOLDER)

        super().open()

    def getFolderLocationFromUser(self):
        main_window = self.parent()

        home_folder_paths = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.StandardLocation.DesktopLocation)
        home_folder = ''

        if len(home_folder_paths) > 0:
            home_folder = home_folder_paths[0]

        folder_location = QtWidgets.QFileDialog.getExistingDirectory(
            main_window,
            'Choose project folder location',
            home_folder, # default directory
            QtWidgets.QFileDialog.Option.ShowDirsOnly | QtWidgets.QFileDialog.Option.ReadOnly
        )

        self.folder_location_field.setText(folder_location)
        self.folder_location_field.setToolTip(folder_location)



class SpriteSheetInfoDialog(QtWidgets.QDialog):
    def __init__(self, parent = ..., f = ...):
        super().__init__(parent, f)

        self.uploaded_sprite_sheet_path = None
        self.sprite_sheet_bg_color = None

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.original_width = 350
        self.original_height = 600
        self.setFixedSize(self.original_width, self.original_height)

        self.setStyleSheet(
            """
            QDialog {
                background-color: transparent;
            }

            #DialogTitleBar {
                background-color: #2f2f36;
            }

            #DialogTitleBar QLabel {
                font-weight: bold;
                margin-left: 8px;
            }

            #DialogTitleBar QPushButton {
                color: #fff;
                padding: 3px 10px;
                border-radius: 0px;
                font-size: 15px;
            }

            #DialogTitleBar QPushButton:hover {
                background-color: red;
            }

            #DialogBody {
                background-color: #36363c;
            }
            """
        )

        # dialog title bar
        title_bar = QtWidgets.QWidget()
        title_bar.setObjectName('DialogTitleBar')
        title_bar.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))

        self.close_button = QtWidgets.QPushButton('X')
        self.close_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        self.close_button.clicked.connect(self.close)

        tb_lyt = QtWidgets.QHBoxLayout(title_bar)
        tb_lyt.addWidget(QtWidgets.QLabel('Provide info about your sheet'))
        tb_lyt.addStretch(0)
        tb_lyt.addWidget(self.close_button)

        layout.addWidget(title_bar)

        # dialog body
        body = QtWidgets.QWidget()
        body.setObjectName('DialogBody')

        dimensions_field_width = self.width() * 0.28

        # INFO: area to scan
        area_to_scan_container = components.shared.VerticalBoxLayout()
        area_to_scan_container.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        area_to_scan_container.lyt.setSpacing(0)
        ats_container_title = QtWidgets.QLabel('Area of sprite sheet to scan')

        ats_width_field_container = components.shared.HorizontalBoxLayout()
        ats_width_field_title = QtWidgets.QLabel('W:')
        ats_width_field_title.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.ats_width_field = QtWidgets.QSpinBox()
        self.ats_width_field.setFixedWidth(dimensions_field_width)
        self.ats_width_field.setMinimum(1)
        self.ats_width_field.setCorrectionMode(QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue)
        ats_width_field_container.addWidgets([ats_width_field_title, self.ats_width_field])
        ats_width_field_container.lyt.addStretch(0)

        ats_height_field_container = components.shared.HorizontalBoxLayout()
        ats_height_field_title = QtWidgets.QLabel('H:')
        ats_height_field_title.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.ats_height_field = QtWidgets.QSpinBox()
        self.ats_height_field.setFixedWidth(dimensions_field_width)
        self.ats_height_field.setMinimum(1)
        self.ats_height_field.setCorrectionMode(QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue)
        ats_height_field_container.addWidgets([ats_height_field_title, self.ats_height_field])
        ats_height_field_container.lyt.addStretch(0)

        area_to_scan_container.addWidgets([
            ats_container_title,
            ats_width_field_container,
            ats_height_field_container
        ])

        area_to_scan_container.setStyleSheet(
            """
            QLabel {
                margin-bottom: 5px;
            }

            QSpinBox {
                border-radius: 5px;
                border: 1px solid #545458;
                color: #a6a6ad;
                padding: 3px;
                background-color: transparent;
            }

            QSpinBox QLabel {
                margin: 0;
            }

            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
            }
            """
        )

        # INFO: grid square dimensions
        grid_square_dimensions_container = components.shared.VerticalBoxLayout()
        grid_square_dimensions_container.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        grid_square_dimensions_container.lyt.setSpacing(0)
        gsd_container_title = QtWidgets.QLabel('Grid square dimensions')

        gsd_width_field_container = components.shared.HorizontalBoxLayout()
        gsd_width_field_title = QtWidgets.QLabel('W:')
        gsd_width_field_title.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.gsd_width_field = QtWidgets.QSpinBox()
        self.gsd_width_field.setFixedWidth(dimensions_field_width)
        self.gsd_width_field.setMinimum(1)
        self.gsd_width_field.setValue(50) # temp
        self.gsd_width_field.setCorrectionMode(QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue)
        gsd_width_field_container.addWidgets([gsd_width_field_title, self.gsd_width_field])
        gsd_width_field_container.lyt.addStretch(0)

        gsd_height_field_container = components.shared.HorizontalBoxLayout()
        gsd_height_field_title = QtWidgets.QLabel('H:')
        gsd_height_field_title.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.gsd_height_field = QtWidgets.QSpinBox()
        self.gsd_height_field.setFixedWidth(dimensions_field_width)
        self.gsd_height_field.setMinimum(1)
        self.gsd_height_field.setValue(50) # temp
        self.gsd_height_field.setCorrectionMode(QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue)
        gsd_height_field_container.addWidgets([gsd_height_field_title, self.gsd_height_field])
        gsd_height_field_container.lyt.addStretch(0)

        grid_square_dimensions_container.addWidgets([
            gsd_container_title,
            gsd_width_field_container,
            gsd_height_field_container
        ])

        grid_square_dimensions_container.setStyleSheet(
            """
            QLabel {
                margin-bottom: 5px;
            }

            QSpinBox {
                border-radius: 5px;
                border: 1px solid #545458;
                color: #a6a6ad;
                padding: 3px;
                background-color: transparent;
            }

            QSpinBox QLabel {
                margin: 0;
            }

            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
            }
            """
        )

        # INFO: background color
        background_color_container = components.shared.VerticalBoxLayout()
        background_color_container.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        bgc_field_title = QtWidgets.QLabel('Background color')

        bgc_subcontainer = components.shared.HorizontalBoxLayout()
        bgc_subcontainer.lyt.setContentsMargins(0,0,0,0)
        self.bgc_field = QtWidgets.QLineEdit('')
        self.bgc_field.setPlaceholderText('R,G,B or #aabbcc')
        auto_find_bgc_button = QtWidgets.QPushButton('Auto Find')
        auto_find_bgc_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        auto_find_bgc_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        auto_find_bgc_button.clicked.connect(self.autoFindBackgroundColor)

        bgc_subcontainer2 = components.shared.VerticalBoxLayout()
        bgc_subcontainer2.lyt.setSpacing(0)
        bgc_subcontainer2.lyt.setContentsMargins(0,0,0,0)
        bgc_opacity_field_title = QtWidgets.QLabel('Opacity (%)')
        self.bgc_opacity_field = QtWidgets.QSpinBox()
        self.bgc_opacity_field.setMaximum(100)
        self.bgc_opacity_field.setFixedWidth(dimensions_field_width)
        self.bgc_opacity_field.setCorrectionMode(QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue)

        bgc_subcontainer2.setStyleSheet(
            """
            QLabel {
                margin-bottom: 10px;
            }

            QSpinBox {
                border-radius: 5px;
                border: 1px solid #545458;
                color: #a6a6ad;
                padding: 3px;
                background-color: transparent;
            }

            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
            }
            """
        )

        background_color_container.setStyleSheet(
            """
            QLabel {
                margin-bottom: 5px;
            }

            QLineEdit {
                margin-bottom: 15px;
                border-radius: 5px;
                border: 1px solid #545458;
                color: #a6a6ad;
                padding: 3px;
                background-color: transparent;
            }

            QPushButton {
                border-radius: 0px;
                background-color: #2b2b35;
                padding: 5px 8px;
            }
            """
        )

        bgc_subcontainer.addWidgets([
            self.bgc_field,
            auto_find_bgc_button
        ])

        bgc_subcontainer.lyt.setAlignment(auto_find_bgc_button, QtCore.Qt.AlignmentFlag.AlignTop)

        bgc_subcontainer2.addWidgets([
            bgc_opacity_field_title,
            self.bgc_opacity_field
        ])

        background_color_container.addWidgets([
            bgc_field_title,
            bgc_subcontainer,
            bgc_subcontainer2
        ])

        body_lyt = QtWidgets.QVBoxLayout(body)
        body_lyt.addWidget(area_to_scan_container)
        body_lyt.addWidget(grid_square_dimensions_container)
        body_lyt.addWidget(background_color_container)

        submit_button = QtWidgets.QPushButton('Start Scan')
        submit_button.setObjectName('SubmitButton')
        submit_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        submit_button.clicked.connect(self.submit)
        submit_button.setStyleSheet(
            """
            QPushButton {
                margin: 40px 10px 15px;
                padding: 6px;
                border-radius: 6px;
                background-color: #47474e;
            }

            QPushButton:hover {
                border: 1px solid gray;
            }
            """
        )

        body_lyt.addWidget(submit_button)

        layout.addWidget(body)

    def open(self, uploadedSpriteSheetPath: str):
        if os.path.exists(uploadedSpriteSheetPath):
            self.uploaded_sprite_sheet_path = uploadedSpriteSheetPath

            with PIL.Image.open(uploadedSpriteSheetPath) as sprite_sheet:
                # change the maximum values of the dimension fields
                self.ats_width_field.setMaximum(sprite_sheet.width)
                self.ats_height_field.setMaximum(sprite_sheet.height)

                self.gsd_width_field.setMaximum(sprite_sheet.width)
                self.gsd_height_field.setMaximum(sprite_sheet.height)

                # pre-populate the fields with the sprite sheet's dimensions
                self.ats_width_field.setValue(sprite_sheet.width)
                self.ats_height_field.setValue(sprite_sheet.height)

            return super().open()

    def close(self):
        # delete the recently uploaded sprite sheet
        pathlib.Path.unlink(self.uploaded_sprite_sheet_path, missing_ok=True)

        # reset data
        self.uploaded_sprite_sheet_path = None
        self.sprite_sheet_bg_color = None

        return super().close()

    def autoFindBackgroundColor(self):
        if os.path.exists(self.uploaded_sprite_sheet_path):
            with PIL.Image.open(self.uploaded_sprite_sheet_path) as sprite_sheet:
                pixels = list(sprite_sheet.getdata())

                # count the no. times each pixel appears
                frequencies = {}

                i = 0
                j = len(pixels) - 1

                while i <= j:
                    left_pixel = str(pixels[i])

                    if left_pixel in frequencies:
                        frequencies[left_pixel] += 1
                    else:
                        frequencies[left_pixel] = 1

                    if i != j:
                        right_pixel = str(pixels[j])

                        if right_pixel in frequencies:
                            frequencies[right_pixel] += 1
                        else:
                            frequencies[right_pixel] = 1

                    i += 1
                    j -= 1

                # get the most common pixel
                most_common = ('', -1)

                for key in frequencies:
                    frequency = frequencies[key]

                    if frequency > most_common[1]:
                        most_common = (key, frequency)

                # convert the RGBA data of the pixel back into a tuple and update the background color field
                if most_common[0] != '':
                    rgba = ast.literal_eval(most_common[0])

                    self.sprite_sheet_bg_color = rgba

                    self.bgc_field.setText(f'{rgba[0]},{rgba[1]},{rgba[2]}')
                    self.bgc_opacity_field.setValue(round((rgba[3] / 255) * 100))
        else:
            main_window = self.parent()

            QtWidgets.QMessageBox.critical(
                main_window,
                'Upload Missing',
                "The sprite sheet you uploaded either no longer exists or it was moved. The sprite sheet info dialog will now be closed as a result.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )

            self.close()

    def submit(self):
        main_window = self.parent()

        if os.path.exists(self.uploaded_sprite_sheet_path):
            # get user inputs
            ats_width = self.ats_width_field.value()
            ats_height = self.ats_height_field.value()

            gsd_width = self.gsd_width_field.value()
            gsd_height = self.gsd_height_field.value()

            bg_color = self.bgc_field.text().rstrip()
            bg_color_opacity = round((self.bgc_opacity_field.value() / 100) * 255) # converted from % to RGB

            # validate background color
            rgb_pattern = re.compile(r'^\d+, ?\d+, ?\d+$')
            hex_pattern = re.compile(r'^#([a-fA-F0-9]{2}[a-fA-F0-9]{2}[a-fA-F0-9]{2})|#([a-fA-F0-9][a-fA-F0-9][a-fA-F0-9])$')

            if rgb_pattern.match(bg_color) != None:
                # validate RGB values
                r, g, b = bg_color.replace(' ', '').split(',')

                r = int(r)
                g = int(g)
                b = int(b)

                if (r < 0 or r > 255) or (g < 0 or g > 255) or (b < 0 or b > 255):
                    QtWidgets.QMessageBox.critical(
                        main_window,
                        'Invalid RGB',
                        "RGB values can only be between 0 and 255.",
                        QtWidgets.QMessageBox.StandardButton.Ok
                    )

                    return 

                # save background color
                self.sprite_sheet_bg_color = (r, g, b, bg_color_opacity)
            elif hex_pattern.match(bg_color) != None:
                # convert hex code to RGB and save it
                self.sprite_sheet_bg_color = PIL.ImageColor.getcolor(bg_color, 'RGB') + (bg_color_opacity,)
            else:
                QtWidgets.QMessageBox.critical(
                    main_window,
                    'Invalid Background Color',
                    "The background color you provided is not an acceptable RGB or hex. Please follow one of the formats shown in the field's placeholder.",
                    QtWidgets.QMessageBox.StandardButton.Ok
                )

                return

            if self.sprite_sheet_bg_color != None:
                # initialize the sprite sheet (it will validate the uploaded file)
                sprite_sheet = components.shared.SpriteSheet(self.uploaded_sprite_sheet_path, self.sprite_sheet_bg_color)

                try:
                    sprites = sprite_sheet.getSprites(
                        ats_width,
                        ats_height,
                        gsd_width,
                        gsd_height
                    )

                    if len(sprites) > 0 and main_window.sprites_folder_path != None:
                        # save the sprites in the sprite folder
                        for i in range(len(sprites)):
                            sprite = sprites[i]

                            timestamp = datetime.datetime.today().strftime('%d%m%Y%H%M%S%f')
                            new_file_name = f'sprite{i}{i*2}{i*3}{timestamp}' + '.png'

                            sprite.save(os.path.join(main_window.sprites_folder_path, new_file_name))

                        # reload the sprites list
                        main_window.workspace.sprites_manager.sprites_list.reloadList()

                        # close the sprite sheet and the dialog
                        sprite_sheet.close()

                        return self.accept()
                except Exception as error:
                    QtWidgets.QMessageBox.critical(
                        main_window,
                        'Scan Failed',
                        str(error),
                        QtWidgets.QMessageBox.StandardButton.Ok
                    )

            # close the sprite sheet file
            sprite_sheet.close()
        else:
            QtWidgets.QMessageBox.critical(
                main_window,
                'Upload Missing',
                "The sprite sheet you uploaded either no longer exists or it was moved. The sprite sheet info dialog will now be closed as a result.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )

            self.close()