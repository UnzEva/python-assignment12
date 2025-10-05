import pandas as pd
import plotly.express as px
import plotly.data as pldata
import os

def load_data():
    """Load wind dataset with fallback methods"""
    try:
        return pldata.wind(return_type='pandas')
    except TypeError:
        return pldata.wind()

def clean_strength(df):
    """Clean and convert strength column to float"""
    df['strength'] = (
        df['strength']
        .astype(str)
        .str.replace(r'^\s*([0-9]+(?:\.[0-9]+)?)\D.*$', r'\1', regex=True)
        .astype(float)
    )
    return df

def create_plot(df):
    """Create interactive scatter plot"""
    fig = px.scatter(
        df, 
        x='strength', 
        y='frequency', 
        color='direction',
        title='Wind Strength vs Frequency by Direction',
        labels={'strength': 'Wind Strength', 'frequency': 'Frequency', 'direction': 'Direction'},
        hover_data=df.columns.tolist(),
        opacity=0.7
    )
    
    fig.update_layout(
        plot_bgcolor='rgba(240,240,240,0.8)',
        paper_bgcolor='white',
        title_x=0.5,
        width=1000,
        height=600
    )
    
    fig.update_traces(
        marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey'))
    )
    
    return fig

def save_and_verify(fig, filename):
    """Save plot and verify file was created correctly"""
    fig.write_html(filename, include_plotlyjs='cdn', full_html=True)
    
    if os.path.exists(filename):
        file_size = os.path.getsize(filename)
        print(f"Saved to: {filename} ({file_size} bytes)")
        
        with open(filename, "r", encoding="utf-8") as f:
            html_content = f.read()
        
        return "Plotly.newPlot" in html_content
    return False

def main():
    # Load data
    df = load_data()
    
    print("First 10 rows:")
    print(df.head(10))
    print("\nLast 10 rows:")
    print(df.tail(10))
    
    # Clean data
    df = clean_strength(df)
    
    print("\nData types after cleaning:")
    print(df.dtypes)
    
    # Create plot
    fig = create_plot(df)
    
    # Save and verify
    html_path = "wind.html"
    verified = save_and_verify(fig, html_path)
    
    print(f"Verification passed: {verified}")
    print("Done! Open wind.html in your browser.")

if __name__ == "__main__":
    main()