import os
from src.data_preparation import prepare_data
from src.score_statistics import run_score_statistics
from src.gender_analysis import gender_mean_scores
from src.first_child_analysis import first_child_analysis
from src.study_hours_analysis import study_hours_analysis

# -----------------------------
# File paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'dataset.csv')
PROCESSED_DATA = os.path.join(BASE_DIR, "data", "processed", "processed.csv")

PLOTS_DIR = os.path.join(BASE_DIR, "outputs")
INTERACTIVE_DIR = os.path.join(BASE_DIR, "docs")

SCORE_STATISTICS_PATH = os.path.join(PLOTS_DIR, "score_statistics")
GENDER_PATH = os.path.join(PLOTS_DIR, "gender_analysis")
FIRST_CHILD_ANALYSIS_PATH = os.path.join(PLOTS_DIR, "first_child_analysis")
STUDY_HOURS_PATH = os.path.join(PLOTS_DIR, "study_hours")
#SCORE_STATISTICS_PATH = os.path.join(PLOTS_DIR, "score_statistics")


INTERACTIVE_HTML_PATH = os.path.join(INTERACTIVE_DIR, "index.html")


# -----------------------------
# Main function
# -----------------------------
def main():
    # Prepare and clean the dataset
    prepare_data(RAW_DATA, PROCESSED_DATA)

    run_score_statistics(PROCESSED_DATA, SCORE_STATISTICS_PATH)

    gender_mean_scores(PROCESSED_DATA,GENDER_PATH)

    first_child_analysis(PROCESSED_DATA,FIRST_CHILD_ANALYSIS_PATH)

    study_hours_analysis(PROCESSED_DATA,STUDY_HOURS_PATH)



if __name__ == '__main__':
    main()
