# STAGE 1: Builder
FROM python:3.12.3-slim as builder

WORKDIR /app

# Create a virtual environment to isolate dependencies
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY project_docker_k8s_helm/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# STAGE 2: Final Runtime
FROM python:3.12.3-slim

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]