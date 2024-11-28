import streamlit as st
import numpy as np
from scipy.stats import poisson

# Define the function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate the implied probability from odds
def implied_prob(odds):
    return 1 / odds * 100

# Function to adjust for bias towards home team scoring
def adjust_for_home_advantage(lambda_home, lambda_away, home_biased_goals=1):
    # Bias the home team's goal count to force the system to favor home team scoring 1 goal
    home_goals_prob = poisson_prob(lambda_home, home_biased_goals)
    away_goals_prob = poisson_prob(lambda_away, 0)  # Away team scoring 0 goals
    return home_goals_prob * away_goals_prob

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

    # Bias FT: 1-0 and HT: 0-0
    biased_ft_prob = adjust_for_home_advantage(team_a_ft_goal_rate, team_b_ft_goal_rate, home_biased_goals=1)
    biased_ht_prob = adjust_for_home_advantage(team_a_ht_goal_rate, team_b_ht_goal_rate, home_biased_goals=1)

    # Display results
    st.subheader(f"Most Likely Full-Time Scoreline (Biased): FT 1-0 with Adjusted Poisson Probability: {biased_ft_prob * 100:.2f}%")
    st.subheader(f"Most Likely Half-Time Scoreline (Biased): HT 0-0 with Adjusted Poisson Probability: {biased_ht_prob * 100:.2f}%")
    
    # Display top 3 scorelines based on Poisson probabilities
    top_ft_results = sorted(ft_results, key=lambda x: x[2], reverse=True)[:3]
    top_ht_results = sorted(ht_results, key=lambda x: x[2], reverse=True)[:3]

    st.write("Top 3 Full-Time Scoreline Predictions:")
    for home_goals, away_goals, prob in top_ft_results:
        st.write(f"FT {home_goals}-{away_goals}: Probability: {prob * 100:.2f}%")

    st.write("Top 3 Half-Time Scoreline Predictions:")
    for home_goals, away_goals, prob in top_ht_results:
        st.write(f"HT {home_goals}-{away_goals}: Probability: {prob * 100:.2f}%")

# Main app
st.title("Football Match Prediction with Poisson Distribution and Home Advantage")

calculate_predictions()
