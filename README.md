AI Resume Generator - Sprint 2 Update
📌 How to Run the Program
1️⃣ Install Dependencies
Run the following command to install required libraries:
pip install -r requirements.txt
2️⃣ Set Up API Key
Create a .env file in the project folder and add your Together.AI API key:
TOGETHER_API_KEY=your_api_key_here
3️⃣ Run the Program
Execute the script using:
python resume_generator.py
4️⃣ Enter Your Details
When prompted, provide your:
✅ Name
✅ Experience
✅ Skills
✅ Education
✅ Job Description (optional for customization)

5️⃣ Get Your Resume
The AI will generate a professional resume and save it as resume.md.

🛠 Sprint 2 Enhancements
Sprint 2 focused on database integration, automated testing, and CI/CD improvements to make the AI Resume Generator more robust.

✅ New Features in Sprint 2
1️⃣ Database Integration
Stores generated resumes in an SQLite database (resumes.db).
Tracks generated resumes to prevent duplicates.
Uses SQLAlchemy for efficient database operations.
2️⃣ Automated Testing
Ensures AI output is stored correctly in the database.
Tests API calls to verify AI-generated responses.
Uses pytest for test automation.
3️⃣ Continuous Integration (CI/CD)
GitHub Actions automates:
✅ Code linting (flake8)
✅ Automated testing (pytest)
✅ Build and execution verification
Prevents errors from breaking the project.