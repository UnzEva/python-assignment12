import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

def load_employee_revenue():
    # The path to the database
    db_path = 'db/lesson.db'
    
    print(f"Database path: {db_path}")
    print(f"File exists: {os.path.exists(db_path)}")
    
    try:
        # Connecting to the database
        conn = sqlite3.connect(db_path)
        print("Database connection successful!")
        
        # Check the tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Available tables:", [table[0] for table in tables])
        
        # SQL query for getting revenue data for employees
        sql_query = """
        SELECT last_name, SUM(price * quantity) AS revenue 
        FROM employees e 
        JOIN orders o ON e.employee_id = o.employee_id 
        JOIN line_items l ON o.order_id = l.order_id 
        JOIN products p ON l.product_id = p.product_id 
        GROUP BY e.employee_id;
        """
        
        # Uploading data to the DataFrame
        employee_results = pd.read_sql_query(sql_query, conn)
        
        # Closing the connection
        conn.close()
        
        return employee_results
        
    except sqlite3.Error as e:
        print(f" Database error: {e}")
        return None

def create_bar_chart(df):
    if df is None or df.empty:
        print(" No data to plot!")
        return
    
    # Creating a bar chart using Pandas plotting
    ax = df.plot.bar(
        x='last_name', 
        y='revenue',
        figsize=(12, 8),
        color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
        edgecolor='black',
        alpha=0.7
    )
    
    # Setting up the title and tags
    ax.set_title('Employee Revenue Performance', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Employee Last Name', fontsize=12, fontweight='bold')
    ax.set_ylabel('Revenue ($)', fontsize=12, fontweight='bold')
    
    # Setting up the view
    ax.grid(axis='y', alpha=0.3)
    ax.legend(['Revenue'], loc='upper right')
    
    # Rotate the captions on the X-axis 
    plt.xticks(rotation=45, ha='right')
    
    # Setting up layout
    plt.tight_layout()
    
    return ax

def main():
    print("Loading employee revenue data...")
    
    # Uploading data
    employee_results = load_employee_revenue()
    
    if employee_results is not None and not employee_results.empty:
        # Displaying data
        print("\nEmployee Revenue Data:")
        print(employee_results)
        
        # Creating chart
        print("\nCreating bar chart...")
        create_bar_chart(employee_results)
        
        # Saving chart
        plt.savefig('employee_revenue_chart.png', dpi=300, bbox_inches='tight')
        print("Chart saved as 'employee_revenue_chart.png'")
        
        # Displaying chart
        plt.show()
        
    else:
        print("No data retrieved from database")

if __name__ == "__main__":
    main()