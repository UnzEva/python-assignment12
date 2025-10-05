import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

def load_order_totals():
    """Loads data on order amounts from the database"""
    conn = sqlite3.connect('db/lesson.db')
    
    # SQL query to get the total amount of each order
    sql_query = """
    SELECT 
        o.order_id,
        SUM(p.price * l.quantity) AS total_price
    FROM orders o
    JOIN line_items l ON o.order_id = l.order_id
    JOIN products p ON l.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id;
    """
    
    df = pd.read_sql_query(sql_query, conn)
    conn.close()
    return df

def add_cumulative_column_apply(df):
    """Adds a cumulative column"""
    def cumulative(row):
        totals_above = df['total_price'][0:row.name+1]
        return totals_above.sum()
    
    df['cumulative'] = df.apply(cumulative, axis=1)
    return df

def create_line_plot(df):
    """Creates a line graph of cumulative revenue"""
    ax = df.plot.line(
        x='order_id',
        y='cumulative',
        figsize=(12, 8),
        linewidth=2.5,
        color='#2E8B57',
        marker='o',
        markersize=4,
        markerfacecolor='#FF6347',
        markeredgecolor='#FF6347'
    )
    
    # Setting up the title and tags
    ax.set_title('Cumulative Revenue Over Orders', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Order ID', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Revenue ($)', fontsize=12, fontweight='bold')
    
    # Setting up the grid and view
    ax.grid(True, alpha=0.3)
    ax.legend(['Cumulative Revenue'], loc='upper left')
    
    # Adding an annotation with the total revenue in the upper right corner
    total_revenue = df['cumulative'].iloc[-1]
    ax.annotate(f'Total Revenue: ${total_revenue:,.2f}', 
                xy=(0.98, 0.95), xycoords='axes fraction',  # changed x to 0.98 (right edge)
                fontsize=12, 
                bbox=dict(boxstyle="round,pad=0.3", fc="lightblue", alpha=0.7),
                ha='right',  
                va='top')    
    
    plt.tight_layout()
    return ax

def main():
    print("Loading order data for cumulative revenue analysis...")
    
    # Uploading data
    df = load_order_totals()
    
    if df is not None and not df.empty:
        print(f"\nFound {len(df)} orders")
        print("\nFirst 5 orders:")
        print(df.head())
        
        # Adding a cumulative column
        df = add_cumulative_column_apply(df)
        
        print("\nData with cumulative revenue:")
        print(df.head())
        
        print(f"\nTotal revenue: ${df['total_price'].sum():,.2f}")
        print(f"Average order value: ${df['total_price'].mean():,.2f}")
        
        # Creating the graph
        print("\nCreating cumulative revenue line plot...")
        create_line_plot(df)
        
        # Saving the graph
        plt.savefig('cumulative_revenue.png', dpi=300, bbox_inches='tight')
        print("Chart saved as 'cumulative_revenue.png'")
        
        # Showing the graph
        plt.show()
        
    else:
        print("No data retrieved from database")

if __name__ == "__main__":
    main()