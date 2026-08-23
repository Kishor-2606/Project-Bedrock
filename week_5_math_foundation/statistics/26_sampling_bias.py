students = [
    {"attendance": 95, "marks": 90},
    {"attendance": 92, "marks": 85},
    {"attendance": 88, "marks": 82},
    {"attendance": 60, "marks": 55},
    {"attendance": 55, "marks": 50},
]

biased_sample = [
    student
    for student in students
    if student["attendance"] > 85
]

print("Biased sample:")
print(biased_sample)