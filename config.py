# =================================================
# FMCG EXECUTIVE INTELLIGENCE PLATFORM
# Global Application Configuration
# =================================================

# -------------------------------------------------
# App Identity
# -------------------------------------------------
APP_TITLE = "FMCG Executive Intelligence Dashboard"
APP_TAGLINE = "Production-Grade FMCG & MFD Business Intelligence System"
APP_ICON = "📊"
LAYOUT = "wide"

# -------------------------------------------------
# Branding
# -------------------------------------------------
BRAND_NAME = "DS Group"
PRIMARY_COLOR = "#1F7A4F"
SECONDARY_COLOR = "#F5F7FA"

# -------------------------------------------------
# Session State Keys (⚠ DO NOT CHANGE)
# -------------------------------------------------
SESSION_DF_KEY = "df"
SESSION_SOURCE_KEY = "data_source"   # uploader | snowflake
SESSION_SNOWFLAKE_CONN = "sf_conn"

# -------------------------------------------------
# Formatting
# -------------------------------------------------
DEFAULT_DATE_FORMAT = "%Y-%m-%d"
CURRENCY_SYMBOL = "₹"
NUMBER_FORMAT = ",.0f"

# -------------------------------------------------
# Forecasting Defaults
# -------------------------------------------------
DEFAULT_FORECAST_MONTHS = 12
MIN_FORECAST_MONTHS = 3
MAX_FORECAST_MONTHS = 24

# -------------------------------------------------
# Segmentation Defaults
# -------------------------------------------------
DEFAULT_CLUSTERS = 3
MIN_CLUSTERS = 2
MAX_CLUSTERS = 6

# -------------------------------------------------
# Churn / Risk Rules
# -------------------------------------------------
HIGH_CHURN_DAYS = 60
MEDIUM_CHURN_DAYS = 30

# -------------------------------------------------
# Snowflake Configuration (ENV-BASED)
# -------------------------------------------------
SNOWFLAKE_ACCOUNT = None
SNOWFLAKE_USER = None
SNOWFLAKE_PASSWORD = None
SNOWFLAKE_WAREHOUSE = None
SNOWFLAKE_DATABASE = None
SNOWFLAKE_SCHEMA = None
SNOWFLAKE_ROLE = None

# -------------------------------------------------
# Feature Flags
# -------------------------------------------------
DEBUG_MODE = False
ENABLE_PROPHET = True
ENABLE_SNOWFLAKE = True
ENABLE_AI_SUMMARY = True

# -------------------------------------------------
# Performance Guards
# -------------------------------------------------
MAX_ROWS_PREVIEW = 50000
ENABLE_CACHING = True
