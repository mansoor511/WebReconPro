#!/bin/bash

# ============================================================
# WebRecon Pro - Installation Script
# Coded by: MANSOOR BIK KAMALI
# ============================================================

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║         WebRecon Pro - Installation Script               ║"
echo "║              Coded by: MANSOOR BIK KAMALI                ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check Python
echo -e "${YELLOW}[*] Checking Python...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[-] Python3 not found! Installing...${NC}"
    sudo apt update
    sudo apt install python3 python3-pip -y
fi
echo -e "${GREEN}[+] Python3 found!${NC}"

# Install packages
echo -e "\n${YELLOW}[*] Installing Python packages...${NC}"

# Try with --break-system-packages first (Kali/Debian new)
pip3 install -r requirements.txt --break-system-packages 2>/dev/null

# If failed, try with --user
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[*] Trying alternative method...${NC}"
    pip3 install -r requirements.txt --user 2>/dev/null
fi

# If failed, try apt
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}[*] Trying apt method...${NC}"
    sudo apt install python3-requests python3-bs4 python3-dnspython python3-whois -y
fi

# Verify installation
echo -e "\n${YELLOW}[*] Verifying installation...${NC}"
python3 -c "import requests; import bs4; import dns.resolver; import whois" 2>/dev/null

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[+] All packages installed successfully!${NC}"
else
    echo -e "${RED}[-] Some packages failed to install!${NC}"
    echo -e "${YELLOW}[!] Try manually: pip3 install -r requirements.txt --break-system-packages${NC}"
fi

# Make executable
chmod +x webrecon.py

# Create output directory
mkdir -p webrecon_output
touch webrecon_output/.gitkeep

echo -e "\n${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${CYAN}▶️  Usage:${NC}"
echo -e "   python3 webrecon.py https://example.com"
echo ""
echo -e "${CYAN}▶️  Example:${NC}"
echo -e "   python3 webrecon.py http://qasid.af"
echo ""