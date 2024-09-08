# This will be the main interface through which
# the frontend will communicate with the backend.

import game_data
import json


MAX_SKILL_TREES = 3
MAX_SKILL_SLOTS = 9

class ActorModel:
    def __init__(self, culture, archetype, deity):
        self.active_skill_trees = []
        self.selected_skills = []
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
        self.set_base_attributes(self.culture)
        self.set_base_attributes(self.archetype)
        self.set_base_attributes(self.deity)


    # Either edit this function or make a new
    # set of functions for updating the stats
    # when either race, archetype, or class are changed
    def set_base_attributes(self, character_creation_option):
        self.strength += character_creation_option.str_bonus
        self.dexterity += character_creation_option.dex_bonus
        self.willpower += character_creation_option.wil_bonus
        self.vigor += character_creation_option.vig_bonus
        self.speed += character_creation_option.speed_bonus

    def update_base_attributes(self, new_option, current_option):
        self.strength += (new_option.str_bonus - current_option.str_bonus)
        self.dexterity += (new_option.dex_bonus - current_option.dex_bonus)
        self.willpower += (new_option.wil_bonus - current_option.wil_bonus)
        self.vigor += (new_option.vig_bonus - current_option.vig_bonus)
        self.speed += (new_option.speed_bonus - current_option.speed_bonus)

    def change_culture(self, new_culture):
        self.update_base_attributes(new_culture, self.culture)
        self.culture = new_culture

    def change_archetype(self, new_archetype):
        self.update_base_attributes(new_archetype, self.archetype)
        self.archetype = new_archetype

    def change_deity(self, new_deity):
        self.update_base_attributes(new_deity, self.deity)
        self.deity = new_deity

    def add_skill(self, skill):
        skill_element = skill.element
        total_active_skill_trees = len(self.active_skill_trees)
        total_selected_skills = len(self.selected_skills)

        if ((total_active_skill_trees == MAX_SKILL_TREES  and skill_element not in self.active_skill_trees)
            or (total_selected_skills == MAX_SKILL_SLOTS)):
            return

        if skill.point_cost > self.skill_points:
            return

        if skill_element not in self.active_skill_trees:
            self.active_skill_trees.append(skill_element)

        self.selected_skills.append(skill)
            
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
        self.glory += 1


# Default TEST case to make sure none
# of the underlying business logic
# has been broken.
def main():
    my_actor = ActorModel('Stran', 'Amir', 'Ashem')
    my_actor.change_culture(game_data.culture_dict['Lochra'])
    my_actor.add_skill(game_data.trait_dict['Bloodcalling'])
    print(f'{my_actor.culture.name} {my_actor.archetype.name} of {my_actor.deity.name}')
    print(f'base STR: {my_actor.strength}, base DEX: {my_actor.dexterity}, base WIL: {my_actor.willpower}',
          f'base vigor: {my_actor.vigor}, base speed: {my_actor.speed}')
    print(f'{my_actor.selected_skills[0].name}')
    my_actor.remove_skill(game_data.trait_dict['Bloodcalling'])
    print('Skill removed!')
    print(my_actor.selected_skills)
    my_actor.level_up('strength')
    print('\nLevelled up!')
    print(f'base STR: {my_actor.strength}, base DEX: {my_actor.dexterity}, base WIL: {my_actor.willpower}',
          f'base vigor: {my_actor.vigor}, base speed: {my_actor.speed}')

if __name__ == '__main__':
    main()
