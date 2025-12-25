import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def study_hours_analysis(input_path, save_path):
    df = pd.read_csv(input_path)
    score_cols = ["MathScore", "ReadingScore", "WritingScore"]

    # Group by study hours
    means = df.groupby("WklyStudyHours")[score_cols].mean()

    # Correct order
    order = ["<5", "5-10", ">10"]
    means = means.reindex(order)

    os.makedirs(save_path, exist_ok=True)

    x = np.arange(len(order))
    width = 0.25

    fig, ax = plt.subplots(figsize=(8,5))

    colors = ["#1f77b4", "#d62728", "#2ca02c"]  # Math, Reading, Writing

    # Barları manuel çiz
    for i, subject in enumerate(score_cols):
        ax.bar(x + i*width, means[subject].values, width, label=subject, color=colors[i], edgecolor="black")

    ax.set_xticks(x + width)
    ax.set_xticklabels(order)
    ax.set_ylabel("Average Score")
    ax.set_xlabel("Weekly Study Hours")
    ax.set_title("Average Scores by Weekly Study Hours")
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    ax.set_axisbelow(True)
    ax.legend(title="Subjects")
    plt.tight_layout()

    # Save as PNG
    plt.savefig(os.path.join(save_path, "study_hours_analysis.png"))
    plt.close()

if __name__ == "__main__":
    study_hours_analysis(
        "data/processed/processed.csv",
        "outputs/study_hours_analysis"
    )
