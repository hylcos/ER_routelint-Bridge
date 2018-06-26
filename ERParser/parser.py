def parse(web_data: dict):
    for a in web_data:
        a = dict(a)
        lat = None
        long = None
        if 'LAT' in a and 'LON' in a:
            mel = a['capcodes'][0]['CTT']
            if 'Ambulance' in mel:
                return a['LAT'], a['LON']
        return None, None
