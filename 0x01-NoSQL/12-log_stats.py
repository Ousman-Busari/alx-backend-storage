#!/usr/bin/env python3
"""
12_log_stats
"""
from pymongo import MongoClient


client = MongoClient()
db = client.logs
print("{} logs".format(db.nginx.count_documents({})))
print("Methods:")
print("\t", "method GET: {}".format(db.nginx.count_documents({
    "method": "GET"
})))
print("\t", "method POST: {}".format(db.nginx.count_documents({
    "method": "POST"
})))
print("\t", "method PUT: {}".format(db.nginx.count_documents({
    "method": "PUT"
})))
print("\t", "method PATCH: {}".format(db.nginx.count_documents({
    "method": "PATCH"
})))
print("\t", "method DELETE: {}".format(db.nginx.count_documents({
    "method": "DELETE"
})))
print("{} status check".format(db.nginx.count_documents({
    "method": "GET",
    "path": "/status"
})))
