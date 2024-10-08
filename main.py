from game_data import Skill, culture_dict, archetype_dict, deity_dict, trait_dict
from actor import main_actor, MAX_SKILL_SLOTS
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton, QWidget, QToolButton,
                              QStackedLayout, QLabel, QComboBox, QToolBar,
                              QAction, QStatusBar)
from PyQt5.QtGui import QPalette, QColor, QPixmap
from PyQt5.QtCore import pyqtSignal


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


class StatButton(QPushButton):
    def __init__(self, attribute, is_level_up=True):
        super().__init__()
        attribute = attribute.lower()

        if is_level_up:
            self.setText(f'{'+' : ^10}')
            self.clicked.connect(lambda state, attribute=attribute : main_actor.level_up_or_down(attribute))
        else:
            self.setText(f'{'-' : ^10}')
            self.clicked.connect(lambda state, attribute=attribute : main_actor.level_up_or_down(attribute, level_up=False))


# TODO
# This really should list skill level instead of
# the SkillButton class
class SkillListButton(QPushButton):
    def __init__(self, display_text='None'):
        super().__init__()
        self.setText(display_text)
        self.clicked.connect(self.remove_skill)

    def remove_skill(self):
        if self.text() == 'None':
            return
        else:
            main_actor.remove_or_downgrade_skill(trait_dict[self.text()])
            if trait_dict[self.text()] not in main_actor.selected_skills:
                self.setText('None')


class ActorControlWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.culture_dropdown = QComboBox()
        self.culture_dropdown.addItems([culture_dict[culture].name for culture in culture_dict])
        self.culture_dropdown.currentTextChanged.connect(main_actor.change_culture)

        self.archetype_dropdown = QComboBox()
        self.archetype_dropdown.addItems([archetype_dict[archetype].name for archetype in archetype_dict])
        self.archetype_dropdown.currentTextChanged.connect(main_actor.change_archetype)

        self.deity_dropdown = QComboBox()
        self.deity_dropdown.addItems([deity_dict[deity].name for deity in deity_dict])
        self.deity_dropdown.currentTextChanged.connect(main_actor.change_deity)

        self.combo_hlay = QHBoxLayout()
        self.combo_hlay.addWidget(self.culture_dropdown)
        self.combo_hlay.addWidget(self.archetype_dropdown)
        self.combo_hlay.addWidget(self.deity_dropdown)
        self.setLayout(self.combo_hlay)


class StatViewerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.stat_names = ['Strength', 'Dexterity', 'Willpower', 'Vigor', 'Skill Points']
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

        for stat in self.stat_names:
            new_label = QLabel(str(stat))
            self.stats_label_hlay.addWidget(new_label)

        self.upgradable_stats = self.stat_names[:-1]
        for stat in self.upgradable_stats:
            self.level_down_button = StatButton(stat, is_level_up=False)
            self.level_down_button.clicked.connect(self.update_display)
            self.level_up_button = StatButton(stat)
            self.level_up_button.clicked.connect(self.update_display)
            self.stats_control_hlay.addWidget(self.level_down_button)
            self.stats_control_hlay.addWidget(self.level_up_button)

        self.glory_text_header = QLabel('Glory')
        self.glory_level_display = QLabel(f'{main_actor.glory}')
        self.stats_control_hlay.addWidget(QLabel('Glory'))
        self.stats_control_hlay.addWidget(self.glory_level_display)

    def update_display(self):
        self.strength_display.setText(str(main_actor.strength))
        self.dexterity_display.setText(str(main_actor.dexterity))
        self.willpower_display.setText(str(main_actor.willpower))
        self.vigor_display.setText(str(main_actor.vigor))
        self.skill_points_display.setText(str(main_actor.skill_points))
        self.glory_level_display.setText(str(main_actor.glory))

class SkillListWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__()
        self.list_hlay = QHBoxLayout()
        self.button_list = []
        for i in range(MAX_SKILL_SLOTS):
            new_button = SkillListButton()
            new_button.clicked.connect(self.update)
            self.list_hlay.addWidget(new_button)
            self.button_list.append(new_button)

        self.setLayout(self.list_hlay)

    # TODO
    # This needs to work both ways
    def update(self):
        amount_of_skills = len(main_actor.selected_skills)
        for i in range(amount_of_skills):
            skill_name = main_actor.selected_skills[i].name
            self.button_list[i].setText(skill_name)

        # There's probably a more elegant way
        # to handle this
        for button in self.button_list[amount_of_skills:]:
            button.setText('None')

       

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
        self.tree_array = [self.martialTree, self.fireTree, self.lightningTree,
                      self.poisonTree, self.deathTree, self.iceTree,
                      self.astralTree, self.psychicTree, self.lifeTree,
                      self.bloodTree]

        lay = QHBoxLayout()
        vlay_array = [QVBoxLayout() for i in range(1, 10)]
        for tree, vlay in zip(self.tree_array, vlay_array):
            self.build_column(tree, vlay)
        for vlay in vlay_array:
            lay.addLayout(vlay)
        self.setLayout(lay)

    def build_column(self, tree, vlay):
        for button in tree:
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
        self.skill_list_widget = SkillListWidget()
       
        _widget = QWidget()
        _layout = QVBoxLayout(_widget)
        _layout.addWidget(self.actor_widget)
        _layout.addWidget(self.stats_widget)
        _layout.addWidget(self.skill_list_widget)
        _layout.addWidget(self.table_widget)
        self.setCentralWidget(_widget)
        self.setWindowTitle("Achra Builder")

        self.actor_widget.culture_dropdown.currentTextChanged.connect(self.stats_widget.update_display)
        self.actor_widget.archetype_dropdown.currentTextChanged.connect(self.stats_widget.update_display)
        self.actor_widget.deity_dropdown.currentTextChanged.connect(self.stats_widget.update_display)

        for tree in self.table_widget.tree_array:
            for button in tree:
                button.clicked.connect(self.stats_widget.update_display)
                button.clicked.connect(self.skill_list_widget.update)

        for button in self.skill_list_widget.button_list:
            button.clicked.connect(self.stats_widget.update_display)

        # TODO refactor in a more modular way
        self.character_control_bar = QToolBar("Main Toolbar")
        self.addToolBar(self.character_control_bar)

        reset_character_button = QAction("Reset", self)
        reset_character_button.setStatusTip("Reset character stats and skill trees")
        reset_character_button.triggered.connect(main_actor.reset_actor)
        reset_character_button.triggered.connect(self.stats_widget.update_display)
        reset_character_button.triggered.connect(self.flush_skill_trees)
        self.character_control_bar.addAction(reset_character_button)
        self.setStatusBar(QStatusBar(self))

    def flush_skill_trees(self):
        for tree in self.table_widget.tree_array:
            for button in tree:
                button.update_text()
        
def main():
    app = QApplication([])
    # app.setStyleSheet(window_stylesheet)
    mainView = MainView()
    mainView.show()
    app.exec()

if __name__ == '__main__':
    main()
