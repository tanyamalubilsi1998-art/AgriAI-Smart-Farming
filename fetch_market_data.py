import requests
import pandas as pd

def fetch_live_mandi_prices(api_key):
    print("Connecting to Government of India Mandi API...")
    resource_id = "9ef84268-d588-465a-a308-a864a43d0070" 
    url = f"https://api.data.gov.in/resource/{resource_id}?api-key={api_key}&format=json&limit=5000"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        records = data.get('records', [])
        
        if not records:
            print("No data found for today yet.")
            return None
            
        df = pd.DataFrame(records)
        df = df[['state', 'district', 'market', 'commodity', 'min_price', 'max_price', 'modal_price']]
        print(f"Success! Fetched {len(df)} live market records.")
        return df

    except Exception as e:
        print(f"Failed to fetch data: {e}")
        return None

if __name__ == "__main__":
    # Put your real API key right here!
    MY_API_KEY = "YOUR_API_KEY_HIDDEN_FOR_SECURITY" 
    live_market_data = fetch_live_mandi_prices(MY_API_KEY)
    
    if live_market_data is not None:
        live_market_data.to_csv("live_market_prices.csv", index=False)
        print("Saved live data to 'live_market_prices.csv'")