import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function to calculate Poisson probability
def poisson_prob(lmbda, k):
    return poisson.pmf(k, lmbda)

# Function to calculate odds implied probability
def implied_probability(odds):
    return 1 / odds

# Main function to calculate match probabilities
def calculate_match_probabilities(home_avg_goals, away_avg_goals, ht_odds, ft_odds, over_2_5_odds, under_2_5_odds):
    # Calculate halftime and full-time probabilities for 0-2 scores based on Poisson distribution
    home_lambda_ht = home_avg_goals / 2  # Halftime goals approximation
    away_lambda_ht = away_avg_goals / 2  # Halftime goals approximation
    
    home_lambda_ft = home_avg_goals     # Full-time goals approximation
    away_lambda_ft = away_avg_goals     # Full-time goals approximation
    
    # Poisson probabilities for 0 goals for Home and 2 goals for Away (Halftime and Full-time)
    prob_0_home_ht = poisson_prob(home_lambda_ht, 0)
    prob_2_away_ht = poisson_prob(away_lambda_ht, 2)

    prob_0_home_ft = poisson_prob(home_lambda_ft, 0)
    prob_2_away_ft = poisson_prob(away_lambda_ft, 2)
    
    # Implied probabilities for HT and FT odds
    implied_prob_ht_0_2 = implied_probability(ht_odds['0-2'])
    implied_prob_ft_1_2 = implied_probability(ft_odds['1-2'])
    
    # Over/Under 2.5 Goals Implied Probabilities
    implied_prob_over_2_5 = implied_probability(over_2_5_odds)
    implied_prob_under_2_5 = implied_probability(under_2_5_odds)
    
    # Combining the probabilities (HT and FT for Team B's Away Win with 1-2 and 0-2 halftime score)
    ht_probability = prob_0_home_ht * prob_2_away_ht  # HT result probability for 0-2
    ft_probability = prob_0_home_ft * prob_2_away_ft  # FT result probability for 1-2
    
    # Final probabilities combining HT, FT, and other odds
    final_ht_ft_probability = ht_probability * ft_probability
    final_over_2_5_probability = final_ht_ft_probability * implied_prob_over_2_5
    
    return final_ht_ft_probability, final_over_2_5_probability

# Streamlit App UI
def app():
    st.title("Football Match Prediction: Halftime and Full-time Correct Score")
    
    # Sidebar Inputs
    st.sidebar.header("Enter Match Statistics and Odds")
    
    home_avg_goals = st.sidebar.number_input("Avg Goals Scored by Home Team", value=1.50)
    away_avg_goals = st.sidebar.number_input("Avg Goals Scored by Away Team", value=1.30)
    
    ht_odds = {
        '0-2': st.sidebar.number_input("HT Odds for 0-2", value=26.08)
    }
    ft_odds = {
        '1-2': st.sidebar.number_input("FT Odds for 1-2", value=13.21)
    }
    
    over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", value=1.87)
    under_2_5_odds = st.sidebar.number_input("Under 2.5 Goals Odds", value=1.80)
    
    # Calculate probabilities
    ht_ft_probability, over_2_5_probability = calculate_match_probabilities(
        home_avg_goals, away_avg_goals, ht_odds, ft_odds, over_2_5_odds, under_2_5_odds
    )
    
    # Display Results
    st.header("Prediction Results")
    st.write(f"Probability of Halftime & Full-time Correct Score (0-2 HT, 1-2 FT): {ht_ft_probability*100:.2f}%")
    st.write(f"Probability of Over 2.5 Goals: {over_2_5_probability*100:.2f}%")
    
    st.write(f"Implied Probability from HT Odds (0-2): {implied_probability(ht_odds['0-2'])*100:.2f}%")
    st.write(f"Implied Probability from FT Odds (1-2): {implied_probability(ft_odds['1-2'])*100:.2f}%")
    st.write(f"Implied Probability for Over 2.5 Goals: {implied_probability(over_2_5_odds)*100:.2f}%")

# Add a submit button to the sidebar
with st.sidebar:
    st.markdown("### Submit Prediction")
    if st.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")


if __name__ == "__main__":
    app()
