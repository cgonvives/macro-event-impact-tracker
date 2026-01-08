"""
Configuration management for Macro Event Tracker
Uses ONLY FREE APIs - No paid subscriptions needed!
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# PROJECT PATHS
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
OUTPUT_DIR = PROJECT_ROOT / 'output'
LOGS_DIR = PROJECT_ROOT / 'logs'
CONFIG_DIR = PROJECT_ROOT / 'config'

# Create subdirectories if they don't exist
for directory in [DATA_DIR, OUTPUT_DIR, LOGS_DIR]:
    directory.mkdir(exist_ok=True)
    (directory / 'raw').mkdir(exist_ok=True)
    (directory / 'processed').mkdir(exist_ok=True)

(OUTPUT_DIR / 'charts').mkdir(exist_ok=True)
(OUTPUT_DIR / 'reports').mkdir(exist_ok=True)

# ============================================================================
# API CREDENTIALS - ALL FREE, NO PAYMENT REQUIRED
# ============================================================================

# FRED API (Federal Reserve Economic Data) - FREE
# Register at: https://fred.stlouisfed.org/docs/api/api-key.html
FRED_API_KEY = os.getenv('FRED_API_KEY', 'demo')

# Trading Economics - OPTIONAL (free tier has limitations)
# Only use if you want to track Mexico, New Zealand, Sweden, Thailand
TRADINGECONOMICS_KEY = os.getenv('TRADINGECONOMICS_KEY', '')
TRADINGECONOMICS_SECRET = os.getenv('TRADINGECONOMICS_SECRET', '')

# Note: We use yfinance (100% free) for all price data
# No API key needed!

if FRED_API_KEY == 'demo':
    print("⚠️  FRED API key not set. Register at:")
    print("   https://fred.stlouisfed.org/docs/api/api-key.html")
    print("   (It's completely free!)")

# ============================================================================
# MACRO INDICATORS TO TRACK - Using FRED API (All US data)
# ============================================================================

# These indicators are available FREE from FRED
# We use FRED series codes (e.g., "CPIAUCSL" = Consumer Price Index)

FRED_INDICATORS = {
    'CPIAUCSL': {
        'name': 'Consumer Price Index (CPI)',
        'frequency': 'monthly',
        'impact': 'HIGH',
        'typical_release': 'Second week of month, 8:30 AM ET'
    },
    'PAYEMS': {
        'name': 'Non-Farm Payroll (NFP) - Total Employment',
        'frequency': 'monthly',
        'impact': 'VERY HIGH',  # Most important!
        'typical_release': 'First Friday of month, 8:30 AM ET'
    },
    'UNRATE': {
        'name': 'Unemployment Rate',
        'frequency': 'monthly',
        'impact': 'HIGH',
        'typical_release': 'First Friday of month, 8:30 AM ET'
    },
    'UMCSENT': {
        'name': 'University of Michigan Consumer Sentiment',
        'frequency': 'monthly',
        'impact': 'MEDIUM',
        'typical_release': 'Mid-month and end-of-month'
    },
    'INDPRO': {
        'name': 'Industrial Production',
        'frequency': 'monthly',
        'impact': 'MEDIUM',
        'typical_release': 'Mid-month, 9:15 AM ET'
    },
    'ICSA': {
        'name': 'Initial Jobless Claims',
        'frequency': 'weekly',
        'impact': 'MEDIUM',
        'typical_release': 'Every Thursday, 8:30 AM ET'
    },
    'T10Y2Y': {
        'name': '10-Year / 2-Year Treasury Spread',
        'frequency': 'daily',
        'impact': 'MEDIUM',
        'typical_release': 'Daily at close'
    }
}

# ============================================================================
# WHICH ASSETS TO MONITOR - 4 Asset Classes (All from FREE yfinance)
# ============================================================================

ASSETS = {
    'equities': [
        'SPY',    # S&P 500 (US large cap)
        'QQQ',    # Nasdaq 100 (US tech)
        'IWM',    # Russell 2000 (US small cap)
        'DIA',    # Dow Jones Industrial Average
    ],
    'fx': [
        'EURUSD=X',   # Euro/Dollar
        'GBPUSD=X',   # Pound/Dollar
        'JPYUSD=X',   # Japanese Yen/Dollar
    ],
    'rates': [
        'TNX',    # 10-Year US Treasury Yield
        '^TNX',   # Alternative ticker for same
    ],
    'volatility': [
        '^VIX',   # Fear Index / VIX
    ]
}

# ============================================================================
# TIME WINDOWS - How to Measure Market Reactions
# ============================================================================

TIME_WINDOWS = {
    'pre_event': 30,          # 30 minutes BEFORE release (baseline)
    'immediate': 60,          # 60 minutes AFTER (immediate market reaction)
    'short_term': 240,        # 4 hours AFTER (broader adjustments)
    'long_term': 1440,        # 24 hours AFTER (overnight/next day effects)
}

# ============================================================================
# EVENT DETECTION THRESHOLDS
# ============================================================================

# Only trigger alerts for SIGNIFICANT surprises
# Example: If NFP expected 150k but actual is 200k, that's a big surprise

SURPRISE_THRESHOLD_STD = 0.5  
# Alert if: |Actual - Forecast| > 0.5 standard deviations

MIN_SURPRISE_MAGNITUDE = 0.1  
# Ignore surprises smaller than 0.1% (noise)

# ============================================================================
# ECONOMIC CALENDAR - Release Times for Major US Events
# ============================================================================

# You'll manually update these or scrape from tradingeconomics.com/calendar
# Format: 'FRED_SERIES_CODE': release_time (in ET)

RELEASE_SCHEDULE = {
    'CPIAUCSL': {
        'month_day': 'Second week of month',
        'time': '08:30 ET',
        'forecast_source': 'FRED'
    },
    'PAYEMS': {
        'month_day': 'First Friday of month',
        'time': '08:30 ET',
        'forecast_source': 'FRED'
    },
    'UNRATE': {
        'month_day': 'First Friday of month',
        'time': '08:30 ET',
        'forecast_source': 'FRED'
    },
    'ICSA': {
        'month_day': 'Every Thursday',
        'time': '08:30 ET',
        'forecast_source': 'FRED'
    },
}

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = LOGS_DIR / 'macro_tracker.log'

# ============================================================================
# SCHEDULER CONFIGURATION
# ============================================================================

SCHEDULER_CONFIG = {
    'macro_data_interval': 60,          # Check FRED for new data every 60 min
    'market_data_interval': 5,          # Get prices every 5 minutes
    'event_detection_interval': 2,      # Check for events every 2 minutes
    'report_generation_hour': 8,        # Generate report at 8 AM
    'report_generation_minute': 0,
}

# ============================================================================
# DATABASE CONFIGURATION - Local SQLite (Free, no setup needed)
# ============================================================================

DATABASE_URL = f'sqlite:///{DATA_DIR / "macro_tracker.db"}'

# ============================================================================
# STREAMLIT DASHBOARD CONFIGURATION
# ============================================================================

STREAMLIT_CONFIG = {
    'theme_primary_color': '#2180a1',
    'max_rows_to_display': 100,
    'chart_height': 400,
    'cache_duration_hours': 24,
}

# ============================================================================
# HELPER FUNCTION
# ============================================================================

def print_config():
    """Print current configuration"""
    print("\n" + "="*60)
    print("MACRO EVENT TRACKER - CONFIGURATION")
    print("="*60)
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Output Directory: {OUTPUT_DIR}")
    print(f"\n📊 Data Sources (ALL FREE):")
    print(f"   - FRED API: ✅ Configured" if FRED_API_KEY != 'demo' else "   - FRED API: ⚠️  Not configured")
    print(f"   - yfinance: ✅ Always available (no key needed)")
    print(f"\n📈 Tracking:")
    print(f"   - Macro Indicators: {len(FRED_INDICATORS)}")
    print(f"   - Assets: {sum(len(v) for v in ASSETS.values())}")
    print(f"     • Equities: {len(ASSETS['equities'])}")
    print(f"     • FX Pairs: {len(ASSETS['fx'])}")
    print(f"     • Rates: {len(ASSETS['rates'])}")
    print(f"     • Volatility: {len(ASSETS['volatility'])}")
    print(f"\n💰 Total Cost: $0 (completely free)")
    print("="*60 + "\n")

if __name__ == '__main__':
    print_config()
