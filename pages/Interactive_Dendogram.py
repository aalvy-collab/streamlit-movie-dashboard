import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import plotly.graph_objects as go

#Load dataset

df = pd.read_csv("cluster_final.csv")
genre_columns = df.columns[3:]
data = df[genre_columns].values


#Cluster Labels

labels = [
    "Horror Fans", "Comedy Fans", "Family Friendly",
    "Drama Buffs", "Action Junkies", "Doc Watchers", "History Fiends"
]

#Linkage matrix
linkage_matrix = sch.linkage(data, method='ward')

#Dendogram
dendro = sch.dendrogram(linkage_matrix, labels=labels, orientation='top', no_plot=True)

#Data for plot
icoord = np.array(dendro['icoord'])
dcoord = np.array(dendro['dcoord'])
leaf_labels = dendro['ivl']

#Plot
fig = go.Figure()

#Add trace lines
for i in range(len(icoord)):
    fig.add_trace(go.Scatter(
        x=icoord[i],
        y=dcoord[i],
        mode='lines',
        line=dict(color='black', width=2),
        hoverinfo='none'
    ))

#Add Labels
fig.update_layout(
    title="Interactive Dendrogram – Cluster Similarity by Genre"
xaxis=dict(
        tickvals=[(x[1] + x[2]) / 2 for x in icoord],
        ticktext=leaf_labels,
        tickfont=dict(size=12),
        title='Clusters'
)
yaxis=dict(
        title='Distance',
        tickfont=dict(size=12)
    ),
    plot_bgcolor='white',
    margin=dict(l=60, r=20, t=60, b=80),
    height=500
)

fig.show()
