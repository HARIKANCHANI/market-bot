import requests
import re

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

symbol = "HDFCBANK"
url = f"https://www.screener.in/company/{symbol}/consolidated/"
headers = {"User-Agent": USER_AGENT, "Referer": "https://www.screener.in/"}

print(f"Fetching: {url}")
resp = requests.get(url, headers=headers, timeout=10)
print("Status:", resp.status_code)
html = resp.text

print("Has 'Shareholding Pattern'?:", "Shareholding Pattern" in html)

start_idx = html.find("Shareholding Pattern")
print("Start index:", start_idx)

snippet = html[start_idx:start_idx+3000]
print("\n=== SNIPPET (Shareholding Pattern block) ===\n")
print(snippet)

print("\n=== FIIs row match ===")
m_fii = re.search(r"FIIs.*?</tr>", snippet, re.S)
print(m_fii.group(0) if m_fii else "NO MATCH FOR FIIs")

print("\n=== DIIs row match ===")
m_dii = re.search(r"DIIs.*?</tr>", snippet, re.S)
print(m_dii.group(0) if m_dii else "NO MATCH FOR DIIs")
