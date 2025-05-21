import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib.colors import rgb2hex
import seaborn as sns

# Page configuration
st.set_page_config(page_title="Movie Clusters", layout="wide")

# Load dataset 
df = pd.read_csv("cluster_final.csv")

# Define cluster labels
cluster_labels = [
    "Horror Fans", "Comedy Fans", "Family Lovers",
    "Drama Buffs", "Action Junkies", "Doc Watchers", "History Crowd"
]
df['cluster_label'] = cluster_labels

# Calculate genre diversity
genre_columns = df.columns[3:-1]  # Adjust if needed
df['genre_diversity'] = (df[genre_columns] > 0.05).sum(axis=1)

# Find top genres for dropdown labels
df['top_genres'] = df[genre_columns].apply(lambda row: row.nlargest(2).index.tolist(), axis=1)
df['dropdown_label'] = df.apply(
    lambda row: f"{row['cluster_label']} — Top: {', '.join(row['top_genres'])}",
    axis=1
)

# Custom colours
cluster_colors = [
    "#E63946", "#457B9D", "#2A9D8F",
    "#1D3557", "#F28482", "#6D597A", "#264653"
]
color_map = dict(zip(cluster_labels, cluster_colors))

# Header Title
st.title("How Do Movie Clusters Behave?")
st.markdown("Visualizing cluster-level movie rating behavior for personalized insight.")

# Scatterplot
fig = px.scatter(
    df,
    x='avg_rating',
    y='rating_count',
    size='genre_diversity',
    color='cluster_label',
    color_discrete_map=color_map,
    text='cluster_label',
    height=600
)

# Add styling
fig.update_traces(
    textposition="top center",
    textfont=dict(size=14),
    marker=dict(line=dict(width=1, color='black'))
)

fig.update_layout(
    showlegend=False,
    plot_bgcolor="#fafafa",
    font=dict(family="Poppins", size=14),
    margin=dict(t=60, l=80, r=40, b=40),
    title=dict(
	text"How Do Movie Clusters Behave?"
	 font=dict(size=26),
        x=0.5,
        xanchor='center'
    ),
	xaxis=dict(
        title="Average Rating",
        title_font=dict(size=18),
        tickfont=dict(size=14),
        title_standoff=20
    ),
    yaxis=dict(
        title="Total Ratings",
        title_font=dict(size=18),
        tickfont=dict(size=14),
        title_standoff=30
    )
)

# Plot
st.plotly_chart(fig, use_container_width=True)

