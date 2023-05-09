#!/usr/bin/env python3
"""
101-student
"""


def top_students(mongo_collection):
    """
    returns all students sorted by average score
    """
    for student_doc in mongo_collection.find():
        total_score = 0
        for topic in student_doc.get("topics"):
            total_score += topic.get("score")
        averageScore = total_score / len(student_doc.get("topics"))
        mongo_collection.update_one(
            {"name": student_doc.get("name")},
            {"$set": {"averageScore": averageScore}}
        )

    students_with_sorted_avgScore = mongo_collection.find().sort(
                                    "averageScore", -1)
    return list(students_with_sorted_avgScore)
