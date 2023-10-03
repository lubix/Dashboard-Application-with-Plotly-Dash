# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

def dropdownOptions():
    options_list = [{'label':'All Site', 'value':'ALL'}]
    for row in spacex_df['Launch Site'].unique():
        options_list.append({'label': row, 'value': row},)
    return options_list
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div( dcc.Dropdown(id='site-dropdown',
                                    options= dropdownOptions(),
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True,
                                    clearable=False   
                                    ),),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider',
                                                        min=0, max=10000, step=1000,
                                                        marks={i: '{}'.format(i) for i in range(int(min_payload),int(max_payload),2500)},
                                                         #marks={0: '0',100: '100'},
                                                        value=[min_payload, max_payload],
                                                         dots = False,
                                                         #updatemode = 'drag'
                                                        )),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
            Input(component_id='site-dropdown', component_property='value'))


def get_pie_chart(entered_site):
    filtered_df = spacex_df.fillna(0)
    if entered_site == 'ALL':
        data =  filtered_df['Launch Site']
        column_name = filtered_df['Launch Site']
        fig = px.pie(filtered_df,names=filtered_df['Launch Site'], values=filtered_df['class'],             
                 title=entered_site)
        return fig
        
    else:
        data =  filtered_df[filtered_df['Launch Site']==entered_site]
        #print(data)
        fig = px.pie(data,names=data['class'],                
                 title=entered_site)
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
                Input(component_id='payload-slider', component_property='value'))


def get_pay_load(value_payload):
    
    filtered_df = spacex_df.fillna(0)
    print(filtered_df)
    if not value_payload:
        return dash.no_update
    df_payload = filtered_df[filtered_df['Payload Mass (kg)'].between(value_payload[0], value_payload[1])]  
    fig = px.scatter(
        df_payload,
        x=df_payload['Payload Mass (kg)'],
        y=df_payload['class'],
        color=df_payload['Booster Version Category'],
        title=f"Correlation between Payload an Success for all Sites",
    )
    return fig



# Run the app
if __name__ == '__main__':
    app.run_server()