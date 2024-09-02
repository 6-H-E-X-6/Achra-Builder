from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QToolButton, QStackedLayout, QLabel
from PyQt5.QtGui import QPalette, QColor, QPixmap


class TablesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.martialTree = [0 for _ in range(9)]
        self.fireTree = [0 for _ in range(9)]
        self.lightningTree = [0 for _ in range(9)]
        self.poisonTree = [0 for _ in range(9)]
        self.deathTree = [0 for _ in range(9)]
        self.iceTree = [0 for _ in range(9)]
        self.astralTree = [0 for _ in range(9)]
        self.psychicTree= [0 for _ in range(9)]
        self.lifeTree = [0 for _ in range(9)]
        self.bloodTree = [0 for _ in range(9)]
        tree_array = [self.martialTree, self.fireTree, self.lightningTree,
                      self.poisonTree, self.deathTree, self.iceTree,
                      self.astralTree, self.psychicTree, self.lifeTree,
                      self.bloodTree]

        lay = QHBoxLayout()
        vlay_array = [QVBoxLayout() for i in range(1, 10)]
        for tree, vlay in zip(tree_array, vlay_array):
            self.build_column(tree, vlay)
        for vlay in vlay_array:
            lay.addLayout(vlay)
        self.setLayout(lay)

    def build_column(self, tree, vlay):
        for i in tree:
            button = QToolButton()
            button.setCheckable(True)
            vlay.addWidget(button)


stylesheet = """
    QMainWindow {
        border-image: url(graphical/Approach48.png);
        background-repeat: no-repeat;
        background-position: center;
    }
"""

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = TablesWidget()
        _widget = QWidget()
        _layout = QStackedLayout(_widget)
        _layout.addWidget(self.table_widget)
        self.setCentralWidget(_widget)
        self.setWindowTitle("Achra Builder")
        
app = QApplication([])
app.setStyleSheet(stylesheet)
mainView = MainView()
mainView.show()
app.exec()
