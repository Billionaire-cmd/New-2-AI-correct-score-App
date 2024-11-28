import streamlit as st
import numpy as np
from scipy.stats import poisson

# Define the function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to adjust for over 2.5 goals odds
def adjust_for_over_2_5_goals(over_2_5_odds, poisson_prob):
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

# Function to apply a bias to specific scorelines
def apply_bias(scoreline, poisson_probs, bias_scoreline, bias_factor=1.5):
    """
    Apply a bias in favor of a specific scoreline (like FT 1-0) 
    by increasing its probability.
    """
    for idx, (home_goals, away_goals, prob) in enumerate(poisson_probs):
        if (home_goals == bias_scoreline[0] and away_goals == bias_scoreline[1]):
            poisson_probs[idx] = (home_goals, away_goals, prob * bias_factor)  # Increase bias
    return poisson_probs

# Main function to calculate and display predictions
def calculate_predictions():
    # User input: Team A and Team B stats
    team_a_home_goals = st.number_input("Team A Average Goals Scored (Home)", min_value=0.0, value=0.30)
    team_b_away_goals = st.number_input("Team B Average Goals Scored (Away)", min_value=0.0, value=1.00)
    team_a_home_conceded = st.number_input("Team A Average Goals Conceded (Home)", min_value=0.0, value=1.50)
    team_b_away_conceded = st.number_input("Team B Average Goals Conceded (Away)", min_value=0.0, value=2.00)

    # Sidebar inputs
    st.sidebar.subheader("Odds Inputs")
    over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.92)  # Example: 1.87

    # Generate all possible scorelines (for both HT and FT)
    max_goals = 5  # Define the maximum number of goals to consider for scorelines
    ht_scorelines = generate_scorelines(max_goals)
    ft_scorelines = generate_scorelines(max_goals)

    # Calculate Poisson probabilities for HT scorelines
    team_a_ht_goal_rate = team_a_home_goals / 2  # Approximate halftime goals
    team_b_ht_goal_rate = team_b_away_goals / 2  # Approximate halftime goals
    ht_results = []

    for home_goals, away_goals in ht_scorelines:
        ht_prob = poisson_prob(team_a_ht_goal_rate, home_goals) * poisson_prob(team_b_ht_goal_rate, away_goals)
        ht_results.append((home_goals, away_goals, ht_prob))

    # Calculate Poisson probabilities for FT scorelines
    team_a_ft_goal_rate = team_a_home_goals  # Full-time goal rate
    team_b_ft_goal_rate = team_b_away_goals  # Full-time goal rate
    ft_results = []

    for home_goals, away_goals in ft_scorelines:
        ft_prob = poisson_prob(team_a_ft_goal_rate, home_goals) * poisson_prob(team_b_ft_goal_rate, away_goals)
        ft_results.append((home_goals, away_goals, ft_prob))

    # Apply bias for certain scorelines (e.g., FT 1-0)
    biased_ft_results = apply_bias(ft_scorelines, ft_results, bias_scoreline=(1, 0), bias_factor=1.5)

    # Adjust for over 2.5 goals
    adjusted_ft_results = [
        (home_goals, away_goals, adjust_for_over_2_5_goals(over_2_5_odds, prob))
        for home_goals, away_goals, prob in biased_ft_results
    ]

    # Find the most likely HT and FT scorelines
    highest_ht_prob = max(ht_results, key=lambda x: x[2])
    highest_ft_prob = max(adjusted_ft_results, key=lambda x: x[2])

    # Display results
    st.subheader(f"Most Likely Full-Time Scoreline: {highest_ft_prob[0]}-{highest_ft_prob[1]} with Poisson Probability: {highest_ft_prob[2] * 100:.2f}%, Adjusted for Over 2.5: {highest_ft_prob[2] * 100:.2f}%")
    st.subheader(f"Most Likely Half-Time Scoreline: {highest_ht_prob[0]}-{highest_ht_prob[1]} with Poisson Probability: {highest_ht_prob[2] * 100:.2f}%")

# Main app
st.title("Football Match Prediction using Poisson Distribution")

calculate_predictions()
