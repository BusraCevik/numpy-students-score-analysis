import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def gender_mean_scores(input_path, save_path):
    df = pd.read_csv(input_path)
    score_cols = ["MathScore", "ReadingScore", "WritingScore"]
    means = df.groupby("Gender")[score_cols].mean()


    # saving as png
    os.makedirs(save_path, exist_ok=True)

    colors = ["#FADADD", "#F4A7B9", "#E38AAE"]

    ax = means.plot(
        kind="bar",
        figsize=(10, 6),
        color=colors,
        edgecolor="black"
    )

    ax.set_title("Average Scores by Gender")
    ax.set_ylabel("Average Score")
    ax.set_xlabel("Gender")

    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)


    ax.legend(title="Subject")

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, "gender_mean_scores.png"))
    plt.close()


if __name__ == "__main__":
    gender_mean_scores("data/processed/processed.csv","outputs/gender_analysis")