
import pandas as pd
import glob
import os

# path = r"c:/retrosheet/downloads/parsed/event"
# all_files = glob.glob(path + "/*.csv")

# li = []

# for filename in all_files:
#     df = pd.read_csv(filename, index_col=None, header=0)
#     li.append(df)

# frame = pd.concat(li, axis=0, ignore_index=True)


path = r"c:/retrosheet/downloads/parsed/event"          # use your path
all_files = glob.glob(os.path.join(path, "*.csv"))      # advisable to use os.path.join as this makes concatenation OS independent

df_from_each_file = (pd.read_csv(f) for f in all_files)
concatenated_df   = pd.concat(df_from_each_file, ignore_index=True)
# doesn't create a list, nor does it append to one

concatenated_df.to_csv("c:/retrosheet/downloads/parsed/event_all.csv", encoding='utf-8', index=False)