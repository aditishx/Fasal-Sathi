import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Sample market data for different crops
CROP_MARKET_DATA = {
    'Rice': {
        'base_price': 45,
        'demand': 'High',
        'trend': 'Stable',
        'seasonality': [1.0, 0.95, 0.90, 0.85, 0.80, 0.85, 0.90, 1.0, 1.05, 1.1, 1.15, 1.2],
    },
    'Wheat': {
        'base_price': 35,
        'demand': 'High',
        'trend': 'Stable',
        'seasonality': [1.1, 1.15, 1.2, 0.95, 0.80, 0.75, 0.80, 0.85, 0.95, 1.05, 1.1, 1.15],
    },
    'Corn': {
        'base_price': 28,
        'demand': 'Medium',
        'trend': 'Increasing',
        'seasonality': [0.9, 0.85, 0.80, 1.0, 1.1, 1.2, 1.15, 1.05, 0.95, 0.90, 0.85, 0.90],
    },
    'Maize': {
        'base_price': 30,
        'demand': 'High',
        'trend': 'Stable',
        'seasonality': [0.9, 0.85, 0.80, 1.0, 1.1, 1.2, 1.15, 1.05, 0.95, 0.90, 0.85, 0.90],
    },
    'Sugarcane': {
        'base_price': 50,
        'demand': 'Medium',
        'trend': 'Decreasing',
        'seasonality': [0.8, 0.8, 0.85, 0.9, 1.0, 1.1, 1.2, 1.15, 1.0, 0.9, 0.85, 0.80],
    },
    'Cotton': {
        'base_price': 60,
        'demand': 'Medium',
        'trend': 'Stable',
        'seasonality': [0.85, 0.85, 0.9, 1.0, 1.1, 1.2, 1.15, 1.05, 0.95, 0.90, 0.85, 0.85],
    },
    'Potato': {
        'base_price': 20,
        'demand': 'High',
        'trend': 'Increasing',
        'seasonality': [0.8, 0.85, 0.9, 1.1, 1.2, 1.15, 1.0, 0.9, 0.85, 0.80, 0.75, 0.80],
    },
    'Tomato': {
        'base_price': 25,
        'demand': 'High',
        'trend': 'Stable',
        'seasonality': [0.9, 0.95, 1.0, 1.1, 1.15, 1.2, 1.1, 1.0, 0.95, 0.90, 0.85, 0.85],
    },
    'Onion': {
        'base_price': 30,
        'demand': 'High',
        'trend': 'Stable',
        'seasonality': [1.0, 1.05, 1.1, 1.15, 1.2, 1.1, 0.95, 0.85, 0.80, 0.85, 0.90, 0.95],
    },
    'Cabbage': {
        'base_price': 15,
        'demand': 'Medium',
        'trend': 'Stable',
        'seasonality': [0.85, 0.90, 0.95, 1.0, 1.05, 1.1, 1.05, 1.0, 0.95, 0.90, 0.85, 0.85],
    },
}

def predict_prices(crop, days_ahead=30):
    """Predict crop prices for the next N days"""
    if crop not in CROP_MARKET_DATA:
        return None
    
    data = CROP_MARKET_DATA[crop]
    base_price = data['base_price']
    current_month = datetime.now().month - 1  # 0-indexed
    
    prices = []
    dates = []
    
    for day in range(days_ahead):
        date = datetime.now() + timedelta(days=day)
        month = (current_month + day // 30) % 12
        
        # Get seasonality factor
        seasonality = data['seasonality'][month]
        
        # Add some random fluctuation
        fluctuation = 1 + (np.random.random() - 0.5) * 0.1
        
        # Trend adjustment
        if data['trend'] == 'Increasing':
            trend_factor = 1 + (day / days_ahead) * 0.05
        elif data['trend'] == 'Decreasing':
            trend_factor = 1 - (day / days_ahead) * 0.05
        else:
            trend_factor = 1.0
        
        price = base_price * seasonality * fluctuation * trend_factor
        prices.append(round(price, 2))
        dates.append(date.strftime('%Y-%m-%d'))
    
    return {
        'crop': crop,
        'dates': dates,
        'prices': prices,
        'avg_price': round(np.mean(prices), 2),
        'min_price': round(np.min(prices), 2),
        'max_price': round(np.max(prices), 2),
        'trend': data['trend'],
    }

def get_market_insights(crop):
    """Get detailed market insights for a crop"""
    if crop not in CROP_MARKET_DATA:
        return None
    
    data = CROP_MARKET_DATA[crop]
    
    # Generate demand forecast
    demand_levels = {
        'High': ['Very strong market', 'Good selling opportunity', 'Limited surplus risk'],
        'Medium': ['Moderate market activity', 'Fair prices expected', 'Some price volatility'],
        'Low': ['Weak demand', 'Buyer\'s market', 'Higher storage costs needed'],
    }
    
    demand_insights = demand_levels.get(data['demand'], [])
    
    # Generate trend insights
    trend_insights = {
        'Increasing': 'Prices are expected to rise. Good time to plan production.',
        'Decreasing': 'Prices are expected to fall. Consider market timing.',
        'Stable': 'Prices are relatively stable. Consistent returns expected.',
    }
    
    # Calculate estimated profit per hectare (simplified)
    estimated_yield_per_hectare = {
        'Rice': 50,  # quintal
        'Wheat': 45,
        'Corn': 55,
        'Maize': 55,
        'Sugarcane': 70,
        'Cotton': 20,
        'Potato': 200,
        'Tomato': 400,
        'Onion': 250,
        'Cabbage': 300,
    }
    
    yield_val = estimated_yield_per_hectare.get(crop, 0)
    base_price = data['base_price']
    estimated_revenue = round(yield_val * base_price, 2)
    
    return {
        'crop': crop,
        'current_price': data['base_price'],
        'demand': data['demand'],
        'trend': data['trend'],
        'demand_insights': demand_insights,
        'trend_insight': trend_insights[data['trend']],
        'estimated_yield_per_hectare': yield_val,
        'estimated_revenue_per_hectare': estimated_revenue,
    }

def get_all_crops():
    """Get list of all available crops"""
    return list(CROP_MARKET_DATA.keys())

def compare_crops(crops_list):
    """Compare market metrics for multiple crops"""
    comparison = []
    
    for crop in crops_list:
        if crop in CROP_MARKET_DATA:
            data = CROP_MARKET_DATA[crop]
            comparison.append({
                'crop': crop,
                'base_price': data['base_price'],
                'demand': data['demand'],
                'trend': data['trend'],
            })
    
    return comparison
