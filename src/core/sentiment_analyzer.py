#!/usr/bin/env python3
"""
Optimized Sentiment Analyzer for Market Bot AI
Provides efficient, reliable, and scalable FinBERT sentiment analysis

Features:
- Proper tokenization (not just character truncation)
- Batch processing support for 1000+ stocks
- Graceful fallback to keyword-based analysis
- Comprehensive error handling
- Memory-efficient processing
"""

import logging
from typing import List, Dict, Tuple, Optional
from transformers import AutoTokenizer, pipeline

logger = logging.getLogger(__name__)

# Fallback keywords for when FinBERT is unavailable
POSITIVE_KEYWORDS = [
    "wins", "won", "award", "beats", "surges", "jumps", "rallies", "gains",
    "record", "profit", "growth", "dividend", "expansion", "order", "contract",
    "upgrade", "acquisition", "launch", "partnership", "breakthrough", "innovation"
]

NEGATIVE_KEYWORDS = [
    "falls", "drops", "plunges", "crashes", "loss", "decline", "weak", "poor",
    "disappoints", "concern", "debt", "penalty", "resignation", "lawsuit",
    "downgrade", "warning", "cuts", "misses", "slump", "probe", "investigation"
]

# News type classification keywords
NEWS_TYPE_KEYWORDS = {
    "Earnings": ["earnings", "quarter", "q1", "q2", "q3", "q4", "revenue", "profit", "loss", "results"],
    "Product": ["launch", "product", "unveils", "introduces", "release", "model", "variant"],
    "Legal": ["lawsuit", "court", "legal", "case", "trial", "settlement", "penalty", "fine"],
    "M&A": ["merger", "acquisition", "acquires", "deal", "buyout", "takeover", "stake"],
    "Management": ["ceo", "cfo", "resign", "appoint", "director", "board", "executive"],
    "Dividend": ["dividend", "payout", "shareholder", "distribution"],
    "Regulatory": ["sebi", "regulator", "compliance", "violation", "probe", "investigation"],
    "Expansion": ["expansion", "plant", "facility", "capacity", "invest", "capex"],
    "Corporate Action": ["buyback", "split", "bonus", "rights issue"],
    "Technology": ["digital", "technology", "ai", "automation", "innovation", "platform"]
}


class SentimentAnalyzer:
    """
    Optimized sentiment analyzer using FinBERT model
    Handles batching, tokenization, and fallback gracefully
    """
    
    def __init__(self, model_name: str = "ProsusAI/finbert", device: int = -1):
        """
        Initialize sentiment analyzer
        
        Args:
            model_name: HuggingFace model name
            device: -1 for CPU, 0+ for GPU
        """
        self.model_name = model_name
        self.device = device
        self.model = None
        self.tokenizer = None
        self._load_model()
    
    def _load_model(self):
        """Load FinBERT model and tokenizer"""
        try:
            logger.info(f"📥 Loading {self.model_name} model...")

            # Load tokenizer first (fast)
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)

            # Load model pipeline
            self.model = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.tokenizer,
                device=self.device,
                max_length=512,
                truncation=True
            )

            logger.info("✅ FinBERT model loaded successfully!")

        except Exception as e:
            logger.error(f"❌ Failed to load FinBERT model: {str(e)}")
            logger.warning("⚠️  Will use keyword-based fallback for sentiment analysis")
            self.model = None
            self.tokenizer = None
    
    def _preprocess_text(self, text: str) -> str:
        """Clean and prepare text for analysis"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = " ".join(text.split())
        
        # Remove special characters that might cause issues
        text = text.replace("\x00", "")  # Null bytes
        text = text.encode("utf-8", "ignore").decode("utf-8")  # Invalid UTF-8
        
        return text
    
    def _keyword_sentiment(self, text: str) -> float:
        """Fallback keyword-based sentiment analysis"""
        if not text:
            return 0.0
        
        text_lower = text.lower()
        pos_count = sum(1 for kw in POSITIVE_KEYWORDS if kw in text_lower)
        neg_count = sum(1 for kw in NEGATIVE_KEYWORDS if kw in text_lower)
        
        if pos_count + neg_count == 0:
            return 0.0
        
        # Normalize to -1 to +1 range
        sentiment = (pos_count - neg_count) / (pos_count + neg_count)
        return round(sentiment, 2)
    
    def analyze_single(self, text: str) -> Tuple[float, str]:
        """
        Analyze sentiment of a single text
        
        Args:
            text: News text to analyze
        
        Returns:
            (sentiment_score, sentiment_label)
            sentiment_score: -1.0 to +1.0
            sentiment_label: "Positive", "Neutral", "Negative"
        """
        if not text:
            return (0.0, "Neutral")
        
        # Preprocess
        text = self._preprocess_text(text)
        
        if not text:
            return (0.0, "Neutral")
        
        try:
            if self.model and self.tokenizer:
                # Use FinBERT
                result = self.model([text])[0]
                label = result['label'].lower()
                confidence = result['score']
                
                # Convert to numeric sentiment
                if label == 'positive':
                    score = round(confidence, 2)
                    sentiment_label = "Positive"
                elif label == 'negative':
                    score = round(-confidence, 2)
                    sentiment_label = "Negative"
                else:
                    score = 0.0
                    sentiment_label = "Neutral"
                
                return (score, sentiment_label)
            else:
                # Fallback to keywords
                score = self._keyword_sentiment(text)
                if score > 0.2:
                    sentiment_label = "Positive"
                elif score < -0.2:
                    sentiment_label = "Negative"
                else:
                    sentiment_label = "Neutral"
                
                return (score, sentiment_label)
        
        except Exception as e:
            logger.warning(f"Sentiment analysis failed: {str(e)}, using fallback")
            score = self._keyword_sentiment(text)
            if score > 0.2:
                sentiment_label = "Positive"
            elif score < -0.2:
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"
            return (score, sentiment_label)
    
    def analyze_batch(self, texts: List[str], batch_size: int = 32) -> List[Tuple[float, str]]:
        """
        Analyze sentiment of multiple texts efficiently
        
        Args:
            texts: List of news texts
            batch_size: Number of texts to process at once (default: 32)
        
        Returns:
            List of (sentiment_score, sentiment_label) tuples
        """
        if not texts:
            return []
        
        results = []
        
        try:
            if self.model and self.tokenizer:
                # Preprocess all texts
                cleaned_texts = [self._preprocess_text(t) for t in texts]
                
                # Process in batches
                for i in range(0, len(cleaned_texts), batch_size):
                    batch = cleaned_texts[i:i+batch_size]
                    batch_results = self.model(batch)
                    
                    for result in batch_results:
                        label = result['label'].lower()
                        confidence = result['score']
                        
                        if label == 'positive':
                            score = round(confidence, 2)
                            sentiment_label = "Positive"
                        elif label == 'negative':
                            score = round(-confidence, 2)
                            sentiment_label = "Negative"
                        else:
                            score = 0.0
                            sentiment_label = "Neutral"
                        
                        results.append((score, sentiment_label))
            else:
                # Fallback for all texts
                for text in texts:
                    score = self._keyword_sentiment(text)
                    if score > 0.2:
                        sentiment_label = "Positive"
                    elif score < -0.2:
                        sentiment_label = "Negative"
                    else:
                        sentiment_label = "Neutral"
                    results.append((score, sentiment_label))
        
        except Exception as e:
            logger.error(f"Batch sentiment analysis failed: {str(e)}")
            # Fallback to individual analysis
            for text in texts:
                results.append(self.analyze_single(text))

        return results


def classify_news_type(news_text: str) -> List[str]:
    """
    Classify news into categories using keyword matching

    Args:
        news_text: News text to classify

    Returns:
        List of news types (max 3)
    """
    if not news_text:
        return []

    text_lower = news_text.lower()
    types = []

    for news_type, keywords in NEWS_TYPE_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            types.append(news_type)

    # Return unique types, max 3
    return list(set(types))[:3] if types else []
