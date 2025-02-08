import sqlite3
import json
import os
import pytest
from database import create_database, insert_jobs_into_db, load_jobs

# Use a temporary database for testing
TEST_DB_FILE = "test_jobs.db"
TEST_JOBS_FILE = "test_jobs.json"


@pytest.fixture
def setup_test_db(monkeypatch):
    """Sets up a temporary test database."""
    # Use test DB instead of real DB
    monkeypatch.setattr("database.DB_FILE", TEST_DB_FILE)

    # Ensure a clean test environment
    if os.path.exists(TEST_DB_FILE):
        os.remove(TEST_DB_FILE)

    conn = sqlite3.connect(TEST_DB_FILE)
    cursor = conn.cursor()

    # Create table with updated schema
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
        )
        """
    )

    conn.commit()
    conn.close()

    yield  # Run the test

    os.remove(TEST_DB_FILE)  # Cleanup after tests


@pytest.fixture
def create_test_json():
    """Creates a test JSON file with known job data."""
    test_data = [
        {
            "id": "s-GCjOL5C9JmbOP8AAAAAA==",
            "title": "Staff Software Engineer, Risk",
            "company": "WEXWEXUS",
        },
        {
            "id": "li-4027570412",
            "title": "Principal Analog Methodology Specialist",
            "company": "Synopsys Inc",
        }
    ]

    with open(TEST_JOBS_FILE, "w", encoding="utf-8") as file:
        json.dump(test_data, file)

    yield TEST_JOBS_FILE  # Run the test

    os.remove(TEST_JOBS_FILE)  # Cleanup after test


# First Test
def test_load_jobs(create_test_json, monkeypatch):
    """Ensure job data loads correctly from a known JSON file."""
    # Override the global JOBS_FILE variable to use the test file
    monkeypatch.setattr("database.JOBS_FILE1", TEST_JOBS_FILE)

    jobs = load_jobs(TEST_JOBS_FILE)

    # Check that the function returns a list
    assert isinstance(jobs, list)
    assert len(jobs) == 2  # We added 2 test jobs

    # Validate first job
    assert jobs[0]["id"] == "s-GCjOL5C9JmbOP8AAAAAA=="
    assert jobs[0]["title"] == "Staff Software Engineer, Risk"
    assert jobs[0]["company"] == "WEXWEXUS"

    # Validate last job
    assert jobs[1]["id"] == "li-4027570412"
    assert jobs[1]["title"] == "Principal Analog Methodology Specialist"
    assert jobs[1]["company"] == "Synopsys Inc"


# Second Test
def test_database_insertion(setup_test_db, create_test_json, monkeypatch):
    """Test if jobs are inserted correctly into the database."""
    monkeypatch.setattr("database.JOBS_FILE1", TEST_JOBS_FILE)
    monkeypatch.setattr("database.JOBS_FILE2", TEST_JOBS_FILE)

    create_database()
    insert_jobs_into_db()

    conn = sqlite3.connect(TEST_DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    cursor.execute("SELECT title, company FROM jobs LIMIT 1")
    job_entry = cursor.fetchone()

    conn.close()

    assert count == 2  # Ensure exactly 2 jobs are inserted
    assert job_entry is not None
    assert all(job_entry)

# Ensure newline at end of file (Fix W292)
