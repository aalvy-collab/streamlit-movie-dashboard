import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(page_title="Unique Movies per Tag", layout="wide")
st.title("Unique Movies per Tag Over Time")
st.markdown("This chart tracks the number of unique movies associated with selected tags per month.")

# Load data
tags_df = pd.read_csv("tags.csv", encoding="ISO-8859-1")
movies_df = pd.read_csv("movies_clustered.csv")

# Convert timestamp to datetime
tags_df['timestamp'] = pd.to_datetime(tags_df['timestamp'], unit='s')

# Merge tag + movie cluster info
merged = pd.merge(tags_df, movies_df[['movieId', 'cluster']], on='movieId', how='inner')

# Add month column
merged['month'] = merged['timestamp'].dt.to_period('M').dt.to_timestamp()

# Build list of popular tags
tag_counts = merged['tag'].value_counts()
popular_tags = tag_counts[tag_counts > 50].index.tolist()  # threshold to avoid noise

# --- Streamlit dropdown ---
selected_tags = st.multiselect(
    "Select tags to visualize:",
    options=popular_tags,
    default=["zombies", "romance"]
)

# Filter by selected tags
filtered = merged[merged['tag'].isin(selected_tags)]

# Group by tag and month, count unique movies
tag_trend = (
    filtered.groupby(['month', 'tag'])['movieId']
    .nunique()
    .reset_index(name='unique_movies')
)

# --- Plot ---
fig = px.area(
    tag_trend,
    x='month',
    y='unique_movies',
    color='tag',
    title="Number of Unique Movies Tagged Per Month",
    labels={'unique_movies': 'Unique Movies', 'month': 'Month'},
    height=550
)

fig.update_layout(
    xaxis=dict(rangeslider=dict(visible=True), tickformat='%b %Y'),
    plot_bgcolor="#f9f9f9",
    font=dict(family="Poppins", size=14),
    margin=dict(t=60, l=60, r=30, b=60)
)

st.plotly_chart(fig, use_container_width=True)




