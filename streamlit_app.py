import streamlit as st

# Function to calculate the final correct score based on user rules
def calculate_final_score(scorelines):
    # Sort scorelines by probability in descending order
    sorted_scorelines = sorted(scorelines, key=lambda x: x[1], reverse=True)
    
    # Extract specific probabilities for rules
    highest = sorted_scorelines[0]
    second_highest = sorted_scorelines[1]
    middle_high = sorted_scorelines[3]
    middle_second_high = sorted_scorelines[1]
    final_score = None

    # Implement rules based on the given probabilities
    if highest[1] >= 11.23 and 6.02 <= middle_second_high[1] <= 6.8:
        final_score = middle_second_high[0]
    elif highest[1] >= 12.9 and 5.2 <= middle_second_high[1] <= 5.71:
        final_score = middle_second_high[0]
    elif highest[1] >= 11.38 and 6.19 <= middle_second_high[1] <= 6.5:
        final_score = middle_second_high[0]
    elif highest[1] >= 12.26 and 6.07 <= middle_second_high[1] <= 6.38:
        final_score = middle_high[0]
    elif highest[1] >= 11.99 and 6.39 <= middle_second_high[1] <= 6.85:
        final_score = middle_second_high[0]
    elif highest[1] >= 20.39 and middle_high[1] == 10.15:
        final_score = middle_high[0]
    elif highest[1] >= 11.92 and middle_high[1] == 6.08:
        final_score = middle_high[0]
    elif highest[1] == 9.25:
        final_score = sorted_scorelines[2][0]
    elif highest[1] >= 12.26 and 6.67 in [x[1] for x in sorted_scorelines]:
        final_score = second_highest[0]
    elif highest[1] >= 11.54 and 6.99 in [x[1] for x in sorted_scorelines]:
        final_score = second_highest[0]
    else:
        final_score = highest[0]  # Default to the highest scoreline if no rule applies

    return final_score

# Streamlit app UI
st.title("🤖🤖🤖Rabiotic Correct Score Probability℅ of Scorelines Analyzer for Final 💯 Correct Score")

st.sidebar.header("Input Top 12 Most Likely Scorelines")
st.sidebar.write("Enter the scorelines and their corresponding probabilities (%):")

# Sidebar input for scorelines and probabilities
scorelines = []
for i in range(1, 13):
    scoreline = st.sidebar.text_input(f"Scoreline {i}", key=f"scoreline_{i}")
    probability = st.sidebar.number_input(
        f"Probability℅ for Scoreline {i}", min_value=0.0, max_value=100.0, step=0.01, key=f"probability_{i}"
    )
    if scoreline and probability > 0:
        scorelines.append((scoreline, probability))

# Predict button
if st.sidebar.button("Predict"):
    if len(scorelines) == 12:
        final_correct_score = calculate_final_score(scorelines)
        st.success(f"The Final Correct Score is: **{final_correct_score}**")
        
        # Display a table of scorelines and probabilities
        st.write("### Input Scorelines and Probabilities")
        st.table(scorelines)
    else:
        st.error("Please input all 12 scorelines with their probabilities.")
