import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sales_data(num_records=5000):
    # Setup categories and products
    categories = {
        'Electronics': ['Laptops', 'Smartphones', 'Tablets', 'Monitors'],
        'Clothing': ['T-Shirts', 'Jeans', 'Sneakers', 'Jackets'],
        'Home Goods': ['Desks', 'Chairs', 'Lamps', 'Sofas'],
        'Accessories': ['Smartwatches', 'Headphones', 'Backpacks', 'Chargers']
    }
    
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
    
    # Generate dates over the last 2 years
    end_date = datetime.today()
    start_date = end_date - timedelta(days=730)
    
    data = []
    
    for _ in range(num_records):
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        region = random.choice(regions)
        
        # Calculate base prices roughly based on category
        if category == 'Electronics':
            base_price = random.uniform(300, 2000)
            cost_multiplier = random.uniform(0.6, 0.8)
        elif category == 'Home Goods':
            base_price = random.uniform(50, 800)
            cost_multiplier = random.uniform(0.5, 0.7)
        elif category == 'Clothing':
            base_price = random.uniform(20, 150)
            cost_multiplier = random.uniform(0.3, 0.5)
        else:
            base_price = random.uniform(15, 300)
            cost_multiplier = random.uniform(0.4, 0.6)
            
        quantity = random.randint(1, 10)
        sales_amount = base_price * quantity
        cost = base_price * cost_multiplier * quantity
        profit = sales_amount - cost
        profit_margin = profit / sales_amount
        
        # Random date
        random_days = random.randint(0, (end_date - start_date).days)
        order_date = start_date + timedelta(days=random_days)
        
        data.append({
            'Order ID': f'ORD-{random.randint(10000, 99999)}',
            'Date': order_date.strftime('%Y-%m-%d'),
            'Product Category': category,
            'Product': product,
            'Region': region,
            'Quantity': quantity,
            'SalesAmount': round(sales_amount, 2),
            'Cost': round(cost, 2),
            'Profit': round(profit, 2),
            'ProfitMargin': round(profit_margin, 4)
        })

    df = pd.DataFrame(data)
    # Sort chronologically
    df.sort_values(by='Date', inplace=True)
    df.to_csv('SalesData.csv', index=False)
    print(f"Successfully generated {num_records} records in 'SalesData.csv'")

if __name__ == '__main__':
    generate_sales_data(10000)
