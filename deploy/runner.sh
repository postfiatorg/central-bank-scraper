#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

exec python -m central_bank_scraper.main