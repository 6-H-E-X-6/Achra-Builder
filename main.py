from game_data import Skill, culture_dict, archetype_dict, deity_dict, trait_dict
from actor import main_actor
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QToolButton, QStackedLayout, QLabel, QComboBox
from PyQt5.QtGui import QPalette, QColor, QPixmap


class SkillButton(QPushButton):
    def __init__(self, skill):
        super().__init__()
        self.skill = skill
        self.name = skill.name
        self.level = skill.level
        self.setText(f'{skill.name}: {skill.level}')
        self.clicked.connect(lambda state, skill=skill : main_actor.add_or_upgrade_skill(skill))
        self.clicked.connect(self.update_text)

    def update_text(self):
        self.setText(f'{self.skill.name}: {self.skill.level}')


class ActorControlWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.culture_dropdown = QComboBox()
        self.culture_dropdown.addItems([culture_dict[culture].name for culture in culture_dict])
        self.archetype_dropdown = QComboBox()
        self.archetype_dropdown.addItems([archetype_dict[archetype].name for archetype in archetype_dict])
        self.deity_dropdown = QComboBox()
        self.deity_dropdown.addItems([deity_dict[deity].name for deity in deity_dict])

        self.combo_hlay = QHBoxLayout()
        self.combo_hlay.addWidget(self.culture_dropdown)
        self.combo_hlay.addWidget(self.archetype_dropdown)
        self.combo_hlay.addWidget(self.deity_dropdown)
        self.setLayout(self.combo_hlay)

            
    # TODO Add control logic.
    # This is, as it stands,
    # a purely visual element.


class StatViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.stats_label_hlay = QHBoxLayout()
        self.stats_display_hlay = QHBoxLayout()
        self.stats_control_hlay = QHBoxLayout()
        self.stats_widget_full = QVBoxLayout()
        self.stats_widget_full.addLayout(self.stats_label_hlay)
        self.stats_widget_full.addLayout(self.stats_display_hlay)
        self.stats_widget_full.addLayout(self.stats_control_hlay)
        self.setLayout(self.stats_widget_full)


        self.strength_display = QLabel(str(main_actor.strength))
        self.dexterity_display = QLabel(str(main_actor.dexterity))
        self.willpower_display = QLabel(str(main_actor.willpower))
        self.vigor_display = QLabel(str(main_actor.vigor))
        self.skill_points_display = QLabel(str(main_actor.skill_points))
        self.stats_display_hlay_array = [self.strength_display, self.dexterity_display,
                                         self.willpower_display, self.vigor_display,
                                         self.skill_points_display]
        for display_component in self.stats_display_hlay_array:
            self.stats_display_hlay.addWidget(display_component)

        self.stat_names = ['Strength', 'Dexterity', 'Willpower', 'Vigor', 'Skill Points']
        for stat in self.stat_names:
            new_label = QLabel(str(stat))
            self.stats_label_hlay.addWidget(new_label)

        

        


class TablesWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.martialTree = [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Body']
        self.fireTree = [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Fire']
        self.lightningTree = [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Lightning']
        self.poisonTree = [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Poison']
        self.deathTree = [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Death']
        self.iceTree = [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Ice']
        self.astralTree = [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Astral']
        self.psychicTree= [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Psychic']
        self.lifeTree = [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Life']
        self.bloodTree = [SkillButton(trait_dict[skill]) for skill in trait_dict if trait_dict[skill].element == 'Blood']
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


window_stylesheet = """
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
        self.actor_widget = ActorControlWidget()
        self.stats_widget = StatViewerWidget()
       
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.actor_widget)
        _layout.addWidget(self.stats_widget)
        _layout.addWidget(self.table_widget)
        self.setCentralWidget(_widget)
        self.setWindowTitle("Achra Builder")
        
app = QApplication([])
# app.setStyleSheet(window_stylesheet)
mainView = MainView()
mainView.show()
app.exec()
