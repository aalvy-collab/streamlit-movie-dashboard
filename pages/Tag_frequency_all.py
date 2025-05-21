import streamlit as st
import pandas as pd
import plotly.express as px


#Page configuration
st.set_page_config(page_title="Tag Trend Over Time", layout="wide")
st.title("Tag Frequency Over Time")
st.markdown("Explore how frequently selected tags were applied over time.")

#Load dataset
@st.cache_data
def load_data():
    tags = pd.read_csv("tags.csv", encoding="ISO-8859-1")
    clusters = pd.read_csv("movies_clustered.csv")
    tags['timestamp'] = pd.to_datetime(tags['timestamp'], unit='s')
    merged = pd.merge(tags, clusters[['movieId', 'cluster']], on='movieId', how='inner')
    return merged

merged = load_data()

#Tag selection
all_tags = sorted(merged['tag'].dropna().str.lower().unique())
default_tags = ["zombies", "romance", "time travel", "space", "superhero"]

selected_tags = st.multiselect(
    "Select tags to display:",
    options=all_tags,
    default=default_tags
)

#Filter data
filtered = merged[merged['tag'].str.lower().isin([tag.lower() for tag in selected_tags])].copy()
filtered['month'] = filtered['timestamp'].dt.to_period('M').dt.to_timestamp()

tag_trends = (
    filtered
    .groupby(['month', 'tag'])
    .size()
    .reset_index(name='count')
)

#Colourt chart
custom_colors = [
    "#E63946", "#457B9D", "#2A9D8F", "#F4A261", "#8E3B8E",
    "#1D3557", "#FF6B6B", "#3A86FF", "#8338EC", "#FFBE0B"
]

#Plot
if not tag_trends.empty:
    fig = px.area(
        tag_trends,
        x='month',
        y='count',
        color='tag',
        color_discrete_sequence=custom_colors,
        line_shape='spline',
        title=None,
        labels={'month': 'Month', 'count': 'Frequency', 'tag': 'Tag'},
        height=550
    )

    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            type='date',
            tickformat='%b %Y'
        ),
        yaxis_title='Tag Frequency',
        legend_title='Tag',
        plot_bgcolor='#fafafa',
        font=dict(family='Poppins', size=13),
        margin=dict(l=60, r=20, t=60, b=80)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("No data available for the selected tags.")

