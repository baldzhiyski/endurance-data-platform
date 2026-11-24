FROM node:22-bookworm-slim AS web
WORKDIR /build
COPY frontend/package*.json ./
RUN npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app/backend
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY backend/endurance ./endurance
COPY --from=web /build/dist /app/frontend/dist
USER 65532:65532
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "endurance.main:app", "--host", "0.0.0.0", "--port", "8000"]
