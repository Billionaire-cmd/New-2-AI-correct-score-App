import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function to Calculate Poisson Probabilities
def calculate_poisson_prob(lambda_, max_goals):
    """Calculate Poisson probabilities up to max_goals."""
    return [poisson.pmf(i, lambda_) for i in range(max_goals + 1)]

# Function to Calculate Bookmaker's Margin
def calculate_margin(odds_list):
    """Calculate bookmaker's margin given a list of odds."""
    return (sum(1 / odds for odds in odds_list) - 1) * 100

# Function to Calculate Expected Value
def calculate_expected_value(prob, odds):
    """Calculate expected value."""
    return (prob * odds) - 1

# App Title and Introduction
st.title("🤖 Rabiotic Advanced HT/FT Correct Score Predictor")
st.markdown("""
Welcome to the **Rabiotic Advanced Halftime/Full-time Correct Score Predictor**!  
This app uses advanced statistical models, including the Poisson distribution, betting odds, and team statistics, 
to predict realistic halftime and full-time correct scores for football matches.  
It is designed to enhance your betting strategies by providing precise calculations for maximum ROI.
""")

# Sidebar for Inputs
st.sidebar.header("Match Statistics and Inputs")

# Average Goals Scored
avg_goals_home = st.sidebar.number_input("Average Goals Scored by Home Team", min_value=0.0, step=0.1, value=1.5)
avg_goals_away = st.sidebar.number_input("Average Goals Scored by Away Team", min_value=0.0, step=0.1, value=1.2)

# Average Points
avg_points_home = st.sidebar.number_input("Average Points for Home Team", min_value=0.0, step=0.1, value=1.8)
avg_points_away = st.sidebar.number_input("Average Points for Away Team", min_value=0.0, step=0.1, value=1.5)

# Betting Odds
st.sidebar.subheader("Halftime Odds")
ht_home = st.sidebar.number_input("Halftime Home Odds", min_value=1.0, step=0.1, value=2.5)
ht_draw = st.sidebar.number_input("Halftime Draw Odds", min_value=1.0, step=0.1, value=2.9)
ht_away = st.sidebar.number_input("Halftime Away Odds", min_value=1.0, step=0.1, value=3.1)

st.sidebar.subheader("Fulltime Odds")
ft_home = st.sidebar.number_input("Fulltime Home Odds", min_value=1.0, step=0.1, value=2.2)
ft_draw = st.sidebar.number_input("Fulltime Draw Odds", min_value=1.0, step=0.1, value=3.2)
ft_away = st.sidebar.number_input("Fulltime Away Odds", min_value=1.0, step=0.1, value=3.4)

# BTTS and Over/Under Odds
st.sidebar.subheader("BTTS GG/NG Odds")
btts_gg = st.sidebar.number_input("BTTS (Yes) Odds", min_value=1.0, step=0.1, value=1.8)
btts_ng = st.sidebar.number_input("BTTS (No) Odds", min_value=1.0, step=0.1, value=1.9)

st.sidebar.subheader("Over/Under Odds (Halftime)")
over_1_5_ht = st.sidebar.number_input("Over 1.5 HT Odds", min_value=1.0, step=0.1, value=2.5)
under_1_5_ht = st.sidebar.number_input("Under 1.5 HT Odds", min_value=1.0, step=0.1, value=1.6)

st.sidebar.subheader("Over/Under Odds (Fulltime)")
over_1_5_ft = st.sidebar.number_input("Over 1.5 FT Odds", min_value=1.0, step=0.1, value=1.4)
under_1_5_ft = st.sidebar.number_input("Under 1.5 FT Odds", min_value=1.0, step=0.1, value=2.9)
over_2_5_ft = st.sidebar.number_input("Over 2.5 FT Odds", min_value=1.0, step=0.1, value=2.0)
under_2_5_ft = st.sidebar.number_input("Under 2.5 FT Odds", min_value=1.0, step=0.1, value=1.8)

# Correct Score Odds (Fulltime)
st.sidebar.subheader("Correct Score Odds (Fulltime)")
correct_score_odds_fulltime = {}
for i in range(5):
    for j in range(5):
        score = f"{i}:{j}"
        correct_score_odds_fulltime[score] = st.sidebar.number_input(f"FT Odds for {score}", value=10.0, step=0.01)
# "Other" scores for Fulltime
correct_score_odds_fulltime["Other"] = st.sidebar.number_input("FT Odds for scores exceeding 4:4", value=50.0, step=0.01)

# Correct Score Odds (Halftime)
st.sidebar.subheader("Correct Score Odds (Halftime)")
correct_score_odds_halftime = {}
for i in range(3):
    for j in range(3):
        ht_score = f"{i}:{j}"
        correct_score_odds_halftime[ht_score] = st.sidebar.number_input(f"HT Odds for {ht_score}", value=10.0, step=0.01)
# "Other" scores for Halftime
correct_score_odds_halftime["Other"] = st.sidebar.number_input("HT Odds for scores exceeding 2:2", value=50.0, step=0.01)

# Function to Calculate Poisson Probabilities
def calculate_poisson_prob(lambda_, max_goals=4):
    """Calculate Poisson probabilities up to max_goals."""
    return [poisson.pmf(i, lambda_) for i in range(max_goals + 1)]

# Function to Calculate Bookmaker's Margin
def calculate_margin(odds_list):
    """Calculate bookmaker's margin given a list of odds."""
    return (sum(1 / odds for odds in odds_list) - 1) * 100

# Function to Calculate Expected Value
def calculate_expected_value(prob, odds):
    """Calculate expected value."""
    return (prob * odds) - 1

def main():
    st.title("BTTS GG/NG Insights")

    # Input for Score Matrix
    st.header("Input Score Matrix")
    st.write("Enter probabilities for each scoreline as a decimal (e.g., 0.18 for 18%). Leave blank for scores not applicable.")

    # Create user input fields for the score matrix
    score_matrix = {}
    for i in range(5):
        for j in range(5):
            key = f"Score {i}:{j}"
            value = st.text_input(f"Probability for {key}:", value="", key=f"score_{i}_{j}")
            if value:
                try:
                    score_matrix[(i, j)] = float(value)
                except ValueError:
                    st.warning(f"Invalid input for {key}. Skipping this scoreline.")

    # Show inputted score matrix
    if score_matrix:
        st.subheader("Your Inputted Score Matrix:")
        st.write(score_matrix)
    else:
        st.warning("Please input at least one probability.")

    # Only proceed if the score matrix is not empty
    if score_matrix:
        # Calculate BTTS GG/NG Insights
        btts_yes_scores = [(i, j) for i in range(1, 5) for j in range(1, 5)]
        btts_no_scores = [(i, 0) for i in range(5)] + [(0, j) for j in range(5)]

        # Probabilities for BTTS GG
        btts_yes_prob = sum(score_matrix.get((i, j), 0) for i, j in btts_yes_scores) * 100
        btts_yes_top_scores = sorted(
            {f"{i}:{j}": score_matrix.get((i, j), 0) for i, j in btts_yes_scores}.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        # Probabilities for BTTS NG
        btts_no_prob = sum(score_matrix.get((i, j), 0) for i, j in btts_no_scores) * 100
        btts_no_top_scores = sorted(
            {f"{i}:{j}": score_matrix.get((i, j), 0) for i, j in btts_no_scores}.items(),
            key=lambda x: x[1],
            reverse=True,
        )

        # Display BTTS GG/NG Insights
        st.subheader("BTTS GG/NG Results")
        st.write(f"**BTTS GG (Yes) Probability:** {btts_yes_prob:.2f}%")
        st.write("Top Correct Scores for BTTS GG (Yes):")
        for score, prob in btts_yes_top_scores[:5]:  # Top 5 scores
            st.write(f"  - {score}: {prob * 100:.2f}%")

        st.write(f"**BTTS NG (No) Probability:** {btts_no_prob:.2f}%")
        st.write("Top Correct Scores for BTTS NG (No):")
        for score, prob in btts_no_top_scores[:5]:  # Top 5 scores
            st.write(f"  - {score}: {prob * 100:.2f}%")

if __name__ == "__main__":
    main()

# Predict Probabilities and Insights
if st.button("Predict Probabilities and Insights"):
    try:
        # Calculate Poisson Probabilities for Fulltime
        fulltime_home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
        fulltime_away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)
        score_matrix = np.outer(fulltime_home_probs, fulltime_away_probs)

        # Calculate Poisson Probabilities for Halftime (assuming halftime goals are ~50% of fulltime goals)
        halftime_home_avg = avg_goals_home / 2
        halftime_away_avg = avg_goals_away / 2
        halftime_home_probs = calculate_poisson_prob(halftime_home_avg, max_goals=2)
        halftime_away_probs = calculate_poisson_prob(halftime_away_avg, max_goals=2)
        halftime_score_matrix = np.outer(halftime_home_probs, halftime_away_probs)

        # Calculate Fulltime Score Probabilities
        fulltime_score_probs = {f"{i}:{j}": score_matrix[i, j] for i in range(5) for j in range(5)}
        fulltime_other_prob = 1 - sum(fulltime_score_probs.values())
        fulltime_score_probs["Other"] = fulltime_other_prob

        # Calculate Halftime Score Probabilities
        halftime_score_probs = {f"{i}:{j}": halftime_score_matrix[i, j] for i in range(3) for j in range(3)}
        halftime_other_prob = 1 - sum(halftime_score_probs.values())
        halftime_score_probs["Other"] = halftime_other_prob

        # Sort Scores by Probability
        sorted_fulltime_scores = sorted(fulltime_score_probs.items(), key=lambda x: x[1], reverse=True)
        sorted_halftime_scores = sorted(halftime_score_probs.items(), key=lambda x: x[1], reverse=True)

        # BTTS Probabilities
        btts_yes_prob = sum(score_matrix[i][j] for i in range(1,5) for j in range(1,5)) * 100
        btts_no_prob = 100 - btts_yes_prob

        # Over/Under 2.5 Goals Probabilities (Fulltime)
        over_2_5_prob = sum(score_matrix[i][j] for i in range(3,5) for j in range(5)) * 100
        under_2_5_prob = 100 - over_2_5_prob

        # Over/Under 1.5 Goals Probabilities (Halftime)
        over_1_5_ht_prob = sum(halftime_score_matrix[i][j] for i in range(2,3) for j in range(3)) * 100
        under_1_5_ht_prob = 100 - over_1_5_ht_prob

        # Display Insights
        st.subheader("Football Match Outcome Probabilities")

        st.write(f"**Halftime Probabilities:**")
        for score, prob in sorted_halftime_scores:
            st.write(f"  - {score}: {prob * 100:.2f}%")
        st.write(f"**Fulltime Probabilities:**")
        for score, prob in sorted_fulltime_scores:
            st.write(f"  - {score}: {prob * 100:.2f}%")

        st.write(f"\n**BTTS Probabilities:**")
        st.write(f"  - BTTS Yes: {btts_yes_prob:.2f}%")
        st.write(f"  - BTTS No: {btts_no_prob:.2f}%")

        st.write(f"\n**Over/Under 2.5 Goals (Fulltime):**")
        st.write(f"  - Over 2.5 Goals: {over_2_5_prob:.2f}%")
        st.write(f"  - Under 2.5 Goals: {under_2_5_prob:.2f}%")

        st.write(f"\n**Over/Under 1.5 Goals (Halftime):**")
        st.write(f"  - Over 1.5 Goals: {over_1_5_ht_prob:.2f}%")
        st.write(f"  - Under 1.5 Goals: {under_1_5_ht_prob:.2f}%")

        # Display Final Recommendations
        st.subheader("Final Recommendation")

        # Halftime Correct Score Recommendation
        top_halftime_score = sorted_halftime_scores[0]  # Get the top HT score
        st.write(f"**Halftime Correct Score Recommendation:** {top_halftime_score[0]} "
                 f"(Probability: {top_halftime_score[1] * 100:.2f}%)")

        # Fulltime Correct Score Recommendation
        top_fulltime_score = sorted_fulltime_scores[0]  # Get the top FT score
        st.write(f"**Fulltime Correct Score Recommendation:** {top_fulltime_score[0]} "
                 f"(Probability: {top_fulltime_score[1] * 100:.2f}%)")  
    
except Exception as e:
        st.error(f"Error in prediction: {e}")
