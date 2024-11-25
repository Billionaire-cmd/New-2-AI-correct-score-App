import streamlit as st
import numpy as np
from scipy.stats import poisson

# App Title and Introduction
st.title("🤖 Rabiotic Advanced HT/FT Correct Score Predictor")
st.markdown("""
Welcome to the **Rabiotic Advanced Halftime/Full-time Correct Score Predictor**!  
This app uses advanced statistical models, including the Poisson distribution, betting odds, and team statistics, 
to predict realistic halftime and full-time correct scores for football matches.
""")

# Sidebar for Inputs
st.sidebar.header("Match Statistics and Inputs")

# Average Goals Scored
avg_goals_home = st.sidebar.number_input("Average Goals Scored by Home Team", min_value=0.0, step=0.1, value=1.5)
avg_goals_away = st.sidebar.number_input("Average Goals Scored by Away Team", min_value=0.0, step=0.1, value=1.2)

# Betting Odds
st.sidebar.subheader("Halftime Odds")
ht_home = st.sidebar.number_input("Halftime Home Odds", min_value=1.0, step=0.1, value=2.5)
ht_draw = st.sidebar.number_input("Halftime Draw Odds", min_value=1.0, step=0.1, value=2.9)
ht_away = st.sidebar.number_input("Halftime Away Odds", min_value=1.0, step=0.1, value=3.1)

st.sidebar.subheader("Fulltime Odds")
ft_home = st.sidebar.number_input("Fulltime Home Odds", min_value=1.0, step=0.1, value=2.2)
ft_draw = st.sidebar.number_input("Fulltime Draw Odds", min_value=1.0, step=0.1, value=3.2)
ft_away = st.sidebar.number_input("Fulltime Away Odds", min_value=1.0, step=0.1, value=3.4)

# BTTS and Over/Under Odds
st.sidebar.subheader("BTTS GG/NG Odds")
btts_gg = st.sidebar.number_input("BTTS (Yes) Odds", min_value=1.0, step=0.1, value=1.8)
btts_ng = st.sidebar.number_input("BTTS (No) Odds", min_value=1.0, step=0.1, value=1.9)

st.sidebar.subheader("Over/Under Odds (Halftime)")
over_1_5_ht = st.sidebar.number_input("Over 1.5 HT Odds", min_value=1.0, step=0.1, value=2.5)
under_1_5_ht = st.sidebar.number_input("Under 1.5 HT Odds", min_value=1.0, step=0.1, value=1.6)

st.sidebar.subheader("Over/Under Odds (Fulltime)")
over_1_5_ft = st.sidebar.number_input("Over 1.5 FT Odds", min_value=1.0, step=0.1, value=1.4)
under_1_5_ft = st.sidebar.number_input("Under 1.5 FT Odds", min_value=1.0, step=0.1, value=2.9)
over_2_5_ft = st.sidebar.number_input("Over 2.5 FT Odds", min_value=1.0, step=0.1, value=2.0)
under_2_5_ft = st.sidebar.number_input("Under 2.5 FT Odds", min_value=1.0, step=0.1, value=1.8)

# Correct Score Odds
st.sidebar.subheader("Correct Score Odds (HT and FT)")
correct_score_odds = {}
for score in ["0:0", "1:0", "0:1", "1:1", "2:0", "2:1", "2:2", "3:0", "3:1", "3:2", "3:3", "4:0", "4:1", "4:2", "4:3", "4:4"]:
    correct_score_odds[score] = st.sidebar.number_input(f"Odds for {score}", value=10.0, step=0.01)

# Function to Calculate Probabilities
def calculate_poisson_prob(lambda_, max_goals):
    """Calculate Poisson probabilities."""
    return [poisson.pmf(i, lambda_) for i in range(max_goals + 1)]

# Predict Probabilities and Correct Scores
if st.button("Predict Correct Scores"):
    try:
        # Calculate Poisson Probabilities for Home and Away Teams
        home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
        away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)

        # Calculate Match Probabilities
        score_matrix = np.outer(home_probs, away_probs)

        # Extract Probabilities for Specific Scores
        score_probs = {}
        for i in range(5):
            for j in range(5):
                score_probs[f"{i}:{j}"] = score_matrix[i, j]

        # Sort Scores by Probability
        sorted_scores = sorted(score_probs.items(), key=lambda x: x[1], reverse=True)

        # Display Results
        st.header("Correct Score Predictions")
        st.write("### Top 5 Likely Scores (with Probabilities):")
        for score, prob in sorted_scores[:5]:
            st.write(f"**{score}:** {prob * 100:.2f}%")

        # Recommendations
        st.subheader("Recommendations")
        ht_recommend = max(sorted_scores, key=lambda x: x[1] if int(x[0].split(":")[0]) <= 2 else 0)
        ft_recommend = max(sorted_scores, key=lambda x: x[1])
        st.write(f"**Recommended Halftime Score:** {ht_recommend[0]} ({ht_recommend[1] * 100:.2f}%)")
        st.write(f"**Recommended Fulltime Score:** {ft_recommend[0]} ({ft_recommend[1] * 100:.2f}%)")

    except Exception as e:
        st.error(f"Error in calculation: {e}")
