

def bad_request(msg, desc=None):
    status_code = 400
    return {'message': msg, 'description': desc, 'status_code': status_code}


def not_found(msg, desc=None):
    status_code = 404
    return {'message': msg, 'description': desc, 'status_code': status_code}
