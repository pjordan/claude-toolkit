#!/bin/bash
# Script to run tests for an A2A agent

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🧪 Running A2A Agent Tests${NC}"
echo ""

# Check if we're in an agent directory
if [ ! -f "main.py" ]; then
    echo -e "${RED}❌ Error: main.py not found. Run this script from your agent directory.${NC}"
    exit 1
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${YELLOW}⚠️  pytest not installed. Installing...${NC}"
    pip install pytest pytest-asyncio httpx
fi

# Run tests
echo -e "${GREEN}Running unit tests...${NC}"
if [ -f "test_agent.py" ]; then
    pytest test_agent.py -v
else
    echo -e "${YELLOW}⚠️  No test_agent.py found${NC}"
fi

# Check if agent can start
echo ""
echo -e "${GREEN}Testing agent startup...${NC}"
timeout 5s python main.py &
PID=$!
sleep 2

if ps -p $PID > /dev/null; then
    echo -e "${GREEN}✅ Agent started successfully${NC}"
    kill $PID
else
    echo -e "${RED}❌ Agent failed to start${NC}"
    exit 1
fi

# Test health endpoint
echo ""
echo -e "${GREEN}Testing health endpoint...${NC}"
python main.py &
PID=$!
sleep 2

HEALTH_CHECK=$(curl -s http://localhost:8000/health || echo "failed")
kill $PID

if [[ $HEALTH_CHECK == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ All tests passed!${NC}"
