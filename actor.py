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


    def add_or_upgrade_skill(self, skill):
        total_active_skill_trees = len(self.active_skill_trees)
        total_selected_skills = len(self.selected_skills)

        if ((total_active_skill_trees == MAX_SKILL_TREES  and skill.element not in self.active_skill_trees)
            or (total_selected_skills == MAX_SKILL_SLOTS)):
            return

        if skill.point_cost > self.skill_points:
            return

        if skill.element not in self.active_skill_trees:
            self.active_skill_trees.append(skill.element)

        if skill in self.selected_skills:
            skill_location = self.selected_skills.index(skill)
            self.selected_skills[skill_location].level += 1
        else:
            self.selected_skills.append(skill)

        self.skill_points -= skill.point_cost

    def remove_or_downgrade_skill(self, skill):
        if skill not in self.selected_skills:
            return

        skill.level -= 1
        if skill.level == 0:
            self.selected_skills.remove(skill)
        self.skill_points += skill.point_cost
            

    def level_up_or_down(self, attribute, level_up = True):
        can_level_down = self.glory > 1 and self.skill_points > 0

        match attribute:
            case 'strength':
                if level_up:
                    self.strength += 1
                    self.vigor += 25
                else:
                    if not can_level_down:
                        return
                    self.strength -= 1
                    self.vigor += 25

            case 'dexterity':
                if level_up:
                    self.dexterity += 1
                else:
                    if not can_level_down:
                        return
                    self.dexterity -= 1

            case 'willpower':
                if level_up:
                    self.willpower += 1
                else:
                    if not can_level_down:
                        return
                    self.willpower -= 1

            case 'vigor':
                if level_up:
                    self.vigor += 75
                else:
                    if not can_level_down:
                        return
                    self.vigor -= 75

        if level_up:
            self.skill_points += 1
            self.glory += 1
        else:
            self.skill_points -= 1
            self.glory -= 1


main_actor = ActorModel('Stran', 'Amir', 'Ashem')

# Default TEST case to make sure none
# of the underlying business logic
# has been broken.
def main():
    my_actor = ActorModel('Stran', 'Amir', 'Ashem')
    my_actor.change_culture(game_data.culture_dict['Lochra'])
    my_actor.add_or_upgrade_skill(game_data.trait_dict['Bloodcalling'])
    print(f'{my_actor.culture.name} {my_actor.archetype.name} of {my_actor.deity.name}')
    print(f'base STR: {my_actor.strength}, base DEX: {my_actor.dexterity}, base WIL: {my_actor.willpower}',
          f'base vigor: {my_actor.vigor}, base speed: {my_actor.speed}')
    print(f'{my_actor.selected_skills[0].name} level {my_actor.selected_skills[0].level}')
    my_actor.remove_or_downgrade_skill(game_data.trait_dict['Bloodcalling'])
    print('Skill levelled down!')
    print(my_actor.selected_skills)
    my_actor.level_up_or_down('strength')
    print('\nLevelled up!')
    print(f'base STR: {my_actor.strength}, base DEX: {my_actor.dexterity}, base WIL: {my_actor.willpower}',
          f'base vigor: {my_actor.vigor}, base speed: {my_actor.speed}')

if __name__ == '__main__':
    main()
