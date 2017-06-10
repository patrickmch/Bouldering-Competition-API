#generic error messages
err_messages = {
    400 : 'Some or all of your request was not valid and cannot be processed',
    401 : 'You are not authorized to access the requested resource, either because your credentials are not valid or you did not provide them',
    403 : 'You do not have permission to access the requested resource',
    404 : 'The requested resource could not be found',
    500 : 'The server encountered an error'
}

# this dict determines user roles
user_authorization = {
    'users': {
        'participant': False,
        'judge' : True,
        'admin': True
    },
    'competitions': {
        'participant' : False,
        'judge' : True,
        'admin': True
    },
    'venue' : {
        'participant' : False,
        'judge' : False,
        'admin' : True
    }
}
