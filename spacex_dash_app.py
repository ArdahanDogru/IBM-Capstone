# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout

sites = spacex_df['Launch Site'].unique().tolist()
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options = [
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': sites[0], 'value': sites[0]},
                                    {'label': sites[1], 'value': sites[1]},
                                    {'label': sites[2], 'value': sites[2]},
                                    {'label': sites[3], 'value': sites[3]}],
                                    value = 'ALL', 
                                    placeholder = 'Select Launch Site', 
                                    searchable = True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min = 0, max = 10000, step = 100, 
                                    marks = {0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                    value = [min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names= 'Launch Site', 
        title='Success Among Sites')
        return fig
    else:
        site_specific = filtered_df[filtered_df['Launch Site'] == entered_site].value_counts().reset_index()
        #print(site_specific)
        fig = px.pie(site_specific, values='count',
        names= 'class',
        title='Success Percentage')
        return fig
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='payload-slider', component_property='value'),
              Input(component_id='site-dropdown', component_property='value'))

def get_scatter_plot(payload_value, entered_site):
    filtered_df = spacex_df
    minp, maxp = payload_value
    if entered_site == 'ALL':
        payload = filtered_df[(filtered_df['Payload Mass (kg)'] <= maxp) & (filtered_df['Payload Mass (kg)'] >= minp)]
        fig = px.scatter(payload, y='class', 
        x= 'Payload Mass (kg)', 
        color="Booster Version Category",
        title='Payload Success')
        return fig
    else:
        site_specific = filtered_df[filtered_df['Launch Site'] == entered_site]
        site_payload = site_specific[(site_specific['Payload Mass (kg)'] <= maxp) & (site_specific['Payload Mass (kg)'] >= minp)]
        #print(site_specific)
        fig = px.scatter(site_payload, x='Payload Mass (kg)',
        y= 'class',
        color = 'Booster Version Category',
        title='Success Percentage')
        return fig

# Run the app
if __name__ == '__main__':
    #print(spacex_df.head(59))
    app.run_server()
