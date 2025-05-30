# -*- coding: utf-8 -*-
"""Flipkart_SentimentalAnalysis.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1EuZNg3UI3Abzs0UXSC-KLHCs_OcK5emf
"""

!pip install streamlit

!pip install pyngrok

!ngrok authtoken 2uOOgR7354izHGpF5fMFYLKnG4I_5iJho2gVRdjYo7hcpy7hS

with open('app.py', 'w') as f:
    f.write("""
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, ConfusionMatrixDisplay
import re

# Load Data
st.title("Sentiment Analysis Model")

uploaded_file = st.file_uploader("Upload your dataset (CSV format)", type=["csv"])
if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file, encoding='ISO-8859-1').fillna('')

        # Data Cleaning and Sentiment Creation
        df['Product_name'] = df['Product_name'].astype(str).str.encode('ascii', 'ignore').str.decode('ascii').str.strip()

        if 'Review' in df.columns and 'Rate' in df.columns:
            df.dropna(subset=['Review', 'Rate'], inplace=True)
            df['Rate'] = df['Rate'].astype(str).str.strip()
            df = df[df['Rate'].str.isnumeric()]
            df['Rate'] = df['Rate'].astype(int)

            df['Sentiment'] = df['Rate'].apply(lambda x: 'Positive' if x >= 4
                                               else 'Neutral' if x == 3
                                               else 'Negative')

            # Visualization: Sentiment Distribution
            st.subheader("Sentiment Distribution")
            fig, ax = plt.subplots(figsize=(7, 5))
            sns.countplot(x='Sentiment', data=df, palette='viridis', ax=ax)
            st.pyplot(fig)

            # Feature and Target Selection
            X = df['Review']
            y = df['Sentiment']

            # Text Vectorization
            vectorizer = CountVectorizer(stop_words='english')
            X_vectorized = vectorizer.fit_transform(X)

            # Train-Test Split
            X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.3, random_state=42)

            # Model Training
            model = MultinomialNB()
            model.fit(X_train, y_train)

            # Predictions and Evaluation
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            st.subheader(f"Accuracy: {accuracy:.2f}")

            # Displaying Classification Report as Table
            df_report = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose().round(2)
            st.subheader("Classification Report Table")
            st.dataframe(df_report)

            # Visualization: Confusion Matrix
            st.subheader("Confusion Matrix")
            fig, ax = plt.subplots(figsize=(7, 5))
            cm = confusion_matrix(y_test, y_pred, labels=['Positive', 'Neutral', 'Negative'])
            disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['Positive', 'Neutral', 'Negative'])
            disp.plot(cmap='viridis', ax=ax)
            st.pyplot(fig)

            # New Feature: Sentiment Analysis by Item
            st.subheader("Sentiment Analysis by Item")
            item_input = st.text_input("Enter the item name for sentiment analysis:")

            def analyze_item_sentiment(item_name):
                item_data = df[df['Product_name'].str.contains(re.escape(item_name), case=False, na=False)]
                if item_data.empty:
                    st.warning(f"No data found for item: {item_name}")
                    return

                sentiment_counts = item_data['Sentiment'].value_counts()

                st.subheader(f"Sentiment Analysis for '{item_name}':")
                st.write(sentiment_counts)

                fig, ax = plt.subplots(figsize=(6, 6))
                plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', colors=['green', 'grey', 'red'])
                plt.title(f'Sentiment Distribution for {item_name}')
                st.pyplot(fig)

            if item_input:
                analyze_item_sentiment(item_input)
        else:
            st.error("Error: Columns 'Review' or 'Rate' not found.")
    except Exception as e:
        st.error(f"Error loading data: {e}")
# Ngrok Integration
import os
from pyngrok import ngrok

if __name__ == '__main__':
    public_url = ngrok.connect(8501).public_url
    print(f'Your Streamlit app is live at: {public_url}')
    os.system("streamlit run app.py")
""")

from pyngrok import ngrok
import os
import threading

# Start ngrok tunnel
public_url = ngrok.connect(8501).public_url
print(f'Your Streamlit app is live at: {public_url}')

# Run Streamlit app in a separate thread
def run_streamlit():
    os.system("streamlit run app.py")

thread = threading.Thread(target=run_streamlit)
thread.start()

!streamlit run app.py