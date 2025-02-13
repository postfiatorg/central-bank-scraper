# Use Python 3.11 slim as the base image
FROM python:3.11-slim AS base


ENV DEBIAN_FRONTEND=noninteractive \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_ROOT_USER_ACTION=ignore \
  # poetry:
  POETRY_VERSION=2.0.1 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/tmp/poetry_cache' \
  POETRY_HOME=/etc/poetry \
  PATH="${PATH}:/etc/poetry/bin"


SHELL ["/bin/bash", "-eo", "pipefail", "-c"]

# Install required tools and dependencies
# Install required tools and dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    tini \
    curl \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcairo2 \
    libcups2 \
    libcurl4 \
    libdbus-1-3 \
    libexpat1 \
    libgbm1 \
    libgtk-3-0 \
    libpango-1.0-0 \
    libvulkan1 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    libnss3 \
    xdg-utils \
    --no-install-recommends && \
    curl -sSL "https://install.python-poetry.org" | python - && \
    # Cleaning cache:
    apt-get -y purge --auto-remove -o APT::AutoRemove::RecommendsImportant=false && \
    apt-get -y clean && rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Download and install a specific version of Google Chrome
RUN wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_132.0.6834.110-1_amd64.deb -O google-chrome.deb && \
    dpkg -i google-chrome.deb  && \
    rm google-chrome.deb

# Install ChromeDriver
RUN wget -q https://storage.googleapis.com/chrome-for-testing-public/132.0.6834.110/linux64/chromedriver-linux64.zip && \
    unzip chromedriver-linux64.zip && \
    mv chromedriver-linux64/chromedriver /usr/bin/chromedriver

RUN groupadd -r scraper && useradd -d /app -r -g scraper scraper  \
    && chown scraper:scraper -R /app 


COPY --chown=scraper:scraper ./pyproject.toml ./poetry.lock /app/
COPY --chown=scraper:scraper agti /app/agti
COPY ./central_bank_scraper/__init__.py /app/central_bank_scraper/

RUN poetry run pip install pip --upgrade \
  && poetry --version && poetry run pip --version \
  && poetry install \
    --no-interaction --no-ansi --sync --no-root && \
    rm -rf "$POETRY_CACHE_DIR"



USER scraper

FROM base AS production_build
COPY --chown=scraper:scraper . /app
RUN chmod +x /app/deploy/*.sh
ENTRYPOINT ["tini", "-g", "--", "/app/deploy/runner.sh"]

