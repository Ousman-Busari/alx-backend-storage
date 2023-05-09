#!/usr/bin/env python3
"""
12_log_stats
"""
from pymongo import MongoClient


if __name__ == "__main__":
    client = MongoClient()
    db = client.logs
    print("{} logs".format(db.nginx.count_documents({})))
    print("Methods:")
    print("{}method GET: {}".format("\t", db.nginx.count_documents({
        "method": "GET"
    })))
    print("{}method POST: {}".format("\t", db.nginx.count_documents({
        "method": "POST"
    })))
    print("{}method PUT: {}".format("\t", db.nginx.count_documents({
        "method": "PUT"
    })))
    print("{}method PATCH: {}".format("\t", db.nginx.count_documents({
        "method": "PATCH"
    })))
    print("{}method DELETE: {}".format("\t", db.nginx.count_documents({
        "method": "DELETE"
    })))
    print("{} status check".format(db.nginx.count_documents({
        "method": "GET",
        "path": "/status"
    })))

    print("IPs:")
    ips = db.nginx.aggregate([
        {"$group":
            {
                "_id": "$ip",
                "count": {"$sum": 1}
            }
         },
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project": {
            "_id": 0,
            "ip": "$_id",
            "count": 1
        }}
    ])

    for ip in ips:
        print("{}{}: {}".format("\t", ip.get("ip"), ip.get("count")))
