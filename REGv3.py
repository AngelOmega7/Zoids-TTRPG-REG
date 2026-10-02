import random
import pandas as pd
import os

#pull Database

#Ask user for Level Input
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(SCRIPT_DIR, "ZoidsDB.csv")
df = pd.read_csv(CSV_PATH)


#generator engine
def generate_encounter(encounter_level):
#filter database by input
    encounter_level_mod = encounter_level + 2
    filtered_df = df[df["Level Required 5"] <= int(encounter_level_mod)]
#select random zoid and then limit returned info to Zoid's name

    spawn_count = random.randint(3, 6)
    mob = []
    difficulty = 0
    for _ in range(spawn_count):
        random_row = filtered_df.sample(n=1)
        chosen_item = random_row['Name 1'].iloc[0]
        chosen_level = random_row['Level Required 5'].iloc[0]
        chosen_HP = int(random_row['Health 6'].iloc[0])
        chosen_armor = int(random_row['Armor 7'].iloc[0])
        chosen_defense = int(random_row['Defense 8'].iloc[0])

        if difficulty + chosen_level < encounter_level * 3:
            difficulty = difficulty + chosen_level
            mob.append({
                "Name": chosen_item, "LV": chosen_level,
                "HP": chosen_HP, "AR": chosen_armor, "DF": chosen_defense
            })
    return mob
