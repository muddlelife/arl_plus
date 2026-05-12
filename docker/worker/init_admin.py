#!/usr/bin/env python3
"""Initialize the ARL admin user with credentials from environment variables.

Reads ARL_ADMIN_USERNAME and ARL_ADMIN_PASSWORD from the environment.
Falls back to admin / arlpass if not set.
"""
import os
import hashlib
import sys
import time
from pymongo import MongoClient

username = os.environ.get("ARL_ADMIN_USERNAME", "admin")
password = os.environ.get("ARL_ADMIN_PASSWORD", "arlpass")
# Use the same auth behavior as docker/config-docker.yaml:
# root user lives in the `admin` database, app database is usually `arl`.
mongo_uri = os.environ.get(
    "MONGO_URI",
    "mongodb://admin:admin@mongodb:27017/arl?authSource=admin",
)
salt = "arlsalt!@#"

max_retries = 30
for i in range(max_retries):
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        break
    except Exception:
        if i == max_retries - 1:
            print("ERROR: unable to connect to MongoDB", file=sys.stderr)
            sys.exit(1)
        time.sleep(1)

db = client.get_default_database()
hashed = hashlib.md5((salt + password).encode()).hexdigest()

result = db.user.delete_one({"username": username})
db.user.insert_one({"username": username, "password": hashed})
print(f"Admin user '{username}' initialized successfully")
