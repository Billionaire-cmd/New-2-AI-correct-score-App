import streamlit as st
import numpy as np
from scipy.stats import poisson

# Define the function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the odds-based probabilities
def odds_to_prob(odds):
    return 1 / odds

# Main function to calculate and display predictions
def calculate_predictions():
    # User input: Team A and Team B stats
    team_a_home_goals = st.number_input("Team A Average Goals Scored (Home)", min_value=0.0, value=1.50)
    team_b_away_goals = st.number_input("Team B Average Goals Scored (Away)", min_value=0.0, value=1.30)
    team_a_home_conceded = st.number_input("Team A Average Goals Conceded (Home)", min_value=0.0, value=1.30)
    team_b_away_conceded = st.number_input("Team B Average Goals Conceded (Away)", min_value=0.0, value=1.50)

    # User input: Odds for HT and FT outcomes
    ht_home_win_odds = st.number_input("HT Home Win Odds", min_value=0.0, value=2.40)
    ht_draw_odds = st.number_input("HT Draw Odds", min_value=0.0, value=2.10)
    ht_away_win_odds = st.number_input("HT Away Win Odds", min_value=0.0, value=4.50)
    ft_home_win_odds = st.number_input("FT Home Win Odds", min_value=0.0, value=1.80)
    ft_draw_odds = st.number_input("FT Draw Odds", min_value=0.0, value=3.50)
    ft_away_win_odds = st.number_input("FT Away Win Odds", min_value=0.0, value=3.90)

    # User input: Over/Under 2.5 Goals and BTTS
    over_2_5_odds = st.number_input("Over 2.5 Goals Odds", min_value=0.0, value=1.87)
    under_2_5_odds = st.number_input("Under 2.5 Goals Odds", min_value=0.0, value=1.80)
    btts_gg_odds = st.number_input("BTTS GG Odds", min_value=0.0, value=1.77)
    btts_ng_odds = st.number_input("BTTS NG Odds", min_value=0.0, value=1.83)

    # Generate all possible scorelines (for both HT and FT)
    max_goals = 5  # Define the maximum number of goals to consider for scorelines
    ht_scorelines = generate_scorelines(max_goals)
    ft_scorelines = generate_scorelines(max_goals)

    # Calculate Poisson probabilities for each scoreline
    team_a_ht_goal_rate = team_a_home_goals / 2  # Approximate halftime goals
    team_b_ht_goal_rate = team_b_away_goals / 2  # Approximate halftime goals
    team_a_ft_goal_rate = team_a_home_goals  # Full-time goal rate
    team_b_ft_goal_rate = team_b_away_goals  # Full-time goal rate

    # Initialize lists to store results
    ht_results = []
    ft_results = []

    # Calculate Poisson probabilities for HT scorelines
    for home_goals, away_goals in ht_scorelines:
        ht_prob = poisson_prob(team_a_ht_goal_rate, home_goals) * poisson_prob(team_b_ht_goal_rate, away_goals)
        ht_results.append((home_goals, away_goals, ht_prob))

    # Calculate Poisson probabilities for FT scorelines
    for home_goals, away_goals in ft_scorelines:
        ft_prob = poisson_prob(team_a_ft_goal_rate, home_goals) * poisson_prob(team_b_ft_goal_rate, away_goals)
        ft_results.append((home_goals, away_goals, ft_prob))

    # Display HT and FT predictions
    st.subheader("Halftime Correct Score Predictions")
    for home_goals, away_goals, prob in ht_results:
        st.write(f"HT {home_goals}-{away_goals}: Poisson Probability: {prob:.4f}")

    st.subheader("Full-time Correct Score Predictions")
    for home_goals, away_goals, prob in ft_results:
        st.write(f"FT {home_goals}-{away_goals}: Poisson Probability: {prob:.4f}")

    # Combine odds for each scoreline and display the odds-based probability
    st.subheader("Odds-based Probabilities for Correct Scorelines")
    for home_goals, away_goals, _ in ht_results:
        # Here, you could use HT Odds (such as home win, away win, or draw) to calculate probabilities
        # For simplicity, using just the Poisson probabilities here
        ht_odds = ht_home_win_odds if home_goals > away_goals else ht_away_win_odds  # Example
        ht_odds_prob = odds_to_prob(ht_odds)
        st.write(f"HT {home_goals}-{away_goals}: Odds-based Probability: {ht_odds_prob:.4f}")

    for home_goals, away_goals, _ in ft_results:
        # Similarly, apply the FT odds (home win, away win, or draw) to calculate probabilities
        ft_odds = ft_home_win_odds if home_goals > away_goals else ft_away_win_odds  # Example
        ft_odds_prob = odds_to_prob(ft_odds)
        st.write(f"FT {home_goals}-{away_goals}: Odds-based Probability: {ft_odds_prob:.4f}")

# Create the app layout
def main():
    st.title("Football Match Prediction: All Halftime & Full-time Correct Scorelines")
    st.sidebar.header("Enter Match Inputs")
    
    # Call the function to calculate predictions
    calculate_predictions()

if __name__ == "__main__":
    main()
