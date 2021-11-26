from typing import Optional, Dict, Any, List
from datetime import datetime

def ftx_date_to_timestamp(str_date: str) -> int:
    return int(datetime.strptime(str_date, '%Y-%m-%dT%H:%M:%S.%f+00:00').timestamp())

    