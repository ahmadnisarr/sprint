import sqlite3
import json
import os

DB_FILE = "jobs.db"
JOBS_FILE = "rapid_jobs2.json"


def database_exists():
    """Checks if the database file exists."""
    return os.path.exists(DB_FILE)


def create_database():
    """Creates the database and jobs table only if the database doesn't exist."""
    if database_exists():
        print("Database already exists. Skipping creation.")
        return  # Exit if the database is already present

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            description TEXT,
            location TEXT,
            employmentType TEXT,
            datePosted TEXT,
            salaryRange TEXT,
            job_link TEXT NOT NULL
        )
        """
    )

    conn.commit()
    conn.close()
    print("Database and table created successfully.")


def load_jobs():
    """Loads job data from JSON file."""
    if not os.path.exists(JOBS_FILE):
        print("Error: Job data file not found.")
        return []

    with open(JOBS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def insert_jobs_into_db():
    """Reads job data and inserts it into the database while avoiding duplicates."""
    jobs = load_jobs()
    if not jobs:
        print("No jobs to insert.")
        return

    print("Inserting job data into:", DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for job in jobs:
        job_id = job.get("id", "")
        title = job.get("title", "")
        company = job.get("company", "")
        description = job.get("description", "")
        location = job.get("location", "Not specified")
        employment_type = job.get("employmentType", "Not specified")
        date_posted = job.get("datePosted", "Not available")
        salary_range = job.get("salaryRange", "Not disclosed")
        job_links = job.get("jobProviders", [])

        if not job_id or not title or not company:
            continue  # Skip invalid entries

        # Choose the first available job link
        job_link = job_links[0]["url"] if job_links else "No link available"

        # Insert job while avoiding duplicates
        cursor.execute(
            """
            INSERT OR IGNORE INTO jobs 
            (id, title, company, description, location, employmentType, datePosted, 
            salaryRange, job_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                job_id,
                title,
                company,
                description,
                location,
                employment_type,
                date_posted,
                salary_range,
                job_link,
            )
        )

    conn.commit()
    conn.close()
    print("Job data inserted successfully.")


if __name__ == "__main__":
    create_database()  # Will only create if DB does not exist
    insert_jobs_into_db()  # Inserts job data, avoiding duplicates
