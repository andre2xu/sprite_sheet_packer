from PySide6 import QtWidgets



class Layout(QtWidgets.QWidget):
    def __init__(self, layout: QtWidgets.QLayout):
        super(Layout, self).__init__()

        self.lyt = layout
        self.setLayout(layout)

    def addWidgets(self, widgets: list):
        for i in range(len(widgets)):
            self.lyt.addWidget(widgets[i])

class HorizontalBoxLayout(Layout):
    def __init__(self):
        super(HorizontalBoxLayout, self).__init__(QtWidgets.QHBoxLayout())

class VerticalBoxLayout(Layout):
    def __init__(self):
        super(VerticalBoxLayout, self).__init__(QtWidgets.QVBoxLayout())