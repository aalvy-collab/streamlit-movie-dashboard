import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.colors import rgb2hex 
import numpy as np
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as sch


#Page configuration
st.set_page_config(page_title="Radar Chart", layout="wide")
st.title("Radar Chart of Genres Represented by Cluster")
st.markdown("This chart shows the top 8 genre preferences for each movie cluster.")

#Load database
@st.cache_data
def load_data():
    df = pd.read_csv("cluster_final.csv")
    return df

df = load_data()
genre_columns = df.columns[3:]


#Cluster labels
cluster_labels = [
    "Horror Fans", "Comedy Fans", "Family Friendly",
    "Drama Buffs", "Action Junkies", "Doc Watchers", "History Fiends"
]
df["cluster_label"] = cluster_labels

#Colour palette
hex_colors = [
    "#D72631",  # Horror Fans
    "#0F4C81",  # Comedy Fans
    "#007F5F",  # Family Friendly
    "#332F3E",  # Drama Buffs
    "#FF5A1F",  # Action Junkies
    "#8E3B8E",  # Doc Watchers
    "#17BEBB"   # History Fiends
]
color_map = dict(zip(cluster_labels, hex_colors))

#Top eight genres
top_genres = genre_columns[:8].tolist()

#Chart
fig = go.Figure()

for i, row in df.iterrows():
    values = row[top_genres].tolist() + [row[top_genres[0]]]
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=top_genres + [top_genres[0]],
        name=row['cluster_label'],
        fill='toself',
        opacity=0.45,
        line=dict(color=color_map[row['cluster_label']], width=2)
    ))

#Plot
fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(size=12)),
        angularaxis=dict(tickfont=dict(size=13))
    ),
    title=dict(
        text="Top 8 Genre Profiles Across Clusters",
        font=dict(size=18),
        x=0.5,
        xanchor='center'
    ),
    font=dict(family='Poppins', size=14),
    showlegend=True,
    height=700
)

# --- DISPLAY CHART ---
st.plotly_chart(fig, use_container_width=True)






