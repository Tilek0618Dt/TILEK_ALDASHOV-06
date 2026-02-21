import datetime as dt

def utcnow() -> dt.datetime:
    return dt.datetime.utcnow()

def day_key_utc() -> str:
    now = utcnow()
    return now.strftime("%Y-%m-%d")

def in_30_days(from_dt: dt.datetime | None = None) -> dt.datetime:
    base = from_dt or utcnow()
    return base + dt.timedelta(days=30)
