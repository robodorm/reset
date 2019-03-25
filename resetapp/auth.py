"""
According to the roadmap, this
functionality will be moved
to external "Passport" service
"""

USERS = {
    "test": {
        "test": {"id": 1},
    },
    "user": {
        "user": {"id": 2},
    },
    "admin": {
        "admin": {"id": 3},
    },
}


def auth(username, password):
    return USERS.get(username, {}).get(password, {}).get("id")
