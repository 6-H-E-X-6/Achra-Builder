import json
from json_cleaner import sanitize


class Race:
    def __init__ (self, id: dict):
        self.name = sanitize(id['name'])
        self.description = sanitize(id['brief'])
        self.str_bonus = id['str']
        self.dex_bonus = id['dex']
        self.wil_bonus = id['wil']
        self.vig_bonus = id['life']
        self.speed_bonus = id['speed']


class ArchetypeOrReligion:
    def __init__ (self, id: dict):
        self.name = sanitize(id['name'])
        self.description = id['description']
        self.str_bonus = id['str']
        self.dex_bonus = id['dex']
        self.wil_bonus = id['wil']
        self.vig_bonus = id['life']
        self.speed_bonus = id['speed']

class Skill:
    def __init__ (self, name, description, point_cost, element ):
        self.name = name
        self.description = description
        self.point_cost = point_cost
        self.element = element
        self.levels = 0


class SkillTree:
    def __init__(self, element, table: dict):
        self.skill_list = []
        self.total_points = 0
        self.element = element
        self.build_tree(element, table)

    def add_skill(self, skill: Skill):
        '''Takes a dictionary object from
        the imported JSON and fills out
        the Skill object with its data'''

        self.skill_list.append(Skill(sanitize(skill['Name']),
                                      sanitize(skill['Description']),
                                       skill['cost'],
                                        skill['Element']))

    def build_tree(self, element: str, table: json):
        '''Populates a tree given a JSON table'''

        # Filters skills by the element variable
        # provided in the constructor
        id_list = {i: table[i] for i in table if table[i]['Element'] == element}
        for id in id_list:
            self.add_skill(skill_list[id])

    def update_points(self):
        for skill in self.skill_list:
            self.total_points += (skill.point_cost * skill.levels)
