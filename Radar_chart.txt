import streamlit as st
import pandas as pd
import plotly.graph_objects as go

#Page config
st.set_page_config(page_title="Cluster Radar Chart", layout="wide")
st.title("Cluster Comparison – Genre Radar Chart")
st.markdown("Each colored shape shows a cluster's genre preference profile across top genres.")

#Load dataset
df = pd.read_csv("cluster_final.csv")
genre_columns = df.columns[3:]

#Assign labels
cluster_labels = [
    "Horror Fans", "Comedy Fans", "Family Friendly",
    "Drama Buffs", "Action Junkies", "Doc Watchers", "History Fiends"
]
df['cluster_label'] = cluster_labels

#Colour map
hex_colors = [
    "#D72631",  # Red
    "#0F4C81",  # Blue
    "#007F5F",  # Green
    "#332F3E",  # Dark Gray
    "#FF5A1F",  # Orange
    "#8E3B8E",  # Purple
    "#17BEBB"   # Teal
]
color_map = dict(zip(cluster_labels, hex_colors))

#Top genres, average across clusters
avg_importance = df[genre_columns].mean().sort_values(ascending=False)
top_genres = avg_importance.head(8).index.tolist()

#Radar chart
fig = go.Figure()

for i, row in df.iterrows():
    cluster = row['cluster_label']
    values = row[top_genres].tolist()
    values += [values[0]] 

 fig.add_trace(go.Scatterpolar(
        r=values,
        theta=top_genres + [top_genres[0]],
        name=cluster,
        line=dict(color=color_map[cluster], width=2),
        fill='toself',
        opacity=0.4
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(size=12)),
        angularaxis=dict(tickfont=dict(size=13))
    ),
    title=dict(
    	text="enre Preference Profiles Across Clusters",
        font=dict(size=24),
        x=0.5,
        xanchor='center'
    ),
    font=dict(family='Poppins', size=14),
    showlegend=True,
    height=700
)

#Plot
st.plotly_chart(fig, use_container_width=True)
