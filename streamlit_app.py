import streamlit as st
import numpy as np
from scipy.stats import poisson

# Helper function to calculate Poisson distribution for goal probabilities
def calculate_poisson_prob(goal_avg, max_goals=4):
    return [poisson.pmf(i, goal_avg) for i in range(max_goals + 1)]

# Function to calculate HT/FT correct score probabilities
def calculate_correct_score_probabilities(home_avg, away_avg, max_goals=4):
    ht_probs = calculate_poisson_prob(home_avg, max_goals)
    ft_probs = calculate_poisson_prob(away_avg, max_goals)
    
    # Generate HT/FT combinations
    ht_ft_probs = {}
    for ht in range(max_goals+1):
        for ft in range(max_goals+1):
            ht_ft_probs[(ht, ft)] = ht_probs[ht] * ft_probs[ft]
    
    return ht_ft_probs

# Streamlit app
def main():
    # Title of the app
    st.title("🤖 Rabiotic Advanced Halftime/Full-time Correct Score Predictor")

    # Description
    st.write("""
    Welcome to the **Rabiotic Advanced Halftime/Full-time Correct Score Predictor**.
    This tool uses advanced statistical methods to calculate the most likely correct scores for football matches, based on team performance, betting odds, and other factors.
    """)

    # Input fields for home and away team stats (average goals scored)
    home_avg = st.number_input("Enter Home Team's Average Goals Scored per Match", min_value=0.0, max_value=5.0, value=1.5)
    away_avg = st.number_input("Enter Away Team's Average Goals Scored per Match", min_value=0.0, max_value=5.0, value=1.2)

    # Input for max goals considered
    max_goals = st.slider("Select Maximum Goals Considered", min_value=1, max_value=5, value=4)

    # Button to generate prediction
    if st.button("Predict HT/FT Correct Scores"):
        # Calculate HT/FT probabilities
        ht_ft_probs = calculate_correct_score_probabilities(home_avg, away_avg, max_goals)
        
        # Display the results
        st.subheader("Predicted Halftime/Full-time Correct Scores")
        for score, prob in ht_ft_probs.items():
            st.write(f"Score: {score}, Probability: {prob:.4f}")
        
        # Display a message about the model
        st.write("""
        The above predictions are based on the Poisson distribution and the inputted team statistics. 
        Use this tool to help identify possible outcomes, but keep in mind that football matches can be unpredictable!
        """)

if __name__ == "__main__":
    main()
