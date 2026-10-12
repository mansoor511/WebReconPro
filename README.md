# 🔍 WebRecon Pro

<div align="center">

![Version](https://img.shields.io/badge/version-3.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![License](https://img.shields.io/badge/license-MIT-red)
![Author](https://img.shields.io/badge/author-MANSOOR%20BIK%20KAMALI-purple)

**Ultimate Web Reconnaissance Tool for Ethical Security Testing**

</div>

---

## 📌 About

**WebRecon Pro** is a powerful and comprehensive web reconnaissance tool designed for ethical hackers, penetration testers, and security researchers.

> ⚠️ **Disclaimer:** Use only on websites you own or have **written permission** to test.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔍 **IP Resolution** | Resolves domain to IP addresses |
| 🌐 **DNS Enumeration** | A, AAAA, MX, NS, TXT, SOA, CNAME records |
| 🔎 **Subdomain Discovery** | 68+ common subdomains |
| 📁 **Directory Brute-Force** | 97+ common directories |
| 🕷️ **URL Crawling** | Crawls and extracts all URLs |
| 📜 **JavaScript Analysis** | Finds API endpoints in JS files |
| 🔌 **Port Scanning** | 40+ common ports |
| ⚙️ **Technology Detection** | Detects server, CMS, frameworks |
| 📋 **WHOIS Lookup** | Domain registration info |
| 🔒 **SSL Check** | Certificate issuer and expiry |

---

## 🖥️ System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Kali Linux / Ubuntu / Debian | Kali Linux 2024+ |
| **Python** | 3.8+ | 3.10+ |
| **RAM** | 2 GB | 4 GB+ |
| **Disk** | 100 MB | 500 MB+ |
| **Internet** | Required | Stable connection |

---

## 📦 Complete Installation Guide

### 🔧 Step 1: Update System

```bash
sudo apt update && sudo apt upgrade -y
```

---

### 🐍 Step 2: Install Python & pip

```bash
# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv -y

# Verify installation
python3 --version
pip3 --version
```

Expected output:
```
Python 3.11.x
pip 23.x.x
```

---

### 📚 Step 3: Install Required Python Packages

WebRecon Pro requires the following Python packages:

| Package | Version | Purpose |
|---------|---------|---------|
| **requests** | ≥2.28.0 | HTTP requests |
| **beautifulsoup4** | ≥4.11.0 | HTML parsing |
| **dnspython** | ≥2.2.0 | DNS resolution |
| **python-whois** | ≥0.9.0 | WHOIS lookup |

#### Method A: Install via pip (Recommended)

```bash
pip3 install requests beautifulsoup4 dnspython python-whois --break-system-packages
```

#### Method B: Install via apt (Debian/Kali)

```bash
sudo apt install python3-requests python3-bs4 python3-dnspython python3-whois -y
```

#### Method C: Install in Virtual Environment

```bash
# Create virtual environment
python3 -m venv webrecon-env

# Activate
source webrecon-env/bin/activate

# Install packages
pip install requests beautifulsoup4 dnspython python-whois
```

#### Method D: Install via requirements.txt

```bash
pip3 install -r requirements.txt --break-system-packages
```

---

### ✅ Step 4: Verify Installation

Run this command to verify all packages are installed:

```bash
python3 -c "import requests; import bs4; import dns.resolver; import whois; print('✅ All packages installed successfully!')"
```

If you see this message, installation is complete:
```
✅ All packages installed successfully!
```

---

### 📥 Step 5: Clone the Repository

```bash
git clone https://github.com/mansoor511/WebReconPro.git
cd WebReconPro
```

---

### 🔐 Step 6: Make Executable

```bash
chmod +x webrecon.py
chmod +x install.sh
```

---

## 🛠️ Manual Installation (Step-by-Step)

If automatic installation fails, follow these steps manually:

### 1️⃣ Install Python 3

```bash
sudo apt update
sudo apt install python3 python3-pip -y
```

### 2️⃣ Install `requests` Package

```bash
pip3 install requests --break-system-packages
```

Verify:
```bash
python3 -c "import requests; print('requests OK')"
```

### 3️⃣ Install `beautifulsoup4` Package

```bash
pip3 install beautifulsoup4 --break-system-packages
```

Verify:
```bash
python3 -c "import bs4; print('beautifulsoup4 OK')"
```

### 4️⃣ Install `dnspython` Package

```bash
pip3 install dnspython --break-system-packages
```

Verify:
```bash
python3 -c "import dns.resolver; print('dnspython OK')"
```

### 5️⃣ Install `python-whois` Package

```bash
pip3 install python-whois --break-system-packages
```

Verify:
```bash
python3 -c "import whois; print('python-whois OK')"
```

### 6️⃣ Verify All Packages

```bash
python3 -c "
import requests
import bs4
import dns.resolver
import whois
print('✅ All packages installed!')
"
```

---

## 🔧 Troubleshooting

### ❌ Error: `externally-managed-environment`

**Solution:** Add `--break-system-packages` flag:

```bash
pip3 install requests --break-system-packages
```

### ❌ Error: `No module named 'dns'`

**Solution:** Install `dnspython`:

```bash
pip3 install dnspython --break-system-packages
```

### ❌ Error: `No module named 'whois'`

**Solution:** Install `python-whois`:

```bash
pip3 install python-whois --break-system-packages
```

### ❌ Error: `No module named 'bs4'`

**Solution:** Install `beautifulsoup4`:

```bash
pip3 install beautifulsoup4 --break-system-packages
```

### ❌ Error: `Permission denied`

**Solution:** Use `sudo` or run in virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ Error: `pip: command not found`

**Solution:** Install pip:

```bash
sudo apt install python3-pip -y
```

---

## 🚀 Usage

### Basic Usage

```bash
python3 webrecon.py https://example.com
```

### Custom Threads

```bash
python3 webrecon.py https://example.com -t 30
```

### Real Examples

```bash
# Scan your own site
python3 webrecon.py http://qasid.af

# Scan with more threads
python3 webrecon.py https://example.com -t 50
```

---

## 📁 Output

Results are saved in `webrecon_output/`:

```
webrecon_output/
├── recon_example.com_20261012_062713.json    # JSON format
└── recon_example.com_20261012_062713.txt     # Text report
```

---

## 📋 Package List Summary

| # | Package | Install Command |
|---|---------|-----------------|
| 1 | **requests** | `pip3 install requests --break-system-packages` |
| 2 | **beautifulsoup4** | `pip3 install beautifulsoup4 --break-system-packages` |
| 3 | **dnspython** | `pip3 install dnspython --break-system-packages` |
| 4 | **python-whois** | `pip3 install python-whois --break-system-packages` |

### One-Line Install

```bash
pip3 install requests beautifulsoup4 dnspython python-whois --break-system-packages
```

---

## ⚠️ Disclaimer

This tool is intended for **educational purposes only** and for **ethical security testing**.

- ✅ Use only on websites you **own**
- ✅ Use only with **written permission** from the owner
- ❌ **NEVER** use on websites without authorization

**Unauthorized use is ILLEGAL and UNETHICAL.**

---

## 👨‍💻 Author

**MANSOOR BIK KAMALI**

- Ethical Hacker & Security Researcher
- GitHub: [@YOUR_USERNAME](https://github.com/mansoor511)
- Email: mansoorbik2025@gmail.com

---

## 📜 License

This project is licensed under the **MIT License**.

---

## ⭐ Support

If you find this tool useful, please give it a **star** ⭐ on GitHub!

---

<div align="center">

**Made with ❤️ by MANSOOR BIK KAMALI**

</div>