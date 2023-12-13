def validate(user):
    errors = {}
    if not user['nickname']:
        errors['nickname'] = "Can't be blank"
    if len(user['nickname']) <= 4:
        errors['nickname'] = "Nickname must be grater than 4 characters"
    if not user['email']:
        errors['email'] = "Can't be blank"
    return errors

