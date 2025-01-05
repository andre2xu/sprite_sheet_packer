import pathlib, os
from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtWidgets import QSizePolicy

### GUI COMPONENTS ###
import components.shared
from .dialogs import SpriteInputChoiceDialog



### CUSTOM STYLING ###
class SpritesListItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self):
        super(SpritesListItemDelegate, self).__init__()

    def editorEvent(self, event, model, option, index):
        if event.type() == event.Type.MouseMove:
            option.widget.viewport().setCursor(QtCore.Qt.CursorShape.OpenHandCursor)

        return super().editorEvent(event, model, option, index)

    def paint(self, painter, option, index):
        painter.save()

        if option.state & QtWidgets.QStyle.StateFlag.State_Selected:
            # highlight background when a list item is clicked
            painter.fillRect(option.rect, QtGui.QColor('#3b4045'))
        else:
            # default background
            painter.fillRect(option.rect, QtGui.QColor('#313335'))

        icon = index.data(QtCore.Qt.DecorationRole)
        text = index.data(QtCore.Qt.DisplayRole)

        if icon:
            # draw icon
            icon_size = option.decorationSize

            icon_rect = QtCore.QRect(
                option.rect.x() + 20, # left side of list item widget + offset
                option.rect.y() + ((option.rect.height() - icon_size.height()) // 2), # center vertically in the list item widget
                icon_size.width(),
                icon_size.height()
            )

            painter.drawPixmap(icon_rect, icon.pixmap(icon_size))

            # create custom text position
            icon_right_margin = 15

            text_rect = QtCore.QRect(
                option.rect.x() + (icon_rect.x() + icon_size.width() + icon_right_margin), # start on the right of the icon (with space in-between)
                option.rect.y() - 2, # center vertically in the list item widget
                (option.rect.width() - (icon_size.width() + icon_right_margin)) * 0.79,
                option.rect.height()
            )
        else:
            text_rect = option.rect # use default position if there's no icon

        # shorten long text and add an ellipsis
        if text:
            font_metrics = QtGui.QFontMetrics(option.font)

            label_width = text_rect.width()
            text_length_in_pixels = font_metrics.boundingRect(text).width()

            if text_length_in_pixels > label_width:
                # create ellipsis
                while text_length_in_pixels > label_width:
                    text = text[:-1] # remove last character

                    text_length_in_pixels = font_metrics.boundingRect(text).width()

                text = f'{text[:-3]}...'

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

    def createEditor(self, parent, *_):
        # change styling of the line edit that's used for renaming
        editor = QtWidgets.QLineEdit(parent)

        editor.setStyleSheet(
            """
            background-color: #fff;
            color: #000;
            """
        )

        return editor

    def updateEditorGeometry(self, editor, option, index):
        list_widget = option.widget
        list_item = list_widget.itemFromIndex(index)

        list_item_rect = list_widget.visualItemRect(list_item)

        # move the line edit that's used for renaming and change its dimensions
        new_height = option.rect.height() - 40

        new_rect = QtCore.QRect(
            option.rect.x() + 50,
            option.rect.y() + ((list_item_rect.height() * 0.5) - (new_height * 0.5)),
            list_item_rect.width() * 0.8,
            new_height
        )

        editor.setGeometry(new_rect)

    def setModelData(self, editor, model, index):
        list_widget = model.parent()

        try:
            # rename the sprite file
            list_item_edited = list_widget.itemFromIndex(index)

            extension = os.path.splitext(list_item_edited.src)[1]
            new_filename = f'{editor.text()}{extension}'

            sprites_folder = os.path.dirname(list_item_edited.src)
            os.rename(list_item_edited.src, os.path.join(sprites_folder, new_filename))

            # change the list item text
            super().setModelData(editor, model, index)

            # reload list (to re-order sprites by name)
            sprites_list_class = list_widget.parent()
            sprites_list_class.reloadList()
        except:
            # show error and don't make any changes
            main_window = list_widget.parent().parent().parent().parent().parent()

            QtWidgets.QMessageBox.critical(
                main_window,
                'Renaming Failed',
                "That file name is invalid. Please make sure to use one that works on your machine.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )






### COMPONENTS ###
class Controls(components.shared.HorizontalBoxLayout):
    def __init__(self, parent=None):
        super(Controls, self).__init__(parent)

        self.main_window = parent.parent().parent()

        add_sprites_btn = QtWidgets.QPushButton('Add Sprites')
        add_sprites_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        add_sprites_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.sprite_input_choice_dialog = SpriteInputChoiceDialog(self.main_window, QtCore.Qt.WindowType.Dialog | QtCore.Qt.WindowType.FramelessWindowHint)
        add_sprites_btn.clicked.connect(self.openSpriteInputChoiceDialog)

        self.clear_all_sprites_btn = QtWidgets.QPushButton('Clear All')
        self.clear_all_sprites_btn.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum))
        self.clear_all_sprites_btn.setCursor(QtCore.Qt.CursorShape.PointingHandCursor)

        self.addWidgets([
            add_sprites_btn,
            self.clear_all_sprites_btn
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

    def openSpriteInputChoiceDialog(self):
        # check if a project folder is opened
        if self.main_window.project_folder_path != None:
            self.sprite_input_choice_dialog.open()
        else:
            QtWidgets.QMessageBox.critical(
                self.main_window,
                'Project Folder Not Found',
                "You need to open an existing project folder or create a new one before you can add sprites.",
                QtWidgets.QMessageBox.StandardButton.Ok
            )



class SpritesList(components.shared.VerticalBoxLayout):
    class List(QtWidgets.QListWidget):
        def __init__(self, parent=None):
            super().__init__(parent)

        def keyReleaseEvent(self, event):
            if event.key() == QtCore.Qt.Key.Key_Delete:
                selected_list_item = self.currentItem()

                self.parent().deleteSprite(selected_list_item)

            return super().keyReleaseEvent(event)

    class ListItem(QtWidgets.QListWidgetItem):
        src = None # path to sprite png

        def __init_subclass__(cls):
            return super().__init_subclass__()

    def __init__(self, parent=None):
        super(SpritesList, self).__init__(parent)

        self.vertical_list = self.List(self)
        self.vertical_list_layout = QtWidgets.QVBoxLayout()

        self.vertical_list.setLayout(self.vertical_list_layout)
        self.vertical_list.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.vertical_list.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.vertical_list.setItemDelegate(SpritesListItemDelegate()) # use custom styling on the list items
        self.vertical_list.setMovement(QtWidgets.QListWidget.Movement.Free) # allow list items to be moved
        self.vertical_list.setDragEnabled(True) # allow dragging
        self.vertical_list.setDragDropMode(QtWidgets.QListWidget.DragDropMode.InternalMove) # move list item instead of copying after it's dragged and dropped

        self.vertical_list.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.vertical_list.customContextMenuRequested.connect(self.displayContextMenu)

        default_sprite_list_item_icon = QtGui.QIcon(os.path.join(pathlib.Path(__file__).parent.resolve(), '../../local/icons/default_sprite_icon.png'))

        # NOTE: the 'QListWidget::item' styles aren't used since the custom list item delegate overrides them but they should be kept for reference and as fallback
        self.vertical_list.setStyleSheet(
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

        self.lyt.addWidget(self.vertical_list)

    def createListItem(self, source: str):
        new_list_item = self.ListItem(
            QtGui.QIcon(source),
            os.path.basename(source).replace('.png', '')
        )

        new_list_item.setFlags(new_list_item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

        new_list_item.src = source

        return new_list_item

    def loadSprites(self, sources: list[str]):
        # empty list
        self.vertical_list.clear()

        # create a list item for each image file and add it to the list
        if len(sources) > 0:
            for i in range(len(sources)):
                self.vertical_list.addItem(self.createListItem(sources[i]))

    def addSprites(self, sources: list[str]):
        # create a list item for each image file and add it to the list
        if len(sources) > 0:
            for i in range(len(sources)):
                self.vertical_list.addItem(self.createListItem(sources[i]))

            self.reloadList()
        else:
            raise Exception("No sprite sources were given")

    def displayContextMenu(self, clickPosition: QtCore.QPoint):
        list_item_clicked = self.vertical_list.itemAt(clickPosition)

        if list_item_clicked != None:
            context_menu = QtWidgets.QMenu(self.vertical_list)
            context_menu.setMinimumWidth(110)

            cm_rename = context_menu.addAction('Rename')
            cm_rename.triggered.connect(lambda: self.renameSprite(list_item_clicked))

            cm_delete = context_menu.addAction('Delete')
            cm_delete.triggered.connect(lambda: self.deleteSprite(list_item_clicked))

            context_menu.setStyleSheet(
                """
                QMenu {
                    background-color: #53585a;
                    padding: 5px;
                }

                QMenu::item {
                    color: #fff;
                    padding: 10px 15px;
                }

                QMenu::item:selected {
                    background-color: #484c4e;
                }
                """
            )

            # display context menu at mouse position
            context_menu.exec(self.vertical_list.viewport().mapToGlobal(clickPosition))

    def renameSprite(self, sprite: QtWidgets.QListWidgetItem):
        self.vertical_list.editItem(sprite)
        self.vertical_list.update(self.vertical_list.indexFromItem(sprite)) # force the list to update the editor's (i.e. the LineEdit for renaming) geometry

    def deleteSprite(self, sprite: QtWidgets.QListWidgetItem):
        # remove sprite from the list
        self.vertical_list.takeItem(self.vertical_list.row(sprite))

        # remove sprite from the sprites folder
        pathlib.Path(sprite.src).unlink(missing_ok=True)

    def deleteAllSprites(self):
        # remove sprites from the sprites folder
        num_of_list_items = self.vertical_list.count()

        for i in range(num_of_list_items):
            sprite = self.vertical_list.item(i)

            pathlib.Path(sprite.src).unlink(missing_ok=True)

        # remove sprites from the list
        self.vertical_list.clear()

    def reloadList(self):
        main_window = self.parent().parent().parent().parent()

        if main_window.sprites_folder_path != None:
            self.vertical_list.clear()

            sprite_file_names = os.listdir(main_window.sprites_folder_path)

            self.loadSprites([os.path.join(main_window.sprites_folder_path, sprite_file_names[i]) for i in range(len(sprite_file_names))])