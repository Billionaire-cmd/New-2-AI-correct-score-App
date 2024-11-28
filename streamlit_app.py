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

    # User input: HT Odds for outcomes
    ht_odds_0_0 = st.number_input("HT Odds for 0:0", min_value=0.0, value=2.80)
    ht_odds_0_1 = st.number_input("HT Odds for 0:1", min_value=0.0, value=4.10)
    ht_odds_0_2 = st.number_input("HT Odds for 0:2", min_value=0.0, value=11.50)
    ht_odds_1_0 = st.number_input("HT Odds for 1:0", min_value=0.0, value=5.60)
    ht_odds_1_1 = st.number_input("HT Odds for 1:1", min_value=0.0, value=8.00)
    ht_odds_1_2 = st.number_input("HT Odds for 1:2", min_value=0.0, value=23.00)
    ht_odds_2_0 = st.number_input("HT Odds for 2:0", min_value=0.0, value=22.00)
    ht_odds_2_1 = st.number_input("HT Odds for 2:1", min_value=0.0, value=32.00)
    ht_odds_2_2 = st.number_input("HT Odds for 2:2", min_value=0.0, value=91.00)
    ht_odds_other = st.number_input("HT Odds for Other Scores", min_value=0.0, value=17.50) 
    
    # User input: FT Odds for outcomes
    ft_odds_0_0 = st.number_input("FT Odds for 0:0", min_value=0.0, value=12.00)
    ft_odds_0_1 = st.number_input("FT Odds for 0:1", min_value=0.0, value=7.80)
    ft_odds_0_2 = st.number_input("FT Odds for 0:2", min_value=0.0, value=9.80)
    ft_odds_0_3 = st.number_input("FT Odds for 0:3", min_value=0.0, value=18.50)
    ft_odds_1_0 = st.number_input("FT Odds for 1:0", min_value=0.0, value=11.00)
    ft_odds_1_1 = st.number_input("FT Odds for 1:1", min_value=0.0, value=6.70)
    ft_odds_2_0 = st.number_input("FT Odds for 2:0", min_value=0.0, value=19.00)
    ft_odds_2_1 = st.number_input("FT Odds for 2:1", min_value=0.0, value=12.00)
    ft_odds_3_0 = st.number_input("FT Odds for 3:0", min_value=0.0, value=50.00)
    ft_odds_1_2 = st.number_input("FT Odds for 1:2", min_value=0.0, value=8.70)
    ft_odds_2_2 = st.number_input("FT Odds for 2:2", min_value=0.0, value=14.50)
    ft_odds_other = st.number_input("FT Odds for Other Scores", min_value=0.0, value=27.00)  # Other FT odds

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

    # Highlight the most likely scorelines for HT and FT and adjust for over 2.5 goals
    highest_ht_prob = max(ht_results, key=lambda x: x[2])
    highest_ft_prob = max(ft_results, key=lambda x: x[2])

    # Adjust the probabilities for over 2.5 goals
    adjusted_ft_prob = adjust_for_over_2_5_goals(over_2_5_odds, highest_ft_prob[2])
    adjusted_ht_prob = adjust_for_over_2_5_goals(over_2_5_odds, highest_ht_prob[2])

    # Output the most likely scorelines and probabilities
    st.subheader(f"Most Likely Full-Time Scoreline: {highest_ft_prob[0]}-{highest_ft_prob[1]} with Poisson Probability: {highest_ft_prob[2] * 100:.2f}%")
    st.subheader(f"Adjusted for Over 2.5: {adjusted_ft_prob * 100:.2f}%")

    st.subheader(f"Most Likely Half-Time Scoreline: {highest_ht_prob[0]}-{highest_ht_prob[1]} with Poisson Probability: {highest_ht_prob[2] * 100:.2f}%")
    st.subheader(f"Adjusted for Over 2.5: {adjusted_ht_prob * 100:.2f}%")

# Main app
st.title("Football Match Prediction using Poisson Distribution")

calculate_predictions()
