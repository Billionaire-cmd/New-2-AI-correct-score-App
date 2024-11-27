import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Sidebar section
st.sidebar.title("💯💯💯🤖Rabiotic HT/FT Correct Score Predictor Pro")
st.sidebar.markdown("""
Welcome to the **Rabiotic HT/FT Correct Score Predictor**!  
This app uses statistical models to predict halftime and full-time correct scores based on:
- Poisson distribution
- Betting odds
- Team statistics
""")

# Sidebar match inputs
st.sidebar.markdown("### Match Inputs")

# Team statistics inputs
avg_goals_home = st.sidebar.number_input("Avg Goals Scored (Home)", value=1.50, step=0.1)
avg_goals_away = st.sidebar.number_input("Avg Goals Scored (Away)", value=1.30, step=0.1)
avg_points_home = st.sidebar.number_input("Avg Points (Home)", value=1.50, step=0.1)
avg_points_away = st.sidebar.number_input("Avg Points (Away)", value=1.30, step=0.1)

# Odds inputs
btts_gg_odds = st.sidebar.number_input("BTTS GG Odds (Both Teams To Score)", value=1.77, step=0.01)
btts_ng_odds = st.sidebar.number_input("BTTS NG Odds (No Goal for One or Both)", value=1.83, step=0.01)
over_2_5_goals_odds = st.sidebar.number_input("Over 2.5 Goals Odds", value=1.87, step=0.01)
under_2_5_goals_odds = st.sidebar.number_input("Under 2.5 Goals Odds", value=1.80, step=0.01)

# HT/FT Odds inputs
ht_home_win_odds = st.sidebar.number_input("HT Home Win Odds", value=2.40, step=0.01)
ht_draw_odds = st.sidebar.number_input("HT Draw Odds", value=2.10, step=0.01)
ht_away_win_odds = st.sidebar.number_input("HT Away Win Odds", value=4.50, step=0.01)
ft_home_win_odds = st.sidebar.number_input("FT Home Win Odds", value=1.80, step=0.01)
ft_draw_odds = st.sidebar.number_input("FT Draw Odds", value=3.50, step=0.01)
ft_away_win_odds = st.sidebar.number_input("FT Away Win Odds", value=3.90, step=0.01)

# Submit prediction button
with st.sidebar:
    st.markdown("### Submit Prediction")
    if st.button("Submit Prediction"):
        st.success("Prediction submitted! Results will be displayed below.")

        # Calculate Poisson distribution probabilities for halftime and full-time scores
        avg_goals_home_ft = avg_goals_home
        avg_goals_away_ft = avg_goals_away
        avg_goals_home_ht = avg_goals_home / 2  # Approximate for HT
        avg_goals_away_ht = avg_goals_away / 2  # Approximate for HT

        # Halftime Poisson probabilities
        ht_home_prob = poisson.pmf([0, 1, 2, 3, 4], avg_goals_home_ht)
        ht_away_prob = poisson.pmf([0, 1, 2, 3, 4], avg_goals_away_ht)

        # Full-time Poisson probabilities
        ft_home_prob = poisson.pmf([0, 1, 2, 3, 4], avg_goals_home_ft)
        ft_away_prob = poisson.pmf([0, 1, 2, 3, 4], avg_goals_away_ft)

        # Display probabilities
        st.subheader("HT/FT Correct Score Prediction")
        st.write(f"**Halftime Prediction (Home/Away)**:")
        st.write(f"Home Team: {ht_home_prob}")
        st.write(f"Away Team: {ht_away_prob}")

        st.write(f"**Fulltime Prediction (Home/Away)**:")
        st.write(f"Home Team: {ft_home_prob}")
        st.write(f"Away Team: {ft_away_prob}")

        # Visualize the results
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        ax[0].bar([0, 1, 2, 3, 4], ht_home_prob, label='Home', alpha=0.6)
        ax[0].bar([0, 1, 2, 3, 4], ht_away_prob, label='Away', alpha=0.6)
        ax[0].set_title("Halftime Score Probability")
        ax[0].set_xlabel("Goals Scored")
        ax[0].set_ylabel("Probability")
        ax[0].legend()

        ax[1].bar([0, 1, 2, 3, 4], ft_home_prob, label='Home', alpha=0.6)
        ax[1].bar([0, 1, 2, 3, 4], ft_away_prob, label='Away', alpha=0.6)
        ax[1].set_title("Fulltime Score Probability")
        ax[1].set_xlabel("Goals Scored")
        ax[1].set_ylabel("Probability")
        ax[1].legend()

        st.pyplot(fig)
