FROM python:3.13-slim as builder

WORKDIR /app

# 安裝構建依賴
RUN pip install --no-cache-dir uv

# 複製 requirements 檔案
COPY requirements.txt .

# 使用 uv 安裝依賴
RUN uv pip install --system -r requirements.txt

# 第二階段：運行階段
FROM python:3.13-slim

WORKDIR /app

# 從 builder 階段複製已安裝的 Python 套件
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# 安裝 curl 用於健康檢查
RUN apt-get update && apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# 建立資料目錄
RUN mkdir -p /app/data && chmod 777 /app/data

# 複製專案檔案
COPY . .

# 設定環境變數
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8811 \
    DATABASE_URL=sqlite+aiosqlite:///data/app.db

# 暴露端口
EXPOSE 8811

# 設定健康檢查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8811/ || exit 1

# 啟動應用
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8811"] 