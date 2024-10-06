
import plotly.express as px
import plotly.graph_objects as go
from dash import html



def line_plot(x,y,mode,name,yaxis_='y1', color_='yellow'):
    return go.Scatter(
            x=x ,
            y=y,
            mode=mode,
            name=name,
            line=dict(color=color_),
            yaxis=yaxis_,
        )




def create_card(id, title, value):
    return html.Div(
        className="card",
        children=[
            html.Div(className="card-body", children=[
                html.H5(title, className="card-title"),
                html.P(value, className="card-text", id=id)
            ])
        ]
    )