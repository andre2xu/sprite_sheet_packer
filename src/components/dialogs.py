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