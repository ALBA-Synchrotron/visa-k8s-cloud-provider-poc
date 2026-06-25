from datetime import datetime


def get_min_date(dates):
    valid_dates = []
    for d in dates:
        if d and isinstance(d, str):
            try:
                dt = datetime.fromisoformat(d.replace("Z", "+00:00"))
                valid_dates.append(dt)
            except ValueError:
                pass
    if not valid_dates:
        return None
    return min(valid_dates).isoformat()