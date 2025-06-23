
import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Load trained model and scaler
model = pickle.load(open('model/kmeans_model.pkl', 'rb'))
scaler = pickle.load(open('model/scaler.pkl', 'rb'))

# Behavior labeling function
def get_behavior_label(income, spending):
    if income >= 70 and spending >= 60:
        return "High Income, High Spending"
    elif income >= 70 and spending < 40:
        return "High Income, Low Spending"
    elif income < 40 and spending >= 60:
        return "Low Income, High Spending"
    else:
        return "Low Income, Low Spending"

st.set_page_config(page_title="Customer Clustering App", layout="wide")
st.title("🛍️ Customer Segmentation and Behavior Analysis")

option = st.sidebar.selectbox(
    "Choose an action",
    ["Dataset Summary", "Behavior-Based Filtering", "Predict Single Customer", "Predict from CSV"]
)

if option == "Dataset Summary":
    st.header("📊 Dataset Summary")
    uploaded_file = st.file_uploader("Upload Customer Dataset (CSV)", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("Preview of Dataset:")
        st.dataframe(df.head())
        st.write("Dataset Description:")
        st.write(df.describe())
        st.write("Missing Values:")
        st.write(df.isnull().sum())

elif option == "Behavior-Based Filtering":
    st.header("🎯 Filter Customers by Behavior Type")
    uploaded_file = st.file_uploader("Upload Customer Dataset (CSV)", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        # Assuming dataset has 'Annual Income (k$)' and 'Spending Score (1-100)' columns
        df['Behavior'] = df.apply(lambda row: get_behavior_label(row['Annual Income (k$)'], row['Spending Score (1-100)']), axis=1)
        behavior = st.selectbox("Select Behavior Type:", df['Behavior'].unique())
        st.dataframe(df[df['Behavior'] == behavior])

elif option == "Predict Single Customer":
    st.header("🧍 Predict Single Customer Cluster")
    gender = st.selectbox("Gender", ["Male", "Female"])
    income = st.number_input("Annual Income (k$)", 0, 150, 50)
    spending = st.number_input("Spending Score (1-100)", 0, 100, 50)
    if st.button("Predict Cluster"):
        gender_num = 1 if gender == "Male" else 0
        features = scaler.transform([[gender_num, income, spending]])
        cluster = model.predict(features)[0]
        behavior = get_behavior_label(income, spending)
        st.success(f"Predicted Cluster: {cluster} ({behavior})")

elif option == "Predict from CSV":
    st.header("📂 Predict Customer Clusters from File")
    uploaded_file = st.file_uploader("Upload Customer Dataset (CSV)", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        features = df[['Gender', 'Annual Income (k$)', 'Spending Score (1-100)']]
        features['Gender'] = features['Gender'].map({'Male':1, 'Female':0})
        scaled_features = scaler.transform(features)
        df['Cluster'] = model.predict(scaled_features)
        df['Behavior'] = df.apply(lambda row: get_behavior_label(row['Annual Income (k$)'], row['Spending Score (1-100)']), axis=1)
        st.write("Predicted Dataset:")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Predictions as CSV", data=csv, file_name="customer_predictions.csv", mime='text/csv')

# 📊 Visualization section (Optional for Dataset Summary or CSV Upload)
if option in ["Dataset Summary", "Predict from CSV"] and uploaded_file:
    try:
        fig, ax = plt.subplots()
        scatter = ax.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'], c=df['Cluster'], cmap='viridis', alpha=0.7)
        ax.set_xlabel("Annual Income (k$)")
        ax.set_ylabel("Spending Score (1-100)")
        ax.set_title("Customer Segments Visualization")
        plt.colorbar(scatter, ax=ax, label='Cluster')
        st.pyplot(fig)
    except Exception as e:
        st.warning("Visualization could not be generated. Ensure 'Annual Income (k$)', 'Spending Score (1-100)' and 'Cluster' columns exist.")

