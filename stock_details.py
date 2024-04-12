import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_coin_data(coin_id, days=365):
    try:
        if days > 365:
            raise ValueError("Number of days requested exceeds the allowed limit (365 days).")

        today = datetime.now().date()
        start_date = today - timedelta(days=days)

        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=usd&from={start_date}&to={today}&days={days}"
        response = requests.get(url)
        data = response.json()

        if 'prices' not in data:
            raise ValueError("No price data found in the response.")

        prices = pd.DataFrame(data['prices'], columns=['time', 'price'])
        prices['time'] = pd.to_datetime(prices['time'], unit='ms')

        return prices
    except Exception as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def main():
    st.title("Cryptocurrency Price Details")

    coin_list_url = "https://api.coingecko.com/api/v3/coins/list"
    coin_list_response = requests.get(coin_list_url)
    
    if coin_list_response.status_code != 200:
        st.error("Error fetching coin list. Please try again later.")        
        st.error(coin_list_response.json())
        return

    coin_list = coin_list_response.json()

    if not isinstance(coin_list, list):
        st.error("Unexpected response format from API.")
        return

    coin_names = [coin['name'] for coin in coin_list]

    selected_coin = st.selectbox("Select a cryptocurrency:", coin_names)

    st.write(f"You selected: {selected_coin}")

    coin_id = [coin['id'] for coin in coin_list if coin['name'] == selected_coin][0]

    days_to_plot = st.slider("Select number of days to plot:", min_value=30, max_value=365, value=365)

    coin_data = get_coin_data(coin_id, days_to_plot)

    if coin_data is not None:
        st.write("Price chart:")
        st.line_chart(coin_data.set_index('time'))

        max_price = coin_data['price'].max()
        min_price = coin_data['price'].min()
        max_price_date = coin_data.loc[coin_data['price'].idxmax()]['time'].date()
        min_price_date = coin_data.loc[coin_data['price'].idxmin()]['time'].date()

        st.write(f"Maximum price during the last {days_to_plot} days: ${max_price:.2f} on {max_price_date}")
        st.write(f"Minimum price during the last {days_to_plot} days: ${min_price:.2f} on {min_price_date}")

if __name__ == "__main__":
    main()

