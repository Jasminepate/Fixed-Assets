#!?/usr/bin/python3

import dash
import flask
import dash.dependencies
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd


app = dash.Dash()
df = pd.read_csv("purchases-of-fixed-assets-by-type-and-economic-activity.csv", delimiter=";")
assets = df["Type of Fixed Assets"].unique()
ea = df["Economic Activity"].unique()

app.layout = html.Div([
                       html.Div(children="Select Fixed Asset and hover over marks to display \n"
                                         " detailed view of the Economic Activity."),
    html.H1(["Purchases of Fixed Assets"],
            style={"marginLeft": "400"}),
    html.Div(children="Fixed Asset"),
    html.Div([
        dcc.Dropdown(id="assets",
                     options=[{"label": i, "value": i} for i in assets],
                     value="Land and Buildings"
                     ),
        dcc.Graph(id="economic-graph"),
        dcc.Slider(id='year-slider',
                   min=df["Year"].min(),
                   max=df["Year"].max(),
                   value=df["Year"].min(),
                   step=None,
                   marks={str(year): str(year) for year in df["Year"].unique()}
                   )],
        style={'width': '40%', 'display': 'inline-block'}),

    html.Div([
        dcc.Graph(id="economic-display")],
        style={"display": "inline-block"}
    )])


@app.callback(
    dash.dependencies.Output("economic-graph", "figure"),
    [dash.dependencies.Input("assets", "value"),
     dash.dependencies.Input("year-slider", "value")])
def update_graph(asset_value, year_value):
    dff = df[df["Year"] == year_value]

    callback = {"data": [go.Scatter(
        x=(dff[dff["Type of Fixed Assets"] == asset_value]["Purchases in Thousands SR"]),
        y=df["Purchases in Thousands SR"],
        text=dff[dff["Type of Fixed Assets"] == asset_value]["Economic Activity"],
        mode="markers",
        marker={"size": 14, "opacity": 0.5, "line": {"width": 1, "color": "black"}},
        hoverlabel={"bgcolor": "blue"})],

        "layout": go.Layout(
            xaxis={"title": asset_value, "type": "linear"},
            yaxis={"title": "Purchases in Thousands SR", "type": "linear"},
            margin={"l": 50, "b": 40, "t": 10, "r": 0},
            hovermode="closest"
        )}

    return callback


@app.callback(
    dash.dependencies.Output("economic-display", "figure"),
    [dash.dependencies.Input("economic-graph", "hoverData")])
def detail_graph(economic):

    try:
        e_value = economic['points'][0]['text']
    except TypeError:
        e_value = "Total"

    dff = df[df["Economic Activity"] == e_value]
    callback = {"data": [

        go.Bar(
            x=df["Year"].unique(),
            y=dff[dff["Type of Fixed Assets"] == "Land and Buildings"]["Purchases in Thousands SR"],
            name="Land and Buildings",
            marker=go.Marker(
                color='rgb(72, 229, 36)'),
            hoverinfo="y"),

        go.Bar(
            x=df["Year"].unique(),
            y=dff[dff["Type of Fixed Assets"] == "Transportation Equipment"]["Purchases in Thousands SR"],
            name="Transportation Equipment",
            marker=go.Marker(
                color='rgb(43, 67, 219)'),
            hoverinfo="y"),

        go.Bar(
            x=df["Year"].unique(),
            y=dff[dff["Type of Fixed Assets"] == "Furniture"]["Purchases in Thousands SR"],
            name="Furniture",
            marker=go.Marker(
                color='rgb(228, 239, 14)'),
            hoverinfo="y"),

        go.Bar(
            x=df["Year"].unique(),
            y=dff[dff["Type of Fixed Assets"] == "Other assets"]["Purchases in Thousands SR"],
            name="Other assets",
            marker=go.Marker(
                color='rgb(242, 2, 2)'),
            hoverinfo="y"),

        go.Bar(
            x=df["Year"].unique(),
            y=dff[dff["Type of Fixed Assets"] == "Other Eqiupment"]["Purchases in Thousands SR"],
            name="Other Eqiupment",
            marker=go.Marker(
                color='rgb(244, 244, 2)'),
            hoverinfo="y"),

        go.Bar(
            x=df["Year"].unique(),
            y=dff[dff["Type of Fixed Assets"] == "Total"]["Purchases in Thousands SR"],
            name="Total",
            marker=go.Marker(
                color='rgb(197, 47, 226)'),
            hoverinfo="y"
        )],

        "layout": go.Layout(
            xaxis={"title": e_value, "type": "linear"},
            margin={"t": 10, "r": 0}
        )}
    return callback


if __name__ == "__main__":
    app.run_server(host='0.0.0.0', port=80)
