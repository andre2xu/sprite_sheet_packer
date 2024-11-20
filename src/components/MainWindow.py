import components.shared
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QSizePolicy

# GUI components
from components.Workspace import SpriteSheetPreview, SpritesManager



class Menubar(components.shared.HorizontalBoxLayout):
    def __init__(self):
        super(Menubar, self).__init__()

        file_button = QtWidgets.QPushButton('File')
        file_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        file_button.setStyleSheet("""margin-left: 5px;""")
        file_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        help_button = QtWidgets.QPushButton('Help')
        help_button.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        help_button.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.addWidgets([
            file_button,
            help_button
        ])
        self.lyt.addStretch(0) # move all widgets to the left of the menubar
        self.lyt.setSpacing(0) # remove space in-between widgets

        self.setStyleSheet(
            """
            QWidget {
                background-color: #2f3133;
            }

            QWidget QPushButton {
                border: none;
                padding: 3px 10px;
            }

            QWidget QPushButton::hover {
                background-color: #404244;
                border-radius: 5px;
            }
            """
        )

        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)) # menubar height will only be enough to fit its contents



class Workspace(components.shared.HorizontalBoxLayout):
    def __init__(self):
        super(Workspace, self).__init__()

        self.lyt.setSpacing(0)
        self.lyt.setContentsMargins(0,0,0,0)

        self.addWidgets([
            SpriteSheetPreview(),
            SpritesManager()
        ])