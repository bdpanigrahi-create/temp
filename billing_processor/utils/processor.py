"""
Utils for billing processing.
Contains a memory leak by design.
"""

cache = {}

def process_transaction(tx_id, data):
    """
    Processes a transaction and caches it.
    This cache grows unboundedly.
    """
    # Simulate processing
    cache[tx_id] = data
    return True

def get_cache_size():
    return len(cache)
