import streamlit as st
import numpy as np
from scipy.stats import poisson

# Define the function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to adjust for home advantage
def adjust_for_home_advantage(prob, home_advantage_factor):
    return prob * home_advantage_factor

# Function to generate all possible scorelines for both HT and FT
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

    # Sidebar inputs for odds
    st.sidebar.subheader("Odds Inputs")
    # Full-time odds inputs
    ft_home_odds = st.sidebar.number_input("FT Home Odds", min_value=0.0, value=3.50)
    ft_draw_odds = st.sidebar.number_input("FT Draw Odds", min_value=0.0, value=3.70)
    ft_away_odds = st.sidebar.number_input("FT Away Odds", min_value=0.0, value=2.14)

    # User input: Over 2.5 Goals Odds
    over_2_5_odds = st.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.92)

    # Generate all possible scorelines for HT and FT
    max_goals = 5
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

    # Adjustment for home advantage
    home_advantage_factor = 1.1  # Example factor for home advantage, can be adjusted

    # Apply home advantage adjustment
    adjusted_ft_results = [(home, away, adjust_for_home_advantage(prob, home_advantage_factor)) for home, away, prob in ft_results]
    adjusted_ht_results = [(home, away, adjust_for_home_advantage(prob, home_advantage_factor)) for home, away, prob in ht_results]

    # Find the most likely FT and HT scorelines based on the adjusted probabilities
    most_likely_ft = max(adjusted_ft_results, key=lambda x: x[2])
    most_likely_ht = max(adjusted_ht_results, key=lambda x: x[2])

    # Adjust for over 2.5 goals probability for FT
    ft_1_0_prob = next((prob for home, away, prob in adjusted_ft_results if home == 1 and away == 0), 0)
    adjusted_ft_1_0_prob = adjust_for_home_advantage(ft_1_0_prob, home_advantage_factor)

    # Display results for multiple outcomes
    st.subheader(f"Most Likely Full-Time Scoreline: {most_likely_ft[0]}-{most_likely_ft[1]} with Poisson Probability: {most_likely_ft[2] * 100:.2f}%, Adjusted for Home Advantage: {adjusted_ft_1_0_prob * 100:.2f}%")
    st.subheader(f"Most Likely Half-Time Scoreline: {most_likely_ht[0]}-{most_likely_ht[1]} with Poisson Probability: {most_likely_ht[2] * 100:.2f}%")

# Main app
st.title("Football Match Prediction using Poisson Distribution")

calculate_predictions()
