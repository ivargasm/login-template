FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install astral uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

# Copy dependency files
COPY pyproject.toml .

# Install dependencies (will create a virtualenv managed by uv automatically if we don't, or we can just use uv run)
# We can just sync dependencies
RUN uv sync

# We do not COPY the rest of the application code because we are going to use Docker volumes 
# for hot-reloading in development.
# If this were for production, we would COPY . . here.

# Expose port
EXPOSE 8000

# Set entrypoint to the start script
CMD ["./start.sh"]
