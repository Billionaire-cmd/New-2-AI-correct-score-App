import streamlit as st

# Streamlit UI - Sidebar for Input
st.title("Rabiotic Correct Score Probability℅ Analyzer")
st.sidebar.title("Input Top 12 Scorelines")
st.sidebar.markdown(
    """
    Enter the Top 12 Most Likely Scorelines and their probabilities below:
    """
)

# Create input fields for the 12 most likely scorelines
scorelines = []
probabilities = []
for i in range(1, 13):
    scoreline = st.sidebar.text_input(f"Scoreline {i}", f"0-0" if i == 1 else "")
    probability = st.sidebar.number_input(
        f"Probability% for Scoreline {i}", min_value=0.0, max_value=100.0, value=0.0, step=0.01
    )
    scorelines.append(scoreline)
    probabilities.append(probability)

# Predict Button
if st.sidebar.button("Predict Final Correct Score"):
    # Process the input data
    data = list(zip(scorelines, probabilities))
    data.sort(key=lambda x: x[1], reverse=True)  # Sort by probability in descending order
    
    # Extract probabilities and corresponding scorelines
    sorted_scorelines = [item[0] for item in data]
    sorted_probabilities = [item[1] for item in data]
    
    st.write("### Sorted Scorelines with Probabilities")
    for i, (scoreline, probability) in enumerate(zip(sorted_scorelines, sorted_probabilities), start=1):
        st.write(f"{i}. {scoreline} - {probability:.2f}%")

    # Rules to determine the final correct score
    final_correct_score = None
    
    def apply_rules():
        global final_correct_score
        rules_applied = []
        
        # Rule 1
        if 6.02 <= sorted_probabilities[4] <= 6.8 and sorted_probabilities[0] == 11.23:
            final_correct_score = sorted_scorelines[4]
            rules_applied.append("Rule 1 applied")
        
        # Rule 2
        elif 5.2 <= sorted_probabilities[4] <= 5.71 and sorted_probabilities[0] == 12.9:
            final_correct_score = sorted_scorelines[4]
            rules_applied.append("Rule 2 applied")
        
        # Rule 3
        elif 6.19 <= sorted_probabilities[4] <= 6.50 and sorted_probabilities[0] == 11.38:
            final_correct_score = sorted_scorelines[4]
            rules_applied.append("Rule 3 applied")
        
        # Rule 4
        elif 6.07 <= sorted_probabilities[4] <= 6.38 and sorted_probabilities[0] == 12.26:
            final_correct_score = sorted_scorelines[0]
            rules_applied.append("Rule 4 applied")
        
        # Rule 5
        elif 6.39 <= sorted_probabilities[4] <= 6.85 and sorted_probabilities[0] == 11.99:
            final_correct_score = sorted_scorelines[4]
            rules_applied.append("Rule 5 applied")
        
        # Rule 6
        elif sorted_probabilities[0] == 20.39:
            final_correct_score = sorted_scorelines[1]  # Second highest
            rules_applied.append("Rule 6 applied")
        
        # Rule 7
        elif sorted_probabilities[0] == 11.92 and sorted_probabilities[1] == 6.08:
            final_correct_score = sorted_scorelines[1]
            rules_applied.append("Rule 7 applied")
        
        # Rule 8
        elif sorted_probabilities[0] == 9.25:
            final_correct_score = sorted_scorelines[2]  # Third descending
            rules_applied.append("Rule 8 applied")
        
        # Rule 9
        elif sorted_probabilities[0] == 12.26:
            final_correct_score = sorted_scorelines[1]  # Second highest
            rules_applied.append("Rule 9 applied")
        
        # Rule 10
        elif sorted_probabilities[0] == 11.54:
            final_correct_score = sorted_scorelines[1]  # Second highest
            rules_applied.append("Rule 10 applied")
        
        return rules_applied
    
    # Apply rules and get the final score
    rules_applied = apply_rules()
    if final_correct_score:
        st.success(f"**Final Correct Score Prediction:** {final_correct_score}")
        st.write("### Rules Applied:")
        for rule in rules_applied:
            st.write(f"- {rule}")
    else:
        st.error("Could not determine a final correct score based on the given rules.")
