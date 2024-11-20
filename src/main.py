import sys
from PySide6 import QtWidgets



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())