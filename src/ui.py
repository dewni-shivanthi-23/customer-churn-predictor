# import streamlit as st
# import requests

# st.title("Customer Churn Prediction System")

# tenure = st.number_input("Tenure")
# monthly = st.number_input("Monthly Charges")
# total = st.number_input("Total Charges")

# contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
# internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

# if st.button("Predict"):

#     data = {
#         "tenure": tenure,
#         "MonthlyCharges": monthly,
#         "TotalCharges": total,
#         "Contract": contract,
#         "InternetService": internet
#     }

#     res = requests.post("http://127.0.0.1:8000/predict", json=data)

#     result = res.json()

#     st.success(f"Prediction: {result['prediction']}")
#     st.info(f"Model Used: {result['model_used']}")

# import streamlit as st
# import requests

# st.set_page_config(
#     page_title="Churn Dashboard",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.set_page_config(page_title="Churn Dashboard", layout="wide")

# st.title("Customer Churn Risk Dashboard")

# # -----------------------------
# # Sidebar Input
# # -----------------------------
# st.sidebar.header("Enter Customer Details")

# tenure = st.sidebar.slider("Tenure (months)", 0, 72, 12)
# monthly = st.sidebar.number_input("Monthly Charges", 0.0, 200.0, 70.0)
# total = st.sidebar.number_input("Total Charges", 0.0, 10000.0, 800.0)

# contract = st.sidebar.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
# internet = st.sidebar.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

# predict_btn = st.sidebar.button("🔍 Predict")

# # -----------------------------
# # Main Output
# # -----------------------------
# if predict_btn:

#     data = {
#         "tenure": tenure,
#         "MonthlyCharges": monthly,
#         "TotalCharges": total,
#         "Contract": contract,
#         "InternetService": internet
#     }

#     res = requests.post("http://127.0.0.1:8000/predict", json=data)
#     result = res.json()

#     prediction = result["prediction"]
#     model_used = result["model_used"]

#     # -----------------------------
#     # Display Results
#     # -----------------------------
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.metric("Prediction", "Churn" if prediction == 1 else "Stay")

#     with col2:
#         st.metric("Model Used", model_used)

#     with col3:
#         risk = "High Risk" if prediction == 1 else "Low Risk"
#         st.metric("Risk Level", risk)

#     # -----------------------------
#     # Visual Feedback
#     # -----------------------------
#     if prediction == 1:
#         st.error("Customer is likely to churn!")
#     else:
#         st.success("Customer is likely to stay!")

#     # -----------------------------
#     # Extra Insight
#     # -----------------------------
#     st.subheader("Insight")
#     if prediction == 1:
#         st.write("Consider offering discounts or promotions to retain this customer.")
#     else:
#         st.write("Customer seems stable. Maintain engagement.")

import streamlit as st
import requests
import time

st.set_page_config(page_title="Churn Dashboard", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.markdown(
    "<h1 style='text-align: left;'> Customer Churn Intelligence Dashboard</h1>",
    unsafe_allow_html=True
)

#st.markdown("---")

# -----------------------------
# Sidebar (Styled Inputs)
# -----------------------------
st.sidebar.header(" Customer Inputs")

tenure = st.sidebar.slider("Tenure (months)", 0, 72, 12)
monthly = st.sidebar.slider("Monthly Charges", 0, 200, 70)
total = st.sidebar.slider("Total Charges", 0, 10000, 800)

contract = st.sidebar.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
internet = st.sidebar.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

predict_btn = st.sidebar.button("Analyze Customer")

st.markdown("<br><br>", unsafe_allow_html=True)

# -----------------------------
# Main Area
# -----------------------------
if predict_btn:

    with st.spinner("Analyzing customer behavior..."):
        time.sleep(1)

        data = {
            "tenure": tenure,
            "MonthlyCharges": monthly,
            "TotalCharges": total,
            "Contract": contract,
            "InternetService": internet
        }

        res = requests.post("http://127.0.0.1:8000/predict", json=data)
        result = res.json()

        prediction = result["prediction"]
        model_used = result["model_used"]

    # -----------------------------
    # Metrics Row
    # -----------------------------
    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     st.metric("Prediction", "Churn" if prediction == 1 else "Stay")

    # with col2:
    #     st.metric("Model Used", model_used)

    # with col3:
    #     risk = "High" if prediction == 1 else "Low"
    #     st.metric("Risk Level", risk)'

    col1, col2, col3 = st.columns(3)

    card_style = """
    padding: 20px;
    border-radius: 15px;
    background-color: #E3F2FD;
    text-align: center;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    """

# Prediction Card
    with col1:
       pred_text = "Stay" if prediction == 0 else "Churn"
       st.markdown(f"""
       <div style="{card_style}">
           <h4>Prediction</h4>
           <h2><b>{pred_text}</b></h2>
        </div>
        """, unsafe_allow_html=True)

# Model Card
    with col2:
       st.markdown(f"""
       <div style="{card_style}">
           <h4>Model Used</h4>
           <h2><b>{model_used}</b></h2>
        </div>
        """, unsafe_allow_html=True)

# Risk Card
    with col3:
       risk = "Low" if prediction == 0 else "High"
       st.markdown(f"""
        <div style="{card_style}">
          <h4>Risk Level</h4>
          <h2><b>{risk}</b></h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    #st.markdown("---")

    # -----------------------------
    # Visual Feedback
    # -----------------------------
    if prediction == 1:
        st.error("High churn risk detected!")
    else:
        st.success("Customer likely to stay!")

    # -----------------------------
    # Interactive Chart
    # -----------------------------
    # st.subheader("Customer Profile Overview")

    # chart_data = {
    #     "Feature": ["Tenure", "MonthlyCharges", "TotalCharges"],
    #     "Value": [tenure, monthly, total]
    # }

    # st.bar_chart(chart_data, x="Feature", y="Value")

    # -----------------------------
    # Business Insight
    # -----------------------------
    st.subheader("Smart Recommendation")

    if prediction == 1:
        st.warning("Offer discounts or personalized plans to retain this customer.")
    else:
        st.info("Maintain engagement with loyalty rewards or upgrades.")