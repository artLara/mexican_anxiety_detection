import shutil
import subprocess

import pandas as pd
from pathlib import Path
from tqdm import tqdm
import argparse


def run(csv_file: str|Path,
        input_dir: str|Path,
        output_dir: str|Path) -> None:
    """Move clips of videos and do a commit
    
    csv_file (str|Path): csv file path with clips names information
    input_dir: path of directoiry which contains clips
    output_dir: path of directoy dst
    """


    df = pd.read_csv(input_dir / csv_file)
    for i, row in tqdm(df.iterrows()):
        src_dir = input_dir / (str(row['video_id']) +
                               '_' +
                               str(row['ventana_id']))
        dst_dir = output_dir / (str(row['video_id']) +
                               '_' +
                               str(row['ventana_id'])) 
        shutil.move(src_dir, dst_dir)
        # print(f"Directory '{src_dir}' moved to '{dst_dir}' successfully.")
        command = 'git add .' 
        # subprocess.call(command, shell=True) #Keep shell True because produce errors
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        p.wait()

        command = f'git commit -m "data {row['video_id']} {row['ventana_id']}"'
        # subprocess.call(command, shell=True) #Keep shell True because produce errors
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        p.wait()

        
        command = 'git push'
        # p = subprocess.call(command, shell=True) #Keep shell True because produce errors
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        p.wait()
        # break


def main(args):
    csv_file = Path(args.csv_file)
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    run(csv_file, input_dir, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Move clips of videos and do a commit""")

    parser.add_argument("csv_file", type=str, help="csv file path with clips names information")
    parser.add_argument("input_dir", type=str, help="path of directoiry which contains clips")
    parser.add_argument("output_dir", type=str, help="path of directoy dst")
    args = parser.parse_args()
    main(args)
