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
    team_a_home_goals = st.number_input("Team A Average Goals Scored (Home)", min_value=0.0, value=1.50)
    team_b_away_goals = st.number_input("Team B Average Goals Scored (Away)", min_value=0.0, value=1.30)

    # User input: HT and FT Odds for outcomes
    over_2_5_odds = st.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.87)  # Example: 1.87

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

    # Adjust probabilities for over 2.5 goals
    adjusted_ht_results = []
    adjusted_ft_results = []

    for home_goals, away_goals, prob in ht_results:
        adjusted_prob = adjust_for_over_2_5_goals(over_2_5_odds, prob)
        adjusted_ht_results.append((home_goals, away_goals, adjusted_prob))

    for home_goals, away_goals, prob in ft_results:
        adjusted_prob = adjust_for_over_2_5_goals(over_2_5_odds, prob)
        adjusted_ft_results.append((home_goals, away_goals, adjusted_prob))

    # Display results
    st.subheader("Halftime Correct Score Predictions")
    for home_goals, away_goals, prob in adjusted_ht_results:
        st.write(f"HT {home_goals}-{away_goals}: Adjusted Poisson Probability: {prob:.4f}")

    st.subheader("Full-time Correct Score Predictions")
    for home_goals, away_goals, prob in adjusted_ft_results:
        st.write(f"FT {home_goals}-{away_goals}: Adjusted Poisson Probability: {prob:.4f}")

    # Final recommendation output
    highest_ht_prob = max(adjusted_ht_results, key=lambda x: x[2])
    highest_ft_prob = max(adjusted_ft_results, key=lambda x: x[2])

    st.subheader("Final Recommendations")
    st.write(f"The most likely halftime scoreline based on Poisson distribution is: HT {highest_ht_prob[0]}-{highest_ht_prob[1]} with a probability of {highest_ht_prob[2]:.4f}")
    st.write(f"The most likely full-time scoreline based on Poisson distribution is: FT {highest_ft_prob[0]}-{highest_ft_prob[1]} with a probability of {highest_ft_prob[2]:.4f}")

# Create the app layout
def main():
    st.title("Football Match Prediction: All Halftime & Full-time Correct Scorelines")
    st.sidebar.header("Enter Match Inputs")
    calculate_predictions()

if __name__ == "__main__":
    main()
