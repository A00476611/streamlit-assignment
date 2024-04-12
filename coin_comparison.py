import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_coin_data(coin_id, days=365):
    today = datetime.now().date()
    start_date = today - timedelta(days=days)

    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart/range?vs_currency=usd&from={start_date}&to={today}&days={days}"
    response = requests.get(url)
    data = response.json()

    prices = pd.DataFrame(data['prices'], columns=['time', 'price'])
    prices['time'] = pd.to_datetime(prices['time'], unit='ms')

    return prices

def main():
    st.title("Cryptocurrency Comparison")

    coin_list_url = "https://api.coingecko.com/api/v3/coins/list"
    coin_list_response = requests.get(coin_list_url)
    coin_list = coin_list_response.json()

    coin_names = [coin['name'] for coin in coin_list]

    selected_coins = st.multiselect("Select cryptocurrencies to compare:", coin_names)

    if len(selected_coins) < 2:
        st.warning("Please select at least two cryptocurrencies.")
        return

    st.write(f"You selected: {', '.join(selected_coins)}")

    days_to_plot = st.select_slider("Select number of days to plot:", options=[("1 Week", 7), ("1 Month", 30), ("1 Year", 365), ("5 Years", 1825)])

    plt.figure(figsize=(10, 6))

    for coin in selected_coins:
        coin_id = [c['id'] for c in coin_list if c['name'] == coin][0]
        coin_data = get_coin_data(coin_id, days_to_plot)
        plt.plot(coin_data['time'], coin_data['price'], label=coin)

    plt.xlabel("Date")
    plt.ylabel("Price (USD)")
    plt.title("Cryptocurrency Comparison")
    plt.legend()
    st.pyplot()

if __name__ == "__main__":
    main()
