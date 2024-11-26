import streamlit as st
import numpy as np
from scipy.stats import poisson

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

# Betting Odds for HT and FT
st.sidebar.subheader("Halftime Odds")
ht_home = st.sidebar.number_input("Halftime Home Odds", min_value=1.0, step=0.1, value=2.5)
ht_draw = st.sidebar.number_input("Halftime Draw Odds", min_value=1.0, step=0.1, value=2.9)
ht_away = st.sidebar.number_input("Halftime Away Odds", min_value=1.0, step=0.1, value=3.1)

st.sidebar.subheader("Fulltime Odds")
ft_home = st.sidebar.number_input("Fulltime Home Odds", min_value=1.0, step=0.1, value=2.2)
ft_draw = st.sidebar.number_input("Fulltime Draw Odds", min_value=1.0, step=0.1, value=3.2)
ft_away = st.sidebar.number_input("Fulltime Away Odds", min_value=1.0, step=0.1, value=3.4)

# Correct Score Odds for HT and FT
def get_correct_score_odds(prefix, max_goals, half_time=True):
    """Generate correct score odds inputs for HT or FT."""
    score_odds = {}
    for i in range(max_goals):
        for j in range(max_goals):
            score = f"{i}:{j}"
            score_odds[score] = st.sidebar.number_input(f"{prefix} Odds for {score}", value=10.0, step=0.01)
    score_odds["Other"] = st.sidebar.number_input(f"{prefix} Odds for scores exceeding {max_goals-1}:{max_goals-1}", value=50.0, step=0.01)
    return score_odds

correct_score_odds_halftime = get_correct_score_odds("HT", 3)
correct_score_odds_fulltime = get_correct_score_odds("FT", 5, half_time=False)

# Calculate Probabilities for HT/FT based on odds
def calculate_probabilities(odds_list):
    """Calculate probabilities based on odds."""
    return [1 / odds for odds in odds_list]

ht_probs = calculate_probabilities([ht_home, ht_draw, ht_away])
ft_probs = calculate_probabilities([ft_home, ft_draw, ft_away])

# Predict Probabilities and Insights Button
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
        btts_yes_prob = sum(score_matrix[i][j] for i in range(1, 5) for j in range(1, 5)) * 100
        btts_no_prob = 100 - btts_yes_prob

        # Over/Under 2.5 Goals Probabilities (Fulltime)
        over_2_5_prob = sum(score_matrix[i][j] for i in range(3, 5) for j in range(5)) * 100
        under_2_5_prob = 100 - over_2_5_prob

        # Over/Under 1.5 Goals Probabilities (Halftime)
        over_1_5_ht_prob = sum(halftime_score_matrix[i][j] for i in range(2, 3) for j in range(3)) * 100
        under_1_5_ht_prob = 100 - over_1_5_ht_prob

        # Over/Under 1.5 Goals Probabilities (Fulltime)
        over_1_5_ft_prob = sum(score_matrix[i][j] for i in range(2, 5) for j in range(5)) * 100
        under_1_5_ft_prob = 100 - over_1_5_ft_prob

        # Match Outcome Probabilities
        home_win_prob = sum(score_matrix[i][j] for i in range(1, 5) for j in range(0, i)) * 100
        draw_prob = sum(score_matrix[i][i] for i in range(5)) * 100
        away_win_prob = 100 - home_win_prob - draw_prob

        # Bookmaker's Margins
        margin_btts = calculate_margin([btts_yes_prob, btts_no_prob])
        margin_over_under_2_5 = calculate_margin([over_2_5_prob, under_2_5_prob])
        margin_over_under_1_5_ht = calculate_margin([over_1_5_ht_prob, under_1_5_ht_prob])
        margin_over_under_1_5_ft = calculate_margin([over_1_5_ft_prob, under_1_5_ft_prob])
        margin_match_outcomes = calculate_margin([home_win_prob, draw_prob, away_win_prob])

        # Expected Values for Betting Markets
        btts_yes_ev = calculate_expected_value(btts_yes_prob / 100, btts_yes_prob)
        btts_no_ev = calculate_expected_value(btts_no_prob / 100, btts_no_prob)

        # Show the insights in the Streamlit app
        st.subheader("Fulltime Score Probabilities")
        st.write(sorted_fulltime_scores)

        st.subheader("Halftime Score Probabilities")
        st.write(sorted_halftime_scores)

        st.subheader("BTTS Probabilities")
        st.write(f"BTTS Yes: {btts_yes_prob}%")
        st.write(f"BTTS No: {btts_no_prob}%")

        st.subheader("Over/Under 2.5 Goals (Fulltime) Probabilities")
        st.write(f"Over 2.5 Goals: {over_2_5_prob}%")
        st.write(f"Under 2.5 Goals: {under_2_5_prob}%")

        st.subheader("Over/Under 1.5 Goals (Halftime) Probabilities")
        st.write(f"Over 1.5 Goals: {over_1_5_ht_prob}%")
        st.write(f"Under 1.5 Goals: {under_1_5_ht_prob}%")

        st.subheader("Match Outcome Probabilities")
        st.write(f"Home Win: {home_win_prob}%")
        st.write(f"Draw: {draw_prob}%")
        st.write(f"Away Win: {away_win_prob}%")

        st.subheader("Expected Value (EV) and Betting Margins")
        st.write(f"Expected Value (BTTS Yes): {btts_yes_ev}")
        st.write(f"Expected Value (BTTS No): {btts_no_ev}")
        st.write(f"Margin BTTS: {margin_btts}%")
        st.write(f"Margin Over/Under 2.5 Goals: {margin_over_under_2_5}%")
        st.write(f"Margin Over/Under 1.5 Goals (HT): {margin_over_under_1_5_ht}%")
        st.write(f"Margin Over/Under 1.5 Goals (FT): {margin_over_under_1_5_ft}%")
        st.write(f"Margin Match Outcomes: {margin_match_outcomes}%")

    except Exception as e:
        st.error(f"Error: {e}")
