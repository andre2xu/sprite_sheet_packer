import pathlib, os, ast, re, datetime, rectpack, json
import PIL.Image, PIL.ImageColor
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
import components.shared



class SpriteInputChoiceDialog(QtWidgets.QDialog):
    class Option(components.shared.VerticalBoxLayout, QtCore.QObject):
        clicked = QtCore.Signal(QtGui.QMouseEvent)

        def __init__(self, parent: QtWidgets.QWidget | None = None):
            super().__init__(parent)

            self.setMouseTracking(True)

        def enterEvent(self, event: QtGui.QEnterEvent):
            # change the text color when the mouse is hovering over
            self.children()[1].setStyleSheet(
                """
                    margin-top: 10px;
                    color: yellow;
                """
            )

            return super().enterEvent(event)

        def leaveEvent(self, event: QtGui.QMouseEvent):
            # reset the text color when the mouse is no longer hovering over the option
            self.children()[1].setStyleSheet(
                """
                    margin-top: 10px;
                    color: white;
                """
            )

            return super().leaveEvent(event)

        def mouseReleaseEvent(self, event: QtGui.QMouseEvent):
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self.clicked.emit(event)

            return super().mouseReleaseEvent(event)

    def __init__(self, parent: QtWidgets.QWidget | None = None, f: QtCore.Qt.WindowType = ...):
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
                color: white;
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
                color: white;
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

        ICONS_FOLDER_PATH = os.path.join(pathlib.Path(__file__).parent.parent.resolve(), 'icons')

        self.sprite_sheet_option = self.Option()
        self.sprite_sheet_option.lyt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sprite_sheet_option_image = QtWidgets.QLabel('')
        self.sprite_sheet_option_image.setPixmap(QtGui.QPixmap(os.path.join(ICONS_FOLDER_PATH, 'sprite_input_sheet_option.png')))
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
        self.selection_option_image.setPixmap(QtGui.QPixmap(os.path.join(ICONS_FOLDER_PATH, 'sprite_input_selection_option.png')))
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
    def __init__(self, parent: QtWidgets.QWidget | None = None, f: QtCore.Qt.WindowType = ...):
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
                    color: white;
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
                color: white;
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
        file_dialog_button.setAutoDefault(False)
        file_dialog_button.setDefault(False)

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
                color: white;
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
                color: white;
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
                color: white;
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

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key.Key_Return or key == QtCore.Qt.Key.Key_Enter:
            self.submit_button.click()

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
    def __init__(self, parent: QtWidgets.QWidget | None = None, f: QtCore.Qt.WindowType = ...):
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
                color: white;
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

        ats_startX_field_container = components.shared.HorizontalBoxLayout()
        ats_startX_field_title = QtWidgets.QLabel('StartX:')
        self.ats_startX_field = QtWidgets.QSpinBox()
        self.ats_startX_field.setFixedWidth(dimensions_field_width)
        self.ats_startX_field.setMinimum(0)
        self.ats_startX_field.setCorrectionMode(QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue)
        ats_startX_field_container.addWidgets([ats_startX_field_title, self.ats_startX_field])

        ats_startY_field_container = components.shared.HorizontalBoxLayout()
        ats_startY_field_title = QtWidgets.QLabel('StartY:')
        self.ats_startY_field = QtWidgets.QSpinBox()
        self.ats_startY_field.setFixedWidth(dimensions_field_width)
        self.ats_startY_field.setMinimum(0)
        self.ats_startY_field.setCorrectionMode(QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue)
        ats_startY_field_container.addWidgets([ats_startY_field_title, self.ats_startY_field])

        ats_subcontainer = components.shared.HorizontalBoxLayout()
        ats_subcontainer.lyt.setContentsMargins(0,0,0,0)
        ats_subcontainer_subcontainer1 = components.shared.VerticalBoxLayout()
        ats_subcontainer_subcontainer1.lyt.setContentsMargins(0,0,0,0)
        ats_subcontainer_subcontainer2 = components.shared.VerticalBoxLayout()
        ats_subcontainer_subcontainer2.lyt.setContentsMargins(0,0,0,0)

        ats_subcontainer_subcontainer1.addWidgets([
            ats_width_field_container,
            ats_height_field_container
        ])

        ats_subcontainer_subcontainer2.addWidgets([
            ats_startX_field_container,
            ats_startY_field_container
        ])

        ats_subcontainer.addWidgets([
            ats_subcontainer_subcontainer1,
            ats_subcontainer_subcontainer2
        ])

        area_to_scan_container.addWidgets([
            ats_container_title,
            ats_subcontainer
        ])

        area_to_scan_container.setStyleSheet(
            """
            QLabel {
                margin-bottom: 5px;
                color: white;
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
        self.gsd_width_field.setCorrectionMode(QtWidgets.QSpinBox.CorrectionMode.CorrectToNearestValue)
        gsd_width_field_container.addWidgets([gsd_width_field_title, self.gsd_width_field])
        gsd_width_field_container.lyt.addStretch(0)

        gsd_height_field_container = components.shared.HorizontalBoxLayout()
        gsd_height_field_title = QtWidgets.QLabel('H:')
        gsd_height_field_title.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.gsd_height_field = QtWidgets.QSpinBox()
        self.gsd_height_field.setFixedWidth(dimensions_field_width)
        self.gsd_height_field.setMinimum(1)
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
                color: white;
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
                color: white;
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
                color: white;
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
                color: white;
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
                color: white;
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
                # reset fields
                self.ats_startX_field.setValue(0)
                self.ats_startY_field.setValue(0)
                self.gsd_width_field.setValue(1)
                self.gsd_height_field.setValue(1)
                self.bgc_field.setText('')
                self.bgc_opacity_field.setValue(0)

                # change the maximum values of the dimension fields
                self.ats_width_field.setMaximum(sprite_sheet.width)
                self.ats_height_field.setMaximum(sprite_sheet.height)

                self.gsd_width_field.setMaximum(sprite_sheet.width)
                self.gsd_height_field.setMaximum(sprite_sheet.height)

                # change the maximum values of the area to scan starting coordinates (smallest area is 1x1)
                self.ats_startX_field.setMaximum(sprite_sheet.width - 1)
                self.ats_startY_field.setMaximum(sprite_sheet.height - 1)

                # pre-populate the area to scan fields with the sprite sheet's dimensions
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

            ats_startX = self.ats_startX_field.value()
            ats_startY = self.ats_startY_field.value()

            gsd_width = self.gsd_width_field.value()
            gsd_height = self.gsd_height_field.value()

            bg_color = self.bgc_field.text().rstrip()
            bg_color_opacity = round((self.bgc_opacity_field.value() / 100) * 255) # converted from % to RGB

            # validate area to scan
            with PIL.Image.open(self.uploaded_sprite_sheet_path) as sprite_sheet:
                horizontal_overflow_exists = sprite_sheet.width - (ats_startX + ats_width) < 0
                vertical_overflow_exists = sprite_sheet.height - (ats_startY + ats_height) < 0

                if horizontal_overflow_exists or vertical_overflow_exists:
                    QtWidgets.QMessageBox.critical(
                        main_window,
                        'Out of Bounds',
                        "The area to scan is not fully inside the sprite sheet.",
                        QtWidgets.QMessageBox.StandardButton.Ok
                    )

                    return

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
                sprite_sheet = components.shared.SpriteSheet(self.uploaded_sprite_sheet_path, self.sprite_sheet_bg_color, self)

                try:
                    sprites = sprite_sheet.getSprites(
                        ats_startX,
                        ats_startY,
                        ats_width,
                        ats_height,
                        gsd_width,
                        gsd_height
                    )

                    if len(sprites) > 0:
                        # save the sprites in the sprite folder
                        for i in range(len(sprites)):
                            sprite = sprites[i]

                            timestamp = datetime.datetime.today().strftime('%d%m%Y%H%M%S%f')
                            new_file_name = f'sprite{i}{i*2}{i*3}{timestamp}' + '.png'

                            if os.path.exists(main_window.sprites_folder_path):
                                sprite.save(os.path.join(main_window.sprites_folder_path, new_file_name))
                            else:
                                raise Exception("The sprites folder is missing. It may have been moved or deleted.")

                        # reload the sprites list
                        main_window.workspace.sprites_manager.sprites_list.reloadList()

                        # close the sprite sheet and the dialog
                        sprite_sheet.close()

                        return self.accept()
                except Exception as error:
                    sprite_sheet.progress_bar_dialog.close()

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



class SpriteSheetLayoutDialog(QtWidgets.QDialog):
    def __init__(self, parent: QtWidgets.QWidget | None = None, f: QtCore.Qt.WindowType = ...):
        super().__init__(parent, f)

        self.main_window = self.parent()
        self.sprites_list = self.main_window.workspace.sprites_manager.sprites_list

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
                color: white;
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

            #DialogBody QPushButton {
                background-color: #47474e;
                padding: 10px 0px;
                border: none;
                color: white;
            }

            #DialogBody QPushButton:hover {
                border: 1px solid gray;
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
        tb_lyt.addWidget(QtWidgets.QLabel('Choose Sprite Sheet Layout'))
        tb_lyt.addStretch(0)
        tb_lyt.addWidget(self.close_button)

        layout.addWidget(title_bar)

        # dialog body
        body = QtWidgets.QWidget()
        body.setObjectName('DialogBody')

        body_lyt = QtWidgets.QVBoxLayout(body)
        body_lyt.setSpacing(0)
        body_lyt.setContentsMargins(0,0,0,0)

        # LAYOUT: horizontal
        layout_group1 = components.shared.HorizontalBoxLayout()
        layout_group1.setStyleSheet("""QPushButton { margin: 10px 7px 0px; }""")
        self.horizontal_layout_btn = QtWidgets.QPushButton('Horizontal')
        self.horizontal_reverse_layout_btn = QtWidgets.QPushButton('Horizontal Reverse')
        layout_group1.addWidgets([self.horizontal_layout_btn, self.horizontal_reverse_layout_btn])

        # LAYOUT: vertical
        layout_group2 = components.shared.HorizontalBoxLayout()
        layout_group2.setStyleSheet("""QPushButton { margin: 0px 7px; }""")
        self.vertical_layout_btn = QtWidgets.QPushButton('Vertical')
        self.vertical_reverse_layout_btn = QtWidgets.QPushButton('Vertical Reverse')
        layout_group2.addWidgets([self.vertical_layout_btn, self.vertical_reverse_layout_btn])

        # LAYOUT: compact
        layout_group3 = components.shared.HorizontalBoxLayout()
        layout_group3.setStyleSheet("""QPushButton { margin: 0px 7px 15px; }""")
        self.compact_layout_btn = QtWidgets.QPushButton('Compact')
        layout_group3.addWidgets([self.compact_layout_btn])

        body_lyt.addWidget(layout_group1)
        body_lyt.addWidget(layout_group2)
        body_lyt.addWidget(layout_group3)

        layout.addWidget(body)

        # connect slots
        self.horizontal_layout_btn.clicked.connect(self.createHorizontalSpriteSheet)
        self.horizontal_reverse_layout_btn.clicked.connect(self.createReverseHorizontalSpriteSheet)
        self.vertical_layout_btn.clicked.connect(self.createVerticalSpriteSheet)
        self.vertical_reverse_layout_btn.clicked.connect(self.createReverseVerticalSpriteSheet)
        self.compact_layout_btn.clicked.connect(self.createCompactSpriteSheet)

        # initialize progress dialog
        self.progress_bar_dialog = QtWidgets.QProgressDialog('Sprites Packed', 'Cancel', 0, 100, self, QtCore.Qt.WindowType.FramelessWindowHint)
        self.progress_bar_dialog.setValue(0)
        self.progress_bar_dialog.close()

        self.cancel_packing = False
        self.progress_bar_dialog.canceled.connect(self.cancelPacking)

    def getSpriteImages(self):
        sprite_images = []

        list_widget = self.sprites_list.vertical_list

        if os.path.exists(self.main_window.sprites_folder_path) == False:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                'Missing Sprites Folder',
                "The sprites folder could not be found. It may have been moved or deleted.",
                QtWidgets.QMessageBox.StandardButton.Ok,
            )

            return []
        else:
            for i in range(list_widget.count()):
                list_item = list_widget.item(i)
                sprite_image_src = list_item.src

                if os.path.exists(sprite_image_src):
                    with PIL.Image.open(sprite_image_src) as sprite_image_file:
                        sprite = sprite_image_file.convert('RGBA')

                        sprite.filename = os.path.basename(list_item.src)

                        sprite_images.append(sprite)
                else:
                    # mark sprite as missing and show error message
                    list_item.setText(f'[MISSING] {list_item.text()}')

                    QtWidgets.QMessageBox.critical(
                        self.main_window,
                        'Missing Sprite',
                        f"The sprite \"{os.path.basename(sprite_image_src)}\" is missing. It may have been moved or deleted. To continue the packing, please remove it from the sprites list or put it back in the project's sprites folder if it still exists. You could also re-open the project folder to reload the sprites list.",
                        QtWidgets.QMessageBox.StandardButton.Ok,
                    )

                    return []

        return sprite_images

    def cancelPacking(self):
        self.cancel_packing = True

    def createHorizontalSpriteSheet(self):
        if os.path.exists(self.main_window.project_folder_path) == False:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                'Missing Project Folder',
                "The project folder could not be found. It may have been moved or deleted. Please close the current project and either create a new one or re-open the project from its new location.",
                QtWidgets.QMessageBox.StandardButton.Ok,
            )

            return

        sprites = self.getSpriteImages()

        if len(sprites) > 0:
            total_width = 0
            max_height = 0

            for i in range(len(sprites)):
                sprite = sprites[i]

                total_width += sprite.width

                if sprite.height > max_height:
                    max_height = sprite.height

            # create sprite sheet
            horizontal_sprite_sheet = PIL.Image.new('RGBA', (total_width, max_height))
            x, y = 0, 0

            self.progress_bar_dialog.open()

            data_sheet = {}

            for i in range(len(sprites)):
                if self.cancel_packing:
                    # reset flag
                    self.cancel_packing = False

                    return

                sprite = sprites[i]

                horizontal_sprite_sheet.paste(sprite, (x, y))

                # add the current sprite's bounding box data to the data sheet
                data_sheet[sprite.filename] = {
                    'x': x,
                    'y': y,
                    'w': sprite.width,
                    'h': sprite.height
                }

                # update progress bar
                self.progress_bar_dialog.setValue(((i+1) / len(sprites)) * 100)

                x += sprite.width

            if os.path.exists(self.main_window.temp_folder_path) == False:
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    'Missing Temp Folder',
                    "The folder for temporary files could not be found. It may have been moved or deleted.",
                    QtWidgets.QMessageBox.StandardButton.Ok,
                )

                # close progress bar dialog
                self.progress_bar_dialog.accept()
            else:
                # save sprite sheet in the temp folder
                horizontal_sprite_sheet.save(os.path.join(self.main_window.temp_folder_path, 'spritesheet.png'))

                # create data sheet
                self.createDataSheet(data_sheet)

                # close the dialogs
                self.progress_bar_dialog.accept()
                self.accept()

    def createReverseHorizontalSpriteSheet(self):
        if os.path.exists(self.main_window.project_folder_path) == False:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                'Missing Project Folder',
                "The project folder could not be found. It may have been moved or deleted. Please close the current project and either create a new one or re-open the project from its new location.",
                QtWidgets.QMessageBox.StandardButton.Ok,
            )

            return

        sprites = self.getSpriteImages()

        if len(sprites) > 0:
            total_width = 0
            max_height = 0

            for i in range(len(sprites)):
                sprite = sprites[i]

                total_width += sprite.width

                if sprite.height > max_height:
                    max_height = sprite.height

            # create sprite sheet
            reverse_horizontal_sprite_sheet = PIL.Image.new('RGBA', (total_width, max_height))
            x, y = 0, 0

            self.progress_bar_dialog.open()
            progress = 0

            data_sheet = {}

            for i in range(len(sprites) - 1, -1, -1):
                if self.cancel_packing:
                    # reset flag
                    self.cancel_packing = False

                    return

                sprite = sprites[i]

                reverse_horizontal_sprite_sheet.paste(sprite, (x, y))

                # add the current sprite's bounding box data to the data sheet
                data_sheet[sprite.filename] = {
                    'x': x,
                    'y': y,
                    'w': sprite.width,
                    'h': sprite.height
                }

                # update progress bar
                progress += 1
                self.progress_bar_dialog.setValue((progress / len(sprites)) * 100)

                x += sprite.width

            if os.path.exists(self.main_window.temp_folder_path) == False:
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    'Missing Temp Folder',
                    "The folder for temporary files could not be found. It may have been moved or deleted.",
                    QtWidgets.QMessageBox.StandardButton.Ok,
                )

                # close progress bar dialog
                self.progress_bar_dialog.accept()
            else:
                # save sprite sheet in the temp folder
                reverse_horizontal_sprite_sheet.save(os.path.join(self.main_window.temp_folder_path, 'spritesheet.png'))

                # create data sheet
                self.createDataSheet(data_sheet)

                # close the dialogs
                self.progress_bar_dialog.accept()
                self.accept()

    def createVerticalSpriteSheet(self):
        if os.path.exists(self.main_window.project_folder_path) == False:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                'Missing Project Folder',
                "The project folder could not be found. It may have been moved or deleted. Please close the current project and either create a new one or re-open the project from its new location.",
                QtWidgets.QMessageBox.StandardButton.Ok,
            )

            return

        sprites = self.getSpriteImages()

        if len(sprites) > 0:
            total_height = 0
            max_width = 0

            for i in range(len(sprites)):
                sprite = sprites[i]

                total_height += sprite.height

                if sprite.width > max_width:
                    max_width = sprite.width

            # create sprite sheet
            vertical_sprite_sheet = PIL.Image.new('RGBA', (max_width, total_height))
            x, y = 0, 0

            self.progress_bar_dialog.open()

            data_sheet = {}

            for i in range(len(sprites)):
                if self.cancel_packing:
                    # reset flag
                    self.cancel_packing = False

                    return

                sprite = sprites[i]

                vertical_sprite_sheet.paste(sprite, (x, y))

                # add the current sprite's bounding box data to the data sheet
                data_sheet[sprite.filename] = {
                    'x': x,
                    'y': y,
                    'w': sprite.width,
                    'h': sprite.height
                }

                # update progress bar
                self.progress_bar_dialog.setValue(((i+1) / len(sprites)) * 100)

                y += sprite.height

            if os.path.exists(self.main_window.temp_folder_path) == False:
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    'Missing Temp Folder',
                    "The folder for temporary files could not be found. It may have been moved or deleted.",
                    QtWidgets.QMessageBox.StandardButton.Ok,
                )

                # close progress bar dialog
                self.progress_bar_dialog.accept()
            else:
                # save sprite sheet in the temp folder
                vertical_sprite_sheet.save(os.path.join(self.main_window.temp_folder_path, 'spritesheet.png'))

                # create data sheet
                self.createDataSheet(data_sheet)

                # close the dialogs
                self.progress_bar_dialog.accept()
                self.accept()

    def createReverseVerticalSpriteSheet(self):
        if os.path.exists(self.main_window.project_folder_path) == False:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                'Missing Project Folder',
                "The project folder could not be found. It may have been moved or deleted. Please close the current project and either create a new one or re-open the project from its new location.",
                QtWidgets.QMessageBox.StandardButton.Ok,
            )

            return

        sprites = self.getSpriteImages()

        if len(sprites) > 0:
            total_height = 0
            max_width = 0

            for i in range(len(sprites)):
                sprite = sprites[i]

                total_height += sprite.height

                if sprite.width > max_width:
                    max_width = sprite.width

            # create sprite sheet
            vertical_sprite_sheet = PIL.Image.new('RGBA', (max_width, total_height))
            x, y = 0, 0

            self.progress_bar_dialog.open()
            progress = 0

            data_sheet = {}

            for i in range(len(sprites) - 1, -1, -1):
                if self.cancel_packing:
                    # reset flag
                    self.cancel_packing = False

                    return

                sprite = sprites[i]

                vertical_sprite_sheet.paste(sprite, (x, y))

                # add the current sprite's bounding box data to the data sheet
                data_sheet[sprite.filename] = {
                    'x': x,
                    'y': y,
                    'w': sprite.width,
                    'h': sprite.height
                }

                # update progress bar
                progress += 1
                self.progress_bar_dialog.setValue((progress / len(sprites)) * 100)

                y += sprite.height

            if os.path.exists(self.main_window.temp_folder_path) == False:
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    'Missing Temp Folder',
                    "The folder for temporary files could not be found. It may have been moved or deleted.",
                    QtWidgets.QMessageBox.StandardButton.Ok,
                )

                # close progress bar dialog
                self.progress_bar_dialog.accept()
            else:
                # save sprite sheet in the temp folder
                vertical_sprite_sheet.save(os.path.join(self.main_window.temp_folder_path, 'spritesheet.png'))

                # create data sheet
                self.createDataSheet(data_sheet)

                # close the dialogs
                self.progress_bar_dialog.accept()
                self.accept()

    def createCompactSpriteSheet(self):
        if os.path.exists(self.main_window.project_folder_path) == False:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                'Missing Project Folder',
                "The project folder could not be found. It may have been moved or deleted. Please close the current project and either create a new one or re-open the project from its new location.",
                QtWidgets.QMessageBox.StandardButton.Ok,
            )

            return

        sprites = self.getSpriteImages()

        if len(sprites) > 0:
            # initialize packer
            packer = rectpack.newPacker()

            # iterate over the sprite pillow image instances
            total_width = 0
            total_height = 0

            for i in range(len(sprites)):
                sprite = sprites[i]

                # pass the dimensions of the sprite images (in the form of a rectangle) to the packer
                packer.add_rect(sprite.width, sprite.height, rid=i)

                # calculate the sprite sheet dimensions needed to fit all the sprites (this won't be an exact fit and it will have a large excess of empty pixels because all it gets is the largest box that can fit all the sprites)
                total_width += sprite.width
                total_height += sprite.height

            # pass sprite sheet dimensions (in the form of a rectangle) to the packer
            packer.add_bin(total_width, total_height)

            # arrange all the sprites in the sprite sheet rectangle in a way that reduces the amount of gaps in between them (i.e. compact packing) 
            packer.pack()

            # retrieve the geometry and positional data of the sprites in the compact sprite sheet
            data = packer.rect_list()

            # create sheet using the rough dimensions
            compact_sprite_sheet = PIL.Image.new('RGBA', (total_width, total_height))

            # iterate over the sprite data
            self.progress_bar_dialog.open()

            data_sheet = {}

            for i in range(len(data)):
                if self.cancel_packing:
                    # reset flag
                    self.cancel_packing = False

                    return

                d = data[i]
                sprite_index = d[5]
                sprite = sprites[sprite_index]

                x, y = d[1], d[2]

                if y > 0:
                    # find the empty row (i.e. a horizontal set of transparent pixels. The no. pixels are equal to the width of the current sprite)
                    row_is_empty = False

                    while row_is_empty == False:
                        row_is_empty = True # assume the current row is empty

                        current_x = x
                        last_x = x + sprite.width + 1

                        while current_x < last_x:
                            current_pixel = compact_sprite_sheet.getpixel((current_x, y))

                            # find a non-transparent pixel and, if one is found, skip to the next row
                            if current_pixel != (0,0,0,0):
                                row_is_empty = False
                                break

                            current_x += 1

                        if row_is_empty:
                            # stop searching since the current y value should be pointing to the empty row 
                            break
                        else:
                            y += 1

                if x > 0:
                    # find the empty column (i.e. a vertical set of transparent pixels. The no. pixels are equal to the height of the current sprite)
                    column_is_empty = False

                    while column_is_empty == False:
                        column_is_empty = True # assume the current column is empty

                        current_y = y
                        last_y = y + sprite.height + 1

                        while current_y < last_y:
                            current_pixel = compact_sprite_sheet.getpixel((x, current_y))

                            # find a non-transparent pixel and, if one is found, skip to the next column
                            if current_pixel != (0,0,0,0):
                                column_is_empty = False
                                break

                            current_y += 1

                        if column_is_empty:
                            # stop searching since the current x value should be pointing to the empty column 
                            break
                        else:
                            x += 1

                # add the current sprite on to the sprite sheet
                compact_sprite_sheet.paste(sprite, (x, y))

                # add the current sprite's bounding box data to the data sheet
                data_sheet[sprite.filename] = {
                    'x': x,
                    'y': y,
                    'w': sprite.width,
                    'h': sprite.height
                }

                # update progress bar
                self.progress_bar_dialog.setValue(((i+1) / len(sprites)) * 100)

            if os.path.exists(self.main_window.temp_folder_path) == False:
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    'Missing Temp Folder',
                    "The folder for temporary files could not be found. It may have been moved or deleted.",
                    QtWidgets.QMessageBox.StandardButton.Ok,
                )

                # close progress bar dialog
                self.progress_bar_dialog.accept()
            else:
                # get rid of excess transparent pixels
                compact_sprite_sheet = compact_sprite_sheet.crop(compact_sprite_sheet.getbbox(alpha_only=True))

                # save the sprite sheet in the temp folder
                compact_sprite_sheet.save(os.path.join(self.main_window.temp_folder_path, 'spritesheet.png'))

                # create data sheet
                self.createDataSheet(data_sheet)

                # close the dialogs
                self.progress_bar_dialog.accept()
                self.accept()

    def createDataSheet(self, data: dict):
        with open(os.path.join(self.main_window.temp_folder_path, 'datasheet.json'), 'w+') as json_file:
            json.dump(data, json_file, indent=4)