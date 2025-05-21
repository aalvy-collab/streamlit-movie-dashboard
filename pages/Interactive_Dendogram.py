import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import scipy.cluster.hierarchy as sch

# Page configuration
st.set_page_config(page_title="Interactive Dendrogram", layout="wide")

# Load dataset
df = pd.read_csv("cluster_final.csv")
genre_columns = df.columns[3:]
data = df[genre_columns].values

# Cluster Labels
labels = [
    "Horror Fans", "Comedy Fans", "Family Friendly",
    "Drama Buffs", "Action Junkies", "Doc Watchers", "History Fiends"
]

# Linkage matrix
linkage_matrix = sch.linkage(data, method='ward')

# Dendrogram without plotting
dendro = sch.dendrogram(linkage_matrix, labels=labels, orientation='top', no_plot=True)

icoord = np.array(dendro['icoord'])
dcoord = np.array(dendro['dcoord'])
leaf_labels = dendro['ivl']

# Create Plotly figure
fig = go.Figure()

# Add dendrogram lines
for i in range(len(icoord)):
    fig.add_trace(go.Scatter(
        x=icoord[i],
        y=dcoord[i],
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none'
    ))

# Update layout
fig.update_layout(
    title="Interactive Dendrogram – Cluster Similarity by Genre",
    xaxis=dict(
        tickvals=[(x[1] + x[2]) / 2 for x in icoord],
        ticktext=leaf_labels,
        tickfont=dict(size=12),
        title='Clusters'
    ),
    yaxis=dict(
        title='Distance',
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    margin=dict(l=60, r=20, t=60, b=80),
    height=500
)

# Render in Streamlit
st.title("Interactive Dendrogram")
st.markdown("Visualizing hierarchical similarity between movie clusters based on genre distributions.")
st.plotly_chart(fig, use_container_width=True)
