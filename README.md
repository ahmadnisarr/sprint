AI Resume Generator

How to Run the Program
1. Install Dependencies
Run the following command to install required libraries:
pip install -r requirements.txt

2. Set Up API Key
Create a .env file in the project folder and add your Together.AI API key:
TOGETHER_API_KEY=your_api_key_here

3. Run the Program
Execute the script using:
python resume_generator.py

4. Enter Your Details
When prompted, provide your:
Name
Experience
Skills
Education
Job Description (optional for customization)

5. Get Your Resume
The AI will generate a professional resume and save it as resume.md.

Why We Chose meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo via Together.AI
We selected Meta-Llama 3.1-8B-Instruct-Turbo because:
 It follows detailed instructions, ensuring the resume format is structured and professional.
 It produces high-quality and contextually relevant text.
 It is optimized for instruction-following tasks, making it well-suited for resume generation.
 Together.AI provides a cost-effective and accessible way to use advanced AI models.

How We Improved AI Resume Generation
We optimized the AI-generated resume by:

1 Custom Prompt Engineering

We structured the prompt to include role-specific details and tailor the response to the job description.
Example: "Generate a resume for a software engineer with expertise in Python and cloud computing."
2 Formatting for Professionalism

The AI is instructed to output markdown (.md) format, making the resume clean and readable.
We explicitly guide the model to use sections like "Experience", "Education", and "Skills".
3 Refining Output with Temperature Control

We set a temperature value of 0.7, balancing creativity with precision.
This prevents the AI from generating overly generic or verbose content.
4 Iterative Improvements

We tested multiple prompt variations to refine the resume structure.
Example: Adjusting phrasing to ensure it highlights achievements and impact rather than just listing responsibilities.