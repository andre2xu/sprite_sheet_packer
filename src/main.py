import sys
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

        central_widget.addWidgets([
            Workspace(self)
        ])
        self.setCentralWidget(central_widget)

        self.setMenuBar(Menubar(self))

        self.setMinimumSize(QtCore.QSize(800, 500))
        self.setWindowTitle('Sprite Sheet Packer')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())