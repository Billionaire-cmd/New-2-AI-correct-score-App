import streamlit as st
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

# Function to Calculate Poisson Probabilities
def calculate_poisson_prob(lambda_, max_goals=4):
    """Calculate Poisson probabilities up to max_goals."""
    return [poisson.pmf(i, lambda_) for i in range(max_goals + 1)]

# Function to Calculate Bookmaker's Margin
def calculate_margin(odds_list):
    """Calculate bookmaker's margin given a list of odds."""
    return (sum(1 / odds for odds in odds_list) - 1) * 100

# Function to Calculate Expected Value
def calculate_expected_value(prob, odds):
    """Calculate expected value."""
    return (prob * odds) - 1

# Function to Collect Odds for Correct Scores
def get_correct_score_odds(prefix, max_goals):
    """Generate correct score odds inputs for HT or FT."""
    st.sidebar.subheader(f"{prefix} Correct Score Odds")
    score_odds = {}
    for i in range(max_goals + 1):
        for j in range(max_goals + 1):
            score = f"{i}:{j}"
            score_odds[score] = st.sidebar.number_input(f"{prefix} Odds for {score}", min_value=1.0, value=10.0, step=0.1)
    score_odds["Other"] = st.sidebar.number_input(f"{prefix} Odds for Other Scores", min_value=1.0, value=50.0, step=0.1)
    return score_odds

# Function to Display Score Probabilities as a Heatmap
def display_score_probabilities(prob_matrix, title):
    """Display score probabilities as a heatmap."""
    fig, ax = plt.subplots()
    cax = ax.matshow(prob_matrix, cmap="coolwarm")
    fig.colorbar(cax)
    plt.title(title)
    plt.xlabel("Away Goals")
    plt.ylabel("Home Goals")
    st.pyplot(fig)

# App Title and Introduction
st.title("⚽ Rabiotic HT/FT Correct Score Predictor")
st.markdown("""
Welcome to the **Rabiotic HT/FT Correct Score Predictor**!  
This app uses statistical models to predict halftime and full-time correct scores based on:
- Poisson distribution
- Betting odds
- Team statistics

### Features
- Halftime and Fulltime Probability Calculations
- Bookmaker Margin and Expected Value Analysis
- Custom Correct Score Odds Input
""")

# Sidebar for Inputs
st.sidebar.header("Match Inputs")

# Match Statistics Inputs
st.sidebar.subheader("Team Statistics")
avg_goals_home = st.sidebar.number_input("Avg Goals Scored (Home)", min_value=0.0, value=1.5, step=0.1)
avg_goals_away = st.sidebar.number_input("Avg Goals Scored (Away)", min_value=0.0, value=1.2, step=0.1)

# Sidebar for Average Points Inputs
st.sidebar.subheader("Team Average Points")
avg_points_home = st.sidebar.number_input("Avg Points (Home)", min_value=0.0, value=1.5, step=0.1)
avg_points_away = st.sidebar.number_input("Avg Points (Away)", min_value=0.0, value=1.2, step=0.1)

# Display Average Points Information
st.subheader("Team Average Points")
st.write(f"**Home Team Average Points**: {avg_points_home}")
st.write(f"**Away Team Average Points**: {avg_points_away}")

# Odds Inputs
st.sidebar.subheader("Odds")
ht_home = st.sidebar.number_input("HT Home Win Odds", min_value=1.0, value=2.5, step=0.1)
ht_draw = st.sidebar.number_input("HT Draw Odds", min_value=1.0, value=2.9, step=0.1)
ht_away = st.sidebar.number_input("HT Away Win Odds", min_value=1.0, value=3.1)
ft_home = st.sidebar.number_input("FT Home Win Odds", min_value=1.0, value=2.2, step=0.1)
ft_draw = st.sidebar.number_input("FT Draw Odds", min_value=1.0, value=3.2, step=0.1)
ft_away = st.sidebar.number_input("FT Away Win Odds", min_value=1.0, value=3.4)

# Correct Score Odds Inputs
correct_score_odds_ht = get_correct_score_odds("HT", max_goals=2)
correct_score_odds_ft = get_correct_score_odds("FT", max_goals=4)

# Calculate Probabilities and Margins
ht_probs = [1 / ht_home, 1 / ht_draw, 1 / ht_away]
ft_probs = [1 / ft_home, 1 / ft_draw, 1 / ft_away]
ht_margin = calculate_margin([ht_home, ht_draw, ht_away])
ft_margin = calculate_margin([ft_home, ft_draw, ft_away])

# Display Probabilities and Margins
st.subheader("HT/FT Probabilities and Margins")
st.write(f"**Halftime Probabilities**: {np.round(ht_probs, 3)}")
st.write(f"**Fulltime Probabilities**: {np.round(ft_probs, 3)}")
st.write(f"**Halftime Margin**: {ht_margin:.2f}%")
st.write(f"**Fulltime Margin**: {ft_margin:.2f}%")

# Predict Scores
if st.button("Calculate Probabilities"):
    # Calculate Halftime and Fulltime Probabilities
    ht_home_probs = calculate_poisson_prob(avg_goals_home / 2, max_goals=2)
    ht_away_probs = calculate_poisson_prob(avg_goals_away / 2, max_goals=2)
    ht_matrix = np.outer(ht_home_probs, ht_away_probs)

    ft_home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
    ft_away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)
    ft_matrix = np.outer(ft_home_probs, ft_away_probs)

    # Display Heatmaps
    st.subheader("Halftime Score Probabilities")
    display_score_probabilities(ht_matrix, "Halftime Probabilities")

    st.subheader("Fulltime Score Probabilities")
    display_score_probabilities(ft_matrix, "Fulltime Probabilities")

    # Calculate Recommendations
    ht_score = np.unravel_index(np.argmax(ht_matrix), ht_matrix.shape)
    ft_score = np.unravel_index(np.argmax(ft_matrix), ft_matrix.shape)

    st.subheader("Match Outcome and Strategy Recommendations")

    # Provide Insight based on Margin Calculations
    adjusted_ht_margin = 5.14
    adjusted_ft_margin = 5.55

    st.write("### Recommendation for Halftime Outcome:")
    if adjusted_ht_margin < 6.0:
        st.write("The halftime margin suggests a close contest. **HT Draw** is the most probable outcome based on the statistical analysis. Consider betting on **HT Draw / FT Home** or **HT Draw / FT Away**, depending on the in-game dynamics.")
    
    st.write("### Recommendation for Fulltime Outcome:")
    if adjusted_ft_margin < 6.0:
        st.write("The fulltime margin indicates a narrow result. Based on the model, either **Home Win (2-1)** or **Away Win (1-2)** might be the most likely outcomes. Consider these options for your final bet.")
    
    st.write(f"**Most Likely HT Score**: {ht_score[0]}:{ht_score[1]}")
    st.write(f"**Most Likely FT Score**: {ft_score[0]}:{ft_score[1]}")

    st.write("### Further Strategy Adjustments:")
    st.write("If there are **momentum shifts** in the game, adjust your live bets accordingly, especially if the game is tied at halftime. Momentum is key for making profitable bets in dynamic scenarios.")

    # Add a "summary" of final recommendations
    st.subheader("Final Betting Strategy Summary")
    st.write("""
    - **Halftime Bet**: Consider betting on **HT Draw** for a balanced first half.
    - **Fulltime Bet**: Look for value in betting on **Home Win (2-1)** or **Away Win (1-2)**, depending on in-game changes.
    - **Dynamic Adjustments**: During live betting, adjust bets if the game shows clear momentum for one team.
    """)
