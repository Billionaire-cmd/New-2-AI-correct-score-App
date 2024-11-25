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
to recommend **Low-Value Bets** for halftime and full-time correct scores.
""")

# Sidebar for Inputs
st.sidebar.header("Match Statistics and Inputs")

# Average Goals Scored
avg_goals_home = st.sidebar.number_input("Average Goals Scored by Home Team", min_value=0.0, step=0.1, value=1.5)
avg_goals_away = st.sidebar.number_input("Average Goals Scored by Away Team", min_value=0.0, step=0.1, value=1.2)

# Correct Score Odds (Fulltime)
st.sidebar.subheader("Correct Score Odds (Fulltime)")
correct_score_odds_fulltime = {}
for i in range(5):
    for j in range(5):
        score = f"{i}:{j}"
        correct_score_odds_fulltime[score] = st.sidebar.number_input(f"FT Odds for {score}", value=10.0, step=0.01)
correct_score_odds_fulltime["Other"] = st.sidebar.number_input("FT Odds for scores exceeding 4:4", value=50.0, step=0.01)

# Correct Score Odds (Halftime)
st.sidebar.subheader("Correct Score Odds (Halftime)")
correct_score_odds_halftime = {}
for i in range(3):
    for j in range(3):
        ht_score = f"{i}:{j}"
        correct_score_odds_halftime[ht_score] = st.sidebar.number_input(f"HT Odds for {ht_score}", value=10.0, step=0.01)
correct_score_odds_halftime["Other"] = st.sidebar.number_input("HT Odds for scores exceeding 2:2", value=50.0, step=0.01)

# Predict Probabilities and Insights
if st.button("Predict Low-Value Bets"):
    try:
        # Calculate Poisson Probabilities
        fulltime_home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
        fulltime_away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)
        halftime_home_probs = calculate_poisson_prob(avg_goals_home / 2, max_goals=2)
        halftime_away_probs = calculate_poisson_prob(avg_goals_away / 2, max_goals=2)

        # Fulltime and Halftime Score Matrices
        fulltime_score_matrix = np.outer(fulltime_home_probs, fulltime_away_probs)
        halftime_score_matrix = np.outer(halftime_home_probs, halftime_away_probs)

        # Calculate Fulltime and Halftime Probabilities
        fulltime_score_probs = {f"{i}:{j}": fulltime_score_matrix[i, j] for i in range(5) for j in range(5)}
        fulltime_score_probs["Other"] = 1 - sum(fulltime_score_probs.values())
        halftime_score_probs = {f"{i}:{j}": halftime_score_matrix[i, j] for i in range(3) for j in range(3)}
        halftime_score_probs["Other"] = 1 - sum(halftime_score_probs.values())

        # Calculate Expected Values
        fulltime_ev = {
            score: calculate_expected_value(prob, correct_score_odds_fulltime[score])
            for score, prob in fulltime_score_probs.items()
        }
        halftime_ev = {
            score: calculate_expected_value(prob, correct_score_odds_halftime[score])
            for score, prob in halftime_score_probs.items()
        }

        # Find Low-Value Bets
        low_value_ft_bet = min(fulltime_ev.items(), key=lambda x: x[1])
        low_value_ht_bet = min(halftime_ev.items(), key=lambda x: x[1])

        # Display Results
        st.subheader("Fulltime Low-Value Bet Recommendation")
        st.write(f"Recommended Bet: {low_value_ft_bet[0]} with Expected Value: {low_value_ft_bet[1]:.2f}")

        st.subheader("Halftime Low-Value Bet Recommendation")
        st.write(f"Recommended Bet: {low_value_ht_bet[0]} with Expected Value: {low_value_ht_bet[1]:.2f}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
