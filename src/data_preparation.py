import pandas as pd
import numpy as np
import os


def prepare_data(input_path, output_path):
    df = pd.read_csv(input_path)


    print("Null values per column:")
    print(df.isnull().sum())


    df.dropna(inplace=True)
    print(f"Dataset after dropping nulls: {df.shape[0]} rows")


    os.makedirs(os.path.dirname(output_path), exist_ok=True)


    df.to_csv(output_path, index=False)
    print(f"Processed dataset saved at: {output_path}")

    return df


if __name__ == '__main__':
    prepare_data("data/raw/dataset.csv", "data/processed/processed.csv")
