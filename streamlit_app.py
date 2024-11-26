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

# Exact Score Odds (Halftime and Fulltime)
def input_correct_score_odds(period="Fulltime"):
    correct_score_odds = {}
    for i in range(5):  # Max 4:4 score for Fulltime
        for j in range(5):
            score = f"{i}:{j}"
            correct_score_odds[score] = st.sidebar.number_input(f"{period} Odds for {score}", value=10.0, step=0.01)
    correct_score_odds["Other"] = st.sidebar.number_input(f"{period} Odds for scores exceeding 4:4", value=50.0, step=0.01)
    return correct_score_odds

correct_score_odds_fulltime = input_correct_score_odds("Fulltime")
correct_score_odds_halftime = input_correct_score_odds("Halftime")

# Probabilities for HT/FT based on odds
ht_probs = [1 / ht_home, 1 / ht_draw, 1 / ht_away]
ft_probs = [1 / ft_home, 1 / ft_draw, 1 / ft_away]

# Calculate margins for HT and FT
ht_margin = calculate_margin([ht_home, ht_draw, ht_away])
ft_margin = calculate_margin([ft_home, ft_draw, ft_away])

# Display HT/FT probabilities and margins
st.write(f"Halftime Probabilities: {np.round(ht_probs, 3)}")
st.write(f"Fulltime Probabilities: {np.round(ft_probs, 3)}")
st.write(f"Halftime Bookmaker Margin: {ht_margin:.2f}%")
st.write(f"Fulltime Bookmaker Margin: {ft_margin:.2f}%")

# Exact Goal Probabilities based on odds inputted for Exact Goals
exact_goals_odds = {
    "0 Goals": st.sidebar.number_input("Odds for 0 Goals", min_value=1.0, step=0.1, value=6.0),
    "1 Goal": st.sidebar.number_input("Odds for 1 Goal", min_value=1.0, step=0.1, value=5.5),
    "2 Goals": st.sidebar.number_input("Odds for 2 Goals", min_value=1.0, step=0.1, value=4.0),
    "3 Goals": st.sidebar.number_input("Odds for 3 Goals", min_value=1.0, step=0.1, value=3.0),
    "4 Goals": st.sidebar.number_input("Odds for 4 Goals", min_value=1.0, step=0.1, value=2.5),
    "5 Goals": st.sidebar.number_input("Odds for 5 Goals", min_value=1.0, step=0.1, value=15.0),
    "6+ Goals": st.sidebar.number_input("Odds for 6+ Goals", min_value=1.0, step=0.1, value=30.0)
}

# Calculate Exact Goal Probabilities
exact_goal_probs = {}
total_odds = sum(1 / value for value in exact_goals_odds.values())
for goal, odds in exact_goals_odds.items():
    prob = 1 / odds
    exact_goal_probs[goal] = prob / total_odds * 100

# Recommendation of HT/FT Correct Score
def recommend_correct_score(ht_probs, ft_probs):
    # Example method of recommending based on max probabilities
    ht_max_idx = np.argmax(ht_probs)
    ft_max_idx = np.argmax(ft_probs)
    ht_outcomes = ['Home', 'Draw', 'Away']
    ft_outcomes = ['Home', 'Draw', 'Away']

    recommended_ht = ht_outcomes[ht_max_idx]
    recommended_ft = ft_outcomes[ft_max_idx]

    st.subheader("Recommended HT/FT Correct Score:")
    st.write(f"Recommended HT: {recommended_ht}")
    st.write(f"Recommended FT: {recommended_ft}")

# Call the recommendation function
recommend_correct_score(ht_probs, ft_probs)

# Handle any exceptions for calculations
try:
    st.subheader("Calculation Results")
    st.write(f"Exact Goal Probabilities: {exact_goal_probs}")
except Exception as e:
    st.write(f"An error occurred: {e}")
