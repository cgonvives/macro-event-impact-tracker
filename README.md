# Real-Time Macro Event Impact Tracker - Project Pipeline

**Project Goal:** Build an automated system that detects major macroeconomic releases, captures market reactions across equities, FX, interest rates, and volatility, and visualizes the cross-asset impact within minutes and hours of the event.

**Why This Impresses Recruiters:** Shows you can connect fundamental macro data to real-time market movements, demonstrating genuine market intuition rather than just running ML algorithms on prices.

---

## Executive Pipeline Overview

```
[PHASE 1] → [PHASE 2] → [PHASE 3] → [PHASE 4] → [PHASE 5]
Setup & Auth    Data Ingestion   Event Detection   Market Impact    Dashboard &
                                                   Analysis         Automation
```

---

## PHASE 1: Project Setup & API Authentication

### Task 1.1: Environment Setup and Dependencies

**What to do:**

- Create a Python virtual environment
- Install core packages: `pandas`, `numpy`, `requests`, `matplotlib`, `seaborn`, `yfinance`, `pandas-datareader`
- Install API client libraries: `fredapi` (for macro events)
- Setup `.env` file for API keys
- Create project directory structure with subdirectories: `data/`, `scripts/`, `output/`, `config/`

**Achievements:**

- ✅ Development environment ready and isolated
- ✅ All dependencies documented in `requirements.txt`
- ✅ Secure API key management via environment variables (no hardcoding)

**Deliverable:** `requirements.txt` file and working environment verification script

---

### Task 1.2: Trading Economics API Authentication

**What to do:**

- Register for Fred API account
- Obtain API key and secret
- Test API connectivity with a simple call to retrieve one macro indicator (e.g., USD CPI)
- Create a `config.py` file to centralize API credentials and parameters

**Achievements:**

- ✅ Verified API access working
- ✅ Can pull real macro data successfully
- ✅ Configuration management in place for easy API adjustments

**Deliverable:** Confirmed API access and working `config.py`

---

## PHASE 2: Macro Event Data Ingestion Pipeline

### Task 2.1: Define Key Macro Indicators and Their Calendar

**What to do:**

- Identify the **top macro events** that move markets most (create a priority list):
  - **High Impact:** NFP (Non-Farm Payroll), CPI (Consumer Price Index), PCE, Federal Reserve Rate Decision
  - **Medium Impact:** PMI (Manufacturing & Services), ISM, Unemployment Rate, Retail Sales, Housing Starts
  - **Optional/Supplementary:** Bond Auctions, Earnings Surprises, Fed Minutes Release
- Research typical release times (e.g., NFP always first Friday 8:30 AM ET)
- Build a **macro calendar mapping** in a CSV or JSON file with: Event Name, Typical Release Time, Frequency, Impact Level, Countries

**Achievements:**

- ✅ Clear understanding of which macro events matter most
- ✅ Calendar of expected releases created
- ✅ Can prioritize which events to track

**Deliverable:** `macro_calendar.csv` or `macro_calendar.json` with structured event metadata

---

### Task 2.2: Build Real-Time Macro Data Fetcher

**What to do:**

- Create a Python script `fetch_macro_data.py` that:
  - Connects to Fred API
  - Fetches the latest values for target indicators (CPI, NFP, PMI, etc.)
  - Extracts key information: event name, release date/time, actual value, forecast, previous value
  - Stores data in a structured format (pandas DataFrame or local database)
  - Implements error handling for API failures and rate limiting
- Add logging to track what data was fetched and when

**Achievements:**

- ✅ Automated data collection from macro APIs
- ✅ Structured storage of macro data with timestamps
- ✅ Robust error handling and logging for debugging

**Key data fields to capture:**

```
- Event Name (CPI, NFP, PMI, etc.)
- Release DateTime (UTC timestamp)
- Actual Value (reported)
- Forecast Value (pre-release expectation)
- Previous Value
- Surprise Magnitude (Actual - Forecast)
- Data Source & Timestamp
```

**Deliverable:** Working `fetch_macro_data.py` script that successfully pulls and stores macro data

---

### Task 2.3: Build Market Price Data Fetcher

**What to do:**

- Create a script `fetch_market_data.py` that pulls **near real-time** market data for 4 asset classes:
  1. **Equities:** SPY (S&P 500), QQQ (Nasdaq 100), IWM (Russell 2000) using `yfinance`
  2. **FX:** EUR/USD, GBP/USD, USD/JPY using `yfinance` or Trading Economics streaming data
  3. **Interest Rates:** 10Y US Treasury Yield (using FRED API - Federal Reserve Economic Data)
  4. **Volatility:** VIX (Volatility Index) using `yfinance`
- Fetch 1-minute and 5-minute candlestick data (OHLCV) for the window around macro releases
- Store prices in a time-indexed DataFrame with proper timezone handling (all UTC)

**Achievements:**

- ✅ Access to 4 asset class price feeds simultaneously
- ✅ Intraday granular data (minute-level) for event reaction capture
- ✅ Unified time-series data structure

**Example asset tickers to fetch:**

```python
equities = ['SPY', 'QQQ', 'IWM']
fx_pairs = ['EURUSD=X', 'GBPUSD=X', 'JPYUSD=X']
rates = ['TNX']  # 10Y Treasury Yield
volatility = ['^VIX']
```

**Deliverable:** Working `fetch_market_data.py` that pulls live/near-live OHLCV data

---

## PHASE 3: Event Detection and Data Alignment

### Task 3.1: Event Trigger Detection System

**What to do:**

- Create `event_detector.py` that:
  - Continuously monitors for new macro releases from the macro data feed
  - Detects when a "surprise" occurs (magnitude of Actual vs Forecast > threshold)
  - Filters for **high-impact events only** (save compute by ignoring minor releases)
  - Logs the exact moment an event is detected with a timestamp
  - Creates an event record with: Event ID, Release DateTime, Surprise Size, Expected Impact
- Implement intelligent thresholds (e.g., only trigger if surprise > 0.5 standard deviations)

**Achievements:**

- ✅ Automatic detection of market-moving events
- ✅ Prioritization of high-impact releases only
- ✅ Clean event logs for later analysis

**Deliverable:** Functional event detection system with test events logged

---

### Task 3.2: Time-Series Alignment Around Event

**What to do:**

- Create `align_event_data.py` that takes a detected macro event and:
  - Defines time windows around the event:
    - **Pre-event window:** -30 min to event release
    - **Immediate reaction:** 0 to +60 min after release
    - **Short-term reaction:** +1 hour to +4 hours
    - **Longer-term:** +4 hours to +24 hours (optional)
  - Extracts price data for all 4 asset classes within these windows
  - Aligns all data to the **same UTC timestamp** (macro event release time = T0)
  - Computes **returns and price changes** from T0 onwards
  - Stores aligned data as a structured dataset keyed by event ID

**Achievements:**

- ✅ Clean, organized time-series data centered on event releases
- ✅ Standardized format for cross-event comparisons
- ✅ Basis for building impact analysis visualizations

**Data structure example:**

```
Event ID: NFP_2024_01_05
Release Time (UTC): 2024-01-05 13:30:00
[-30 min] Asset prices → [0 min] Asset prices → [+60 min] Asset prices
SPY: 475.23 → 475.15 → 476.89
EURUSD: 1.1050 → 1.1045 → 1.1030
TNX: 4.25 → 4.26 → 4.28
VIX: 15.2 → 15.8 → 17.3
```

**Deliverable:** Aligned event-centric datasets for 5-10 detected events

---

### Task 3.3: Compute Event Impact Metrics

**What to do:**

- Create `compute_impact_metrics.py` that for each event calculates:
  - **Price moves (absolute):** Δ price from -30 min to +60 min
  - **Directional moves:** Positive or negative reaction
  - **Volatility surge:** Intraday vol change post-release vs pre-release
  - **Cross-asset correlation:** Which assets moved together/divergently
  - **Beta to macro surprise:** Magnitude of asset move vs size of surprise
  - **Time-to-reversion:** How long did the reaction last
- Create a summary metric: "Impact Score" (aggregate effect across all 4 asset classes)

**Achievements:**

- ✅ Quantified understanding of market reactions
- ✅ Comparable metrics across different events
- ✅ Foundation for pattern analysis

**Example metrics output:**

```
NFP_2024_01_05:
  Surprise: +250k (expected 150k)
  SPY Return: +0.34% (60 min post-release)
  EURUSD Change: -0.23%
  TNX Change: +8 bps
  VIX Surge: +2.1 points
  Volatility Impact Score: 7.8/10
```

**Deliverable:** Metrics CSV/database for all detected events

---

## PHASE 4: Market Impact Analysis & Pattern Discovery

### Task 4.1: Build Cross-Asset Reaction Dashboard (Interactive Visualization)

**What to do:**

- Create `visualize_event_impact.py` using `matplotlib` and `seaborn` that produces:

  1. **4-Panel Price Chart:** One row per asset class (Equities, FX, Rates, Vol) showing 2-hour window around release with:
     - Price line chart
     - Event release marked with vertical red line at T=0
     - Shaded regions for pre-event (-30 to 0) and post-event periods
  2. **Returns Heatmap:** Comparison of returns across asset classes for different time windows
  3. **Volatility Comparison:** Pre-event vs post-event vol for each asset
  4. **Event Metadata Panel:** Text overlay with event details (name, surprise, forecast vs actual)

- Save individual event charts to `output/event_charts/` directory
- Create a **summary dashboard** showing the top 5-10 events in a grid layout

**Achievements:**

- ✅ Clear visual communication of market reactions
- ✅ Instantly see which assets reacted and how much
- ✅ Professional-quality visualizations for portfolio/presentation

**Chart structure example:**

```
┌─────────────────────────────────────────┐
│ Event: CPI Release | Jan 5, 2024 @ 1:30 PM
│ Surprise: +0.15% (expected +0.05%)     │
├─────────────────────────────────────────┤
│ [SPY 2-hr Price Chart with T=0 line]    │
│ [EURUSD 2-hr Price Chart with T=0 line]│
│ [TNX (10Y Yield) 2-hr Chart]            │
│ [VIX 2-hr Chart]                        │
├─────────────────────────────────────────┤
│ 60-Min Returns: SPY -0.24% | EUR -0.18%│
│ Vol Spike: VIX +1.8pts                  │
└─────────────────────────────────────────┘
```

**Deliverable:** Gallery of 10+ professional event impact charts

---

### Task 4.2: Statistical Analysis of Macro-to-Market Linkages

**What to do:**

- Create `analyze_macro_linkages.py` that builds a **correlation matrix:**

  - X-axis: Different macro surprises (CPI surprise, NFP surprise, rate surprise magnitude)
  - Y-axis: Asset reactions (SPY return, EURUSD move, TNX change, VIX change)
  - Calculate Pearson correlation coefficients
  - Identify which macro indicators move which assets most
  - Produce a heatmap: "Which Macro Events Move Which Assets"

- Conduct **regression analysis** (optional, shows advanced quant skills):
  - Regress each asset's reaction on the macro surprise magnitude
  - Report R-squared and coefficients
  - Example: `SPY_60min_return = α + β * NFP_surprise + ε`

**Achievements:**

- ✅ Data-driven understanding of macro-to-market transmission
- ✅ Quantified causal relationships (not just price patterns)
- ✅ Shows you understand economic theory applied to markets

**Example correlation output:**

```
                    CPI_Surprise  NFP_Surprise  RateDecision
SPY_Return               0.32         0.58         0.22
EURUSD_Change           -0.41         0.15        -0.38
TNX_Change               0.85         0.42         0.91
VIX_Change               0.52         0.49         0.67
```

**Deliverable:** Correlation heatmaps and regression summary report

---

### Task 4.3: Identify Recurring Patterns and Edge Cases

**What to do:**

- Create `pattern_detection.py` that analyzes:

  1. **Direction Consistency:** Do certain macro events ALWAYS move certain assets in the same direction?
     - Example: Does CPI surprise ALWAYS move SPY and TNX in opposite directions?
  2. **Volatility Clustering:** Do certain events always trigger vol spikes? Which assets spike together?
  3. **Mean Reversion:** After an event spike, how quickly do prices revert?
  4. **Asset Relative Performance:** In NFP releases, does energy outperform tech? Does USD strengthen?
  5. **Surprise Magnitude Effect:** Is a +500k NFP surprise proportionally 2x more impactful than +250k?

- Document exceptions/edge cases where normal patterns broke (valuable for interviews!)

**Achievements:**

- ✅ Deep market insights ready to discuss with recruiters
- ✅ Identifies potential trading strategies (without implementing trades)
- ✅ Shows understanding of regime changes in markets

**Deliverable:** Pattern analysis report with documented examples

---

## PHASE 5: Dashboard and Automation

### Task 5.1: Build Automated Report Generation

**What to do:**

- Create `generate_report.py` that:
  - Runs on a scheduled basis (daily or after each major event)
  - Collects all new events detected since last report
  - Generates impact metrics and visualizations
  - Creates a **summary PDF report** or markdown document with:
    - Top events of the day/week
    - Cross-asset impact summary
    - Key insights and correlation changes
    - Individual event detail pages with charts
- Use `matplotlib` + `pypdf` or `reportlab` for PDF generation

**Achievements:**

- ✅ Fully automated workflow (show this works!)
- ✅ Professional reporting (impressive for interviews)
- ✅ Real business-like application

**Deliverable:** Auto-generated PDF report from sample data

---

### Task 5.2: Live Monitoring Dashboard (Web-Based)

**What to do:**

- Create a **web dashboard** using `Streamlit` or `Dash` (easier than full Flask app) that displays:

  1. **Real-Time Macro Calendar:** Upcoming releases for the next 7 days
  2. **Live Event Feed:** Shows newly detected events with immediate impact summary
  3. **Cross-Asset Impact Display:** Real-time 4-panel chart showing latest market reactions
  4. **Historical Event Archive:** Searchable/filterable table of past events with impact metrics
  5. **Correlation Dashboard:** Today's macro-to-market linkages (updates intraday)

- Make it interactive: users can click on past events to see detailed charts

**Example using Streamlit:**

```python
import streamlit as st

st.title("Real-Time Macro Event Impact Tracker")

st.header("Upcoming Events (Next 7 Days)")
st.dataframe(upcoming_events)

st.header("Latest Event Detection")
st.metric("Event", "NFP", "Surprise: +250k")
st.image("nfp_impact_chart.png")

st.header("Historical Events")
st.dataframe(historical_events, height=400)
```

**Achievements:**

- ✅ Professional visualization tool
- ✅ Can run locally or deploy to cloud (e.g., Streamlit Cloud)
- ✅ Impressive portfolio piece - shows full-stack capability

**Deliverable:** Working web dashboard running locally or deployed

---

### Task 5.3: Scheduling and Automation

**What to do:**

- Set up automated task scheduling using `APScheduler` or `schedule` library:
  - Every 30 minutes: check for new macro releases
  - Every 2 hours: update market data and check for reactions
  - Daily at 8 AM: generate and save summary report
  - Real-time streaming (if using Trading Economics WebSocket): continuously monitor for events
- Create a `scheduler.py` file that manages all scheduled jobs
- Log all runs to a `logs/` directory for debugging

**Achievements:**

- ✅ Truly "real-time" system (not manual)
- ✅ Shows production engineering mindset
- ✅ Can run unattended 24/5 (markets not open on weekends)

**Example schedule setup:**

```python
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_macro_data, 'interval', minutes=30)
scheduler.add_job(fetch_market_data, 'interval', minutes=5)
scheduler.add_job(detect_events, 'interval', minutes=2)
scheduler.add_job(generate_report, 'cron', hour=8, minute=0)
scheduler.start()
```

**Deliverable:** Working scheduler that runs all pipeline tasks on a defined schedule

---

## PHASE 6: Deployment & Documentation (Bonus)

### Task 6.1: Code Organization and Documentation

**What to do:**

- Organize code into modular structure:

  ```
  macro_tracker/
  ├── config.py              # API keys, parameters
  ├── api_clients.py         # Trading Economics, yfinance wrappers
  ├── data_fetchers.py       # fetch_macro_data(), fetch_market_data()
  ├── event_detection.py     # detect_events(), compute_metrics()
  ├── analysis.py            # correlation, pattern analysis
  ├── visualization.py       # all plotting functions
  ├── database.py            # data storage/retrieval
  ├── scheduler.py           # automated scheduling
  ├── main.py                # entry point
  ├── requirements.txt       # dependencies
  ├── README.md              # project documentation
  └── data/
      ├── macro_calendar.csv
      ├── events.csv
      └── market_data.parquet
  ```

- Add comprehensive docstrings to all functions
- Create a detailed `README.md` with:
  - Project overview and goals
  - API setup instructions
  - How to run each phase
  - Example outputs and charts
  - Architecture diagram

**Achievements:**

- ✅ Professional code quality
- ✅ Easy for recruiters/collaborators to understand
- ✅ Demonstrates software engineering best practices

**Deliverable:** Well-organized GitHub repo with clear documentation

---

### Task 6.2: GitHub and Portfolio Presentation

**What to do:**

- Push project to GitHub with:
  - Clear commit history (show your development process)
  - Comprehensive README with setup instructions
  - Example output charts and reports in `output/` folder
  - License file
- Create a **project writeup** (1-2 page document) for your portfolio:
  - Problem statement: Why track macro event impacts?
  - Solution architecture: How does your system work?
  - Key insights discovered: What did you learn about markets?
  - Technical highlights: APIs used, challenges solved, design decisions
  - Results: Show sample event analyses and charts

**Achievements:**

- ✅ Impressive GitHub project for portfolio
- ✅ Clear communication of what you built and why
- ✅ Ready to discuss in interviews

**Deliverable:** Professional GitHub repo + written project summary

---

## Success Metrics & Interview Talking Points

### What You'll Be Able to Say in Interviews:

1. **"I built an automated system that ingests real-time macro data and detects market-moving events"**

   - Shows: API integration, data engineering, automation

2. **"I can show you that NFP surprises move equities 58% of the time in the same direction as consensus expectations"**

   - Shows: Statistical analysis, market intuition, data storytelling

3. **"My system captured the FX impact of rate decisions within 60 minutes of release"**

   - Shows: Cross-asset understanding, timing/precision

4. **"I automated the entire pipeline from data ingestion to report generation using APScheduler"**

   - Shows: Full-stack thinking, production readiness

5. **"I discovered that volatility spikes are most pronounced in the 30 minutes immediately after NFP, then mean-revert within 4 hours"**

   - Shows: Pattern recognition, market timing insights

6. **"The dashboard visualizes correlations between macro surprises and asset moves in real-time"**
   - Shows: UX thinking, data visualization skills

---

## Timeline Estimate

| Phase     | Tasks                       | Estimated Time  |
| --------- | --------------------------- | --------------- |
| 1         | Setup & Auth                | 2-3 hours       |
| 2         | Data Ingestion              | 8-10 hours      |
| 3         | Event Detection & Alignment | 6-8 hours       |
| 4         | Analysis & Patterns         | 8-10 hours      |
| 5         | Dashboard & Automation      | 6-8 hours       |
| 6         | Deployment & Docs           | 3-4 hours       |
| **TOTAL** |                             | **33-43 hours** |

**Realistic pace:** 1-2 weeks part-time, 3-5 days full-time

---

## Resources & Learning Links

### APIs

- **Trading Economics:** https://tradingeconomics.com/member/register (free tier available)
- **FRED (Federal Reserve):** https://fred.stlouisfed.org/docs/api/ (free, no key needed for basic use)
- **Yahoo Finance (yfinance):** https://finance.yahoo.com (free via yfinance library)

### Python Libraries

- `yfinance` - stock/ETF/index data
- `pandas-datareader` - FRED and other sources
- `tradingeconomics` - macro data
- `APScheduler` - task scheduling
- `Streamlit` or `Dash` - web dashboards
- `matplotlib`, `seaborn` - visualizations

### Concepts to Understand

- Macro event calendars and impact classifications
- Cross-asset correlations and contagion
- Mean reversion in asset prices
- Volatility clustering
- FX carry trades and rate parity

---

## Final Advice for Recruiters

Frame your project like this:

> "I built a real-time macro event impact tracker that automatically detects major economic releases and measures their ripple effects across equities, currencies, interest rates, and volatility. The system revealed that NFP surprises drive 58% of near-term equity moves and that FX reacts most strongly to rate decisions. This taught me how macro shocks propagate through markets in real time."

**This shows:** Full-stack engineering (data pipelines, APIs, automation), quantitative analysis (statistics, correlation), domain knowledge (macro, markets), and the ability to connect dots between different asset classes.

Good luck! 🚀
