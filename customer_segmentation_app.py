import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt

# Load saved model and scaler
model = pickle.load(open('kmeans_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))

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

st.set_page_config(page_title="Customer Segmentation Tool", layout="wide")
st.title("🛍️ Customer Segmentation & Behavior Analysis App")

# Tab-based interface
tab1, tab2, tab3 = st.tabs(["📊 Dataset Summary + Predict", "🎯 Behavior-Based Filtering", "👤 Predict Single Customer"])

with tab1:
    st.header("📊 Dataset Summary + Predict")
    uploaded_file = st.file_uploader("Upload Customer Dataset (CSV)", type=['csv'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write("### Preview of Dataset:")
        st.dataframe(df.head())

        st.write("### Dataset Description:")
        st.write(df.describe())
        st.write("Missing Values:")
        st.write(df.isnull().sum())

        if st.button("Run Predictions for This Dataset"):
            features = df[['Annual Income (k$)', 'Spending Score (1-100)']]
            scaled_features = scaler.transform(features)
            df['Cluster'] = model.predict(scaled_features)
            df['Behavior'] = df.apply(lambda row: get_behavior_label(row['Annual Income (k$)'], row['Spending Score (1-100)']), axis=1)
            st.success("✅ Predictions completed. 'Cluster' and 'Behavior' columns added.")
            st.write("### Dataset with Predictions:")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Predicted Dataset", data=csv, file_name="predicted_customers.csv", mime='text/csv')

            try:
                fig, ax = plt.subplots(figsize=(10, 6))
                scatter = ax.scatter(df['Annual Income (k$)'], df['Spending Score (1-100)'], c=df['Cluster'], cmap='viridis', alpha=0.7)
                ax.set_xlabel("Annual Income (k$)")
                ax.set_ylabel("Spending Score (1-100)")
                ax.set_title("Customer Segments Visualization")
                plt.colorbar(scatter, ax=ax, label='Cluster')
                st.pyplot(fig)
            except Exception as e:
                st.warning("⚠️ Visualization could not be generated.")

with tab2:
    st.header("🎯 Filter Customers by Behavior Type")
    uploaded_file = st.file_uploader("Upload Customer Dataset (CSV)", type=['csv'], key="filter")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        if 'Behavior' not in df.columns:
            st.warning("⚠️Please use the Predicted Dataset with 'Behaviour' and 'Cluster' columns generated in the 'Dataset Summary + Predict' tab")
        else:
            behavior = st.selectbox("Select Behavior Type:", df['Behavior'].unique())
            st.dataframe(df[df['Behavior'] == behavior])

with tab3:
    st.header("👤 Predict Single Customer Segment")
    income = st.number_input("Annual Income (k$)", 0, 150, 50)
    spending = st.number_input("Spending Score (1-100)", 0, 100, 50)
    if st.button("Predict Customer Segment"):
        input_data = scaler.transform([[income, spending]])
        cluster = model.predict(input_data)[0]
        behavior = get_behavior_label(income, spending)
        st.success(f"Predicted Cluster: {cluster} ({behavior})")
