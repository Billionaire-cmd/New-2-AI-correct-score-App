import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt
import seaborn as sns

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

# Function to Perform Monte Carlo Simulation
def monte_carlo_simulation(home_avg, away_avg, simulations=10000):
    """Perform Monte Carlo simulation to predict scoreline distributions."""
    home_goals = np.random.poisson(home_avg, simulations)
    away_goals = np.random.poisson(away_avg, simulations)
    return home_goals, away_goals

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

# Function to Adjust for Team Strength
def adjust_for_team_strength(home_avg, away_avg, home_strength, away_strength):
    """Adjust team averages based on team strength."""
    adjusted_home_avg = home_avg * (1 + home_strength / 10)
    adjusted_away_avg = away_avg * (1 + away_strength / 10)
    return adjusted_home_avg, adjusted_away_avg

# Betting Strategy Suggestions Based on Expected Value
def betting_strategy_suggestion(expected_value_home, expected_value_away, expected_value_draw):
    """Suggest a betting strategy based on expected values."""
    if expected_value_home > expected_value_away and expected_value_home > expected_value_draw:
        return "Bet on Home Win"
    elif expected_value_away > expected_value_home and expected_value_away > expected_value_draw:
        return "Bet on Away Win"
    else:
        return "Bet on Draw"

# Predict Probabilities and Insights
if st.button("Predict Probabilities and Insights"):
    try:
        # Adjust for Team Strength
        home_strength = st.sidebar.number_input("Home Team Strength (0-10)", min_value=0, max_value=10, step=1, value=5)
        away_strength = st.sidebar.number_input("Away Team Strength (0-10)", min_value=0, max_value=10, step=1, value=5)
        
        adjusted_home_avg, adjusted_away_avg = adjust_for_team_strength(avg_goals_home, avg_goals_away, home_strength, away_strength)

        # Monte Carlo Simulation
        simulations = 10000
        home_goals, away_goals = monte_carlo_simulation(adjusted_home_avg, adjusted_away_avg, simulations)

        # Plot Monte Carlo Simulation Results
        fig, ax = plt.subplots()
        ax.hist(home_goals, bins=range(0, 6), alpha=0.7, label="Home Goals")
        ax.hist(away_goals, bins=range(0, 6), alpha=0.7, label="Away Goals")
        ax.set_xlabel("Goals")
        ax.set_ylabel("Frequency")
        ax.legend()
        st.pyplot(fig)

        # Calculate Poisson Probabilities for Fulltime
        fulltime_home_probs = calculate_poisson_prob(adjusted_home_avg, max_goals=4)
        fulltime_away_probs = calculate_poisson_prob(adjusted_away_avg, max_goals=4)
        score_matrix = np.outer(fulltime_home_probs, fulltime_away_probs)

        # Calculate Poisson Probabilities for Halftime (assuming halftime goals are ~50% of fulltime goals)
        halftime_home_avg = adjusted_home_avg / 2
        halftime_away_avg = adjusted_away_avg / 2
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

        # Over/Under 1.5 Goals Probabilities (Fulltime)
        over_1_5_ft_prob = sum(score_matrix[i][j] for i in range(2,5) for j in range(5)) * 100
        under_1_5_ft_prob = 100 - over_1_5_ft_prob

        # Display Results
        st.subheader("Predicted Fulltime Probabilities")
        st.write(sorted_fulltime_scores)

        st.subheader("Predicted Halftime Probabilities")
        st.write(sorted_halftime_scores)

        st.subheader("Predicted BTTS Probability")
        st.write(f"BTTS Yes: {btts_yes_prob:.2f}%  |  BTTS No: {btts_no_prob:.2f}%")

        st.subheader("Over/Under 2.5 Goals (Fulltime) Probability")
        st.write(f"Over 2.5: {over_2_5_prob:.2f}%  |  Under 2.5: {under_2_5_prob:.2f}%")

        st.subheader("Over/Under 1.5 Goals (Halftime) Probability")
        st.write(f"Over 1.5: {over_1_5_ht_prob:.2f}%  |  Under 1.5: {under_1_5_ht_prob:.2f}%")

        st.subheader("Over/Under 1.5 Goals (Fulltime) Probability")
        st.write(f"Over 1.5: {over_1_5_ft_prob:.2f}%  |  Under 1.5: {under_1_5_ft_prob:.2f}%")

        # Suggest Betting Strategy
        ev_home = calculate_expected_value(fulltime_home_probs[1], ht_home)
        ev_away = calculate_expected_value(fulltime_away_probs[1], ht_away)
        ev_draw = calculate_expected_value(fulltime_home_probs[0] + fulltime_away_probs[0], ht_draw)

        strategy = betting_strategy_suggestion(ev_home, ev_away, ev_draw)
        st.subheader(f"Betting Strategy Suggestion: {strategy}")

    except Exception as e:
        st.error(f"An error occurred: {e}")
