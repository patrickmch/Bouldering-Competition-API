def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        try:
            app_key = ObjectId(kwargs.get("id"))
            find_key = db.participants.find_one({"_id" : ObjectId(app_key)})
            if find_key["_id"] == app_key:
                return view_function(*args, **kwargs)
            else:
                abort(401)
        except:
            return "invalid or no api key supplied"

    return decorated_function
