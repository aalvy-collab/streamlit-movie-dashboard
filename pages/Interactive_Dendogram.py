import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import leaves_list

# Page config
st.set_page_config(page_title="Interactive Dendrogram", layout="wide")
st.title("Interactive Dendrogram")
st.markdown("Visualizing hierarchical similarity between movie clusters based on genre distributions.")

# Load data
df = pd.read_csv("cluster_final.csv")
genre_columns = df.columns[3:]
data = df[genre_columns].values

# Labels
cluster_labels = [
    "Horror Fans", "Comedy Fans", "Family Friendly",
    "Drama Buffs", "Action Junkies", "Doc Watchers", "History Fiends"
]

# Linkage matrix
linkage_matrix = sch.linkage(data, method='ward')

# Match leaf order to linkage
leaf_order = leaves_list(linkage_matrix)
ordered_labels = [cluster_labels[i] for i in leaf_order]

# Dendrogram without plot
dendro = sch.dendrogram(linkage_matrix, labels=ordered_labels, orientation='top', no_plot=True)
icoord = np.array(dendro['icoord'])
dcoord = np.array(dendro['dcoord'])

# Create Plotly figure
fig = go.Figure()

# Add lines
for i in range(len(icoord)):
    fig.add_trace(go.Scatter(
        x=icoord[i],
        y=dcoord[i],
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none'
    ))

# Style layout
fig.update_layout(
    title="Cluster Similarity by Genre Profile",
    xaxis=dict(
        tickvals=[(x[1] + x[2]) / 2 for x in icoord],
        ticktext=ordered_labels,
        tickangle=45,
        title='Clusters',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title='Distance',
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    margin=dict(l=60, r=40, t=60, b=80),
    height=550,
    showlegend=False,
    font=dict(family='Poppins', size=14)
)

st.plotly_chart(fig, use_container_width=True)