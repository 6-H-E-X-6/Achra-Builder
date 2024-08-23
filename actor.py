# This will be the main interface through which
# the frontend will communicate with the backend.

import game_data
import json

class Actor:
    def __init__(self):
        self.skill_trees = []
        self.strength = 0
        self.dexterity = 0
        self.willpower = 0
        self.vigor = 0
        self.speed = 0
        self.glory = 1
        self.skill_points = 9

    def add_attributes(self, option):
        self.strength += option.str_bonus
        self.dexterity += option.dex_bonus
        self.willpower += option.wil_bonus
        self.vigor += option.vig_bonus
        self.speed += option.speed_bonus

# THIS IS DRIVER CODE TO TEST THE MODULE

# with open('tables/Table_Gods.json') as table:
#     deity_table = json.load(table)
#     deity_dict = {deity : game_data.ArchetypeOrReligion(deity_table[deity]) for deity in deity_table}
# with open('tables/Table_Classes.json') as table:
#     archetype_table = json.load(table)
#     archetype_dict = {archetype : game_data.ArchetypeOrReligion(archetype_table[archetype]) for archetype in archetype_table}
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
