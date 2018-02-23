import time,datetime
def followage(args):
    try:
        utc_dt = datetime.datetime.strptime(args, '%Y-%m-%dT%H:%M:%SZ')
        # Convert UTC datetime to seconds since the Epoch
        timestamp = (utc_dt - datetime.datetime(1970, 1, 1)).total_seconds()

        _followage = time.time()-timestamp

        return timestamp
    except:
        return time.time()