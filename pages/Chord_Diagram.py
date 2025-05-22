import streamlit as st
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import holoviews as hv
from holoviews import opts
hv.extension('bokeh')

# Main Header
st.set_page_config(page_title="Chord Diagram", layout="wide")

st.title("Genre Similarity Between Clusters")
st.markdown("Explore how movie clusters are connected through shared genre preferences.")

#Load Data
@st.cache_data
def load_data():
    return pd.read_csv("cluster_final.csv")

df = load_data()

# Labels
cluster_labels = [
    "Horror Fans", "Comedy Fans", "Family Friendly",
    "Drama Buffs", "Action Junkies", "Doc Watchers", "History Fiends"
]
df['cluster_label'] = cluster_labels


# Isolate genre columns
genre_columns = df.columns[3:-1]
genre_data = df[genre_columns].values

# Cluster similarity
similarity = cosine_similarity(genre_data)

# Info for chords
chord_links = []
for i in range(len(cluster_labels)):
    for j in range(i + 1, len(cluster_labels)):
        weight = similarity[i][j]
        if weight > 0.15:
            chord_links.append((cluster_labels[i], cluster_labels[j], round(weight, 2)))


# Chord plot
chord = hv.Chord((chord_links, hv.Dataset(pd.DataFrame(cluster_labels, columns=["cluster"]))))
chord = chord.opts(
    opts.Chord(
        labels='cluster',
        node_color='cluster',
        edge_color='source',
        cmap='Category20',
        edge_alpha=0.7,
        node_size=15,
        width=700,
        height=600,
        title="Cluster Genre Overlap – Chord Diagram"
    )
)
st.bokeh_chart(hv.render(chord, backend='bokeh'), use_container_width=True)
