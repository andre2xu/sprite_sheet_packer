import pathlib, os
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

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.original_width = 350
        self.original_height = 500
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

        # INFO: area to scan
        area_to_scan_container = components.shared.VerticalBoxLayout()
        area_to_scan_container.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        ats_container_title = QtWidgets.QLabel('Area of sprite sheet to scan')

        ats_width_field_container = components.shared.HorizontalBoxLayout()
        ats_width_field_title = QtWidgets.QLabel('W:')
        ats_width_field = QtWidgets.QSpinBox()
        ats_width_field_container.addWidgets([ats_width_field_title, ats_width_field])

        ats_height_field_container = components.shared.HorizontalBoxLayout()
        ats_height_field_title = QtWidgets.QLabel('H:')
        ats_height_field = QtWidgets.QSpinBox()
        ats_height_field_container.addWidgets([ats_height_field_title, ats_height_field])

        area_to_scan_container.addWidgets([
            ats_container_title,
            ats_width_field_container,
            ats_height_field_container
        ])

        # INFO: grid square dimensions
        grid_square_dimensions_container = components.shared.VerticalBoxLayout()
        grid_square_dimensions_container.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        gsd_container_title = QtWidgets.QLabel('Grid square dimensions')

        gsd_width_field_container = components.shared.HorizontalBoxLayout()
        gsd_width_field_title = QtWidgets.QLabel('W:')
        gsd_width_field = QtWidgets.QSpinBox()
        gsd_width_field_container.addWidgets([gsd_width_field_title, gsd_width_field])

        gsd_height_field_container = components.shared.HorizontalBoxLayout()
        gsd_height_field_title = QtWidgets.QLabel('H:')
        gsd_height_field = QtWidgets.QSpinBox()
        gsd_height_field_container.addWidgets([gsd_height_field_title, gsd_height_field])

        grid_square_dimensions_container.addWidgets([
            gsd_container_title,
            gsd_width_field_container,
            gsd_height_field_container
        ])

        # INFO: background color
        background_color_container = components.shared.VerticalBoxLayout()
        bgc_field_title = QtWidgets.QLabel('Background color')
        bgc_subcontainer = components.shared.HorizontalBoxLayout()
        bgc_field = QtWidgets.QLineEdit('')
        bgc_field.setPlaceholderText('R,G,B or #aabbcc')
        auto_find_bgc_button = QtWidgets.QPushButton('Auto Find')

        bgc_subcontainer.addWidgets([
            bgc_field,
            auto_find_bgc_button
        ])

        background_color_container.addWidgets([
            bgc_field_title,
            bgc_subcontainer
        ])

        body_lyt = QtWidgets.QVBoxLayout(body)
        body_lyt.addWidget(area_to_scan_container)
        body_lyt.addWidget(grid_square_dimensions_container)
        body_lyt.addWidget(background_color_container)

        submit_button = QtWidgets.QPushButton('Start Scan')
        body_lyt.addWidget(submit_button)

        layout.addWidget(body)