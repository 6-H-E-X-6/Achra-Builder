import json
import os
from json_cleaner import sanitize

GAME_SPEED_BREAKPOINTS = [5, 11, 17, 24, 32, 40, 50, 62, 75, 91, 111, 134, 163, 200, 250, 320, 425, 600, 950, 2000]

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
        self.level = 0


# TODO
# Couldn't find a better way to
# initialize business models from
# the JSON. Might revise later
required_files = ['tables/Table_Gods.json', 'tables/Table_Classes.json', 'tables/Table_Races.json', 'tables/Table_Traits.json']
missing_files = 0
for file_path in required_files:
    if not os.path.exists(file_path):
        print(f'Missing file: {file_path}')
        missing_files += 1
if missing_files > 0:
    exit('Process aborted: missing JSON files')
with open('tables/Table_Gods.json') as table:
    deity_table = json.load(table)
    deity_dict = {sanitize(deity_table[deity]['name']): Archetype_Or_Religion(deity_table[deity]) for deity in deity_table}
with open('tables/Table_Classes.json') as table:
    archetype_table = json.load(table)
    archetype_dict = {sanitize(archetype_table[archetype]['name']) : Archetype_Or_Religion(archetype_table[archetype]) for archetype in archetype_table}
with open('tables/Table_Races.json') as table:
    culture_table = json.load(table)
    culture_dict = {sanitize(culture_table[culture]['name']) : Race(culture_table[culture]) for culture in culture_table}
with open('tables/Table_Traits.json') as table:
    trait_table = json.load(table)
    cut_skills = ['Order of Ice', 'Obedient Ice', 'Icewalking', 'Warlord', 'Blademaster', 'War Chant',
                  'Heartseeker', 'Order of the Stars', 'Cosmic Shield', 'Fume', 'Order of Flame', 'Immolation', 'Fire Chant']
    trait_dict = {sanitize(trait_table[trait]['Name']) : Skill(trait_table[trait]) for trait in trait_table 
                    if sanitize(trait_table[trait]['Name']) not in cut_skills}


def main():
    for trait in trait_dict:
        print(trait_dict[trait].name)

if __name__ == '__main__':
    main()
