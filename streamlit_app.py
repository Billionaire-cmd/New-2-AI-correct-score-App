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
st.title("💯💯💯🤖Rabiotic HT/FT Correct Score Predictor pro")
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

# Calculate Halftime Probabilities (Dividing goals by 2 for Halftime)
ht_home_probs = calculate_poisson_prob(avg_goals_home / 2, max_goals=2)
ht_away_probs = calculate_poisson_prob(avg_goals_away / 2, max_goals=2)
ht_matrix = np.outer(ht_home_probs, ht_away_probs)

# Calculate Fulltime Probabilities
ft_home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
ft_away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)
ft_matrix = np.outer(ft_home_probs, ft_away_probs)

# Function to find the best HT/FT combination
def calculate_best_ht_ft_combination(ht_matrix, ft_matrix):
    """
    Finds the highest HT/FT combinations based on probabilities.
    """
    # Identify the index of the maximum value in the HT matrix
    ht_max_idx = np.unravel_index(np.argmax(ht_matrix), ht_matrix.shape)
    ft_max_idx = np.unravel_index(np.argmax(ft_matrix), ft_matrix.shape)
    
    # Extract HT/FT results with their probabilities
    ht_max_prob = ht_matrix[ht_max_idx]
    ft_max_prob = ft_matrix[ft_max_idx]

    # Get HT/FT results
    ht_result = f"HT: {ht_max_idx[0]}-{ht_max_idx[1]}"  # HT result
    ft_result = f"FT: {ft_max_idx[0]}-{ft_max_idx[1]}"  # FT result
    
    # Recommendation based on highest HT/FT probabilities
    recommendation = f"The most likely HT/FT combination is {ht_result} and {ft_result} with probabilities " \
                     f"of {ht_max_prob:.2f} for Halftime and {ft_max_prob:.2f} for Fulltime."

    return recommendation, ht_max_prob, ft_max_prob, ht_result, ft_result

# Streamlit UI
st.title("HT/FT Probability Prediction")

# Button to trigger the HT/FT best combination calculation
if st.button("Calculate HT/FT Best Combination"):
    # Display Heatmaps for HT and FT
    st.subheader("Halftime Score Probabilities")
    display_score_probabilities(ht_matrix, "Halftime Probabilities")

    st.subheader("Fulltime Score Probabilities")
    display_score_probabilities(ft_matrix, "Fulltime Probabilities")

    # Best HT/FT Combination
    recommendation, ht_max_prob, ft_max_prob, ht_result, ft_result = calculate_best_ht_ft_combination(ht_matrix, ft_matrix)

    # Display Recommendation
    st.subheader("Best HT/FT Combination Recommendation")
    st.write(f"**Best HT/FT Combination**: {ht_result} and {ft_result}")
    st.write(f"**Halftime Probability**: {ht_max_prob:.2f}")
    st.write(f"**Fulltime Probability**: {ft_max_prob:.2f}")
    st.write(recommendation)

# Sidebar for Average Points Inputs
st.sidebar.subheader("Team Average Points")
avg_points_home = st.sidebar.number_input("Avg Points (Home)", min_value=0.0, value=1.5, step=0.1)
avg_points_away = st.sidebar.number_input("Avg Points (Away)", min_value=0.0, value=1.2, step=0.1)

# Sidebar for BTTS Inputs
st.sidebar.subheader("BTTS (Both Teams To Score) Inputs")
btts_gg_odds = st.sidebar.number_input("BTTS GG Odds (Both Teams To Score)", min_value=1.0, value=1.9, step=0.1)
btts_ng_odds = st.sidebar.number_input("BTTS NG Odds (No Goal for One or Both)", min_value=1.0, value=2.0, step=0.1)

# Sidebar for Over/Under 2.5 Inputs
st.sidebar.subheader("Over/Under 2.5 Goals Inputs")
over_2_5_odds = st.sidebar.number_input("Over 2.5 Goals Odds", min_value=1.0, value=1.8, step=0.1)
under_2_5_odds = st.sidebar.number_input("Under 2.5 Goals Odds", min_value=1.0, value=2.0, step=0.1)

# Display Over/Under 2.5 Information
st.subheader("Over/Under 2.5 Goals Odds")
st.write(f"**Over 2.5 Goals Odds**: {over_2_5_odds}")
st.write(f"**Under 2.5 Goals Odds**: {under_2_5_odds}")

# Calculation: Based on odds, calculate and display the likelihood of Over 2.5 and Under 2.5
# Example: Calculate the implied probability of Over 2.5 and Under 2.5
prob_over_2_5 = 1 / over_2_5_odds * 100  # Convert odds to percentage probability
prob_under_2_5 = 1 / under_2_5_odds * 100  # Convert odds to percentage probability

# Display Calculated Probabilities
st.write(f"**Implied Probability for Over 2.5 Goals**: {prob_over_2_5:.2f}%")
st.write(f"**Implied Probability for Under 2.5 Goals**: {prob_under_2_5:.2f}%")

# Display BTTS Information
st.subheader("BTTS (Both Teams To Score) Odds")
st.write(f"**BTTS GG Odds** (Both Teams To Score): {btts_gg_odds}")
st.write(f"**BTTS NG Odds** (No Goal for One or Both): {btts_ng_odds}")

# Calculation: Based on odds, calculate and display the likelihood of GG or NG
# Example: Calculate the implied probability of BTTS GG and BTTS NG
prob_btts_gg = 1 / btts_gg_odds * 100  # Convert odds to percentage probability
prob_btts_ng = 1 / btts_ng_odds * 100  # Convert odds to percentage probability

# Display Calculated Probabilities
st.write(f"**Implied Probability for BTTS GG**: {prob_btts_gg:.2f}%")
st.write(f"**Implied Probability for BTTS NG**: {prob_btts_ng:.2f}%")
