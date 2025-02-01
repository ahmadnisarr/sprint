import os
from dotenv import load_dotenv
import openai

load_dotenv()

client = openai.OpenAI(
    api_key=os.environ.get("TOGETHER_API_KEY"),
    base_url="https://api.together.xyz/v1",
)

def generate_resume(user_profile):
    """Generate a tailored resume using the AI API."""
    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[
            {"role": "system", "content": "You are a professional resume generator."},
            {
                "role": "user",
                "content": (
                    f"Create a detailed, professional resume in Markdown format based on the following user profile:\n\n"
                    f"{user_profile}\n\n"
                    "Extract the person's name and place it as a main heading.\n"
                    "The resume should include the following sections:\n"
                    "- **Name** (as a primary heading)\n"
                    "- **Summary**\n"
                    "- **Skills**\n"
                    "- **Experience**\n"
                    "- **Education**\n\n"
                    "Ensure the resume is professional, well-formatted, and ready for immediate use."
                ),
            },
        ],
    )
    return response.choices[0].message.content

def save_resume(file_path, resume_content):
    """Save the generated resume to a Markdown file."""
    with open(file_path, "w") as file:
        file.write(resume_content)
    print(f"Resume saved to {file_path}")

def main():
    # Take user profile input
    print("Enter your profile details (e.g., name, role, experience, skills, education):")
    user_profile = input("User Profile: ")

    # Generate the resume
    print("\nGenerating your resume...")
    resume_content = generate_resume(user_profile)

    # Save the resume
    save_resume("resume.md", resume_content)

if __name__ == "__main__":
    main()
