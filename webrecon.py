#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔═══════════════════════════════════════════════════════════════════════════╗
║                       WEBRECON PRO v3.0                                   ║
║              Ultimate Web Reconnaissance Tool                             ║
║                                                                           ║
║                      Coded by: MANSOOR BIK KAMALI                         ║
║                    For Educational & Ethical Testing                      ║
╚═══════════════════════════════════════════════════════════════════════════╝
"""

import requests
import socket
import re
import sys
import os
import json
import time
import dns.resolver
import argparse
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import ssl
import whois
from datetime import datetime

# ============================================================
# COLOR CODES
# ============================================================
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
MAGENTA = '\033[95m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

# ============================================================
# SUBDOMAIN WORDLIST
# ============================================================
SUBDOMAINS = [
    'www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'stage',
    'blog', 'shop', 'store', 'app', 'mobile', 'm', 'portal', 'dashboard',
    'panel', 'cpanel', 'webmail', 'smtp', 'pop', 'imap', 'ns1', 'ns2',
    'ns3', 'dns', 'cdn', 'static', 'media', 'images', 'img', 'files',
    'download', 'uploads', 'docs', 'support', 'help', 'forum', 'community',
    'news', 'events', 'careers', 'jobs', 'about', 'contact', 'login',
    'signup', 'register', 'account', 'profile', 'user', 'users', 'admin',
    'secure', 'ssl', 'vpn', 'remote', 'backup', 'old', 'new', 'beta',
    'alpha', 'demo', 'sandbox', 'staging', 'production', 'prod', 'qa',
]

# ============================================================
# COMMON DIRECTORIES
# ============================================================
DIRECTORIES = [
    'admin', 'administrator', 'login', 'wp-admin', 'wp-login',
    'dashboard', 'panel', 'cpanel', 'manage', 'management',
    'api', 'api/v1', 'api/v2', 'rest', 'graphql', 'swagger',
    'docs', 'documentation', 'help', 'support', 'faq',
    'backup', 'backups', 'old', 'new', 'temp', 'tmp', 'test',
    'uploads', 'upload', 'files', 'file', 'download', 'downloads',
    'images', 'img', 'media', 'static', 'assets', 'css', 'js',
    'config', 'configuration', 'settings', 'setup', 'install',
    'database', 'db', 'sql', 'mysql', 'phpmyadmin', 'adminer',
    'logs', 'log', 'error_log', 'access_log', 'debug',
    'phpinfo.php', 'info.php', 'test.php', 'phpMyAdmin',
    'robots.txt', 'sitemap.xml', 'crossdomain.xml', '.htaccess',
    '.env', '.git', '.git/config', '.svn', '.DS_Store',
    'server-status', 'server-info', 'status', 'health',
    'webmail', 'mail', 'email', 'newsletter',
    'forum', 'forums', 'board', 'community',
    'shop', 'store', 'cart', 'checkout', 'payment',
    'user', 'users', 'profile', 'account', 'settings',
    'search', 'sitemap', 'rss', 'feed', 'atom',
]

# ============================================================
# COMMON PORTS
# ============================================================
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445,
    993, 995, 1433, 1521, 1723, 2082, 2083, 2086, 2087, 2095,
    2096, 3306, 3389, 5432, 5900, 5984, 6379, 8080, 8443, 8888,
    9000, 9090, 9200, 27017
]

class WebReconPro:
    def __init__(self, target_url, threads=20, timeout=10):
        self.target_url = target_url.rstrip('/')
        self.parsed = urlparse(target_url)
        self.domain = self.parsed.netloc
        self.base_domain = self.domain.replace('www.', '')
        self.threads = threads
        self.timeout = timeout
        self.results = {
            'target': target_url,
            'domain': self.domain,
            'base_domain': self.base_domain,
            'scan_date': datetime.now().isoformat(),
            'ip_addresses': [],
            'subdomains': [],
            'directories': [],
            'urls': [],
            'ports': [],
            'technologies': [],
            'dns_records': {},
            'whois_info': {},
            'ssl_info': {},
            'js_endpoints': [],
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.session.verify = False
        
    def banner(self):
        print(f"""
{BOLD}{CYAN}╔═══════════════════════════════════════════════════════════════════════╗{RESET}
{BOLD}{CYAN}║{RESET}                       {BOLD}{WHITE}WEBRECON PRO v3.0{RESET}{CYAN}                              ║
{BOLD}{CYAN}║{RESET}                 {BOLD}{YELLOW}Ultimate Web Reconnaissance Tool{RESET}{CYAN}                   ║
{BOLD}{CYAN}║{RESET}                                                               ║
{BOLD}{CYAN}║{RESET}                    {BOLD}{MAGENTA}Coded by: MANSOOR BIK KAMALI{RESET}{CYAN}                      ║
{BOLD}{CYAN}║{RESET}                  {BOLD}{RED}For Educational Testing Only{RESET}{CYAN}                    ║
{BOLD}{CYAN}╚═══════════════════════════════════════════════════════════════════════╝{RESET}
        """)
    
    # ============================================================
    # 1. IP RESOLUTION
    # ============================================================
    def resolve_ip(self):
        """پیدا کردن IP دامنه"""
        print(f"\n{YELLOW}[*] STEP 1: IP Resolution{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        
        try:
            ips = socket.gethostbyname_ex(self.domain)[2]
            self.results['ip_addresses'] = ips
            for ip in ips:
                print(f"{GREEN}[+] IP: {WHITE}{ip}{RESET}")
        except:
            print(f"{RED}[-] Could not resolve IP{RESET}")
    
    # ============================================================
    # 2. DNS ENUMERATION
    # ============================================================
    def dns_enum(self):
        """جستجوی رکوردهای DNS"""
        print(f"\n{YELLOW}[*] STEP 2: DNS Enumeration{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        
        record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'SOA', 'CNAME']
        
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(self.base_domain, record_type)
                records = [str(r) for r in answers]
                self.results['dns_records'][record_type] = records
                for r in records:
                    print(f"{GREEN}[+] {record_type}: {WHITE}{r[:80]}{RESET}")
            except:
                pass
    
    # ============================================================
    # 3. SUBDOMAIN ENUMERATION
    # ============================================================
    def subdomain_enum(self):
        """پیدا کردن ساب‌دامین‌ها"""
        print(f"\n{YELLOW}[*] STEP 3: Subdomain Enumeration{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        print(f"{YELLOW}[*] Testing {len(SUBDOMAINS)} subdomains...{RESET}")
        
        def check_subdomain(sub):
            full_domain = f"{sub}.{self.base_domain}"
            try:
                socket.gethostbyname(full_domain)
                return full_domain
            except:
                return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(check_subdomain, sub): sub for sub in SUBDOMAINS}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.results['subdomains'].append(result)
                    print(f"{GREEN}[+] Found: {WHITE}{result}{RESET}")
        
        print(f"{GREEN}[+] Total subdomains: {len(self.results['subdomains'])}{RESET}")
    
    # ============================================================
    # 4. DIRECTORY BRUTE-FORCE
    # ============================================================
    def dir_brute(self):
        """Brute-force دایرکتوری‌ها"""
        print(f"\n{YELLOW}[*] STEP 4: Directory Brute-Force{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        print(f"{YELLOW}[*] Testing {len(DIRECTORIES)} directories...{RESET}")
        
        def check_dir(directory):
            url = f"{self.target_url}/{directory}"
            try:
                response = self.session.get(url, timeout=self.timeout, allow_redirects=False)
                if response.status_code in [200, 301, 302, 403]:
                    return {
                        'url': url,
                        'status': response.status_code,
                        'size': len(response.content)
                    }
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(check_dir, d): d for d in DIRECTORIES}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    self.results['directories'].append(result)
                    color = GREEN if result['status'] == 200 else YELLOW
                    print(f"{color}[+] [{result['status']}] {WHITE}{result['url']}{RESET}")
        
        print(f"{GREEN}[+] Total directories: {len(self.results['directories'])}{RESET}")
    
    # ============================================================
    # 5. CRAWL & EXTRACT URLS
    # ============================================================
    def crawl_urls(self, max_urls=100):
        """خزش و استخراج URLها"""
        print(f"\n{YELLOW}[*] STEP 5: Crawling URLs{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        
        queue = set([self.target_url])
        crawled = set()
        found = set([self.target_url])
        
        while queue and len(found) < max_urls:
            current = list(queue)[:10]
            queue.clear()
            
            for url in current:
                if url in crawled:
                    continue
                crawled.add(url)
                
                try:
                    response = self.session.get(url, timeout=self.timeout)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    for a in soup.find_all('a', href=True):
                        link = urljoin(url, a['href'])
                        if self.base_domain in link and link not in found:
                            found.add(link)
                            queue.add(link)
                            print(f"{GREEN}[+] {WHITE}{link[:80]}{RESET}")
                except:
                    pass
        
        self.results['urls'] = list(found)
        print(f"{GREEN}[+] Total URLs: {len(found)}{RESET}")
    
    # ============================================================
    # 6. JS ANALYZER
    # ============================================================
    def js_analyzer(self):
        """تحلیل JavaScript برای پیدا کردن API Endpoints"""
        print(f"\n{YELLOW}[*] STEP 6: JavaScript Analysis{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        
        try:
            response = self.session.get(self.target_url, timeout=self.timeout)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            js_files = []
            for script in soup.find_all('script', src=True):
                js_url = urljoin(self.target_url, script['src'])
                if self.base_domain in js_url:
                    js_files.append(js_url)
            
            print(f"{YELLOW}[*] Found {len(js_files)} JS files{RESET}")
            
            endpoints = set()
            for js_url in js_files[:5]:  # فقط 5 فایل اول
                try:
                    js_response = self.session.get(js_url, timeout=self.timeout)
                    # پیدا کردن API endpoints
                    patterns = [
                        r'["\'](/api/[^"\']+)["\']',
                        r'["\'](/v[0-9]+/[^"\']+)["\']',
                        r'url:\s*["\']([^"\']+)["\']',
                    ]
                    for pattern in patterns:
                        matches = re.findall(pattern, js_response.text)
                        for match in matches:
                            full_url = urljoin(self.target_url, match)
                            endpoints.add(full_url)
                except:
                    pass
            
            self.results['js_endpoints'] = list(endpoints)
            for ep in endpoints:
                print(f"{GREEN}[+] Endpoint: {WHITE}{ep[:80]}{RESET}")
            
            print(f"{GREEN}[+] Total endpoints: {len(endpoints)}{RESET}")
        except:
            print(f"{RED}[-] JS analysis failed{RESET}")
    
    # ============================================================
    # 7. PORT SCAN
    # ============================================================
    def port_scan(self):
        """اسکن پورت‌های باز"""
        print(f"\n{YELLOW}[*] STEP 7: Port Scan{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        
        if not self.results['ip_addresses']:
            print(f"{RED}[-] No IP to scan{RESET}")
            return
        
        target_ip = self.results['ip_addresses'][0]
        print(f"{YELLOW}[*] Scanning {target_ip}...{RESET}")
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                sock.close()
                if result == 0:
                    return port
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(check_port, p): p for p in COMMON_PORTS}
            
            for future in as_completed(futures):
                port = future.result()
                if port:
                    self.results['ports'].append(port)
                    print(f"{GREEN}[+] Port {WHITE}{port}{RESET} {GREEN}OPEN{RESET}")
        
        print(f"{GREEN}[+] Total open ports: {len(self.results['ports'])}{RESET}")
    
    # ============================================================
    # 8. TECHNOLOGY DETECTION
    # ============================================================
    def tech_detect(self):
        """تشخیص تکنولوژی‌ها"""
        print(f"\n{YELLOW}[*] STEP 8: Technology Detection{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        
        try:
            response = self.session.get(self.target_url, timeout=self.timeout)
            headers = response.headers
            html = response.text
            
            techs = []
            
            # از هدرها
            if 'Server' in headers:
                techs.append(f"Server: {headers['Server']}")
            if 'X-Powered-By' in headers:
                techs.append(f"Powered: {headers['X-Powered-By']}")
            
            # از HTML
            patterns = {
                'WordPress': r'wp-content|wp-includes',
                'React': r'react|_react',
                'Vue.js': r'vue\.js|vuejs',
                'Angular': r'angular',
                'jQuery': r'jquery',
                'Bootstrap': r'bootstrap',
                'Tailwind': r'tailwind',
                'Laravel': r'laravel',
                'Django': r'django',
                'PHP': r'\.php',
                'ASP.NET': r'asp\.net',
                'Nginx': r'nginx',
                'Apache': r'apache',
                'Cloudflare': r'cloudflare',
            }
            
            for tech, pattern in patterns.items():
                if re.search(pattern, html, re.IGNORECASE) or re.search(pattern, str(headers), re.IGNORECASE):
                    techs.append(tech)
            
            self.results['technologies'] = list(set(techs))
            
            for tech in self.results['technologies']:
                print(f"{GREEN}[+] {WHITE}{tech}{RESET}")
        except:
            print(f"{RED}[-] Technology detection failed{RESET}")
    
    # ============================================================
    # 9. WHOIS LOOKUP
    # ============================================================
    def whois_lookup(self):
        """اطلاعات WHOIS"""
        print(f"\n{YELLOW}[*] STEP 9: WHOIS Lookup{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        
        try:
            w = whois.whois(self.base_domain)
            info = {
                'registrar': str(w.registrar),
                'creation_date': str(w.creation_date),
                'expiration_date': str(w.expiration_date),
                'name_servers': str(w.name_servers),
            }
            self.results['whois_info'] = info
            
            for key, value in info.items():
                if value and value != 'None':
                    print(f"{GREEN}[+] {key}: {WHITE}{value[:60]}{RESET}")
        except:
            print(f"{RED}[-] WHOIS failed{RESET}")
    
    # ============================================================
    # 10. SSL CHECK
    # ============================================================
    def ssl_check(self):
        """بررسی SSL"""
        print(f"\n{YELLOW}[*] STEP 10: SSL Certificate{RESET}")
        print(f"{CYAN}{'─'*60}{RESET}")
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    info = {
                        'issuer': dict(x[0] for x in cert['issuer']),
                        'subject': dict(x[0] for x in cert['subject']),
                        'expiry': cert['notAfter'],
                    }
                    self.results['ssl_info'] = info
                    print(f"{GREEN}[+] Issuer: {WHITE}{info['issuer'].get('organizationName', 'N/A')}{RESET}")
                    print(f"{GREEN}[+] Expiry: {WHITE}{info['expiry']}{RESET}")
        except:
            print(f"{RED}[-] SSL check failed{RESET}")
    
    # ============================================================
    # SAVE RESULTS
    # ============================================================
    def save_results(self):
        """ذخیره نتایج"""
        output_dir = "webrecon_output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{output_dir}/recon_{self.base_domain}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n{GREEN}[+] Results saved: {WHITE}{filename}{RESET}")
        
        # ذخیره به صورت TXT
        txt_file = filename.replace('.json', '.txt')
        with open(txt_file, 'w') as f:
            f.write(f"WEBRECON PRO - RECONNAISSANCE REPORT\n")
            f.write(f"{'='*60}\n")
            f.write(f"Target: {self.results['target']}\n")
            f.write(f"Date: {self.results['scan_date']}\n\n")
            
            f.write(f"IP ADDRESSES:\n")
            for ip in self.results['ip_addresses']:
                f.write(f"  - {ip}\n")
            
            f.write(f"\nSUBDOMAINS ({len(self.results['subdomains'])}):\n")
            for sub in self.results['subdomains']:
                f.write(f"  - {sub}\n")
            
            f.write(f"\nDIRECTORIES ({len(self.results['directories'])}):\n")
            for d in self.results['directories']:
                f.write(f"  - [{d['status']}] {d['url']}\n")
            
            f.write(f"\nURLS ({len(self.results['urls'])}):\n")
            for url in self.results['urls']:
                f.write(f"  - {url}\n")
            
            f.write(f"\nOPEN PORTS:\n")
            for port in self.results['ports']:
                f.write(f"  - {port}\n")
            
            f.write(f"\nTECHNOLOGIES:\n")
            for tech in self.results['technologies']:
                f.write(f"  - {tech}\n")
        
        print(f"{GREEN}[+] Text report: {WHITE}{txt_file}{RESET}")
    
    # ============================================================
    # SUMMARY
    # ============================================================
    def show_summary(self):
        """نمایش خلاصه"""
        print(f"\n{BOLD}{CYAN}{'='*60}{RESET}")
        print(f"{BOLD}{GREEN}📊 FINAL SUMMARY{RESET}")
        print(f"{BOLD}{CYAN}{'='*60}{RESET}")
        
        print(f"{WHITE}Target: {YELLOW}{self.target_url}{RESET}")
        print(f"{WHITE}IPs: {YELLOW}{len(self.results['ip_addresses'])}{RESET}")
        print(f"{WHITE}Subdomains: {YELLOW}{len(self.results['subdomains'])}{RESET}")
        print(f"{WHITE}Directories: {YELLOW}{len(self.results['directories'])}{RESET}")
        print(f"{WHITE}URLs: {YELLOW}{len(self.results['urls'])}{RESET}")
        print(f"{WHITE}Open Ports: {YELLOW}{len(self.results['ports'])}{RESET}")
        print(f"{WHITE}Technologies: {YELLOW}{len(self.results['technologies'])}{RESET}")
        print(f"{WHITE}JS Endpoints: {YELLOW}{len(self.results['js_endpoints'])}{RESET}")
        
        print(f"{BOLD}{CYAN}{'='*60}{RESET}")
    
    # ============================================================
    # RUN ALL
    # ============================================================
    def run(self):
        """اجرای کامل"""
        self.banner()
        print(f"{YELLOW}[!] Target: {WHITE}{self.target_url}{RESET}")
        print(f"{YELLOW}[!] Started: {WHITE}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{RESET}")
        
        start_time = time.time()
        
        # اجرای همه مراحل
        self.resolve_ip()
        self.dns_enum()
        self.subdomain_enum()
        self.dir_brute()
        self.crawl_urls()
        self.js_analyzer()
        self.port_scan()
        self.tech_detect()
        self.whois_lookup()
        self.ssl_check()
        
        elapsed = time.time() - start_time
        
        self.save_results()
        self.show_summary()
        
        print(f"\n{GREEN}[+] Scan completed in {elapsed:.2f} seconds{RESET}")
        print(f"{GREEN}[+] Coded by: MANSOOR BIK KAMALI{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description='WebRecon Pro - Ultimate Web Reconnaissance Tool',
        epilog='Coded by: MANSOOR BIK KAMALI'
    )
    parser.add_argument('url', help='Target URL')
    parser.add_argument('-t', '--threads', type=int, default=20, help='Threads (default: 20)')
    
    args = parser.parse_args()
    
    if not args.url.startswith(('http://', 'https://')):
        args.url = f"https://{args.url}"
    
    tool = WebReconPro(args.url, args.threads)
    tool.run()


if __name__ == "__main__":
    main()