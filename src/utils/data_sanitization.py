"""
Data Sanitization Utilities
Centralized functions for cleaning and validating data before upload/export
"""

import math
from typing import Any, Optional


def sanitize_number(value: Any, default: Optional[float] = 0.0) -> Optional[float]:
    """
    Replace NaN/None with default value for safe JSON serialization and Excel export.
    
    Args:
        value: The value to sanitize (can be float, int, None, NaN)
        default: The default value to return if value is NaN/None (default: 0.0)
    
    Returns:
        Sanitized numeric value or default
    
    Examples:
        >>> sanitize_number(np.float64(nan), 0.0)
        0.0
        
        >>> sanitize_number(None, 0.0)
        0.0
        
        >>> sanitize_number(5.5, 0.0)
        5.5
        
        >>> sanitize_number(0, 0.0)  # Zero is valid!
        0
    
    Note:
        This is critical for:
        - Notion API (JSON doesn't support NaN)
        - Excel export (avoids #NUM! errors)
        - Data consistency across all bots
    """
    if value is None:
        return default
    
    if isinstance(value, float) and math.isnan(value):
        return default
    
    return value


def sanitize_stock_data(data: dict) -> dict:
    """
    Sanitize all numeric fields in stock data dictionary.
    
    Args:
        data: Dictionary containing stock data with numeric fields
    
    Returns:
        Dictionary with sanitized numeric values
    
    Fields sanitized:
        - sent/sentiment: Default 0.0 (Neutral)
        - mom/momentum: Default 0.0 (No change)
        - vol/volume_surge: Default 1.0 (Normal volume)
        - price: Default None (will skip field if missing)
        - market_cap: Default None (will skip field if missing)
        - score: Default 0.0 (Neutral score)
        - Holdings data (FII, DII, Promoter, MF): Default None
    """
    # Sentiment (handle both 'sent' and 'sentiment' keys)
    if 'sent' in data:
        data['sent'] = sanitize_number(data.get('sent'), 0.0)
    if 'sentiment' in data:
        data['sentiment'] = sanitize_number(data.get('sentiment'), 0.0)
    
    # Momentum (handle both 'mom' and 'momentum' keys)
    if 'mom' in data:
        data['mom'] = sanitize_number(data.get('mom'), 0.0)
    if 'momentum' in data:
        data['momentum'] = sanitize_number(data.get('momentum'), 0.0)
    
    # Volume (handle both 'vol' and 'volume_surge' keys)
    if 'vol' in data:
        data['vol'] = sanitize_number(data.get('vol'), 1.0)
    if 'volume_surge' in data:
        data['volume_surge'] = sanitize_number(data.get('volume_surge'), 1.0)
    
    # Price and Market Cap (None if missing - will skip field in Notion)
    data['price'] = sanitize_number(data.get('price'), None)
    data['market_cap'] = sanitize_number(data.get('market_cap'), None)
    
    # Score
    if 'score' in data:
        data['score'] = sanitize_number(data.get('score'), 0.0)
    
    # Holdings data (for Excel bot and advanced features)
    for field in ['fii_pct', 'dii_pct', 'promoter_pct', 'mf_pct', 'institutional_score']:
        if field in data:
            data[field] = sanitize_number(data.get(field), None)
    
    return data


def validate_numeric_range(value: float, min_val: float = None, max_val: float = None, 
                           default: float = 0.0) -> float:
    """
    Validate that a numeric value is within acceptable range.
    
    Args:
        value: The value to validate
        min_val: Minimum acceptable value (optional)
        max_val: Maximum acceptable value (optional)
        default: Default value if out of range
    
    Returns:
        Validated value or default if out of range
    
    Examples:
        >>> validate_numeric_range(150, min_val=0, max_val=100, default=50)
        50  # Out of range, returns default
        
        >>> validate_numeric_range(75, min_val=0, max_val=100)
        75  # Within range
    """
    # First sanitize NaN
    value = sanitize_number(value, default)
    
    if value is None:
        return default
    
    # Check range
    if min_val is not None and value < min_val:
        return default
    
    if max_val is not None and value > max_val:
        return default
    
    return value


# Export all functions
__all__ = [
    'sanitize_number',
    'sanitize_stock_data',
    'validate_numeric_range'
]
