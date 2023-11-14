

#--------- Formatting time ----------

def format_date(raw_date):
    """formats date input to API friendly data."""

    query_date = raw_date.strftime("%Y-%m-%d")

    return query_date

def format_time(raw_time):
    """formats time input into API friendly data."""

    query_time = raw_time.strftime("%H:%M:%S")

    return query_time

def format_date_time(raw_time):
    """formats both date and time for one input"""

    query_date_time = raw_time.strftime("%Y-%m-%d-%H-%M")

    return query_date_time