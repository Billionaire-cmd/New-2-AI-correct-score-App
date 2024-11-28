import streamlit as st
import numpy as np
from scipy.stats import poisson

# Define the function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to calculate the odds-based probabilities (adjusted for over 2.5 goals)
def adjust_for_over_2_5_goals(over_2_5_odds, poisson_prob):
    # Over 2.5 goals implies scoring more than 2 goals, let's scale the probability
    over_2_5_prob = implied_prob(over_2_5_odds)
    adjusted_prob = poisson_prob * (over_2_5_prob / 100)
    return adjusted_prob

# Generate all possible scorelines for both HT and FT
def generate_scorelines(max_goals=5):
    scorelines = []
    for home_goals in range(max_goals + 1):
        for away_goals in range(max_goals + 1):
            scorelines.append((home_goals, away_goals))
    return scorelines

# Main function to calculate and display predictions
def calculate_predictions():
    # User input: Team A and Team B stats
    team_a_home_goals = st.number_input("Team A Average Goals Scored (Home)", min_value=0.0, value=0.30)
    team_b_away_goals = st.number_input("Team B Average Goals Scored (Away)", min_value=0.0, value=1.00)
    team_a_home_conceded = st.number_input("Team A Average Goals Conceded (Home)", min_value=0.0, value=1.50)
    team_b_away_conceded = st.number_input("Team B Average Goals Conceded (Away)", min_value=0.0, value=2.00)

    # Sidebar inputs
    st.sidebar.subheader("Odds Inputs")
    # Halftime odds inputs
    ht_home_odds = st.sidebar.number_input("HT Home Odds", min_value=0.0, value=4.10)
    ht_draw_odds = st.sidebar.number_input("HT Draw Odds", min_value=0.0, value=2.25)
    ht_away_odds = st.sidebar.number_input("HT Away Odds", min_value=0.0, value=2.70)
    
    # Full-time odds inputs
    ft_home_odds = st.sidebar.number_input("FT Home Odds", min_value=0.0, value=3.50)
    ft_draw_odds = st.sidebar.number_input("FT Draw Odds", min_value=0.0, value=3.70)
    ft_away_odds = st.sidebar.number_input("FT Away Odds", min_value=0.0, value=2.14)

    # User input: Over 2.5 Goals Odds
    over_2_5_odds = st.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.92)  # Example: 1.87
    
    # Generate all possible scorelines (for both HT and FT)
    max_goals = 5  # Define the maximum number of goals to consider for scorelines
    ht_scorelines = generate_scorelines(max_goals)
    ft_scorelines = generate_scorelines(max_goals)

    # Calculate Poisson probabilities for each scoreline
    team_a_ht_goal_rate = team_a_home_goals / 2  # Approximate halftime goals
    team_b_ht_goal_rate = team_b_away_goals / 2  # Approximate halftime goals
    team_a_ft_goal_rate = team_a_home_goals  # Full-time goal rate
    team_b_ft_goal_rate = team_b_away_goals  # Full-time goal rate

    # Slightly bias the home team's goal rate
    home_team_bias_factor = 1.1  # Slight bias towards home team (increase their goal rate)
    team_a_ht_goal_rate *= home_team_bias_factor
    team_a_ft_goal_rate *= home_team_bias_factor

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

    # Calculate adjusted probabilities for over 2.5 goals
    adjusted_ft_results = []
    for home, away, prob in ft_results:
        adjusted_prob = adjust_for_over_2_5_goals(over_2_5_odds, prob)
        adjusted_ft_results.append((home, away, prob, adjusted_prob))

    # Sort the results to find the most likely outcomes
    ht_results.sort(key=lambda x: x[2], reverse=True)  # Sort by Poisson probability
    ft_results.sort(key=lambda x: x[2], reverse=True)  # Sort by Poisson probability
    adjusted_ft_results.sort(key=lambda x: x[3], reverse=True)  # Sort by adjusted probability for over 2.5

    # Display top 5 most likely scorelines for HT and FT
    st.subheader("Most Likely Half-Time Scorelines (Top 5)")
    for i in range(min(5, len(ht_results))):
        st.write(f"HT {ht_results[i][0]}-{ht_results[i][1]} with Poisson Probability: {ht_results[i][2] * 100:.2f}%")

    st.subheader("Most Likely Full-Time Scorelines (Top 5) with Adjusted Over 2.5 Goals Probability")
    for i in range(min(5, len(adjusted_ft_results))):
        st.write(f"FT {adjusted_ft_results[i][0]}-{adjusted_ft_results[i][1]} with Poisson Probability: {adjusted_ft_results[i][2] * 100:.2f}%, Adjusted for Over 2.5: {adjusted_ft_results[i][3] * 100:.2f}%")

# Main app
st.title("Football Match Prediction using Poisson Distribution")

calculate_predictions()
