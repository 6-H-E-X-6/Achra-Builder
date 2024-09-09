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

# This class exists because the
# final descriptions for the 
# classes and religions are stored
# under description unlike
# races, which store their
# description in brief
class Archetype_Or_Religion:
    def __init__ (self, id: dict):
        self.name = sanitize(id['name'])
        self.description = id['description']
        self.str_bonus = id['str']
        self.dex_bonus = id['dex']
        self.wil_bonus = id['wil']
        self.vig_bonus = id['life']
        self.speed_bonus = id['speed']

class Skill:
    def __init__ (self, id: dict):
        self.name = sanitize(id['Name'])
        self.description = sanitize(id['Description'])
        self.point_cost = id['cost']
        self.element = id['Element']
        self.level = 1


# TO BE DELETED?
# class SkillTree:
#     def __init__(self, element, table: dict):
#         self.skill_list = []
#         self.total_points = 0
#         self.element = element
#         self.build_tree(element, table)

#     def add_skill(self, skill: Skill):
#         '''Takes a dictionary object from
#         the imported JSON and fills out
#         the Skill object with its data'''

#         self.skill_list.append(Skill(sanitize(skill['Name']),
#                                       sanitize(skill['Description']),
#                                        skill['cost'],
#                                         skill['Element']))

#     def build_tree(self, element: str, table: json):
#         '''Populates a tree given a JSON table'''

#         # Filters skills by the element variable
#         # provided in the constructor
#         id_list = {i: table[i] for i in table if table[i]['Element'] == element}
#         for id in id_list:
#             self.add_skill(id_list[id])

#     def update_points(self):
#         for skill in self.skill_list:
#             self.total_points += (skill.point_cost * skill.levels)

# TODO
# Couldn't find a better way to
# initialize business models from
# the JSON. Might revise later
with open('tables/Table_Gods.json') as table:
    deity_table = json.load(table)
    deity_dict = {deity : Archetype_Or_Religion(deity_table[deity]) for deity in deity_table}
with open('tables/Table_Classes.json') as table:
    archetype_table = json.load(table)
    archetype_dict = {archetype : Archetype_Or_Religion(archetype_table[archetype]) for archetype in archetype_table}
with open('tables/Table_Races.json') as table:
    culture_table = json.load(table)
    culture_dict = {culture : Race(culture_table[culture]) for culture in culture_table}
with open('tables/Table_Traits.json') as table:
    trait_table = json.load(table)
    cut_skills = ['Order of Ice', 'Obedient Ice', 'Icewalking', 'Warlord', 'Blademaster', 'War Chant',
                  'Heartseeker', 'Order of the Stars', 'Cosmic Shield', 'Fume', 'Order of Flame', 'Immolation', 'Fire Chant']
    trait_dict = {trait : Skill(trait_table[trait]) for trait in trait_table 
                    if sanitize(trait_table[trait]['Name']) not in cut_skills}

    # LEFTOVER CODE - MIGHT NEED LATER
    # martial_tree = SkillTree('Body', trait_table)
    # fire_tree = SkillTree('Fire', trait_table)
    # lightning_tree = SkillTree('Lightning', trait_table)
    # poison_tree = SkillTree('Poison', trait_table)
    # death_tree = SkillTree('Death', trait_table)
    # astral_tree = SkillTree('Astral', trait_table)
    # life_tree = SkillTree('Life', trait_table)
    # psychic_tree = SkillTree('Psychic', trait_table)
    # blood_tree = SkillTree('Blood', trait_table)

def main():
    for trait in trait_dict:
        print(trait_dict[trait].name)

if __name__ == '__main__':
    main()
