import streamlit as st

# App Title and Description
st.set_page_config(page_title="Rabiotic Correct Score Probability℅ Analyzer", layout="wide")
st.title("Rabiotic Correct Score Probability℅ Analyzer")
st.subheader("Final 💯 Correct Score with Machine Learning-Driven Rules")

st.sidebar.header("Input the 12 Top Most Likely Scorelines")
st.sidebar.markdown(
    """
    Input the **Scorelines** and their **Probability%** below. 
    Example format:  
    **Scoreline: Probability%**  
    1-1: 6.85%  
    """
)

# Input Fields for 12 Scorelines and Probabilities
input_data = {}
for i in range(1, 13):
    input_data[f"scoreline_{i}"] = st.sidebar.text_input(f"Scoreline {i}", "")
    input_data[f"probability_{i}"] = st.sidebar.text_input(f"Probability {i} (%)", "")

# Predict Button
if st.sidebar.button("Predict Final Correct Score"):
    try:
        # Parse Input Data
        scorelines = []
        probabilities = []
        for i in range(1, 13):
            if input_data[f"scoreline_{i}"] and input_data[f"probability_{i}"]:
                scorelines.append(input_data[f"scoreline_{i}"])
                probabilities.append(float(input_data[f"probability_{i}"]))

        if len(scorelines) != 12 or len(probabilities) != 12:
            st.error("Please input all 12 scorelines and their probabilities.")
        else:
            # Combine and Sort Data
            scoreline_data = list(zip(scorelines, probabilities))
            sorted_data = sorted(scoreline_data, key=lambda x: x[1], reverse=True)

            # Calculate the Final Correct Score Based on Your Rules
            final_correct_score = None
            highest = sorted_data[0]
            middle_scores = sorted_data[4:6]
            lowest_scores = sorted_data[6:]

            # Example Calculation Based on Rule 1 (Adjust Logic for Each Rule)
            if 6.02 <= middle_scores[0][1] <= 7.30:
                final_correct_score = middle_scores[0][0]
            else:
                final_correct_score = highest[0]  # Default to highest scoreline if rules aren't matched

            # Display Results
            st.success("Final Correct Score Calculated!")
            st.write(f"**Final Correct Score:** {final_correct_score}")
            st.write("### Scorelines and Probabilities (Descending Order)")
            for score, prob in sorted_data:
                st.write(f"**{score}: {prob:.2f}%**")

    except ValueError:
        st.error("Please ensure all probabilities are valid numbers.")

# Footer
st.markdown(
    """
    ---
    **Created by:** Rabiotic Analyzer System  
    """
)
