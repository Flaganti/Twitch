import time,datetime
def followage(args):
    try:
        utc_dt = datetime.datetime.strptime(args, '%Y-%m-%dT%H:%M:%SZ')
        # Convert UTC datetime to seconds since the Epoch
        timestamp = (datetime.datetime.utcnow() - utc_dt - utc_dt).total_seconds()

        return timestamp
    except:
        return time.time()