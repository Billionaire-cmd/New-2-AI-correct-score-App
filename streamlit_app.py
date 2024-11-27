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
    team_a_home_conceded = st.number_input("Team A Average Goals Conceded (Home)", min_value=0.0, value=1.30)
    team_b_away_conceded = st.number_input("Team B Average Goals Conceded (Away)", min_value=0.0, value=1.50)

    # User input: HT Odds for outcomes
    ht_odds_0_0 = st.number_input("HT Odds for 0:0", min_value=0.0, value=2.58)
    ht_odds_0_1 = st.number_input("HT Odds for 0:1", min_value=0.0, value=5.84)
    ht_odds_0_2 = st.number_input("HT Odds for 0:2", min_value=0.0, value=26.08)
    ht_odds_1_0 = st.number_input("HT Odds for 1:0", min_value=0.0, value=3.63)
    ht_odds_1_1 = st.number_input("HT Odds for 1:1", min_value=0.0, value=8.07)
    ht_odds_1_2 = st.number_input("HT Odds for 1:2", min_value=0.0, value=36.39)
    ht_odds_2_0 = st.number_input("HT Odds for 2:0", min_value=0.0, value=9.73)
    ht_odds_2_1 = st.number_input("HT Odds for 2:1", min_value=0.0, value=22.15)
    ht_odds_2_2 = st.number_input("HT Odds for 2:2", min_value=0.0, value=100.00)
    ht_odds_other = st.number_input("HT Odds for Other Scores", min_value=0.0, value=100.00)
    
    # User input: FT Odds for outcomes
    ft_odds_0_0 = st.number_input("FT Odds for 0:0", min_value=0.0, value=10.41)
    ft_odds_0_1 = st.number_input("FT Odds for 0:1", min_value=0.0, value=10.74)
    ft_odds_0_2 = st.number_input("FT Odds for 0:2", min_value=0.0, value=20.77)
    ft_odds_0_3 = st.number_input("FT Odds for 0:3", min_value=0.0, value=60.40)
    ft_odds_1_0 = st.number_input("FT Odds for 1:0", min_value=0.0, value=7.03)
    ft_odds_1_1 = st.number_input("FT Odds for 1:1", min_value=0.0, value=6.51)
    ft_odds_2_0 = st.number_input("FT Odds for 2:0", min_value=0.0, value=8.83)
    ft_odds_2_1 = st.number_input("FT Odds for 2:1", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 3:1", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 4:1", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 1:2", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 1:3", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 1:4", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 2:2", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 2:3", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 2:4", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 3:3", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 3:4", min_value=0.0, value=8.63)
    ft_odds_2_1 = st.number_input("FT Odds for 4:4", min_value=0.0, value=8.64)
    ft_odds_other = st.number_input("FT Odds for Other Scores", min_value=0.0, value=31.65)  # Other FT odds

    # User input: Over 2.5 Goals Odds
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

    # Final recommendation for the highest probability HT and FT scoreline
    highest_ht_prob = max(ht_results, key=lambda x: x[2])  # HT scoreline with the highest probability
    highest_ft_prob = max(ft_results, key=lambda x: x[2])  # FT scoreline with the highest probability

    # Display HT and FT predictions
    st.subheader("Halftime Correct Score Predictions")
    for home_goals, away_goals, prob in ht_results:
        adjusted_prob = adjust_for_over_2_5_goals(over_2_5_odds, prob)
        implied_ht_prob = implied_prob(ht_odds_0_0)  # For example, use HT odds for 0:0
        st.write(f"HT {home_goals}-{away_goals}: Poisson Probability: {prob*100:.2f}%, Adjusted for Over 2.5: {adjusted_prob*100:.2f}%")

    st.subheader("Full-time Correct Score Predictions")
    for home_goals, away_goals, prob in ft_results:
        adjusted_prob = adjust_for_over_2_5_goals(over_2_5_odds, prob)
        implied_ft_prob = implied_prob(ft_odds_0_0)  # For example, use FT odds for 0:0
        st.write(f"FT {home_goals}-{away_goals}: Poisson Probability: {prob*100:.2f}%, Adjusted for Over 2.5: {adjusted_prob*100:.2f}%")

    # Final recommendation output
    st.subheader("Final Recommendations")
    st.write(f"The most likely halftime scoreline based on Poisson distribution is: HT {highest_ht_prob[0]}-{highest_ht_prob[1]} with a probability of {highest_ht_prob[2]*100:.2f}%")
    st.write(f"The most likely full-time scoreline based on Poisson distribution is: FT {highest_ft_prob[0]}-{highest_ft_prob[1]} with a probability of {highest_ft_prob[2]*100:.2f}%")

# Create the app layout
def main():
    st.title("Football Match Prediction: All Halftime & Full-time Correct Scorelines")
    st.sidebar.header("Enter Match Inputs")
    calculate_predictions()

if __name__ == "__main__":
    main()
