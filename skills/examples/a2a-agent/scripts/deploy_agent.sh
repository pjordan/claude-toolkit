#!/bin/bash
# Script to deploy an A2A agent using Docker

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default values
AGENT_NAME="a2a-agent"
PORT=8000
BUILD_ONLY=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --name)
            AGENT_NAME="$2"
            shift 2
            ;;
        --port)
            PORT="$2"
            shift 2
            ;;
        --build-only)
            BUILD_ONLY=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${YELLOW}🚀 Deploying A2A Agent: $AGENT_NAME${NC}"
echo ""

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo -e "${RED}❌ Error: Dockerfile not found${NC}"
    exit 1
fi

# Build Docker image
echo -e "${GREEN}Building Docker image...${NC}"
docker build -t "$AGENT_NAME:latest" .

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Docker build failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker image built successfully${NC}"

# Exit if build-only
if [ "$BUILD_ONLY" = true ]; then
    echo -e "${YELLOW}Build complete (--build-only specified)${NC}"
    exit 0
fi

# Stop existing container
echo ""
echo -e "${GREEN}Stopping existing container (if any)...${NC}"
docker stop "$AGENT_NAME" 2>/dev/null || true
docker rm "$AGENT_NAME" 2>/dev/null || true

# Run container
echo ""
echo -e "${GREEN}Starting container...${NC}"
docker run -d \
    --name "$AGENT_NAME" \
    -p "$PORT:8000" \
    --restart unless-stopped \
    "$AGENT_NAME:latest"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to start container${NC}"
    exit 1
fi

# Wait for health check
echo ""
echo -e "${GREEN}Waiting for agent to be ready...${NC}"
sleep 3

HEALTH_CHECK=$(curl -s "http://localhost:$PORT/health" || echo "failed")

if [[ $HEALTH_CHECK == *"healthy"* ]]; then
    echo -e "${GREEN}✅ Agent deployed successfully!${NC}"
    echo ""
    echo "Agent details:"
    echo "  Name: $AGENT_NAME"
    echo "  Port: $PORT"
    echo "  Health: http://localhost:$PORT/health"
    echo "  Docs: http://localhost:$PORT/docs"
    echo ""
    echo "View logs: docker logs -f $AGENT_NAME"
    echo "Stop agent: docker stop $AGENT_NAME"
else
    echo -e "${RED}❌ Agent health check failed${NC}"
    echo "View logs: docker logs $AGENT_NAME"
    exit 1
fi
