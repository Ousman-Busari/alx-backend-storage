#!/usr/bin/env python3
"""
10-update_topic
"""


def update_topics(mongo_collection, name, topic):
    """
    changes all topics of a school document based on
    the name
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topic}})
