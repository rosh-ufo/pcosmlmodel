import streamlit as st
import pickle
import numpy as np

# Load the regression model
with open('pcosmodel.pkl', 'rb') as file:
    model = pickle.load(file)

st.title("PCOS Detection Prediction")
st.subheader("Fill in the details below:")

# Collect inputs for each feature
age = st.number_input("Age (in Years):", min_value=1, max_value=100, value=25)

# Encode categorical inputs as numerical values
blood_group = st.selectbox("Blood Group:", ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"])
blood_group_mapping = {"A+": 0, "A-": 1, "B+": 2, "B-": 3, "AB+": 4, "AB-": 5, "O+": 6, "O-": 7}
blood_group_encoded = blood_group_mapping.get(blood_group, 0)

# Encode Yes/No responses
def yes_no_to_int(response):
    return 1 if response == "Yes" else 0

weight_gain = yes_no_to_int(st.radio("Have you gained weight recently?", ["Yes", "No"]))
body_hair_growth = yes_no_to_int(st.radio("Excessive body/facial hair growth?", ["Yes", "No"]))
skin_darkening = yes_no_to_int(st.radio("Noticing skin darkening recently?", ["Yes", "No"]))
hair_loss = yes_no_to_int(st.radio("Hair loss/hair thinning/baldness?", ["Yes", "No"]))
acne = yes_no_to_int(st.radio("Pimples/acne on face/jawline?", ["Yes", "No"]))
fast_food = yes_no_to_int(st.radio("Eat fast food regularly?", ["Yes", "No"]))
exercise = yes_no_to_int(st.radio("Exercise regularly?", ["Yes", "No"]))
mood_swings = yes_no_to_int(st.radio("Experience mood swings?", ["Yes", "No"]))
periods_regular = yes_no_to_int(st.radio("Are your periods regular?", ["Yes", "No"]))
period_duration = st.number_input("Period duration (in days):", min_value=1, max_value=10, value=5)

# Prepare the input data for prediction
input_data = np.array([age, blood_group_encoded, weight_gain, body_hair_growth, skin_darkening, hair_loss, acne, fast_food, exercise, mood_swings, periods_regular, period_duration])
input_data = input_data.reshape(1, -1)  # Ensure it is 2D for prediction

# Predict using the model
prediction = model.predict(input_data)

# Since it's a regression model, convert the result into "Yes" or "No"
# If the prediction is above a certain threshold (e.g., 0.5), predict "Yes"
if prediction[0] > 0.5:
    prediction_text = "Yes"
else:
    prediction_text = "No"

# Display the result
st.write(f"Prediction: {prediction_text}")
