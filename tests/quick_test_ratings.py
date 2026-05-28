"""Quick test"""
import yfinance as yf

print("Testing RELIANCE.NS", flush=True)
stock = yf.Ticker("RELIANCE.NS")

try:
    info = stock.info
    print(f"recommendationMean: {info.get('recommendationMean')}", flush=True)
    print(f"numberOfAnalystOpinions: {info.get('numberOfAnalystOpinions')}", flush=True)
    print(f"recommendationKey: {info.get('recommendationKey')}", flush=True)
except Exception as e:
    print(f"Error: {e}", flush=True)

print("Done", flush=True)
