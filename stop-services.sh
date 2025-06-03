#!/bin/bash

# 設置顏色
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}停止 ContextRecord 服務...${NC}"

# 停止MCP服務器
cd /Users/gamepig/projects/MCP_Servers/ContextRecord/mcp-server
echo -e "${RED}停止MCP服務器容器...${NC}"
docker-compose down
sleep 2

# 停止主應用
cd /Users/gamepig/projects/MCP_Servers/ContextRecord
echo -e "${RED}停止主應用容器...${NC}"
docker-compose down
sleep 2

echo -e "${GREEN}檢查服務狀態:${NC}"
docker ps | grep context-record
docker ps | grep contextrecord-mcp

echo -e "${YELLOW}所有服務已停止!${NC}" 