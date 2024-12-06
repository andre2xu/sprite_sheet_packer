import sys, pathlib
from PySide6 import QtWidgets, QtCore

### GUI COMPONENTS ###
import components.shared
from components.MainWindow import Menubar, Workspace



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        central_widget = components.shared.VerticalBoxLayout()
        central_widget.lyt.setSpacing(0)
        central_widget.lyt.setContentsMargins(0,0,0,0)

        self.workspace = Workspace(self)
        self.workspace.sprite_sheet_preview.scrollable_area.displayImage(f'{pathlib.Path(__file__).parent.resolve()}/../local/packed.png')

        central_widget.addWidgets([
            self.workspace
        ])
        self.setCentralWidget(central_widget)

        self.setMenuBar(Menubar(self))

        self.setMinimumSize(QtCore.QSize(800, 500))
        self.setWindowTitle('Sprite Sheet Packer')

    def resizeEvent(self, event):
        super().resizeEvent(event)

        main_window_width = self.width()
        main_window_height = self.height()

        # re-scale the sprite sheet preview's scrollable area body
        self.workspace.sprite_sheet_preview.scrollable_area.rescaleScrollableAreaBody()

        # re-scale the sprite input choice dialog
        sprite_input_choice_dialog = self.workspace.sprites_manager.controls.sprite_input_choice_dialog

        if main_window_width > 1300 and main_window_height > 750:
            sprite_input_choice_dialog.setFixedSize(sprite_input_choice_dialog.original_width * 1.3, sprite_input_choice_dialog.original_height * 1.3)
        else:
            sprite_input_choice_dialog.setFixedSize(sprite_input_choice_dialog.original_width, sprite_input_choice_dialog.original_height)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())