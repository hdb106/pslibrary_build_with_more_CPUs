import json
import re
from pathlib import Path
import pandas as pd
from check_lost_element import all_symbols, get_pp_name

def get_cutoff(path):
    pattern_wfc = re.compile(
        r"\s+Suggested minimum cutoff for wavefunctions:\s*(\d+\.\d*)\s*Ry"
    )
    pattern_rho = re.compile(
        r"\s+Suggested minimum cutoff for charge density:\s*(\d+\.\d*)\s*Ry"
    )
    pattern_config = re.compile(
        r"config='([\w\s\d\.\[\]\-]+)'"
    )
    res = {}
    with open(str(path), "r") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            wfc = pattern_wfc.match(line)
            rho = pattern_rho.match(line)
            config = pattern_config.match(line)
            if wfc:
                res.update(dict(ecutwfc=float(wfc.group(1))))
            elif rho:
                res.update(dict(ecutrho=float(rho.group(1))))
            elif config:
                res.update(dict(config=config.group(1)))
    if not res.get("config"):
        raise SyntaxError(str(path))
    res.update(dict(ppname=path.name))
    return res


path = Path(__file__).parent
cutoff_dir = path / "cutoff"
if not cutoff_dir.exists():
    cutoff_dir.mkdir()

def is_skipdir(dir):
    for i in [".", "__", "cutoff"]:
        if i in dir:
            return True

for func in Path.cwd().iterdir():
    if func.is_dir() and not is_skipdir(func.name):
        for pp_type in func.iterdir():
            if pp_type.is_dir():
                info = dict()
                for file in pp_type.iterdir():
                    
                    if "NC" in pp_type.name:
                        pptype = pp_type.name.replace("NC", "Norm-Conversing")
                    elif "US" in pp_type.name:
                        pptype = pp_type.name.replace("US", "Ultrasoft")
                    else:
                        pptype = pp_type.name

                    json_name = cutoff_dir / \
                        f"{func.name.upper()}_{pptype}.json"
                    if file.is_file():
                        symbol = get_pp_name(file.name)
                        info[symbol] = get_cutoff(file)
                    else:
                        print(file, "不是文件")

                df = pd.DataFrame(info, columns=all_symbols)
                print_df = df.T
                print(print_df)
                with open(json_name, "w", encoding='utf-8') as f:
                    json.dump(info, f, indent=2)
                print(json_name)
