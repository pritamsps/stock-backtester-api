from flask import Flask, request, jsonify
import yfinance as yf
import pandas as pd

app = Flask(__name__)

def run_backtest(ticker):
    """
    This function will contain all your backtesting logic.
    It takes a ticker, runs the simulation, and returns the results.
    """
    # --- Step 1: Fetch Data ---
    stock = yf.Ticker(ticker)
    historical_data = stock.history(period="5y", interval="1d")

    if historical_data.empty:
        return {"error": f"Could not fetch data for ticker {ticker}"}

    # --- Step 2: Calculate SMAs ---
    historical_data['SMA50'] = historical_data['Close'].rolling(window=50).mean()
    historical_data['SMA200'] = historical_data['Close'].rolling(window=200).mean()

    # --- Step 3: Run Trading Simulation ---
    position = 0 
    trades = []
    for i in range(200, len(historical_data)):
        if historical_data['SMA50'][i] > historical_data['SMA200'][i] and historical_data['SMA50'][i-1] < historical_data['SMA200'][i-1] and position == 0:
            position = 1
            trades.append({'action': 'BUY', 'date': historical_data.index[i], 'price': historical_data['Close'][i]})
        elif historical_data['SMA50'][i] < historical_data['SMA200'][i] and historical_data['SMA50'][i-1] > historical_data['SMA200'][i-1] and position == 1:
            position = 0
            trades.append({'action': 'SELL', 'date': historical_data.index[i], 'price': historical_data['Close'][i]})

    # --- Step 4: Calculate Performance ---
    initial_capital = 10000.00
    cash = initial_capital
    shares = 0
    for trade in trades:
        if trade['action'] == 'BUY':
            shares_to_buy = cash / trade['price']
            shares += shares_to_buy
            cash = 0
        elif trade['action'] == 'SELL':
            cash_from_sale = shares * trade['price']
            cash += cash_from_sale
            shares = 0
    
    if shares > 0:
        final_portfolio_value = shares * historical_data['Close'][-1]
    else:
        final_portfolio_value = cash

    profit = final_portfolio_value - initial_capital
    return_percentage = (profit / initial_capital) * 100

    # --- Step 5: Return results as a dictionary ---
    return {
        "ticker": ticker,
        "initial_capital": initial_capital,
        "final_value": final_portfolio_value,
        "profit_loss": profit,
        "return_percentage": return_percentage
    }


@app.route("/backtest", methods=['POST'])
def backtest_endpoint():
    # Get the ticker from the incoming JSON request
    ticker = request.json['ticker']
    
    # Run the backtest
    results = run_backtest(ticker)
    
    # Return the results as a JSON response
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)