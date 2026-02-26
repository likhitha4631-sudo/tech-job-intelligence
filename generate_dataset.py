import pandas as pd
import random


titles = [
    "Data Analyst", "Data Scientist", "ML Engineer",
    "Backend Developer", "Frontend Developer",
    "Full Stack Developer", "DevOps Engineer",
    "Cloud Engineer", "AI Engineer"
]

locations = [
    "Bangalore", "Hyderabad", "Chennai",
    "Mumbai", "Pune", "Delhi"
]

experience_levels = [
    "0-2 Years", "2-5 Years", "5-8 Years", "8+ Years"
]

skills_pool = [
    "Python", "SQL", "AWS", "Docker", "Machine Learning",
    "React", "Java", "C++", "Excel", "Power BI",
    "Tableau", "Kubernetes", "TensorFlow", "Spark"
]

data = []

for _ in range(500):
    title = random.choice(titles)
    location = random.choice(locations)
    experience = random.choice(experience_levels)

    if experience == "0-2 Years":
        salary = random.randint(4, 8) * 100000
    elif experience == "2-5 Years":
        salary = random.randint(8, 15) * 100000
    elif experience == "5-8 Years":
        salary = random.randint(15, 25) * 100000
    else:
        salary = random.randint(25, 40) * 100000

    skills = random.sample(skills_pool, 4)

    data.append([
        title,
        location,
        experience,
        salary,
        f"Looking for {title}",
        ", ".join(skills)
    ])

df = pd.DataFrame(data, columns=[
    "title",
    "location",
    "experience",
    "salary",
    "description",
    "skills"
])

df.to_csv("jobs_dataset.csv", index=False)

print("Dataset generated successfully!")