import sys
from PySide6 import QtWidgets, QtCore

### GUI COMPONENTS ###
import components.shared as shared
from components.MainWindow import Menubar, Workspace



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        central_widget = shared.VerticalBoxLayout()
        central_widget.lyt.setSpacing(0)
        central_widget.lyt.setContentsMargins(0,0,0,0)

        central_widget.addWidgets([
            Menubar(),
            Workspace()
        ])

        self.setCentralWidget(central_widget)
        self.setMinimumSize(QtCore.QSize(800, 500))
        self.setWindowTitle('Sprite Sheet Packer')



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())