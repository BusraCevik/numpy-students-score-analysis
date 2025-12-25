import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def first_child_analysis(input_path, save_path):
    df = pd.read_csv(input_path)
    score_cols = ["MathScore", "ReadingScore", "WritingScore"]

    # Normalize Gender & IsFirstChild
    df["Gender"] = df["Gender"].str.capitalize()
    df["IsFirstChild"] = df["IsFirstChild"].astype(str).str.strip().str.capitalize()

    means = df.groupby(["Gender", "IsFirstChild"])[score_cols].mean()

    os.makedirs(save_path, exist_ok=True)

    subjects = score_cols
    genders = df["Gender"].unique()
    first_child_status = df["IsFirstChild"].unique()

    x = np.arange(len(subjects))
    width = 0.15  # bar width thinner

    fig, ax = plt.subplots(figsize=(10,6))

    # Define colors
    gender_colors = {"Male": "#1f77b4", "Female": "#d62728"}
    fc_alpha = {"Yes": 1.0, "No": 0.4}  # First child darker, not first child lighter

    for i, gender in enumerate(genders):
        for j, fc in enumerate(first_child_status):
            if (gender, fc) in means.index:
                y = means.loc[(gender, fc)].values
                ax.bar(
                    x + (i*len(first_child_status) + j)*width,
                    y,
                    width,
                    label=f"{gender} - {fc}",
                    color=gender_colors.get(gender, "#888888"),
                    alpha=fc_alpha.get(fc, 1.0),
                    edgecolor="black"
                )

    ax.set_xticks(x + width*len(genders)*len(first_child_status)/2 - width/2)
    ax.set_xticklabels(subjects)
    ax.set_ylabel("Average Score")
    ax.set_title("Average Scores by Gender and First-Child Status")
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    ax.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(save_path, "first_child_gender_analysis.png"))
    plt.close()

if __name__ == "__main__":
    first_child_analysis(
        "data/processed/processed.csv",
        "outputs/first_child_analysis"
    )
