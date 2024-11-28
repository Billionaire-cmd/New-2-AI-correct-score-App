# Streamlit app with modified final recommendation

import streamlit as st
import numpy as np
from scipy.stats import poisson

# Define the function to calculate Poisson probabilities
def poisson_prob(lambda_rate, k):
    return poisson.pmf(k, lambda_rate)

# Function to calculate and display predictions
def calculate_predictions():
    st.title("Football Scoreline Prediction")

    # User input: Team A and Team B stats
    team_a_home_goals = st.number_input("Team A Average Goals Scored (Home)", min_value=0.0, value=1.30)
    team_b_away_goals = st.number_input("Team B Average Goals Scored (Away)", min_value=0.0, value=1.00)
    team_a_home_conceded = st.number_input("Team A Average Goals Conceded (Home)", min_value=0.0, value=1.20)
    team_b_away_conceded = st.number_input("Team B Average Goals Conceded (Away)", min_value=0.0, value=1.50)

    # Calculate Poisson goal rates for Team A and Team B
    team_a_ft_goal_rate = team_a_home_goals  # Full-time goal rate
    team_b_ft_goal_rate = team_b_away_goals  # Full-time goal rate

    # Calculate Poisson probabilities for FT: 1-0
    ft_1_0_prob = (
        poisson_prob(team_a_ft_goal_rate, 1) * poisson_prob(team_b_ft_goal_rate, 0)
    )

    # Calculate most likely halftime scoreline
    team_a_ht_goal_rate = team_a_ft_goal_rate / 2  # Approximate halftime goal rate
    team_b_ht_goal_rate = team_b_ft_goal_rate / 2  # Approximate halftime goal rate
    ht_0_0_prob = (
        poisson_prob(team_a_ht_goal_rate, 0) * poisson_prob(team_b_ht_goal_rate, 0)
    )

    # Display results
    st.subheader("Final Recommendations")
    st.write(
        f"The most likely halftime scoreline based on Poisson distribution is: **HT 0-0** with a probability of {ht_0_0_prob * 100:.2f}%"
    )
    st.write(
        f"The most likely full-time scoreline based on Poisson distribution is: **FT 1-0** with a probability of {ft_1_0_prob * 100:.2f}%"
    )

# Run the app
if __name__ == "__main__":
    calculate_predictions()
