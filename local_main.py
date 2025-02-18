#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=".env")
sleep_time = os.getenv("SLEEP")
if sleep_time is None:
    os.environ["SLEEP"] = "-1" # break instead of sleep
from central_bank_scraper.main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Central Bank Scraper")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")

    args = parser.parse_args()
    main(run_headless=args.headless)