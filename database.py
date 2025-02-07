import sqlite3
import json
import os

DB_FILE = "jobs.db"
JOBS_FILE1 = "rapid_jobs2.json"
JOBS_FILE2 = "jobs3.json"

def database_exists():
    """Checks if the database file exists."""
    return os.path.exists(DB_FILE)

def create_database():
    """Creates the database and jobs table only if the database doesn't exist."""
    if database_exists():
        print("Database already exists. Skipping creation.")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            site TEXT,
            job_url TEXT,
            job_url_direct TEXT,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            job_type TEXT,
            employmentType TEXT,
            date_posted TEXT,
            salary_source TEXT,
            interval TEXT,
            min_amount REAL,
            max_amount REAL,
            currency TEXT,
            is_remote INTEGER CHECK (is_remote IN (0, 1)), 
            job_level TEXT,
            job_function TEXT,
            company_industry TEXT,
            listing_type TEXT,
            emails TEXT,
            description TEXT,
            company_url TEXT,
            company_url_direct TEXT,
            company_addresses TEXT,
            company_num_employees TEXT,
            company_revenue TEXT,
            company_description TEXT,
            logo_photo_url TEXT,
            banner_photo_url TEXT,
            ceo_name TEXT,
            ceo_photo_url TEXT,
            salaryRange TEXT,
            image TEXT,
            job_link TEXT
        );
        """
    )

    conn.commit()
    conn.close()
    print("Database and table created successfully.")

def data_inserted_for_rapidjobs_file(jobs):
    """Inserts job data into the database, ensuring no duplicates."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for job in jobs:
        job_id = job.get("id", "")
        site = job.get("site", "")
        job_url = job.get("job_url", "")
        job_url_direct = job.get("job_url_direct", "")
        title = job.get("title", "")
        company = job.get("company", "")
        location = job.get("location", "Not specified")
        job_type = job.get("job_type", "Not specified")
        employment_type = job.get("employmentType", "Not specified")
        date_posted = job.get("datePosted") or job.get("date_posted") or "Not available"
        salary_source = job.get("salary_source", "Not disclosed")
        interval = job.get("interval", "Unknown")
        min_amount = job.get("min_amount", None)
        max_amount = job.get("max_amount", None)
        currency = job.get("currency", "USD")
        is_remote = 1 if job.get("is_remote", "False") == "True" else 0
        job_level = job.get("job_level", "Unknown")
        job_function = job.get("job_function", "Not specified")
        company_industry = job.get("company_industry", "Unknown")
        listing_type = job.get("listing_type", "General")
        emails = job.get("emails", "")
        description = job.get("description", "")
        company_url = job.get("company_url", "")
        company_url_direct = job.get("company_url_direct", "")
        company_addresses = job.get("company_addresses", "")
        company_num_employees = job.get("company_num_employees", "Unknown")
        company_revenue = job.get("company_revenue", "Unknown")
        company_description = job.get("company_description", "")
        logo_photo_url = job.get("logo_photo_url", "")
        banner_photo_url = job.get("banner_photo_url", "")
        ceo_name = job.get("ceo_name", "")
        ceo_photo_url = job.get("ceo_photo_url", "")
        salary_range = job.get("salaryRange", "Not disclosed")

        job_links = job.get("jobProviders", [])
        job_link = job_links[0]["url"] if job_links else "No link available"

        if not job_id or not title or not company:
            continue  # Skip invalid entries

        # Insert job while avoiding duplicates
        cursor.execute(
            """
            INSERT OR IGNORE INTO jobs (
                id, site, job_url, job_url_direct, title, company, location, 
                job_type, employmentType, date_posted, salary_source, interval, 
                min_amount, max_amount, currency, is_remote, job_level, job_function, 
                company_industry, listing_type, emails, description, company_url, 
                company_url_direct, company_addresses, company_num_employees, 
                company_revenue, company_description, logo_photo_url, banner_photo_url, 
                ceo_name, ceo_photo_url, salaryRange, job_link
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            """,
            (
                job_id, site, job_url, job_url_direct, title, company, location,
                job_type, employment_type, date_posted, salary_source, interval,
                min_amount, max_amount, currency, is_remote, job_level, job_function,
                company_industry, listing_type, emails, description, company_url,
                company_url_direct, company_addresses, company_num_employees,
                company_revenue, company_description, logo_photo_url, banner_photo_url,
                ceo_name, ceo_photo_url, salary_range, job_link
            )
        )

    conn.commit()
    conn.close()
    print("Jobs data inserted successfully.")


def load_jobs(JOBS_FILE):
    """Loads job data from a JSON file."""
    if not os.path.exists(JOBS_FILE):
        print(f"Error: {JOBS_FILE} not found.")
        return []
    with open(JOBS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)
    
def insert_jobs_into_db():
    """Reads job data and inserts it into the database while avoiding duplicates."""
    jobs1 = load_jobs(JOBS_FILE1)
    jobs2 = load_jobs(JOBS_FILE2)

    if not jobs1 and not jobs2:
        print("No jobs to insert.")
        return

    print("Inserting job data into the database...")
    data_inserted_for_rapidjobs_file(jobs1 + jobs2)  # Merging both lists

    print("Inserted jobs data into:", DB_FILE)


if __name__ == "__main__":
    create_database()  # Only creates if DB does not exist
    insert_jobs_into_db()  # Inserts job data, avoiding duplicates
