from PySide6 import QtWidgets, QtGui



# LAYOUTS
class Layout(QtWidgets.QWidget):
    def __init__(self, layout: QtWidgets.QLayout):
        super(Layout, self).__init__()

        self.lyt = layout
        self.setLayout(layout)

    def addWidgets(self, widgets: list):
        for i in range(len(widgets)):
            self.lyt.addWidget(widgets[i])

    def paintEvent(self, _):
        # NOTE: this method is needed for stylesheets to work when inheriting QWidget (source: https://stackoverflow.com/questions/18344135/why-do-stylesheets-not-work-when-subclassing-qwidget-and-using-q-object)

        style_option = QtWidgets.QStyleOption()
        style_option.initFrom(self)

        painter = QtGui.QPainter(self)

        self.style().drawPrimitive(
            QtWidgets.QStyle.PrimitiveElement.PE_Widget,
            style_option,
            painter,
            self
        )

class HorizontalBoxLayout(Layout):
    def __init__(self):
        super(HorizontalBoxLayout, self).__init__(QtWidgets.QHBoxLayout())

class VerticalBoxLayout(Layout):
    def __init__(self):
        super(VerticalBoxLayout, self).__init__(QtWidgets.QVBoxLayout())



# SCROLLABLE WIDGETS
class ScrollableWidget(QtWidgets.QScrollArea):
    def __init__(self, layoutWidget: Layout):
        super(ScrollableWidget, self).__init__()

        self.lytw = layoutWidget
        self.setWidget(layoutWidget)

    def addWidgets(self, widgets: list):
        for i in range(len(widgets)):
            self.lytw.lyt.addWidget(widgets[i])

class HorizontallyScrollableWidget(ScrollableWidget):
    def __init__(self):
        super(HorizontallyScrollableWidget, self).__init__(HorizontalBoxLayout())

class VerticallyScrollableWidget(ScrollableWidget):
    def __init__(self):
        super(VerticallyScrollableWidget, self).__init__(VerticalBoxLayout())