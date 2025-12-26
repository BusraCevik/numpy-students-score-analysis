import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


def score_relationships(input_path, save_path):
    df = pd.read_csv(input_path)

    score_cols = ["MathScore", "ReadingScore", "WritingScore"]

    # Sadece bu analiz için gerekli kolonları al
    df = df[
        ["ParentMaritalStatus"] + score_cols
    ].dropna()

    # Normalize category names
    df["ParentMaritalStatus"] = (
        df["ParentMaritalStatus"]
        .astype(str)
        .str.strip()
        .str.capitalize()
    )

    # Group by Parent Marital Status
    means = df.groupby("ParentMaritalStatus")[score_cols].mean()

    os.makedirs(save_path, exist_ok=True)

    # Prepare bar positions
    x = np.arange(len(means.index))
    width = 0.25

    fig, ax = plt.subplots(figsize=(10, 6))

    colors = ["#FADADD", "#F4A7B9", "#E38AAE"]

    for i, subject in enumerate(score_cols):
        ax.bar(
            x + i * width,
            means[subject].values,
            width,
            label=subject,
            color=colors[i],
            edgecolor="black"
        )
    ax.set_xticks(x + width)
    ax.set_xticklabels(means.index)
    ax.set_ylabel("Average Score")
    ax.set_xlabel("Parent Marital Status")
    ax.set_title("Average Scores by Parent Marital Status")

    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    ax.legend(title="Subjects")

    plt.tight_layout()
    plt.savefig(os.path.join(save_path, "parent_marital_status_scores.png"))
    plt.close()


if __name__ == "__main__":
    score_relationships(
        "data/processed/processed.csv",
        "outputs/parent_marital_status"
    )
