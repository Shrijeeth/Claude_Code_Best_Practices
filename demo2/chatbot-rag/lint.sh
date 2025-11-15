#!/bin/bash

# Ruff linting and formatting script for chatbot-rag project

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Default action
ACTION="${1:-check}"

echo -e "${GREEN}Running ruff ${ACTION}...${NC}\n"

case "$ACTION" in
    format)
        echo -e "${YELLOW}Formatting code with ruff...${NC}"
        uv run ruff format backend/ frontend/
        echo -e "${GREEN}✓ Formatting complete${NC}"
        ;;

    check)
        echo -e "${YELLOW}Checking code with ruff (no fixes)...${NC}"
        uv run ruff check backend/ frontend/
        echo -e "${GREEN}✓ Check complete${NC}"
        ;;

    fix)
        echo -e "${YELLOW}Checking and auto-fixing issues...${NC}"
        uv run ruff check --fix backend/ frontend/
        echo -e "${GREEN}✓ Auto-fix complete${NC}"
        ;;

    all)
        echo -e "${YELLOW}Running full lint and format...${NC}"
        echo -e "\n${YELLOW}Step 1: Auto-fixing lint issues...${NC}"
        uv run ruff check --fix backend/ frontend/

        echo -e "\n${YELLOW}Step 2: Formatting code...${NC}"
        uv run ruff format backend/ frontend/

        echo -e "\n${YELLOW}Step 3: Final check...${NC}"
        uv run ruff check backend/ frontend/

        echo -e "\n${GREEN}✓ All checks complete${NC}"
        ;;

    *)
        echo -e "${RED}Unknown action: $ACTION${NC}"
        echo ""
        echo "Usage: ./lint.sh [action]"
        echo ""
        echo "Actions:"
        echo "  format  - Format code using ruff (includes import sorting)"
        echo "  check   - Check for linting issues without fixing"
        echo "  fix     - Auto-fix linting issues (includes import sorting)"
        echo "  all     - Run fix + format + check (recommended)"
        echo ""
        echo "Examples:"
        echo "  ./lint.sh format    # Format code"
        echo "  ./lint.sh fix       # Fix linting issues"
        echo "  ./lint.sh all       # Full lint and format"
        exit 1
        ;;
esac
