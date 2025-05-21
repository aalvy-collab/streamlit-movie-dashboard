import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch

st.set_page_config(page_title="Tag Trends Over Time", layout="wide")
st.title("Tag Trends Over Time")
st.markdown("Explore tag frequency and unique movie counts over time by selecting tags below.")


#Load dataset
@st.cache_data
def load_tags():
    return pd.read_csv("tags.csv", encoding="ISO-8859-1")

tags_df = load_tags()

@st.cache_data
def load_movies_clustered():
    return pd.read_csv("movies_clustered.csv", encoding="ISO-8859-1")

movies_clustered_df = load_movies_clustered()

# Convert timestamps
tags_df['timestamp'] = pd.to_datetime(tags_df['timestamp'], unit='s')

tags_df['timestamp'] = pd.to_datetime(tags_df['timestamp'], unit='s')
tags_df['tag'] = tags_df['tag'].str.lower()

merged = pd.merge(tags_df, movies_clustered_df[['movieId', 'cluster']], on='movieId', how='inner')
merged['month'] = merged['timestamp'].dt.to_period('M').dt.to_timestamp()

all_tags = sorted(merged['tag'].dropna().unique())


# Colour palette 
custom_colors = [
    "#E63946", "#457B9D", "#2A9D8F", "#F4A261", "#8E3B8E",
    "#1D3557", "#FF6B6B", "#3A86FF", "#8338EC", "#FFBE0B",
    "#264653", "#A8DADC", "#F77F00"
]

# Tags for Frequency

selected_freq_tags = st.multiselect(
	"ags for Frequency Chart:",
	options=all_tags,
    	default=["zombies", "romance"]
)

# Chart
if selected_freq_tags:
    freq_filtered = merged[merged['tag'].isin(selected_freq_tags)]
    freq_trend = (
        freq_filtered.groupby(['month', 'tag'])
        .size()
        .reset_index(name='count')
    )

    freq_fig = px.area(
        freq_trend,
        x='month',
        y='count',
        color='tag',
        title="Tag Frequency Over Time",
        labels={'count': 'Frequency', 'month': 'Month'},
        color_discrete_sequence=custom_colors
    )

    freq_fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True), type='date'),
        height=500
    )

    st.plotly_chart(freq_fig, use_container_width=True)

#Unique movies tags
selected_unique_tags = st.multiselect(
	"Tags for Unique Movie Chart:",
	options=all_tags,
    default=["zombies", "romance"]
)

# Unique Movies Chart

if selected_unique_tags:
    unique_filtered = merged[merged['tag'].isin(selected_unique_tags)]
    unique_trend = (
        unique_filtered.groupby(['month', 'tag'])['movieId']
        .nunique()
        .reset_index(name='unique_movie_count')
    )

    unique_fig = px.area(
        unique_trend,
        x='month',
        y='unique_movie_count',
        color='tag',
        title="Unique Movies Tagged Over Time",
        labels={'unique_movie_count': 'Unique Movies', 'month': 'Month'},
        color_discrete_sequence=custom_colors
    )

    unique_fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True), type='date'),
        height=500
    )

    st.plotly_chart(unique_fig, use_container_width=True)

