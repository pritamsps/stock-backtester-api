import yfinance as yf
import pandas as pd

# Set pandas to display all rows so you can see the full data
pd.set_option('display.max_rows', None)

def fetch_stock_data(ticker):
    """
    Fetches historical stock data for a given ticker.
    """
    # Create a Ticker object
    stock = yf.Ticker(ticker)
    
    # Fetch historical data for the last 5 years
    # '1d' means daily intervals
    hist_data = stock.history(period="5y", interval="1d")
    
    return hist_data

# --- Main part of the script ---
if __name__ == "__main__":
    target_ticker = "AAPL" # Apple Inc.
    print(f"Fetching 5-year historical data for {target_ticker}...")
    
    historical_data = fetch_stock_data(target_ticker)
    
    historical_data['SMA50'] = historical_data['Close'].rolling(window=50).mean()

    # Calculate the 200-day Simple Moving Average
    historical_data['SMA200'] = historical_data['Close'].rolling(window=200).mean()
    # --- Backtesting Logic ---
# 0 = "out" of the market, 1 = "in" the market
    position = 0 
    trades = []

    # Loop through the data, starting from the 200th day since we need SMA200 data
    for i in range(200, len(historical_data)):
        # Check for a Buy Signal (Golden Cross)
        # Is the SMA50 crossing above the SMA200?
        if historical_data['SMA50'][i] > historical_data['SMA200'][i] and historical_data['SMA50'][i-1] < historical_data['SMA200'][i-1] and position == 0:
            position = 1 # We are now "in" the market
            buy_price = historical_data['Close'][i]
            buy_date = historical_data.index[i]
            trades.append({'action': 'BUY', 'date': buy_date, 'price': buy_price})
            print(f"BUY signal on {buy_date.date()} at ${buy_price:.2f}")

        # Check for a Sell Signal (Death Cross)
        # Is the SMA50 crossing below the SMA200?
        elif historical_data['SMA50'][i] < historical_data['SMA200'][i] and historical_data['SMA50'][i-1] > historical_data['SMA200'][i-1] and position == 1:
            position = 0 # We are now "out" of the market
            sell_price = historical_data['Close'][i]
            sell_date = historical_data.index[i]
            trades.append({'action': 'SELL', 'date': sell_date, 'price': sell_price})
            print(f"SELL signal on {sell_date.date()} at ${sell_price:.2f}")

    print("\n--- All Trades ---")
    print(trades)
    # --- Performance Calculation ---
    initial_capital = 10000.00
    cash = initial_capital
    shares = 0
    portfolio_value = initial_capital

    print("\n--- Portfolio Simulation ---")

    for trade in trades:
        if trade['action'] == 'BUY':
            # Calculate how many shares we can buy
            shares_to_buy = cash / trade['price']
            shares += shares_to_buy
            cash = 0 # All cash is invested
            print(f"Bought {shares_to_buy:.2f} shares on {trade['date'].date()} at ${trade['price']:.2f}")

        elif trade['action'] == 'SELL':
            # Sell all shares
            cash_from_sale = shares * trade['price']
            cash += cash_from_sale
            shares = 0
            print(f"Sold shares on {trade['date'].date()} for ${cash_from_sale:.2f}")

    # At the end, calculate the final portfolio value
    # If we are still holding shares, their value is the last known price
    if shares > 0:
        last_price = historical_data['Close'][-1]
        final_portfolio_value = shares * last_price
    else:
        final_portfolio_value = cash

    # Calculate performance metrics
    profit = final_portfolio_value - initial_capital
    return_percentage = (profit / initial_capital) * 100

    print("\n--- Final Performance Report ---")
    print(f"Initial Capital: ${initial_capital:,.2f}")
    print(f"Final Portfolio Value: ${final_portfolio_value:,.2f}")
    print(f"Total Profit/Loss: ${profit:,.2f}")
    print(f"Total Return: {return_percentage:.2f}%")