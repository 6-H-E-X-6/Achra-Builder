from game_data import Skill, culture_dict, archetype_dict, deity_dict, trait_dict
from actor import main_actor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QToolButton, QStackedLayout, QLabel
from PyQt5.QtGui import QPalette, QColor, QPixmap


class SkillButton(QPushButton):
    def __init__(self, skill):
        super().__init__()
        self.setText(trait_dict[skill].name)



class TablesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.martialTree = [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Body']
        self.fireTree = [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Fire']
        self.lightningTree = [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Lightning']
        self.poisonTree = [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Poison']
        self.deathTree = [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Death']
        self.iceTree = [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Ice']
        self.astralTree = [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Astral']
        self.psychicTree= [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Psychic']
        self.lifeTree = [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Life']
        self.bloodTree = [SkillButton(skill) for skill in trait_dict if trait_dict[skill].element == 'Blood']
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
        for button in tree:
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
