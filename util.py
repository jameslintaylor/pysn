from functools import wraps
from flask import render_template, request

def request_needs(*params, in_):
    """extracts the parameters from either request.args or request.form
    (in_ can either be 'args' or 'form'). if the parameters are not there,
    returns a 400 status code displaying the first missing parameter"""
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            d = getattr(request, in_)
            try:
                kwargs.update({param: d[param] for param in params})
            except KeyError as e:
                message = "missing parameter '{}'".format(e.args[0])
                return render_template('error.html', message=message), 400
            return f(*args, **kwargs)
        return decorated
    return decorator
