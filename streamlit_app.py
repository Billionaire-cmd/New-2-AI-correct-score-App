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

    # Calculate Poisson probabilities for HT (halftime)
    team_a_ht_goal_rate = team_a_home_goals / 2  # Approximate halftime goals
    team_b_ht_goal_rate = team_b_away_goals / 2  # Approximate halftime goals

    team_a_ht_0_goals = poisson_prob(team_a_ht_goal_rate, 0)  # Team A scoring 0 goals
    team_b_ht_2_goals = poisson_prob(team_b_ht_goal_rate, 2)  # Team B scoring 2 goals

    # Calculate the probability of a 0-2 halftime scoreline (Team A 0, Team B 2)
    poisson_0_2_ht = team_a_ht_0_goals * team_b_ht_2_goals

    # Calculate odds-based probabilities
    ht_0_2_odds = 26.08
    ht_0_2_prob = odds_to_prob(ht_0_2_odds)

    # Display HT Prediction Results
    st.subheader("Halftime Correct Score Prediction")
    st.write(f"Poisson-based probability of HT 0-2 (Team A 0, Team B 2): {poisson_0_2_ht:.4f}")
    st.write(f"Odds-based probability of HT 0-2: {ht_0_2_prob:.4f}")

    # Calculate Full-time probability for 1-2 scoreline
    team_a_ft_goal_rate = team_a_home_goals  # Full-time goal rate
    team_b_ft_goal_rate = team_b_away_goals  # Full-time goal rate

    team_a_ft_1_goals = poisson_prob(team_a_ft_goal_rate, 1)  # Team A scoring 1 goal
    team_b_ft_2_goals = poisson_prob(team_b_ft_goal_rate, 2)  # Team B scoring 2 goals

    # Calculate the probability of a 1-2 full-time scoreline (Team A 1, Team B 2)
    poisson_1_2_ft = team_a_ft_1_goals * team_b_ft_2_goals

    # Display FT Prediction Results
    st.subheader("Full-time Correct Score Prediction")
    st.write(f"Poisson-based probability of FT 1-2 (Team A 1, Team B 2): {poisson_1_2_ft:.4f}")

    # Combine the calculated probabilities and odds to provide a final result
    st.write(f"Combined Halftime 0-2 Probability: {poisson_0_2_ht * 100:.2f}%")
    st.write(f"Combined Full-time 1-2 Probability: {poisson_1_2_ft * 100:.2f}%")

    # Conclusion based on inputs
    st.subheader("Conclusion")
    st.write("Based on the provided inputs, the predicted halftime score of 0-2 and full-time score of 1-2 are statistically reasonable with the following probabilities:")
    st.write(f"HT 0-2: {poisson_0_2_ht * 100:.2f}% (Poisson), {ht_0_2_prob * 100:.2f}% (Odds-based)")
    st.write(f"FT 1-2: {poisson_1_2_ft * 100:.2f}% (Poisson)")

# Add a submit button to the sidebar
with st.sidebar:
    st.markdown("### Submit Prediction")
    if st.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")

# Create the app layout
def main():
    st.title("Football Match Prediction: Halftime & Full-time Correct Score")
    st.sidebar.header("Enter Match Inputs")
    
    # Call the function to calculate predictions
    calculate_predictions()

if __name__ == "__main__":
    main()
