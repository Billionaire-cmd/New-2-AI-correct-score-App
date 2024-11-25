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

# Monte Carlo Simulation for Goal Prediction
def monte_carlo_simulation(home_avg, away_avg, num_simulations=10000):
    """Run Monte Carlo simulations for goal prediction."""
    home_goals = np.random.poisson(home_avg, num_simulations)
    away_goals = np.random.poisson(away_avg, num_simulations)
    return home_goals, away_goals

# Function to Adjust for Team Strength
def adjust_for_team_strength(home_goals, away_goals, home_strength=1.0, away_strength=1.0):
    """Adjust home and away team goals based on strength."""
    adjusted_home_goals = home_goals * home_strength
    adjusted_away_goals = away_goals * away_strength
    return adjusted_home_goals, adjusted_away_goals

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

# Predict Probabilities and Insights
if st.button("Predict Probabilities and Insights"):
    try:
        # Calculate Poisson Probabilities for Fulltime
        fulltime_home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
        fulltime_away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)
        score_matrix = np.outer(fulltime_home_probs, fulltime_away_probs)

        # Monte Carlo Simulation for goal prediction
        home_goals, away_goals = monte_carlo_simulation(avg_goals_home, avg_goals_away)

        # Adjust for Team Strength
        home_strength = 1.1  # Example strength factor for home team
        away_strength = 0.9  # Example strength factor for away team
        adjusted_home_goals, adjusted_away_goals = adjust_for_team_strength(home_goals, away_goals, home_strength, away_strength)

        # Create Histogram of Goals
        st.subheader("Goal Distribution from Monte Carlo Simulation")
        fig, ax = plt.subplots()
        ax.hist(home_goals, bins=30, alpha=0.5, label='Home Team Goals')
        ax.hist(away_goals, bins=30, alpha=0.5, label='Away Team Goals')
        ax.legend(loc='best')
        ax.set_title("Monte Carlo Simulation - Goals Distribution")
        st.pyplot(fig)

        # Betting Strategy Suggestion based on Odds and Probabilities
        home_odds = np.array([ht_home, ft_home])
        away_odds = np.array([ht_away, ft_away])
        draw_odds = np.array([ht_draw, ft_draw])

        best_betting_strategy = "None"
        best_value = -float('inf')
        
        # Calculate the best betting strategy based on expected value
        for odds, team in zip([home_odds, away_odds, draw_odds], ["Home", "Away", "Draw"]):
            expected_value = calculate_expected_value(np.mean(score_matrix), np.mean(odds))
            if expected_value > best_value:
                best_value = expected_value
                best_betting_strategy = team
        
        st.subheader("Betting Strategy Suggestion")
        st.write(f"The best betting strategy based on expected value is: **{best_betting_strategy}**")

        # Display Monte Carlo Simulation Results
        st.subheader("Monte Carlo Simulation Results")
        st.write(f"Home Goals (mean): {np.mean(home_goals)} | Away Goals (mean): {np.mean(away_goals)}")
        st.write(f"Adjusted Home Goals (mean): {np.mean(adjusted_home_goals)} | Adjusted Away Goals (mean): {np.mean(adjusted_away_goals)}")
        
    except Exception as e:
        st.error(f"An error occurred: {e}")
