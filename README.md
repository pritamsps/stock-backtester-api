# Historical Trading Strategy Backtester API

This project is a Python-based backend service that backtests a Simple Moving Average (SMA) crossover trading strategy against historical stock data. It provides a RESTful API to run simulations for any given stock ticker and returns a performance report.

## Core Features

-   **Data Ingestion:** Fetches up to five years of historical daily stock data from Yahoo! Finance.
-   **Indicator Calculation:** Calculates the 50-day and 200-day Simple Moving Averages for the given stock.
-   **Trading Simulation:** Executes a "Golden Cross" / "Death Cross" trading strategy, generating a list of buy and sell signals.
-   **Performance Analysis:** Simulates the strategy with an initial capital to calculate final portfolio value, total profit/loss, and percentage return.

## Tech Stack

-   **Language:** Python
-   **Framework:** Flask
-   **Data Processing:** Pandas, yfinance
-   **Server:** Gunicorn

## API Endpoint

The service exposes a single endpoint for running the backtest.

### `POST /backtest`

This endpoint runs a full simulation for the specified stock ticker.

**Request Body:**

```json
{
  "ticker": "GOOG"
}
