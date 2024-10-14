# This will be the main interface through which
# the frontend will communicate with the backend.

import game_data
import json


MAX_SKILL_TREES = 3
MAX_SKILL_SLOTS = 9


# TODO prevent the user from going under
# the base stat totals
class ActorModel:
    def __init__(self, culture, archetype, deity):
        self.active_skill_trees = []
        self.selected_skills = []
        self.base_stats = {}
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
        self.set_base_attributes()


    def set_base_attributes(self):
        for character_creation_option in [self.culture, self.archetype, self.deity]:
            self.strength += character_creation_option.str_bonus
            self.dexterity += character_creation_option.dex_bonus
            self.willpower += character_creation_option.wil_bonus
            self.vigor += character_creation_option.vig_bonus
            self.speed += character_creation_option.speed_bonus
            self.base_stats = {'strength' : self.strength, 'dexterity' : self.dexterity,
                                'willpower' : self.willpower, 'vigor' : self.vigor,
                                'speed' : self.speed}

    def update_base_attributes(self, new_option, current_option):
        self.strength += (new_option.str_bonus - current_option.str_bonus)
        self.dexterity += (new_option.dex_bonus - current_option.dex_bonus)
        self.willpower += (new_option.wil_bonus - current_option.wil_bonus)
        self.vigor += (new_option.vig_bonus - current_option.vig_bonus)
        self.speed += (new_option.speed_bonus - current_option.speed_bonus)

        self.base_stats['strength'] += (new_option.str_bonus - current_option.str_bonus)
        self.base_stats['dexterity'] += (new_option.dex_bonus - current_option.dex_bonus)
        self.base_stats['willpower'] += (new_option.wil_bonus - current_option.wil_bonus)
        self.base_stats['vigor'] += (new_option.vig_bonus - current_option.vig_bonus)
        self.base_stats['speed'] += (new_option.speed_bonus - current_option.speed_bonus)


    def change_culture(self, new_culture : str):
        self.update_base_attributes(game_data.culture_dict[new_culture], self.culture)
        self.culture = game_data.culture_dict[new_culture]

    def change_archetype(self, new_archetype : str):
        self.update_base_attributes(game_data.archetype_dict[new_archetype], self.archetype)
        self.archetype = game_data.archetype_dict[new_archetype]

    def change_deity(self, new_deity : str):
        self.update_base_attributes(game_data.deity_dict[new_deity], self.deity)
        self.deity = game_data.deity_dict[new_deity]


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
            skill_location = self.selected_skills.index(skill)
            self.selected_skills[skill_location].level += 1

        self.skill_points -= skill.point_cost

    # TODO make this remove
    # active skill trees too
    def remove_or_downgrade_skill(self, skill):
        if skill not in self.selected_skills:
            return

        skill.level -= 1
        if skill.level <= 0:
            self.selected_skills.remove(skill)
            self.free_unused_tree(skill.element)
        self.skill_points += skill.point_cost

    # Work on this
    def free_unused_tree(self, element):
        active_elements = [skill.element for skill in self.selected_skills]
        if element not in active_elements:
            self.active_skill_trees.remove(element)

    def level_up_or_down(self, attribute, level_up = True):
        can_level_down = self.glory > 1 and self.skill_points > 0
        match attribute:
            case 'strength':
                if level_up:
                    self.strength += 1
                    self.vigor += 25
                    self.base_stats['vigor'] += 25
                else:
                    if not can_level_down or self.strength == self.base_stats['strength']:
                        return
                    self.strength -= 1
                    self.vigor -= 25
                    self.base_stats['vigor'] -= 25

            case 'dexterity':
                if level_up:
                    self.dexterity += 1
                else:
                    if not can_level_down or self.dexterity == self.base_stats['dexterity']:
                        return
                    self.dexterity -= 1

            case 'willpower':
                if level_up:
                    self.willpower += 1
                else:
                    if not can_level_down or self.willpower == self.base_stats['willpower']:
                        return
                    self.willpower -= 1

            case 'vigor':
                if level_up:
                    self.vigor += 75
                else:
                    if not can_level_down or self.vigor == self.base_stats['vigor']:
                        return
                    self.vigor -= 75
            case _:
                return

        if level_up:
            self.skill_points += 1
            self.glory += 1
        else:
            self.skill_points -= 1
            self.glory -= 1

    
    # HACK not happy with how this
    # came out. I should find a way to
    # convert this to an iterative
    # function
    # TODO fix this mess
    def reset_actor(self):
        self.strength = 0
        self.dexterity = 0
        self.willpower = 0
        self.vigor = 0
        self.speed = 0
        self.glory = 1
        self.skill_points = 9
        self.set_base_attributes()

        for skill in self.selected_skills:
            skill.level = 0
            self.selected_skills.remove(skill)
        for skill_tree in self.active_skill_trees:
            self.active_skill_trees.remove(skill_tree)

main_actor = ActorModel('Stran', 'Amir', 'Ashem')

# Default TEST case to make sure none
# of the underlying business logic
# has been broken.
def main():
    my_actor = ActorModel('Stran', 'Amir', 'Ashem')
    print(my_actor.base_stats)
    my_actor.change_culture('Lochra')
    print(my_actor.base_stats)
    my_actor.change_culture('Stran')
    print(my_actor.base_stats)
    my_actor.add_or_upgrade_skill(game_data.trait_dict['Technique'])

    print(f'{my_actor.culture.name} {my_actor.archetype.name} of {my_actor.deity.name}')
    print(f'base STR: {my_actor.strength}, base DEX: {my_actor.dexterity}, base WIL: {my_actor.willpower}',
          f'base vigor: {my_actor.vigor}, base speed: {my_actor.speed}')
    print(f'{my_actor.selected_skills[0].name} level {my_actor.selected_skills[0].level}')
    print('Skill levelled down!')


    my_actor.level_up_or_down('strength')
    print('\nLevelled up!')
    print(f'base STR: {my_actor.strength}, base DEX: {my_actor.dexterity}, base WIL: {my_actor.willpower}',
          f'base vigor: {my_actor.vigor}, base speed: {my_actor.speed}')

    my_actor.reset_actor()
    print('\nReset!')
    print(f'base STR: {my_actor.strength}, base DEX: {my_actor.dexterity}, base WIL: {my_actor.willpower}',
          f'base vigor: {my_actor.vigor}, base speed: {my_actor.speed}')
    print(f'\n{my_actor.culture.description}')

if __name__ == '__main__':
    main()
