def classify_risk(severity_score):
    if severity_score < 1:
        return "Stable"
    elif severity_score < 2:
        return "Watchlist"
    elif severity_score < 3:
        return "Emerging Risk"
    else:
        return "Critical"
