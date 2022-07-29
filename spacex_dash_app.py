# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
launchsites= spacex_df['Launch Site'].unique().tolist()

fig1 = px.pie(spacex_df, values='class', names='Launch Site', title="Pie Chart")
fig1.update_traces(textinfo='value')

fig2= px.scatter(x=spacex_df['Payload Mass (kg)'], y=spacex_df['class'])


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                               
                                html.Div(dcc.Dropdown(id='site-dropdown',options=[{'label': i, 'value': i} for i in launchsites] , placeholder="Select a Launch Site")),
                                
                                #html.Div(dcc.Dropdown(options=['a', 'b'], value='a' ,id='site-dropdown')),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart', figure=fig1)),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(min=min_payload, max=max_payload, step=100, value=[min_payload, max_payload], id='payload-slider',marks={1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000', 7000: '7000', 8000: '8000',9000: '9000'})),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart', figure=fig2)),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_output_div(input_value):
    #return f'Output: {input_value}'
    if input_value:
        filtered_df = spacex_df[spacex_df['Launch Site']==input_value]
        s = filtered_df['class']
        fig = px.pie(s, values=s.value_counts().values, names=s.value_counts().index, title="Successfull(1) vs Failed(0) launches")
        fig.update_traces(textinfo='value')
        return fig
    else:
        fig = px.pie(spacex_df, values='class', names='Launch Site', title="Sucessfull Launches")
        fig.update_traces(textinfo='value')
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
    Input(component_id='payload-slider', component_property='value')])
    
def update_scatter_div(input_value1, input_value2):
    #return f'Output: {input_value}'
    filtered_df=spacex_df
    print(input_value1)
    if input_value1:
        filtered_df = filtered_df[filtered_df['Launch Site']==input_value1]
        print(filtered_df)
    if input_value2:
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']>=input_value2[0]]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)']<=input_value2[1]]
    print(filtered_df['class'])
    fig= px.scatter(filtered_df, x='Payload Mass (kg)', y='class')
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()