from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load the gapminder dataset
df = px.data.gapminder()

# Get unique countries for dropdown
countries = df['country'].unique()

# Initialize the Dash app
app = Dash(__name__)

# Deployment
server = app.server

# Define the layout
app.layout = html.Div([
    html.H1("GDP per Capita Over Time by Country", 
            style={'textAlign': 'center', 'marginBottom': 30}),
    
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in countries],
            value='Canada',
            style={'width': '50%', 'margin': 'auto'}
        ),
    ], style={'marginBottom': 30}),
    
    dcc.Graph(id='gdp-growth')
])

# Define the callback
@app.callback(
    Output('gdp-growth', 'figure'),
    Input('country-dropdown', 'value')
)
def update_graph(selected_country):
    # Filter data for selected country
    filtered_df = df[df['country'] == selected_country]
    
    # Create line plot
    fig = px.line(
        filtered_df,
        x='year',
        y='gdpPercap',
        title=f'GDP per Capita Growth: {selected_country} (1952-2007)',
        labels={'year': 'Year', 'gdpPercap': 'GDP per Capita (USD)'}
    )
    
    # Customize the figure
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#2c3e50')
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run(debug=True)