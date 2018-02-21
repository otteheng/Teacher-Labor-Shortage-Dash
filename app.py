# Dependencies for project
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State

# Saved on Github
excel = pd.read_excel('https://github.com/otteheng/Teacher-Labor-Shortage-Dash/blob/master/Data/Aggregated%20Number%20of%20Degrees%20in%20Education%20(Reshaped%20long%20long)%20(Renamed).xlsx?raw=true')

app = dash.Dash()

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

df = excel2

state = df['state_long'].unique()
available_indicators = ['State Total', 'Bachelor Total', 'Masters Total', 'PhD Total', 'Elementary Total', 'SPED Total',
                        'STEM Total', 'Other Total']

# Organize where items will be on the page
app.layout = html.Div([
    html.H3(
        children='Aggregated Number of Graduates in Education by State',
        style={
            'textAlign': 'center', 'fontFamily': 'Georgia'
        }
    ),

    html.Div([
        html.Div([
            html.Div([html.P('Select a State from the drop down below', id='state-title')],
                     style={'textAlign': 'center', 'fontFamily': 'Georgia'}),
            dcc.Dropdown(
                id='state-id',
                options=[{'label': i, 'value': i} for i in state],
                value='Alaska'
            )
        ],
            style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            html.Div([html.P('Select Totals by broad CIP categories and Award type', id='indicator-title')],
                     style={'textAlign': 'center', 'fontFamily': 'Georgia'}),
            dcc.Dropdown(
                id='indicator-id',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value=['State Total'],
                multi=True  # This treats items as a list.
            )
        ],
            style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    dcc.Graph(id='indicator-graphic')
])


@app.callback(

    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('state-id', 'value'),
     dash.dependencies.Input('indicator-id', 'value')])
def update_time_series(state_id, indicator_ids):
    dff = df[df['state_long'] == state_id]
    lines = {}
    data = []
    for indicator_id in indicator_ids:
        if indicator_id == 'Bachelor Total':
            lines = dict(
                color=("#6b6ecf"),
                width=3,
                dash='dash')
        if indicator_id == 'Masters Total':
            lines = dict(
                color=("#80b1d3"),
                width=3,
                dash='dash')
        if indicator_id == 'State Total':
            lines = dict(
                color=("#333333"),
                width=3)
        if indicator_id == 'PhD Total':
            lines = dict(
                color=("#35B778"),
                width=3,
                dash='dash')
        if indicator_id == 'SPED Total':
            lines = dict(
                color=("#fdb462"),
                width=3,
                dash='dot')
        if indicator_id == 'Elementary Total':
            lines = dict(
                color=("#bebada"),
                width=3,
                dash='dot')
        if indicator_id == 'Other Total':
            lines = dict(
                color=("#fb8072"),
                width=3,
                dash='dot')
        if indicator_id == 'STEM Total':
            lines = dict(
                color=("#8dd3c7"),
                width=3,
                dash='dot')
        trace = go.Scatter(
            x=dff[dff['indicator'] == indicator_id]['year'],
            y=dff[dff['indicator'] == indicator_id]['value'],
            mode='lines',
            name=indicator_id,
            line=lines,
            opacity=0.8
        )

        data.append(trace)
    return {
        'data': data,
        'layout': go.Layout(
            xaxis={'title': 'Year'},
            yaxis={'title': 'Total Graduates in Education'}
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)