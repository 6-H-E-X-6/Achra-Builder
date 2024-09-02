# This will be the main interface through which
# the frontend will communicate with the backend.

import game_data
import json

class Actor:
    def __init__(self, culture, archetype, deity):
        self.active_skill_trees = []
        self.culture = game_data.culture_dict[culture]
        self.archetype = game_data.archetype_dict[archetype]
        self.deity = game_data.deity_dict[deity]
        self.strength = 0
        self.dexterity = 0
        self.willpower = 0
        self.vigor = 0
        self.speed = 0
        self.glory = 1
        self.skill_points = 9
        self.add_base_attributes(self.culture)
        self.add_base_attributes(self.archetype)
        self.add_base_attributes(self.deity)

    def add_base_attributes(self, character_creation_option):
        self.strength += character_creation_option.str_bonus
        self.dexterity += character_creation_option.dex_bonus
        self.willpower += character_creation_option.wil_bonus
        self.vigor += character_creation_option.vig_bonus
        self.speed += character_creation_option.speed_bonus

    def level_up(self, attribute):
        match attribute:
            case 'strength':
                self.strength += 1
                self.vigor += 25
            case 'dexterity':
                self.dexterity += 1
            case 'willpower':
                self.willpower += 1
            case 'vigor':
                self.vigor += 75

        self.skill_points += 1

my_actor = Actor('Stran', 'Amir', 'Ashem')
print(f'{my_actor.culture.name} {my_actor.archetype.name} of {my_actor.deity.name}')
print(f'base STR: {my_actor.strength}, base DEX: {my_actor.dexterity}, base WIL: {my_actor.willpower}',
      f'base vigor: {my_actor.vigor}, base speed: {my_actor.speed}')

# THIS IS DRIVER CODE TO TEST THE MODULE

# with open('tables/Table_Gods.json') as table:
#     deity_table = json.load(table)
#     deity_dict = {deity : game_data.Archetype_Or_Religion(deity_table[deity]) for deity in deity_table}
# with open('tables/Table_Classes.json') as table:
#     archetype_table = json.load(table)
#     archetype_dict = {archetype : game_data.Archetype_Or_Religion(archetype_table[archetype]) for archetype in archetype_table}
# with open('tables/Table_Races.json') as table:
#     cultures_table = json.load(table)
#     cultures_dict = {culture : game_data.Race(cultures_table[culture]) for culture in cultures_table}

# my_test_actor = Actor()
# my_test_actor.add_attributes(cultures_dict['Stran'])
# my_test_actor.add_attributes(archetype_dict['Amir'])
# my_test_actor.add_attributes(deity_dict['Ashem'])

# print(f'Strength = {my_test_actor.strength}')
# print(f'Dexterity = {my_test_actor.dexterity}')
# print(f'Willpower = {my_test_actor.willpower}')
# print(f'Vigor = {my_test_actor.vigor}')
# print(f'Speed = {my_test_actor.speed + (my_test_actor.dexterity * 2)}')
