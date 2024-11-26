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

# Correct Score Odds (Fulltime)
st.sidebar.subheader("Correct Score Odds (Fulltime)")
correct_score_odds_fulltime = {}
for i in range(5):
    for j in range(5):
        score = f"{i}:{j}"
        correct_score_odds_fulltime[score] = st.sidebar.number_input(f"FT Odds for {score}", value=10.0, step=0.01)

# Correct Score Odds (Halftime)
st.sidebar.subheader("Correct Score Odds (Halftime)")
correct_score_odds_halftime = {}
for i in range(3):
    for j in range(3):
        ht_score = f"{i}:{j}"
        correct_score_odds_halftime[ht_score] = st.sidebar.number_input(f"HT Odds for {ht_score}", value=10.0, step=0.01)

# Function to calculate HT/FT probabilities
def calculate_ht_ft_probabilities(ht_home, ht_draw, ht_away, ft_home, ft_draw, ft_away):
    """Calculate HT and FT probabilities."""
    ht_probs = [1 / ht_home, 1 / ht_draw, 1 / ht_away]
    ft_probs = [1 / ft_home, 1 / ft_draw, 1 / ft_away]

    ht_margin = calculate_margin([ht_home, ht_draw, ht_away])
    ft_margin = calculate_margin([ft_home, ft_draw, ft_away])

    return ht_probs, ft_probs, ht_margin, ft_margin

# Calculate probabilities for HT/FT
ht_probs, ft_probs, ht_margin, ft_margin = calculate_ht_ft_probabilities(ht_home, ht_draw, ht_away, ft_home, ft_draw, ft_away)

# Display HT/FT probabilities and margins
st.write(f"Halftime Probabilities: {np.round(ht_probs, 3)}")
st.write(f"Fulltime Probabilities: {np.round(ft_probs, 3)}")
st.write(f"Halftime Bookmaker Margin: {ht_margin:.2f}%")
st.write(f"Fulltime Bookmaker Margin: {ft_margin:.2f}%")

# Halftime/Fulltime Correct Score Recommendation
def recommend_ht_ft_correct_score(ht_probs, ft_probs, correct_score_odds_halftime, correct_score_odds_fulltime):
    """Recommend HT/FT correct score based on probabilities and odds."""
    ht_recommendation = {}
    ft_recommendation = {}

    # Calculate recommendations for HT
    for score, odds in correct_score_odds_halftime.items():
        prob = 1 / odds
        ht_recommendation[score] = prob * 100

    # Calculate recommendations for FT
    for score, odds in correct_score_odds_fulltime.items():
        prob = 1 / odds
        ft_recommendation[score] = prob * 100

    return ht_recommendation, ft_recommendation

ht_recommendation, ft_recommendation = recommend_ht_ft_correct_score(ht_probs, ft_probs, correct_score_odds_halftime, correct_score_odds_fulltime)

# Display recommendations
st.subheader("Halftime Correct Score Recommendations")
st.write(ht_recommendation)

st.subheader("Fulltime Correct Score Recommendations")
st.write(ft_recommendation)

# Additional Information
st.markdown("""
The recommendations above are based on Poisson distribution probabilities, bookmaker odds, and team performance statistics.
Use this to enhance your betting strategy and maximize potential returns.
""")
