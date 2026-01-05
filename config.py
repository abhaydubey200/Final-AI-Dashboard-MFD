# =================================================
# FMCG EXECUTIVE INTELLIGENCE PLATFORM
# Global Application Configuration
# =================================================

import os

# -------------------------------------------------
# App Identity
# -------------------------------------------------
APP_NAME = "Home"
APP_TITLE = "DS Group FMCG Executive Intelligence"
APP_TAGLINE = "AI-Powered FMCG & MFD Business Intelligence Platform"

# Use favicon path (NOT emoji) – enterprise standard
APP_ICON = "assets/ds_group_favicon.png"

LAYOUT = "wide"

# -------------------------------------------------
# Branding (Theme Tokens)
# -------------------------------------------------
BRAND_NAME = "DS Group"

PRIMARY_COLOR = "#1F7A4F"     # DS Group Green
SECONDARY_COLOR = "#F5F7FA"   # Executive Grey
TEXT_COLOR = "#000000"

# -------------------------------------------------
# Session State Keys (⚠ DO NOT CHANGE)
# -------------------------------------------------
SESSION_DF_KEY = "df"
SESSION_SOURCE_KEY = "data_source"        # upload | snowflake
SESSION_SNOWFLAKE_CONN = "sf_connection"

# -------------------------------------------------
# Formatting Standards
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
# Snowflake Configuration (ENV BASED – REQUIRED)
# -------------------------------------------------
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")

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
MAX_ROWS_PREVIEW = 50_000
ENABLE_CACHING = True
