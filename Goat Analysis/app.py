import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import io

plt.style.use("ggplot")

st.set_page_config(page_title="GOAT ANALYTICS", layout="wide")

st.sidebar.title("📊 Messi Extensive Analytics")
st.sidebar.image("messi.jpg", use_container_width=True)  # Updated from use_column_width

sections = [
    "Introduction", "Basic Exploration", "Goals per Competition", "Goals per Season", 
    "Goals per Club", "Goals per Playing Position", "Goals per Game Minute", "Goals per Type", 
    "Scoreline After Goals", "Opponents", "Favorite Opponents", "Assists", "Goals per Venue"
]

selections = st.sidebar.radio("Navigate to", sections)

# Load Data
@st.cache_data  
def load_data():
    df = pd.read_csv("data.csv")
    return df

df = load_data()

# --- Introduction ---
if selections == "Introduction":
    st.title("⚽ Messi - All Club Goals Statistics")
    st.subheader("The Greatest of All Time? Let’s Analyze!")

    st.write("""
    **Lionel Andrés Messi** is an Argentine professional footballer who plays as a forward for Inter Miami and captains the Argentina national team.
    
    - **Current team**: Inter Miami (#10 / Forward)
    - **Born**: June 24, 1987 (age 37 years), Rosario, Argentina
    - **Height**: 1.70 m
    - **Spouse**: Antonela Roccuzzo
    - **Ballon d'Or wins**: 8 (most in history)
    """)

# --- Basic Exploration ---
elif selections == "Basic Exploration":
    st.subheader("🔍 Basic Exploration")
    st.write("### Data Snapshot")
    st.dataframe(df.head())

    st.write("### Dataset Information")
    buffer = io.StringIO()
    df.info(buf=buffer)
    st.text(buffer.getvalue())

    st.write("### Unique Values in Each Column")
    unique_counts = pd.DataFrame(df.nunique(), columns=["Unique Values Count"])
    st.dataframe(unique_counts)

    st.write("### Summary Statistics for Categorical Columns")
    st.dataframe(df.describe(include=['object']).T)

# --- Goals per Competition ---
elif selections == "Goals per Competition":
    st.subheader("🏆 Goals per Competition")
    fig = px.histogram(df, x="Competition", color="Club", title="Goals per Competition", height=500)
    st.plotly_chart(fig)
    st.write("### Competition Goal Counts")
    st.dataframe(df["Competition"].value_counts())

# --- Goals per Season ---
elif selections == "Goals per Season":
    st.subheader("📅 Goals per Season")
    fig = px.histogram(df, x="Season", color="Club", title="Goals per Season", height=500)
    st.plotly_chart(fig)

# --- Goals per Club ---
elif selections == "Goals per Club":
    st.subheader("🏅 Goals per Club")
    fig1 = px.histogram(df, x="Club", color="Season", title="Goals per Club - Season", height=500)
    fig2 = px.histogram(df, x="Club", color="Competition", title="Goals per Club - Competition", height=500)
    st.plotly_chart(fig1)
    st.plotly_chart(fig2)

# --- Goals per Playing Position ---
elif selections == "Goals per Playing Position":
    st.subheader("⚽ Goals per Playing Position")
    fig = px.histogram(df, x="Playing_Position", color="Club", title="Goals per Playing Position", height=500)
    st.plotly_chart(fig)

# --- Goals per Game Minute ---
elif selections == "Goals per Game Minute":
    st.subheader("⏰ Goals per Game Minute")
    df["Minute"] = df["Minute"].str.extract("(\d+)").astype(float).fillna(0).astype(int)
    bins = [0, 15, 30, 45, 60, 75, 90, 105, 120]
    labels = ["0-15", "15-30", "30-45", "45-60", "60-75", "75-90", "90-105", "105-120"]
    df["Minute_Bin"] = pd.cut(df["Minute"], bins=bins, labels=labels, right=False)
    
    fig = px.histogram(df, x="Minute_Bin", color="Club", title="Goals per Game Minute", height=500)
    st.plotly_chart(fig)

# --- Goals per Type ---
elif selections == "Goals per Type":
    st.subheader("🏹 Goals per Type")
    fig = px.histogram(df, x="Type", color="Club", title="Goals per Type", height=500)
    st.plotly_chart(fig)

# --- Scoreline After Goals ---
elif selections == "Scoreline After Goals":
    st.subheader("🔢 Scoreline After Goals")
    top_20_scores = df["At_score"].value_counts().nlargest(20).index
    df_top_20 = df[df["At_score"].isin(top_20_scores)]

    fig, ax = plt.subplots(figsize=(15, 7))
    sns.countplot(x="At_score", data=df_top_20, order=top_20_scores, ax=ax)
    ax.set_title("Top 20 Scoresheets after Scoring", fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    for container in ax.containers:
      ax.bar_label(container)
    st.pyplot(fig)

# --- Opponents ---
elif selections == "Opponents":
    st.subheader("🆚 Opponents")
    top_20_opponents = df["Opponent"].value_counts().nlargest(20).index
    df_top_20 = df[df["Opponent"].isin(top_20_opponents)]

    fig, ax = plt.subplots(figsize=(30, 10))
    sns.countplot(x="Opponent", data=df_top_20, order=top_20_opponents, ax=ax)
    ax.set_title("Goals per Opponent", fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    for container in ax.containers:
      ax.bar_label(container)
    st.pyplot(fig)

# --- Favorite Opponents ---
elif selections == "Favorite Opponents":
    st.subheader("❤️ Favorite Opponents")
    fav_opponents = df["Opponent"].value_counts()[df["Opponent"].value_counts() > 15]
    
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.countplot(x="Opponent", data=df[df["Opponent"].isin(fav_opponents.index)], order=fav_opponents.index, ax=ax)
    ax.set_title("Favorite Opponents", fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    for container in ax.containers:
      ax.bar_label(container)
    st.pyplot(fig)

# --- Assists ---
elif selections == "Assists":
    st.subheader("🤝 Assists")
    top_10_assists = df["Goal_assist"].value_counts().nlargest(10).index
    df_top_10 = df[df["Goal_assist"].isin(top_10_assists)]

    fig, ax = plt.subplots(figsize=(15, 7))
    sns.countplot(x="Goal_assist", data=df_top_10, order=top_10_assists, ax=ax)
    ax.set_title("Top 10 Assists", fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    for container in ax.containers:
      ax.bar_label(container)
    st.pyplot(fig)

# --- Goals per Venue ---
elif selections == "Goals per Venue":
    st.subheader("🏟️ Goals per Venue")
    fig, ax = plt.subplots(figsize=(15, 7))
    sns.countplot(x="Venue", data=df, order=df["Venue"].value_counts().index, ax=ax)
    ax.set_title("Goals per Venue", fontsize=20)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    for container in ax.containers:
      ax.bar_label(container)
    st.pyplot(fig)
