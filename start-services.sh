#!/bin/bash

# 設置顏色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}啟動 ContextRecord 服務...${NC}"

# 啟動主應用
cd /Users/gamepig/projects/MCP_Servers/ContextRecord
echo -e "${GREEN}啟動主應用容器...${NC}"
docker-compose up -d
sleep 2

# 啟動MCP服務器
cd /Users/gamepig/projects/MCP_Servers/ContextRecord/mcp-server
echo -e "${GREEN}啟動MCP服務器容器...${NC}"
docker-compose up -d
sleep 2

echo -e "${GREEN}檢查服務狀態:${NC}"
docker ps | grep context-record
docker ps | grep contextrecord-mcp

echo -e "${YELLOW}所有服務已啟動!${NC}"
echo -e "${GREEN}主應用: http://localhost:8000${NC}"
echo -e "${GREEN}MCP服務: http://localhost:8812/mcp${NC}"
echo -e "${GREEN}API文檔: http://localhost:8000/docs${NC}"

# 完成
echo -e "${YELLOW}您可以在Cursor IDE中使用ContextRecord MCP服務${NC}" 