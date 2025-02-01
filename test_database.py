import sqlite3
import json
import os
import pytest
from database import create_database, insert_jobs_into_db, load_jobs, DB_FILE

# Use a temporary database for testing
TEST_DB_FILE = "test_jobs.db"

@pytest.fixture
def setup_test_db():
    """Sets up a temporary test database."""
    conn = sqlite3.connect(TEST_DB_FILE)
    cursor = conn.cursor()

    # Create table with updated schema
    cursor.execute("""
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
    """)

    conn.commit()
    conn.close()

    yield  # Run tests

    os.remove(TEST_DB_FILE)  # Cleanup after tests

def test_load_jobs():
    """Ensure the job data loads correctly from JSON."""
    jobs = load_jobs()
    assert isinstance(jobs, list)
    assert len(jobs) > 0  # There should be job entries

def test_database_insertion(setup_test_db):
    """Test if jobs are inserted correctly into the database."""
    os.rename(DB_FILE, TEST_DB_FILE)  # Use test DB instead of main DB
    insert_jobs_into_db()

    conn = sqlite3.connect(TEST_DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM jobs")
    count = cursor.fetchone()[0]

    cursor.execute("SELECT title, company, location, employmentType, datePosted, salaryRange FROM jobs LIMIT 1")
    job_entry = cursor.fetchone()

    conn.close()
    
    assert count > 0  # Ensure jobs are inserted
    assert job_entry is not None  # Ensure at least one entry exists
    assert all(job_entry)  # Ensure all fields have values

    os.rename(TEST_DB_FILE, DB_FILE)  # Restore original DB
