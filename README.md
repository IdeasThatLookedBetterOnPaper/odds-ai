# Betfair Trading Lab ⚽📈

A specialized research and automation framework for sports exchange trading on Betfair. This project automates the collection of high-frequency market data and uses **Evolutionary Algorithms (Genetic Algorithms)** and **ARIMAX models** to develop and backtest profitable trading strategies.

---

## 🌟 Overview

The core philosophy of this project is that sports markets are dynamic time-series. Instead of using static betting rules, this system treats strategy development as an **optimization problem**. It "breeds" trading bots (Individuals) by simulating thousands of trades on historical data to find the most robust parameters for market entry and exit.


## 🚀 Key Features

* **Real-time Data Pipeline:** Automated scraping of "Match Odds" markets every 60 seconds, capturing 3-tier BACK/LAY depth and total liquidity.
* **Genetic Strategy Optimizer:** A simulation engine that evolves a population of trading agents using crossover and mutation logic based on their ROI.
* **Sophisticated Betting Logic:**
    * **BACK/LAY Execution:** Full support for both betting on and against outcomes.
    * **Automated Trade-Out (Settle):** Logic for closing positions to lock in profits or mitigate losses (Surebet/Green-up logic).
    * **Liability Management:** Calculates real-time bankroll exposure to ensure the bot operates within safe financial limits.
* **Predictive Modeling:** Implementation of **ARIMAX** (AutoRegressive Integrated Moving Average with Explanatory Variables) to forecast price movements using market depth and metadata.

---

## 🛠 Project Structure

```plaintext
├── config/                # API settings, league definitions, and timing
├── data_gathering/        # Scraping logic, data segregation, and proxy handlers
├── models/                # Dataclasses for Match, Market, and Odds structures
├── reinforcement_learning/# Evolutionary Brain
│   ├── simulation.py      # Genetic algorithm loop (The "Evolution")
│   ├── betting.py         # Simulated order execution & stake management
│   ├── evaluations.py     # P&L calculations and fitness scoring
│   └── types.py           # Core abstractions (Individual, Strategy, Action)
├── utils/                 # Data transformation, ARIMA tests, and File I/O
└── main.py                # Main entry point for data collection or simulation
```

## ⚙️ Installation & Setup

### 1. Prerequisites
Before starting, ensure you have the following ready:
* **Python 3.11+**
* **Betfair Developer App Key:** Obtain this from the Betfair [Developer Portal](https://developer.betfair.com/).
* **SSL Certificates:** Betfair requires `.crt` and `.key` files for non-interactive login.
* **Proxy Provider:** A service like Webshare or Bright Data (optional but recommended for high-frequency scraping).

### 2. Environment Setup
We use **Conda** to manage dependencies and ensure a consistent C-extension environment for ARIMA calculations.

```bash
# Clone the repository
git clone [https://github.com/your-username/betfair-trading-lab.git](https://github.com/your-username/betfair-trading-lab.git)
cd betfair-trading-lab

# Create and activate the environment
conda env create -f conda_environment.yaml
conda activate odds-ai
```

### 3. Secure Configuration
Create a .env file in the root directory to store your credentials. This file is excluded from version control for your safety.

```bash
# Betfair API Credentials
BETFAIR_APP_KEY='your_app_key'
BETFAIR_USERNAME='your_username'
BETFAIR_PASSWORD='your_password'
BETFAIR_CERT_PATH='certs/client-2048.crt'
BETFAIR_KEY_PATH='certs/client-2048.key'

# Proxy Configuration
PROXY_HOST='your_proxy_host'
PROXY_PORT='your_port'
PROXY_USER='your_username'
PROXY_PASS='your_password'
```
## 📈 Usage

### Data Collection
To start building your own dataset of football matches:

1. Configure your target leagues in `config/leagues.py`.
2. Run the collector:

```python
# In main.py
data_collection.collect_data(infinite=True)
```
Data is saved as individual CSVs in the `/data/` folder, labeled by their `marketId`.

### Running the Genetic Simulation
To evolve a trading strategy based on your collected data:

1. Ensure you have CSV files in the `/data/` directory.
2. Uncomment the simulation section in `main.py` and run:

```python
simulation.simulate()
```

The system will output the performance of the best **Individual** in each generation, including their specific trading rules.

---

## 🧪 Research: ARIMA vs. Genetic
The project includes two distinct approaches located in the `utils/` and `reinforcement_learning/` folders:

* **Statistical (ARIMAX):** Attempts to predict the next minute's price based on historical trends.
* **Heuristic (Genetic):** Evolves rules based on game state (e.g., *"If minute > 70 and home_odds dropped by 10%, then LAY"*).



---

## ⚠️ Disclaimer
This software is for educational and research purposes only. Trading on betting exchanges involves significant financial risk. The authors are not responsible for any financial losses incurred through the use of this code.
