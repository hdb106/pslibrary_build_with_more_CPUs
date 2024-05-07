from periodictable import *
from pathlib import Path
import pandas as pd


def symbols():
    for e in elements:
        if e.symbol != "n":
            yield e.symbol


def get_pp_name(filename):
    res = filename.split(".", 1)
    return res[0]


all_symbols = list(symbols())
columns = []
data = {}
for dirpath in Path.cwd().iterdir():
    if dirpath.is_dir() and "." not in dirpath.name and "__" not in dirpath.name:
        for subpath in dirpath.iterdir():
            if subpath.is_dir():
                key = f"{dirpath.name} & {subpath.name}"
                exist_symbol = []
                exist_info = {}
                for file in subpath.iterdir():
                    exist_symbol.append(get_pp_name(file.name))

                for s in all_symbols:
                    if s in exist_symbol:
                        exist_info.update({s: "有"})
                    else:
                        exist_info.update({s: "无"})
                        
                data.update({key: exist_info})

df = pd.DataFrame(data, index=all_symbols)
df.to_csv("pseudo.csv")
