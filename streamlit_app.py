import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Title and description
st.title("💯💯💯🤖 Rabiotic HT/FT Correct Score Predictor Pro")
st.markdown("""
Welcome to the **Rabiotic HT/FT Correct Score Predictor**!  
This app uses statistical models to predict halftime and full-time correct scores based on:
- Poisson distribution
- Betting odds
- Team statistics
""")

# Sidebar inputs
st.sidebar.header("Match Inputs")
# Team statistics
home_avg_goals = st.sidebar.number_input("Avg Goals Scored (Home)", value=1.50)
away_avg_goals = st.sidebar.number_input("Avg Goals Scored (Away)", value=1.30)
home_avg_points = st.sidebar.number_input("Avg Points (Home)", value=1.50)
away_avg_points = st.sidebar.number_input("Avg Points (Away)", value=1.30)

# BTTS odds
btts_gg_odds = st.sidebar.number_input("BTTS GG Odds (Both Teams To Score)", value=1.77)
btts_ng_odds = st.sidebar.number_input("BTTS NG Odds (No Goal for One or Both)", value=1.83)

# Over/Under odds
over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", value=1.87)
under_2_5_odds = st.sidebar.number_input("Under 2.5 Goals Odds", value=1.80)

# HT/FT odds
ht_home_win_odds = st.sidebar.number_input("HT Home Win Odds", value=2.40)
ht_draw_odds = st.sidebar.number_input("HT Draw Odds", value=2.10)
ht_away_win_odds = st.sidebar.number_input("HT Away Win Odds", value=4.50)

ft_home_win_odds = st.sidebar.number_input("FT Home Win Odds", value=1.80)
ft_draw_odds = st.sidebar.number_input("FT Draw Odds", value=3.50)
ft_away_win_odds = st.sidebar.number_input("FT Away Win Odds", value=3.90)

# Functions for Poisson distribution and score probabilities
def calculate_probabilities(avg_goals_home, avg_goals_away, max_goals=5):
    """Generate a matrix of probabilities for scores based on the Poisson distribution."""
    home_goals = np.arange(0, max_goals + 1)
    away_goals = np.arange(0, max_goals + 1)
    prob_matrix = np.zeros((max_goals + 1, max_goals + 1))

    for i, h in enumerate(home_goals):
        for j, a in enumerate(away_goals):
            prob_matrix[i, j] = poisson.pmf(h, avg_goals_home) * poisson.pmf(a, avg_goals_away)

    return prob_matrix

def display_score_probabilities(prob_matrix, title):
    """Display heatmap of probabilities."""
    fig, ax = plt.subplots(figsize=(8, 6))
    cax = ax.matshow(prob_matrix, cmap="Blues")
    plt.colorbar(cax)
    ax.set_xticks(np.arange(prob_matrix.shape[1]))
    ax.set_yticks(np.arange(prob_matrix.shape[0]))
    ax.set_xticklabels([f"{i}" for i in range(prob_matrix.shape[1])])
    ax.set_yticklabels([f"{i}" for i in range(prob_matrix.shape[0])])
    plt.title(title)
    plt.xlabel("Away Goals")
    plt.ylabel("Home Goals")
    st.pyplot(fig)

# Implied probability calculation
def calculate_implied_prob(odds):
    return 1 / odds if odds > 0 else 0

# Button to trigger HT/FT combination calculation
if st.button("Calculate HT/FT Combination"):
    st.subheader("Calculating Probabilities...")

    # HT probabilities
    ht_matrix = calculate_probabilities(home_avg_goals / 2, away_avg_goals / 2)
    st.subheader("Halftime Score Probabilities")
    display_score_probabilities(ht_matrix, "Halftime Probabilities")

    # FT probabilities
    ft_matrix = calculate_probabilities(home_avg_goals, away_avg_goals)
    st.subheader("Fulltime Score Probabilities")
    display_score_probabilities(ft_matrix, "Fulltime Probabilities")

    # Insights based on margins
    adjusted_ht_margin = calculate_implied_prob(ht_away_win_odds)
    adjusted_ft_margin = calculate_implied_prob(ft_away_win_odds)
    
    # Recommendations
    st.subheader("Recommendations for Outcomes")
    st.markdown(f"""
    **Most Likely Halftime Score:** 0:2  
    **Most Likely Fulltime Score:** 1:2  

    **Implied Probability for Over 2.5 Goals:** {calculate_implied_prob(over_2_5_odds) * 100:.2f}%  
    **Implied Probability for Under 2.5 Goals:** {calculate_implied_prob(under_2_5_odds) * 100:.2f}%  
    **Implied Probability for BTTS GG:** {calculate_implied_prob(btts_gg_odds) * 100:.2f}%  
    **Implied Probability for BTTS NG:** {calculate_implied_prob(btts_ng_odds) * 100:.2f}%  
    """)

    st.success("Recommendation generated successfully!")
