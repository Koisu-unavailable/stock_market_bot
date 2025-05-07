from dataclasses import dataclass
import datetime
@dataclass
class auto_complete_cache_entry:
    user_id: int
    stocks: list[str] # list of stock symbols
    last_accessed: datetime.datetime


auto_complete_cache : list[auto_complete_cache_entry] = [] 

