import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "analysis_outputs"

# AWS Configuration
AWS_REGION = "us-west-2"
BEDROCK_MODEL = "anthropic.claude-3-5-haiku-20241022-v1:0"

# Analysis Settings
MAX_NEWS_ITEMS = 5
SENTIMENT_THRESHOLD_POSITIVE = 0.2
SENTIMENT_THRESHOLD_NEGATIVE = -0.2

# Create necessary directories
OUTPUT_DIR.mkdir(exist_ok=True) 