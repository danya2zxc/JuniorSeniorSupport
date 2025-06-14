FROM python:3.12-slim@sha256:0175d8ff0ad1dc8ceca4bcf311c3e47d08807a940959fa1cdbcefa87841883a1


# Set envs to avoid .pyc files and enable Poetry's virtualenv disabling
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Install system dependencies
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \ 
    build-essential \
    curl && \
    # cleaning up unused files
    rm -rf /var/lib/apt/lists/*



# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -



# Set working dir
WORKDIR /app

# Copy only files required to install dependencies
COPY pyproject.toml poetry.lock ./

# install project dependencies
RUN poetry install --no-interaction --no-ansi


# Copy full project
COPY ./ ./

# Expose port
EXPOSE 8000


# Run app 
CMD ["uvicorn", "src.main:app", "--reload", "--port", "8000", "--host", "0.0.0.0", "--log-level=debug"]
