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

# Correct Score Odds (Fulltime and Halftime)
st.sidebar.subheader("Correct Score Odds (Fulltime)")
correct_score_odds_fulltime = {}
for i in range(5):
    for j in range(5):
        score = f"{i}:{j}"
        correct_score_odds_fulltime[score] = st.sidebar.number_input(f"FT Odds for {score}", value=10.0, step=0.01)

correct_score_odds_fulltime["Other"] = st.sidebar.number_input("FT Odds for scores exceeding 4:4", value=50.0, step=0.01)

st.sidebar.subheader("Correct Score Odds (Halftime)")
correct_score_odds_halftime = {}
for i in range(3):
    for j in range(3):
        ht_score = f"{i}:{j}"
        correct_score_odds_halftime[ht_score] = st.sidebar.number_input(f"HT Odds for {ht_score}", value=10.0, step=0.01)

correct_score_odds_halftime["Other"] = st.sidebar.number_input("HT Odds for scores exceeding 2:2", value=50.0, step=0.01)

# Calculate Probabilities from Odds
ht_probs = [1 / ht_home, 1 / ht_draw, 1 / ht_away]
ft_probs = [1 / ft_home, 1 / ft_draw, 1 / ft_away]

# Normalize Probabilities
ht_prob_sum = sum(ht_probs)
ft_prob_sum = sum(ft_probs)
ht_probs_normalized = [round(prob / ht_prob_sum, 3) for prob in ht_probs]
ft_probs_normalized = [round(prob / ft_prob_sum, 3) for prob in ft_probs]

# Calculate Margins
ht_margin = calculate_margin([ht_home, ht_draw, ht_away])
ft_margin = calculate_margin([ft_home, ft_draw, ft_away])

# Display Results
st.write(f"Halftime Probabilities (Normalized): {ht_probs_normalized}")
st.write(f"Fulltime Probabilities (Normalized): {ft_probs_normalized}")
st.write(f"Halftime Bookmaker Margin: {ht_margin:.2f}%")
st.write(f"Fulltime Bookmaker Margin: {ft_margin:.2f}%")

# Recommendation: Halftime/Full-time Correct Score
st.subheader("Recommended Halftime/Full-time Correct Score")
# Logic to determine the best recommended score based on probabilities
best_ht_score = max(ht_probs_normalized)
best_ft_score = max(ft_probs_normalized)

if best_ht_score == ht_probs_normalized[0]:
    ht_result = "Home Team Leads"
elif best_ht_score == ht_probs_normalized[1]:
    ht_result = "Draw"
else:
    ht_result = "Away Team Leads"

if best_ft_score == ft_probs_normalized[0]:
    ft_result = "Home Team Wins"
elif best_ft_score == ft_probs_normalized[1]:
    ft_result = "Draw"
else:
    ft_result = "Away Team Wins"

st.write(f"Recommended Halftime Prediction: {ht_result}")
st.write(f"Recommended Fulltime Prediction: {ft_result}")

# Additional Expected Value Calculations
st.subheader("Expected Value of Predictions")
ht_expected_value = calculate_expected_value(ht_probs_normalized[0], ht_home)
ft_expected_value = calculate_expected_value(ft_probs_normalized[0], ft_home)

st.write(f"Expected Value for Halftime Home Prediction: {ht_expected_value:.2f}")
st.write(f"Expected Value for Fulltime Home Prediction: {ft_expected_value:.2f}")

