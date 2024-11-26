import streamlit as st
import numpy as np
from scipy.stats import poisson

# --- Function Definitions ---
# Function to Calculate Poisson Probabilities for specific goals
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

# Function to Calculate BTTS Probability
def calculate_btts_probability(home_goals_prob, away_goals_prob):
    """Calculate BTTS (Both Teams To Score) probability."""
    btts_yes_prob = sum(h * a for h in home_goals_prob for a in away_goals_prob if h > 0 and a > 0)
    btts_no_prob = 1 - btts_yes_prob
    return btts_yes_prob, btts_no_prob

# --- Streamlit App Layout ---
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

# --- Input Fields ---
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

# --- HT/FT Odds and Probabilities ---
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

# --- Exact Goals Odds ---
st.sidebar.subheader("Exact Goals Odds (0 to 6+ Goals)")
exact_goals_odds = {
    "0 Goals": st.sidebar.number_input("Odds for 0 Goals", min_value=1.0, step=0.1, value=6.0),
    "1 Goal": st.sidebar.number_input("Odds for 1 Goal", min_value=1.0, step=0.1, value=5.5),
    "2 Goals": st.sidebar.number_input("Odds for 2 Goals", min_value=1.0, step=0.1, value=4.0),
    "3 Goals": st.sidebar.number_input("Odds for 3 Goals", min_value=1.0, step=0.1, value=3.0),
    "4 Goals": st.sidebar.number_input("Odds for 4 Goals", min_value=1.0, step=0.1, value=2.5),
    "5 Goals": st.sidebar.number_input("Odds for 5 Goals", min_value=1.0, step=0.1, value=15.0),
    "6+ Goals": st.sidebar.number_input("Odds for 6+ Goals", min_value=1.0, step=0.1, value=30.0)
}

# Calculate Exact Goal Probabilities based on the odds inputted
exact_goal_probs = {}
total_odds = sum(1 / value for value in exact_goals_odds.values())
for goal, odds in exact_goals_odds.items():
    prob = 1 / odds
    exact_goal_probs[goal] = prob / total_odds * 100

# --- BTTS Calculation ---
home_goals_prob = calculate_poisson_prob(avg_goals_home)
away_goals_prob = calculate_poisson_prob(avg_goals_away)

# BTTS (GG/NG) Probability Calculation
btts_yes_prob, btts_no_prob = calculate_btts_probability(home_goals_prob, away_goals_prob)

# Display BTTS Probabilities
st.write(f"BTTS (Yes) Probability: {btts_yes_prob * 100:.2f}%")
st.write(f"BTTS (No) Probability: {btts_no_prob * 100:.2f}%")

# --- Over/Under Goals Calculation ---
# Calculate Over/Under 1.5 and 2.5 Goals for HT/FT
def calculate_over_under_probability(over_odds, under_odds):
    """Calculate probabilities for Over/Under 1.5 and 2.5 goals."""
    over_prob = 1 / over_odds
    under_prob = 1 / under_odds
    total_prob = over_prob + under_prob
    return over_prob / total_prob, under_prob / total_prob

# HT and FT Over/Under probabilities
over_1_5_ht_prob, under_1_5_ht_prob = calculate_over_under_probability(over_1_5_ht, under_1_5_ht)
over_1_5_ft_prob, under_1_5_ft_prob = calculate_over_under_probability(over_1_5_ft, under_1_5_ft)
over_2_5_ft_prob, under_2_5_ft_prob = calculate_over_under_probability(over_2_5_ft, under_2_5_ft)

# Display Over/Under Probabilities
st.write(f"Over 1.5 HT Probability: {over_1_5_ht_prob * 100:.2f}%")
st.write(f"Under 1.5 HT Probability: {under_1_5_ht_prob * 100:.2f}%")
st.write(f"Over 1.5 FT Probability: {over_1_5_ft_prob * 100:.2f}%")
st.write(f"Under 1.5 FT Probability: {under_1_5_ft_prob * 100:.2f}%")
st.write(f"Over 2.5 FT Probability: {over_2_5_ft_prob * 100:.2f}%")
st.write(f"Under 2.5 FT Probability: {under_2_5_ft_prob * 100:.2f}%")
