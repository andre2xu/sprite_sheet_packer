import components.shared, pathlib
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy



class SpritesListItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(SpritesListItemDelegate, self).__init__()

    def paint(self, painter, option, index):
        painter.save()

        icon = index.data(QtCore.Qt.DecorationRole)
        text = index.data(QtCore.Qt.DisplayRole)

        if icon:
            # draw icon
            icon_size = option.decorationSize

            icon_rect = QtCore.QRect(
                option.rect.x() + 20, # start 20px from the left side of list item widget
                option.rect.y() + ((option.rect.height() - icon_size.height()) // 2), # center vertically in the list item widget
                icon_size.width(),
                icon_size.height()
            )

            painter.drawPixmap(icon_rect, icon.pixmap(icon_size))

            # create custom text position
            icon_right_margin = 10

            text_rect = QtCore.QRect(
                option.rect.x() + (icon_rect.x() + icon_size.width() + icon_right_margin), # start on the right of the icon (with space in-between)
                option.rect.y(), # center vertically in the list item widget
                option.rect.width() - (icon_size.width() + icon_right_margin),
                option.rect.height()
            )
        else:
            text_rect = option.rect # use default position if there's no icon

        # draw text
        painter.drawText(
            text_rect,
            QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter,
            text
        )

        # draw border-bottom
        border_color = QtGui.QColor('#37393c')

        painter.setPen(QtCore.Qt.PenStyle.SolidLine)
        painter.setPen(border_color)
        painter.setBrush(border_color)

        painter.drawLine(
            option.rect.left(),
            option.rect.bottom(),
            option.rect.right(),
            option.rect.bottom()
        )

        painter.restore()



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

        vertical_list = QtWidgets.QListWidget()
        vertical_list_layout = QtWidgets.QVBoxLayout()

        vertical_list.setLayout(vertical_list_layout)
        vertical_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        vertical_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        vertical_list.setItemDelegate(SpritesListItemDelegate())

        list_items = [
            QtWidgets.QListWidgetItem('Sprite 1'),
            QtWidgets.QListWidgetItem('Sprite 2'),
            QtWidgets.QListWidgetItem('Sprite 3'),
            QtWidgets.QListWidgetItem('Sprite 4'),
            QtWidgets.QListWidgetItem('Sprite 5'),
            QtWidgets.QListWidgetItem('Sprite 6'),
            QtWidgets.QListWidgetItem('Sprite 7'),
            QtWidgets.QListWidgetItem('Sprite 8'),
            QtWidgets.QListWidgetItem('Sprite 9'),
            QtWidgets.QListWidgetItem('Sprite 10'),
        ]

        default_sprite_list_item_icon = QtGui.QIcon(f'{pathlib.Path(__file__).parent.resolve()}/../../local/default_sprite_icon.png')

        for i in range(len(list_items)):
            li = list_items[i]
            li.setIcon(default_sprite_list_item_icon)

            vertical_list.addItem(li)

        # NOTE: the 'QListWidget::item' styles aren't used since the custom list item delegate overrides them but they should be kept for reference and as fallback
        vertical_list.setStyleSheet(
            """
            QListWidget::item {
                border-bottom: 1px solid #37393c;
                background-color: #2c2e30;
                padding: 20px 10px;
            }

            QListWidget::item:hover {
                background-color: #3b4045;
            }

            QScrollArea {
                border: none;
                background-color: #212124;
            }

            QScrollBar {
                background-color: #212124;
                border: 1px solid #37393c;
            }

            QScrollBar::handle:vertical {
                background-color: #656769;
                border: 1px solid gray;
                border-radius: 2px;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                width: 0px;
                height: 0px;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background-color: #37393c;
            }
            """
        )

        self.lyt.addWidget(vertical_list)