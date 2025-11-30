FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Copy the top-level requirements (project root within the build context)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the full context into the container. This ensures modules like `config` and
# the `ecommerce`/`store` apps are available regardless of layout.
COPY . /app

EXPOSE 8000

# Use the `config` package wsgi entrypoint that was added to the project.
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
