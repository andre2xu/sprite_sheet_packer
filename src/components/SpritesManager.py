import components.shared
from PySide6 import QtWidgets, QtCore
from PySide6.QtWidgets import QSizePolicy



class Controls(components.shared.HorizontalBoxLayout):
    def __init__(self):
        super(Controls, self).__init__()

        add_sprites_btn = QtWidgets.QPushButton('Add Sprites')
        add_sprites_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        add_sprites_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        clear_all_sprites_btn = QtWidgets.QPushButton('Clear All')
        clear_all_sprites_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        clear_all_sprites_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.addWidgets([
            add_sprites_btn,
            clear_all_sprites_btn
        ])
        self.lyt.addStretch(0)

        self.setStyleSheet(
            """
            QWidget {
                border-top: 3px solid #242629;
            }

            QWidget QPushButton {
                border: none;
                background-color: #212124;
                padding: 8px 20px;
                margin: 0px 5px;
            }
            """
        )

        self.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))



class SpritesList(components.shared.VerticalBoxLayout):
    def __init__(self):
        super(SpritesList, self).__init__()

        vertical_list = components.shared.VerticallyScrollableWidget()
        vertical_list.setWidgetResizable(True)
        vertical_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        vertical_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        list_items = [
            QtWidgets.QLabel('Sprite 1'),
            QtWidgets.QLabel('Sprite 2'),
            QtWidgets.QLabel('Sprite 3')
        ]

        for i in range(len(list_items)):
            li = list_items[i]
            li.setContentsMargins(0,0,0,0)
            li.setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        vertical_list.lytw.addWidgets(list_items)
        vertical_list.lytw.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum))
        vertical_list.lytw.lyt.setContentsMargins(0,0,0,0)
        vertical_list.lytw.lyt.setSpacing(0)

        vertical_list.setStyleSheet(
            """
            QScrollArea {
                border: none;
                background-color: #212124;
            }

            QScrollArea QWidget {
                background-color: #212124;
                border: none;
            }

            QScrollArea QWidget QLabel {
                border: 1px solid #37393c;
                background-color: #2c2e30;
                border-bottom: none;
                padding: 20px 10px;
            }

            QScrollArea QWidget QLabel::hover {
                background-color: #3b4045;
            }
            """
        )
        list_items[-1].setStyleSheet("""border-bottom: 1px solid #37393c;""")

        self.lyt.addWidget(vertical_list)