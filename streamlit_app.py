import streamlit as st
import numpy as np
from scipy.stats import poisson

# Function to Calculate Poisson Probabilities
def calculate_poisson_prob(lambda_, max_goals):
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

# App Title and Introduction
st.title("🤖 Rabiotic Advanced HT/FT Correct Score Predictor")
st.markdown("""
Welcome to the **Rabiotic Advanced Halftime/Full-time Correct Score Predictor**!  
This app uses advanced statistical models, including the Poisson distribution, betting odds, and team statistics, 
to predict realistic halftime and full-time correct scores for football matches.  
It is designed to enhance your betting strategies by providing precise calculations for maximum ROI.
""")

# Sidebar for Inputs
st.sidebar.header("Match Statistics and Inputs")

# Average Goals Scored
avg_goals_home = st.sidebar.number_input("Average Goals Scored by Home Team", min_value=0.0, step=0.1, value=1.5)
avg_goals_away = st.sidebar.number_input("Average Goals Scored by Away Team", min_value=0.0, step=0.1, value=1.2)

# Average Points
avg_points_home = st.sidebar.number_input("Average Points for Home Team", min_value=0.0, step=0.1, value=1.8)
avg_points_away = st.sidebar.number_input("Average Points for Away Team", min_value=0.0, step=0.1, value=1.5)

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

# Correct Score Odds (Fulltime)
st.sidebar.subheader("Correct Score Odds (Fulltime)")
correct_score_odds_fulltime = {}
for i in range(5):
    for j in range(5):
        score = f"{i}:{j}"
        correct_score_odds_fulltime[score] = st.sidebar.number_input(f"FT Odds for {score}", value=10.0, step=0.01)
# "Other" scores for Fulltime
correct_score_odds_fulltime["Other"] = st.sidebar.number_input("FT Odds for scores exceeding 4:4", value=50.0, step=0.01)

# Correct Score Odds (Halftime)
st.sidebar.subheader("Correct Score Odds (Halftime)")
correct_score_odds_halftime = {}
for i in range(3):
    for j in range(3):
        ht_score = f"{i}:{j}"
        correct_score_odds_halftime[ht_score] = st.sidebar.number_input(f"HT Odds for {ht_score}", value=10.0, step=0.01)
# "Other" scores for Halftime
correct_score_odds_halftime["Other"] = st.sidebar.number_input("HT Odds for scores exceeding 2:2", value=50.0, step=0.01)

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

# Predict Probabilities and Insights
if st.button("Predict Probabilities and Insights"):
    try:
        # Calculate Poisson Probabilities for Fulltime
        fulltime_home_probs = calculate_poisson_prob(avg_goals_home, max_goals=4)
        fulltime_away_probs = calculate_poisson_prob(avg_goals_away, max_goals=4)
        score_matrix = np.outer(fulltime_home_probs, fulltime_away_probs)

        # Calculate Poisson Probabilities for Halftime (assuming halftime goals are ~50% of fulltime goals)
        halftime_home_avg = avg_goals_home / 2
        halftime_away_avg = avg_goals_away / 2
        halftime_home_probs = calculate_poisson_prob(halftime_home_avg, max_goals=2)
        halftime_away_probs = calculate_poisson_prob(halftime_away_avg, max_goals=2)
        halftime_score_matrix = np.outer(halftime_home_probs, halftime_away_probs)

        # Calculate Fulltime Score Probabilities
        fulltime_score_probs = {f"{i}:{j}": score_matrix[i, j] for i in range(5) for j in range(5)}
        fulltime_other_prob = 1 - sum(fulltime_score_probs.values())
        fulltime_score_probs["Other"] = fulltime_other_prob

        # Calculate Halftime Score Probabilities
        halftime_score_probs = {f"{i}:{j}": halftime_score_matrix[i, j] for i in range(3) for j in range(3)}
        halftime_other_prob = 1 - sum(halftime_score_probs.values())
        halftime_score_probs["Other"] = halftime_other_prob

        # Sort Scores by Probability
        sorted_fulltime_scores = sorted(fulltime_score_probs.items(), key=lambda x: x[1], reverse=True)
        sorted_halftime_scores = sorted(halftime_score_probs.items(), key=lambda x: x[1], reverse=True)

        # BTTS Probabilities
        btts_yes_prob = sum(score_matrix[i][j] for i in range(1,5) for j in range(1,5)) * 100
        btts_no_prob = 100 - btts_yes_prob

        # Over/Under 2.5 Goals Probabilities (Fulltime)
        over_2_5_prob = sum(score_matrix[i][j] for i in range(3,5) for j in range(5)) * 100
        under_2_5_prob = 100 - over_2_5_prob

        # Over/Under 1.5 Goals Probabilities (Halftime)
        over_1_5_ht_prob = sum(halftime_score_matrix[i][j] for i in range(2,3) for j in range(3)) * 100
        under_1_5_ht_prob = 100 - over_1_5_ht_prob

        # Over/Under 1.5 Goals Probabilities (Fulltime)
        over_1_5_ft_prob = sum(score_matrix[i][j] for i in range(2,5) for j in range(5)) * 100
        under_1_5_ft_prob = 100 - over_1_5_ft_prob

        # Match Outcome Probabilities
        home_win_prob = sum(score_matrix[i][j] for i in range(1,5) for j in range(0,i)) * 100
        draw_prob = sum(score_matrix[i][i] for i in range(5)) * 100
        away_win_prob = 100 - home_win_prob - draw_prob

        # Bookmaker's Margins
        margin_btts = calculate_margin([btts_gg, btts_ng])
        margin_over_under_2_5 = calculate_margin([over_2_5_ft, under_2_5_ft])
        margin_over_under_1_5_ht = calculate_margin([over_1_5_ht, under_1_5_ht])
        margin_over_under_1_5_ft = calculate_margin([over_1_5_ft, under_1_5_ft])
        margin_match_outcomes = calculate_margin([ft_home, ft_draw, ft_away])

        # Expected Values for Betting Markets
        # BTTS
        btts_yes_ev = calculate_expected_value(btts_yes_prob / 100, btts_gg)
        btts_no_ev = calculate_expected_value(btts_no_prob / 100, btts_ng)

        # Over/Under 2.5
        over_2_5_ev = calculate_expected_value(over_2_5_prob / 100, over_2_5_ft)
        under_2_5_ev = calculate_expected_value(under_2_5_prob / 100, under_2_5_ft)

        # Over/Under 1.5 (Halftime)
        over_1_5_ht_ev = calculate_expected_value(over_1_5_ht_prob / 100, over_1_5_ht)
        under_1_5_ht_ev = calculate_expected_value(under_1_5_ht_prob / 100, under_1_5_ht)

        # Over/Under 1.5 (Fulltime)
        over_1_5_ft_ev = calculate_expected_value(over_1_5_ft_prob / 100, over_1_5_ft)
        under_1_5_ft_ev = calculate_expected_value(under_1_5_ft_prob / 100, under_1_5_ft)

        # Match Outcomes
        home_win_ev = calculate_expected_value(home_win_prob / 100, ft_home)
        draw_ev = calculate_expected_value(draw_prob / 100, ft_draw)
        away_win_ev = calculate_expected_value(away_win_prob / 100, ft_away)

        # Compile Value Bets
        value_bets = []
        if btts_yes_ev > 0:
            value_bets.append(("BTTS Yes", btts_yes_ev))
        if btts_no_ev > 0:
            value_bets.append(("BTTS No", btts_no_ev))
        if over_2_5_ev > 0:
            value_bets.append(("Over 2.5 FT", over_2_5_ev))
        if under_2_5_ev > 0:
            value_bets.append(("Under 2.5 FT", under_2_5_ev))
        if over_1_5_ht_ev > 0:
            value_bets.append(("Over 1.5 HT", over_1_5_ht_ev))
        if under_1_5_ht_ev > 0:
            value_bets.append(("Under 1.5 HT", under_1_5_ht_ev))
        if over_1_5_ft_ev > 0:
            value_bets.append(("Over 1.5 FT", over_1_5_ft_ev))
        if under_1_5_ft_ev > 0:
            value_bets.append(("Under 1.5 FT", under_1_5_ft_ev))
        if home_win_ev > 0:
            value_bets.append(("Home Win", home_win_ev))
        if draw_ev > 0:
            value_bets.append(("Draw", draw_ev))
        if away_win_ev > 0:
            value_bets.append(("Away Win", away_win_ev))

        # Recommendations
        if value_bets:
            best_value_bet = max(value_bets, key=lambda x: x[1])
        else:
            best_value_bet = None

        # Display Results
        st.header("Predictions and Insights")

        # Correct Score Predictions
        st.subheader("Correct Score Predictions")
        st.write("### Top 5 Likely Halftime Scores:")
        for ht_score, prob in sorted_halftime_scores[:5]:
            st.write(f"**{ht_score}:** {prob * 100:.2f}%")
        st.write("### Top 5 Likely Fulltime Scores:")
        for score, prob in sorted_fulltime_scores[:5]:
            st.write(f"**{score}:** {prob * 100:.2f}%")

        # BTTS Probabilities and Margin
        st.subheader("BTTS (GG/NG) Probabilities and Margin")
        st.write(f"**BTTS (Yes):** {btts_yes_prob:.2f}%")
        st.write(f"**BTTS (No):** {btts_no_prob:.2f}%")
        st.write(f"**Bookmaker's Margin for BTTS:** {margin_btts:.2f}%")

        # Over/Under 2.5 Goals Probabilities and Margin
        st.subheader("Over/Under 2.5 Goals Probabilities and Margin (Fulltime)")
        st.write(f"**Over 2.5 Goals:** {over_2_5_prob:.2f}%")
        st.write(f"**Under 2.5 Goals:** {under_2_5_prob:.2f}%")
        st.write(f"**Bookmaker's Margin for Over/Under 2.5:** {margin_over_under_2_5:.2f}%")

        # Over/Under 1.5 Goals Probabilities and Margin (Halftime)
        st.subheader("Over/Under 1.5 Goals Probabilities and Margin (Halftime)")
        st.write(f"**Over 1.5 Goals (HT):** {over_1_5_ht_prob:.2f}%")
        st.write(f"**Under 1.5 Goals (HT):** {under_1_5_ht_prob:.2f}%")
        st.write(f"**Bookmaker's Margin for Over/Under 1.5 (HT):** {margin_over_under_1_5_ht:.2f}%")

        # Over/Under 1.5 Goals Probabilities and Margin (Fulltime)
        st.subheader("Over/Under 1.5 Goals Probabilities and Margin (Fulltime)")
        st.write(f"**Over 1.5 Goals (FT):** {over_1_5_ft_prob:.2f}%")
        st.write(f"**Under 1.5 Goals (FT):** {under_1_5_ft_prob:.2f}%")
        st.write(f"**Bookmaker's Margin for Over/Under 1.5 (FT):** {margin_over_under_1_5_ft:.2f}%")

        # Match Outcome Probabilities and Margin
        st.subheader("Match Outcome Probabilities and Margin")
        st.write(f"**Home Win:** {home_win_prob:.2f}%")
        st.write(f"**Draw:** {draw_prob:.2f}%")
        st.write(f"**Away Win:** {away_win_prob:.2f}%")
        st.write(f"**Bookmaker's Margin for Match Outcomes:** {margin_match_outcomes:.2f}%")

        # Value Bet Recommendation
        st.subheader("Low Value Bet Recommendation")
        if best_value_bet:
            st.write(f"**Recommended Bet:** {best_value_bet[0]} (Expected Value: {best_value_bet[1]:.2f})")
        else:
            st.write("**No Value Bets Found.**")

    except Exception as e:
        st.error(f"Error in calculation: {e}")
