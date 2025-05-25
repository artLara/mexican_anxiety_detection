import pandas as pd
from sklearn.model_selection import train_test_split
from pathlib import Path
from tqdm import tqdm
import argparse


def run(csv_file: str|Path,
        output_dir: str|Path) -> None:
    """Move clips of videos and do a commit
    
    csv_file (str|Path): csv file path with clips names information
    input_dir: path of directoiry which contains clips
    output_dir: path of directoy dst
    """


    df = pd.read_csv(csv_file)
    data = []
    for i, row in df.iterrows():
        filename = (str(row['video_id']) +
                   '_' +
                   str(row['ventana_id']))
        
        level = row['nivel']
        data.append((filename, level))
        
    df = pd.DataFrame(data, columns=['filename', 'level'])

    # Split the DataFrame into training and testing sets
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df.to_csv(output_dir/'train.csv', index=False) 
    test_df.to_csv(output_dir/'test.csv', index=False) 

    # Print the shapes of the resulting DataFrames
    print("Train DataFrame shape:", train_df.shape)
    print("Test DataFrame shape:", test_df.shape)

        

def main(args):
    csv_file = Path(args.csv_file)
    output_dir = Path(args.output_dir)
    run(csv_file, output_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Move clips of videos and do a commit""")

    parser.add_argument("csv_file", type=str, help="csv file path with clips names information")
    parser.add_argument("output_dir", type=str, help="path of directoy dst")

    args = parser.parse_args()
    main(args)