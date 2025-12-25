import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# -----------------------------
# Compute basic statistics
# -----------------------------
def compute_statistics(scores_df):
    """
    Compute basic statistics for each score column in the DataFrame.
    Returns a dictionary with mean, median, std, and percentiles.
    """
    stats_dict = {}

    for column in scores_df.columns:
        scores = scores_df[column]

        mean_val = scores.mean()
        median_val = scores.median()
        std_val = scores.std()

        percentile_25 = scores.quantile(0.25)
        percentile_50 = scores.quantile(0.50)
        percentile_75 = scores.quantile(0.75)

        stats_dict[column] = {
            'mean': mean_val,
            'median': median_val,
            'std': std_val,
            '25%': percentile_25,
            '50%': percentile_50,
            '75%': percentile_75,
        }

    return stats_dict

# -----------------------------
# Plot histograms
# -----------------------------
def plot_distributions(scores_df, save_path):
    """
    Plot histograms for each score column with more bins and save them to save_path.
    """
    os.makedirs(save_path, exist_ok=True)

    for column in scores_df.columns:
        plt.figure(figsize=(10,6))
        plt.hist(scores_df[column], bins=20, color='pink', edgecolor='black')
        plt.title(f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(os.path.join(save_path, f"{column}_hist.png"))
        plt.close()

# -----------------------------
# Plot mean comparison using 25%-75% percentiles as error
# -----------------------------
def plot_mean_comparison(stats, save_path):

    os.makedirs(save_path, exist_ok=True)
    subjects = list(stats.keys())
    means = [stats[s]["mean"] for s in subjects]
    errors = np.array([stats[s]['75%'] - stats[s]['25%'] for s in subjects])  # IQR

    # Min-max normalize for colormap
    min_err = errors.min()
    max_err = errors.max()

    # Choose colormap
    cmap = cm.get_cmap("YlOrRd")

    plt.figure(figsize=(10,6))
    for i, subj in enumerate(subjects):
        norm_err = (errors[i] - min_err) / (max_err - min_err + 1e-6)
        ecolor = cmap(norm_err)

        plt.bar(subj, means[i], yerr=errors[i], color='pink', edgecolor='black',
                capsize=5, ecolor=ecolor, linewidth=2)

    plt.ylabel("Mean Score")
    plt.title("Comparison of Mean Scores Across Subjects (IQR as Error, Colored)")
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(save_path, "mean_comparison.png"))
    plt.close()

# -----------------------------
# Master function
# -----------------------------
def run_score_statistics(csv_path, save_path):
    """
    Load CSV, select score columns, compute statistics, plot histograms and mean comparison chart, print results.
    """
    # Load dataset
    df = pd.read_csv(csv_path)

    # Select score columns
    score_columns = ["MathScore", "ReadingScore", "WritingScore"]
    scores_df = df[score_columns]

    # Compute statistics
    stats = compute_statistics(scores_df)

    # Print results
    print("=== Score Statistics ===")
    for col, col_stats in stats.items():
        print(f"{col}: {col_stats}")

    # Plot distributions
    plot_distributions(scores_df, save_path)

    # Plot mean comparison chart
    plot_mean_comparison(stats, save_path)

    return stats

# -----------------------------
# Run if file executed directly
# -----------------------------
if __name__ == "__main__":
    run_score_statistics("data/processed/processed.csv", "outputs/score_statistics.csv")
