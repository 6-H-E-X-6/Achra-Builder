from game_data import Skill, culture_dict, archetype_dict, deity_dict, trait_dict
from actor import main_actor, MAX_SKILL_SLOTS
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QHBoxLayout,
                             QVBoxLayout, QPushButton, QWidget, QToolButton,
                              QStackedLayout, QLabel, QComboBox, QToolBar,
                              QAction, QStatusBar, QMenu, QMenuBar, QFileDialog, QSizePolicy)


EMPTY_STRING = ''
EMPTY_SKILL_BUTTON_TEXT = 'None' # Just so no one confuses this for the None type

# TODO:
# -Add a stat/skill info display
# (this is in the Table_TraitsGeneric JSON)
class SkillButton(QPushButton):
    def __init__(self, skill):
        super().__init__()
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setText(f'{skill.name}\n\n{'Cost: ': ^4}{skill.point_cost}')
        self.clicked.connect(lambda state, skill=skill : main_actor.add_or_upgrade_skill(skill))


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


class StatWidget(QWidget):
    def __init__(self, stat,  parent=None):
        super().__init__()
        self.filler = QLabel()
        self.vlay = QVBoxLayout()
        self.text_hlay = QHBoxLayout()
        self.stat_hlay = QHBoxLayout()
        self.button_hlay = QHBoxLayout()
        self.upgrade_button = StatButton(stat)
        self.downgrade_button = StatButton(stat, is_level_up=False)
        self.button_reference_array = [self.upgrade_button, self.downgrade_button]
        self.stat_label = QLabel(f'{stat : ^20}')
        self.stat_display = QLabel(f'{str(0) : ^20}')

        self.text_hlay.addWidget(self.filler)
        self.text_hlay.addWidget(self.stat_label)
        self.text_hlay.addWidget(self.filler)

        self.stat_hlay.addWidget(self.filler)
        self.stat_hlay.addWidget(self.stat_display)
        self.stat_hlay.addWidget(self.filler)

        self.button_hlay.addWidget(self.downgrade_button)
        self.button_hlay.addWidget(self.filler)
        self.button_hlay.addWidget(self.upgrade_button)

        self.vlay.addLayout(self.text_hlay)
        self.vlay.addLayout(self.stat_hlay)
        self.vlay.addLayout(self.button_hlay)

        self.setLayout(self.vlay)


class SkillListButton(QPushButton):
    def __init__(self, display_text=EMPTY_SKILL_BUTTON_TEXT):
        super().__init__()
        self.skill_name = EMPTY_STRING
        self.setText(display_text)
        self.clicked.connect(self.remove_skill)


    def remove_skill(self):
        if self.skill_name == EMPTY_STRING:
            return
        else:
            main_actor.remove_or_downgrade_skill(trait_dict[self.skill_name])
            if trait_dict[self.skill_name] not in main_actor.selected_skills:
                self.store_skill_name(EMPTY_STRING)

    # This exists ONLY to aid in
    # the readability of API calls
    def store_skill_name(self, skill_name):
        self.skill_name = skill_name

    def reset(self):
        self.setText(EMPTY_SKILL_BUTTON_TEXT)
        self.store_skill_name(EMPTY_STRING)


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
        self.stat_hlay = QHBoxLayout()
        self.skill_and_glory_vlay = QVBoxLayout()
        self.speed_vlay = QVBoxLayout()

        self.strength_display = self.create_stat_controller('Strength')
        self.dex_display = self.create_stat_controller('Dexterity')
        self.wil_display = self.create_stat_controller('Willpower')
        self.vig_display = self.create_stat_controller('Vigor')

        self.stat_hlay.addWidget(self.strength_display)
        self.stat_hlay.addWidget(self.dex_display)
        self.stat_hlay.addWidget(self.wil_display)
        self.stat_hlay.addWidget(self.vig_display)

        self.glory_level_display = QLabel()
        self.skill_points_display = QLabel()

        self.skill_and_glory_vlay.addWidget(self.glory_level_display)
        self.skill_and_glory_vlay.addWidget(self.skill_points_display)
        self.stat_hlay.addLayout(self.skill_and_glory_vlay)

        self.speed_display = QLabel()
        self.game_turn_display = QLabel()
        self.speed_vlay.addWidget(self.speed_display)
        self.speed_vlay.addWidget(self.game_turn_display)
        self.stat_hlay.addLayout(self.speed_vlay)

        self.setLayout(self.stat_hlay)
        self.update_display()

    def update_display(self):
        self.strength_display.stat_display.setText(f'{main_actor.strength : ^ 20}')
        self.dex_display.stat_display.setText(f'{main_actor.dexterity : ^ 20}')
        self.wil_display.stat_display.setText(f'{main_actor.willpower : ^ 20}')
        self.vig_display.stat_display.setText(f'{main_actor.vigor : ^ 20}')
        self.glory_level_display.setText(f'Glory: {main_actor.glory}')
        self.skill_points_display.setText(f'Skill Points: {main_actor.skill_points}')
        self.speed_display.setText(f'Speed: {main_actor.speed}')
        self.game_turn_display.setText(f'Turns per game turn: {main_actor.turns_before_game_turn}')

    def create_stat_controller(self, attribute):
        stat_controller = StatWidget(attribute)
        for button in stat_controller.button_reference_array:
            button.clicked.connect(self.update_display)
        return stat_controller


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

    def update(self):
        amount_of_skills = len(main_actor.selected_skills)
        for i in range(amount_of_skills):
            indexed_skill_name = main_actor.selected_skills[i].name
            indexed_skill_level = main_actor.selected_skills[i].level
            self.button_list[i].setText(f'{indexed_skill_name}: {indexed_skill_level}')
            self.button_list[i].store_skill_name(indexed_skill_name)

        # There's probably a more elegant way
        # to handle this
        empty_button_slots = self.button_list[amount_of_skills:]
        for button in empty_button_slots:
            button.reset()


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
        vlay_array = [QVBoxLayout() for i in range(10)]
        for tree, vlay in zip(self.tree_array, vlay_array):
            self.build_column(tree, vlay)
        for vlay in vlay_array:
            lay.addLayout(vlay)
        self.setLayout(lay)

    def build_column(self, tree, vlay):
        for button in tree:
            vlay.addWidget(button)



class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = TablesWidget()
        self.actor_widget = ActorControlWidget()
        self.stats_widget = StatViewerWidget()
        self.skill_list_widget = SkillListWidget()
        self.create_menu_bar()
       
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

        self.initialize_buttons()

    def initialize_buttons(self):
        for tree in self.table_widget.tree_array:
            for button in tree:
                button.clicked.connect(self.stats_widget.update_display)
                button.clicked.connect(self.skill_list_widget.update)

        for button in self.skill_list_widget.button_list:
            button.clicked.connect(self.stats_widget.update_display)

    def write_to_json(self):
        file_name_tuple = QFileDialog.getSaveFileName(self, 'Save file')
        if file_name_tuple[0] == '':
            return # Needed to prevent junk flowing into stdout
        file_name = file_name_tuple[0]
        with open(file_name, 'w') as file:
            file.write(main_actor.export_data())

    def write_to_plaintext(self):
        file_name_tuple = QFileDialog.getSaveFileName(self, 'Save file')
        if file_name_tuple[0] == '':
            return
        file_name = file_name_tuple[0]
        with open(file_name, 'w') as file:
            file.write(main_actor.export_data(export_as_json=False))

    def create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        export_json_action = QAction('Export data as JSON', self)
        export_json_action.setStatusTip('Export this character to a JSON file.')
        export_json_action.triggered.connect(self.write_to_json)

        export_plaintext_action = QAction('Export data as text', self)
        export_plaintext_action.setStatusTip('Export character data to a text document')
        export_plaintext_action.triggered.connect(self.write_to_plaintext)

        reset_character_action = QAction("Reset", self)
        reset_character_action.setStatusTip("Reset character stats and skill trees")
        reset_character_action.triggered.connect(main_actor.reset_actor)
        reset_character_action.triggered.connect(self.skill_list_widget.update)
        reset_character_action.triggered.connect(self.stats_widget.update_display)

        file_menu = QMenu('&File', self)
        file_menu.addActions([export_json_action, export_plaintext_action])
        edit_menu = QMenu('&Edit', self)
        edit_menu.addAction(reset_character_action)

        menu_bar.addMenu(file_menu)
        menu_bar.addMenu(edit_menu)


def main():
    with open('style.css') as stylesheet:
        window_stylesheet = stylesheet.read()
    app = QApplication([])
    app.setStyleSheet(window_stylesheet)
    mainView = MainView()
    mainView.show()
    app.exec()

if __name__ == '__main__':
    main()
