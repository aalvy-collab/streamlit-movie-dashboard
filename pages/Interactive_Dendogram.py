import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import scipy.cluster.hierarchy as sch

# --- Streamlit page config ---
st.set_page_config(page_title="Interactive Dendrogram", layout="wide")
st.title("Interactive Dendrogram")
st.markdown("Visualizing hierarchical similarity between movie clusters based on genre distributions.")

# ---Load data ---
@st.cache_data
def load_data():
    df = pd.read_csv("cluster_final.csv")
    return df

df = load_data()

# --- Define cluster labels ---
cluster_labels = [
    "Horror Fans", "Comedy Fans", "Family Friendly",
    "Drama Buffs", "Action Junkies", "Doc Watchers", "History Fiends"
]

df['cluster_label'] = cluster_labels

# Genre Data
genre_columns = df.columns[3:-1] 
data = df[genre_columns].values


# Generate linkage matrix and dendrogram info 
linkage_matrix = sch.linkage(data, method='ward')
dendro = sch.dendrogram(linkage_matrix, labels=cluster_labels, orientation='top', no_plot=True)

# Extract coordinates 
icoord = np.array(dendro['icoord'])
dcoord = np.array(dendro['dcoord'])
labels = dendro['ivl']
tick_vals = [(x[1] + x[2]) / 2 for x in icoord]

# Plot
fig = go.Figure()

for i in range(len(icoord)):
    fig.add_trace(go.Scatter(
        x=icoord[i],
        y=dcoord[i],
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none'
    ))

# layout 
fig.update_layout(
    title=dict(
        text="Cluster Similarity by Genre",
        x=0.5,
        font=dict(size=22)
    ),
    xaxis=dict(
        tickvals=tick_vals,
        ticktext=labels,
        tickangle=45,
        title='Clusters',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title='Distance',
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    height=550,
    margin=dict(l=60, r=40, t=60, b=80),
    font=dict(family='Poppins', size=14)
)

# Plot
st.plotly_chart(fig, use_container_width=True)