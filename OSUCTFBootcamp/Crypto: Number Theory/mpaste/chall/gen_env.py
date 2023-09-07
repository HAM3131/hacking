import secrets

data = {
    "FLASK_APP": "app",
    "SECRET_KEY": secrets.token_hex(32),
    "FLAG": "osuctf{this_is_a_fake_flag}",
}

data = ["{}={}".format(k, v) for k, v in data.items()]
data = "\n".join(data) + "\n"

open(".env", "w").write(data)
