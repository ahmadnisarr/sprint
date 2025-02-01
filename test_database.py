import sqlite3
import json
import os
import pytest
from database import create_database, insert_jobs_into_db, load_jobs

# Use a temporary database for testing
TEST_JOBS_FILE = "test_jobs.json"
TEST_DB_FILE = "test_jobs.db"


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
            "id": "0cj12RMPoG9gnpZYAAAAAA==",
            "title": "Senior Software Engineer, Back End (Go, Java, AWS)",
            "company": "Capital One",
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
    monkeypatch.setattr("database.JOBS_FILE", TEST_JOBS_FILE)

    jobs = load_jobs()

    # Check that the function returns a list
    assert isinstance(jobs, list)
    assert len(jobs) == 2  # We added 2 test jobs

    # Validate first job
    assert jobs[0]["id"] == "s-GCjOL5C9JmbOP8AAAAAA=="
    assert jobs[0]["title"] == "Staff Software Engineer, Risk"
    assert jobs[0]["company"] == "WEXWEXUS"

    # Validate last job
    assert jobs[1]["id"] == "0cj12RMPoG9gnpZYAAAAAA=="
    assert jobs[1]["title"] == "Senior Software Engineer, Back End (Go, Java, AWS)"
    assert jobs[1]["company"] == "Capital One"


# Second Test
def test_database_insertion(setup_test_db):
    """Test if jobs are inserted correctly into the database."""
    create_database()
    insert_jobs_into_db()

    conn = sqlite3.connect(TEST_DB_FILE)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    cursor.execute("SELECT title, company, location, employmentType FROM jobs LIMIT 1")
    job_entry = cursor.fetchone()

    conn.close()

    assert count > 0  # Ensure jobs are inserted
    assert job_entry is not None  # Ensure at least one entry exists
    assert all(job_entry)  # Ensure all fields have values
