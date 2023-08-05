version = "1.0.8"
auth_server = "http://192.168.12.81:8888/"
secure_access = True

if not secure_access:
    auth_server += "no_auth/"
