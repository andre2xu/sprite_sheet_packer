from PySide6 import QtWidgets

### GUI COMPONENTS ###
import components.shared
from components.Workspace import SpriteSheetPreview, SpritesManager



class Menubar(QtWidgets.QMenuBar):
    def __init__(self, parent=None):
        super(Menubar, self).__init__(parent)

        # FILE MENU
        file_menu = self.addMenu('&File')
        file_menu.setMinimumWidth(250)

        file_menu_new_sheet = file_menu.addAction('&New sheet...')
        file_menu_new_sheet.setShortcut('Ctrl+N')
        file_menu_open_sheet = file_menu.addAction('&Open sheet...')
        file_menu_open_sheet.setShortcut('Ctrl+O')
        file_menu.addSeparator()
        file_menu_save = file_menu.addAction('&Save')
        file_menu_save.setShortcut('Ctrl+S')
        file_menu_save_as = file_menu.addAction('&Save to...')
        file_menu_save_as.setShortcut('Ctrl+Shift+S')
        file_menu.addSeparator()
        file_menu_settings = file_menu.addAction('&Settings')
        file_menu_settings.setShortcut('Ctrl+K')
        file_menu.addSeparator()
        file_menu_exit = file_menu.addAction('&Exit')
        file_menu_exit.triggered.connect(lambda _: self.parent().app.quit())

        self.addMenu(file_menu)

        # HELP MENU
        help_menu = self.addMenu('&Help')
        help_menu.setMinimumWidth(180)

        help_menu_tutorial = help_menu.addAction('&Tutorial')
        help_menu.addSeparator()
        help_menu_my_channel = help_menu.addAction('&My YouTube channel')
        help_menu_source_code = help_menu.addAction('&Project repository')

        self.setStyleSheet(
            """
            QMenuBar {
                background-color: #2f3133;
                padding: 8px 10px;
            }

            QMenuBar::item {
                border: none;
                padding: 3px 10px;
            }

            QMenuBar::item:selected {
                background-color: #404244;
                border-radius: 5px;
            }

            QMenu {
                background-color: #53585a;
                padding: 5px;
            }

            QMenu::separator {
                height: 1px;
                background-color: #3f4344;
                margin: 4px 0px;
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



class Workspace(components.shared.HorizontalBoxLayout):
    def __init__(self, parent=None):
        super(Workspace, self).__init__(parent)

        self.lyt.setSpacing(0)
        self.lyt.setContentsMargins(0,0,0,0)

        self.sprite_sheet_preview = SpriteSheetPreview(self)
        self.sprites_manager = SpritesManager(self)

        self.addWidgets([
            self.sprite_sheet_preview,
            self.sprites_manager
        ])