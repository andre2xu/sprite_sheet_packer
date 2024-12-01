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

        central_widget.addWidgets([
            self.workspace
        ])
        self.setCentralWidget(central_widget)

        self.setMenuBar(Menubar(self))

        self.setMinimumSize(QtCore.QSize(800, 500))
        self.setWindowTitle('Sprite Sheet Packer')

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # rescale the sprite sheet preview's scrollable area body and re-position the image
        ssp_scrollable_area = self.workspace.sprite_sheet_preview.scrollable_area
        ssp_scrollable_area.rescaleScrollableAreaBody()
        ssp_scrollable_area.displayImage(f'{pathlib.Path(__file__).parent.resolve()}/../local/packed.png')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())