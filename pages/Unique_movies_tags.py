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
from IPython.display import display, HTML
import scipy.cluster.hierarchy as sch
import ipywidgets as widgets


#Load dataset
tags_df = pd.read_csv("tags.csv", encoding="ISO-8859-1")
movies_clustered_df = pd.read_csv("movies_clustered.csv")

#Convert timestamp
tags_df['timestamp'] = pd.to_datetime(tags_df['timestamp'], unit='s')

#Merge clusters
merged = pd.merge(tags_df, movies_clustered_df[['movieId', 'cluster']], on='movieId', how='inner')

#Normalize tags
merged['tag'] = merged['tag'].str.lower()
all_tags = sorted(merged['tag'].dropna().unique())

#Colour palette
custom_colors = [
    "#E63946", "#457B9D", "#2A9D8F", "#F4A261", "#8E3B8E",
    "#1D3557", "#FF6B6B", "#3A86FF", "#8338EC", "#FFBE0B",
    "#264653", "#A8DADC", "#F77F00"
]

#Dropdown menu frequency
dropdown1 = widgets.SelectMultiple(
    options=all_tags,
    value=("zombies", "romance"),
    description='Frequency Tags:',
    layout=widgets.Layout(width='50%'),
    style={'description_width': 'initial'}
)

#Dropdown menu unique movies
dropdown2 = widgets.SelectMultiple(
    options=all_tags,
    value=("zombies", "romance"),
    description='Unique Tags:',
    layout=widgets.Layout(width='50%'),
    style={'description_width': 'initial'}
)

#Frequency tags added
def update_tag_frequency(tags):
    filtered = merged[merged['tag'].isin(tags)].copy()
    filtered['month'] = filtered['timestamp'].dt.to_period('M').dt.to_timestamp()
    trend = (
        filtered.groupby(['month', 'tag'])
        .size()
        .reset_index(name='count')
    )
    fig = px.area(
        trend, x='month', y='count', color='tag',
        title="Tag Frequency Over Time",
        labels={'count': 'Frequency', 'month': 'Month'},
        color_discrete_sequence=custom_colors
    )
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True), type='date'),
        height=500
    )
    fig.show()

#Unique movies chart

def update_unique_movies(tags):
    filtered = merged[merged['tag'].isin(tags)].copy()
    filtered['month'] = filtered['timestamp'].dt.to_period('M').dt.to_timestamp()
    trend = (
        filtered.groupby(['month', 'tag'])['movieId']
        .nunique()
        .reset_index(name='unique_movie_count')
    )
    fig = px.area(
        trend, x='month', y='unique_movie_count', color='tag',
        title="Unique Movies Tagged Over Time",
        labels={'unique_movie_count': 'Unique Movies', 'month': 'Month'},
        color_discrete_sequence=custom_colors
    )
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True), type='date'),
        height=500
    )
    fig.show()

#Link dropdown menus
widgets.interact(update_tag_frequency, tags=dropdown1)
widgets.interact(update_unique_movies, tags=dropdown2)




