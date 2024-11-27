import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Page configuration
st.set_page_config(page_title="💯💯💯🤖Rabiotic HT/FT Correct Score Predictor", layout="centered")
st.markdown("""
# 💯💯💯🤖Rabiotic HT/FT Correct Score Predictor

Welcome to the **Rabiotic HT/FT Correct Score Predictor**!  
This app uses statistical models to predict halftime and full-time correct scores based on:
- Poisson distribution
- Betting odds
- Team statistics
""")

# Sidebar for Match Inputs
st.sidebar.title("Match Inputs")
avg_goals_home = st.sidebar.number_input("Avg Goals Scored (Home)", value=1.50)
avg_goals_away = st.sidebar.number_input("Avg Goals Scored (Away)", value=1.30)
avg_points_home = st.sidebar.number_input("Avg Points (Home)", value=1.50)
avg_points_away = st.sidebar.number_input("Avg Points (Away)", value=1.30)

btts_gg_odds = st.sidebar.number_input("BTTS GG Odds", value=1.77)
btts_ng_odds = st.sidebar.number_input("BTTS NG Odds", value=1.83)
over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", value=1.87)
under_2_5_odds = st.sidebar.number_input("Under 2.5 Goals Odds", value=1.80)

# Define Poisson probability matrix for HT and FT
def poisson_matrix(home_avg, away_avg, max_goals=5):
    """Generate a Poisson probability matrix."""
    home_goals = np.arange(0, max_goals + 1)
    away_goals = np.arange(0, max_goals + 1)
    probabilities = np.outer(poisson.pmf(home_goals, home_avg), poisson.pmf(away_goals, away_avg))
    return probabilities

# Display heatmap for probabilities
def display_score_probabilities(matrix, title):
    """Display a heatmap of score probabilities."""
    fig, ax = plt.subplots()
    ax.imshow(matrix, cmap="Blues", interpolation="nearest")
    for (i, j), prob in np.ndenumerate(matrix):
        ax.text(j, i, f"{prob:.2%}", ha="center", va="center", color="black")
    ax.set_xticks(range(matrix.shape[1]))
    ax.set_yticks(range(matrix.shape[0]))
    ax.set_xlabel("Away Goals")
    ax.set_ylabel("Home Goals")
    ax.set_title(title)
    st.pyplot(fig)

# Calculate implied probabilities for betting odds
def implied_probability(odds):
    return 1 / odds if odds > 0 else 0

# Display implied probabilities
under_2_5_prob = implied_probability(under_2_5_odds)
over_2_5_prob = implied_probability(over_2_5_odds)
btts_gg_prob = implied_probability(btts_gg_odds)
btts_ng_prob = implied_probability(btts_ng_odds)

st.sidebar.markdown(f"""
### Implied Probabilities
- **Under 2.5 Goals**: {under_2_5_prob:.2%}
- **Over 2.5 Goals**: {over_2_5_prob:.2%}
- **BTTS GG**: {btts_gg_prob:.2%}
- **BTTS NG**: {btts_ng_prob:.2%}
""")

# Button to trigger calculations
if st.button("Calculate HT/FT Combination"):
    st.subheader("Halftime Score Probabilities")
    ht_matrix = poisson_matrix(avg_goals_home / 2, avg_goals_away / 2)
    display_score_probabilities(ht_matrix, "Halftime Probabilities")

    st.subheader("Fulltime Score Probabilities")
    ft_matrix = poisson_matrix(avg_goals_home, avg_goals_away)
    display_score_probabilities(ft_matrix, "Fulltime Probabilities")

    # Adjusted margins
    adjusted_ht_margin = 5.14
    adjusted_ft_margin = 5.55

    # Most likely HT and FT scores
    most_likely_ht = np.unravel_index(np.argmax(ht_matrix, axis=None), ht_matrix.shape)
    most_likely_ft = np.unravel_index(np.argmax(ft_matrix, axis=None), ft_matrix.shape)

    st.markdown(f"""
    ### Recommendations:
    - **Most Likely HT Score**: {most_likely_ht[0]}:{most_likely_ht[1]}
    - **Most Likely FT Score**: {most_likely_ft[0]}:{most_likely_ft[1]}
    """)

