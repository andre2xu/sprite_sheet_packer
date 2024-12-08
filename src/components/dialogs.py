import pathlib
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
import components.shared



class SpriteInputChoiceDialog(QtWidgets.QDialog):
        class Option(components.shared.VerticalBoxLayout):
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

            icons_folder = f'{pathlib.Path(__file__).parent.parent.parent.resolve()}/local/icons'
            icons_folder = icons_folder.replace('\\', '/')

            self.sprite_sheet_option = self.Option()
            self.sprite_sheet_option.lyt.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            self.sprite_sheet_option_image = QtWidgets.QLabel('')
            self.sprite_sheet_option_image.setPixmap(QtGui.QPixmap(f'{icons_folder}/sprite_input_sheet_option.png'))
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
            self.selection_option_image.setPixmap(QtGui.QPixmap(f'{icons_folder}/sprite_input_selection_option.png'))
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



class FileMenuNewSheetDialog(QtWidgets.QDialog):
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

        folder_name_field_container = components.shared.VerticalBoxLayout()
        folder_name_field_container.setObjectName('FolderNameFieldContainer')
        folder_name_field_container.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        folder_name_field_container.lyt.setSpacing(0)
        folder_name_field_container.lyt.setContentsMargins(0,0,0,0)
        folder_name_field_label = QtWidgets.QLabel('Project Name')
        folder_name_field_label.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        self.folder_name_field = QtWidgets.QLineEdit('New Sheet')

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
        self.folder_location_field = QtWidgets.QLabel('/path/to/project')
        self.folder_location_field.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        self.folder_location_field.setToolTip(self.folder_location_field.text())
        file_explorer_button = QtWidgets.QPushButton('Search')
        file_explorer_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Minimum))
        file_explorer_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)
        file_explorer_button.clicked.connect(self.getFolderLocationFromUser)

        folder_location_field_subcontainer.addWidgets([
            self.folder_location_field,
            file_explorer_button
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

        submit_button = QtWidgets.QPushButton('Create')
        submit_button.setObjectName('SubmitButton')
        submit_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        submit_button.setStyleSheet(
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
        body_lyt.addWidget(submit_button)

        layout.addWidget(body)

    def open(self):
        # reset the default values of the fields
        self.folder_name_field.setText('New Sheet')
        self.folder_location_field.setText('/path/to/project')

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
            home_folder,
            QtWidgets.QFileDialog.Option.ShowDirsOnly | QtWidgets.QFileDialog.Option.ReadOnly
        )

        self.folder_location_field.setText(folder_location)
        self.folder_location_field.setToolTip(folder_location)