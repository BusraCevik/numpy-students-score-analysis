import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import os


def build_dashboard(input_csv_path, output_html_path):
    # -----------------------------
    # Load dataset
    # -----------------------------
    df = pd.read_csv(input_csv_path)

    score_cols = ["MathScore", "ReadingScore", "WritingScore"]
    pink_palette = ["#FADADD", "#F4A7B9", "#E38AAE"]

    # -----------------------------
    # Score Distributions
    # -----------------------------
    dist_fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=score_cols
    )

    for i, col in enumerate(score_cols):
        dist_fig.add_trace(
            go.Histogram(
                x=df[col],
                nbinsx=30,
                name=col,
                marker_color=pink_palette[i],
                showlegend=False
            ),
            row=1,
            col=i + 1
        )

    dist_fig.update_layout(
        title_text="Score Distributions",
        height=400
    )

    # -----------------------------
    # Gender vs Scores
    # -----------------------------
    gender_means = df.groupby("Gender")[score_cols].mean().reset_index()

    gender_fig = px.bar(
        gender_means,
        x="Gender",
        y=score_cols,
        barmode="group",
        title="Average Scores by Gender",
        color_discrete_sequence=pink_palette
    )

    # -----------------------------
    # Parent Marital Status vs Scores (PINK)
    # -----------------------------
    parent_means = df.groupby("ParentMaritalStatus")[score_cols].mean().reset_index()

    parent_fig = px.bar(
        parent_means,
        x="ParentMaritalStatus",
        y=score_cols,
        barmode="group",
        title="Average Scores by Parent Marital Status",
        color_discrete_sequence=pink_palette
    )

    # -----------------------------
    # First Child & Gender Analysis (Interactive)
    # -----------------------------
    first_child_df = df.copy()

    # Normalize columns
    first_child_df["Gender"] = first_child_df["Gender"].str.capitalize()
    first_child_df["IsFirstChild"] = first_child_df["IsFirstChild"].astype(str).str.strip().str.capitalize()

    score_cols = ["MathScore", "ReadingScore", "WritingScore"]

    fc_means = first_child_df.groupby(["Gender", "IsFirstChild"])[score_cols].mean().reset_index()

    # Create interactive bar chart
    fc_fig = px.bar(
        fc_means,
        x="Gender",
        y=score_cols,
        color="IsFirstChild",
        barmode="group",
        title="Average Scores by Gender & First-Child Status",
        color_discrete_map={"Yes": "#E38AAE", "No": "#FADADD"}
    )

    # -----------------------------
    # Combine everything into one HTML
    # -----------------------------
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write("<html><head><title>Student Performance Dashboard</title></head><body>")
        f.write("<h1>Student Performance Analysis Dashboard</h1>")
        f.write("<p>This interactive dashboard provides an overview of key factors affecting student performance.</p>")

        f.write("<h2>Score Distributions</h2>")
        f.write(pio.to_html(dist_fig, full_html=False, include_plotlyjs='cdn'))

        f.write("<h2>Gender Comparison</h2>")
        f.write(pio.to_html(gender_fig, full_html=False, include_plotlyjs=False))

        f.write("<h2>Parent Marital Status</h2>")
        f.write(pio.to_html(parent_fig, full_html=False, include_plotlyjs=False))

        f.write("<h2>First Child vs Gender</h2>")
        f.write(pio.to_html(fc_fig, full_html=False, include_plotlyjs=False))

        f.write("<hr>")
        f.write('<p><b>Dataset:</b> <a href="https://www.kaggle.com/datasets/desalegngeb/students-exam-scores" target="_blank">Kaggle Students Exam Scores Dataset</a></p>')
        f.write("<p><b>Note:</b> All visuals are based on aggregated data.</p>")
        f.write("</body></html>")

    print(f"Interactive dashboard created at: {output_html_path}")


if __name__ == "__main__":
    build_dashboard(
        "data/processed/processed.csv",
        "docs/index.html"
    )
