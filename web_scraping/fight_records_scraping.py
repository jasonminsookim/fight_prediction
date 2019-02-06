# Import libraries
import pandas as pd
import string
import time


# Create function to convert height into inches
def convert_to_inches(height):
    if (height != "NaN") & (height != "--") :
        result = float(height.split("'")[0]) * 12 + float(height.split("'")[1].split('"')[0])
        return result
    else:
        return None


# URLs to fightmetric.com
page_link_part1 = "http://www.fightmetric.com/statistics/fighters?char="
page_link_part2 = "&page=all"

# Create a list of dataframes to concat later
dfs_r = []

# Loop though each character in the alphabet to get fight records from every person
all_chars = string.ascii_lowercase
for char in all_chars:
    url = page_link_part1 + char + page_link_part2
    table = pd.read_html(url)[0]
    dfs_r.append(table)
    time.sleep(1)

# Concatenate the data frames into a single one
df_r = pd.concat(dfs_r, ignore_index=True)

# DATA WRANGLING

# Drops rows that have NaN values for all columns for people who haven't fought
df_r = df_r.dropna(axis=0, how="all")

# Trim Whitespaces
df_obj = df_r.select_dtypes(['object'])
df_r[df_obj.columns] = df_obj.apply(lambda x: x.str.strip())

# Convert height into float
df_r['Ht.'] = df_r['Ht.'].apply(convert_to_inches)

# Convert weight into float
df_r['Wt.'] = df_r['Wt.'].apply(lambda x: x.split(" ")[0])

# Convert reach into float
df_r['Reach'] = df_r['Reach'].apply(lambda x: x.split('"')[0])

# Rename columns
df_r.columns = ['first', 'last', 'nickname', 'height_inches', 'weight_lbs', 'reach_inches', 'stance', 'win', 'loss',
                'draw', 'belt']

# Save fight record data frame to csv
df_r.to_csv("../data/fight_record.csv")
