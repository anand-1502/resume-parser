from openai import OpenAI
import yaml

# Initialize API key and config path
api_key = None
CONFIG_PATH = r"config.yaml"

# Load API key from config file
with open(CONFIG_PATH) as file:
    config_data = yaml.load(file, Loader=yaml.FullLoader)
    api_key = config_data.get('OPENAI_API_KEY')

def extract_resume_info(resume_text):
    """Extract specific information from the resume using OpenAI API."""
    prompt = '''
    You are a specialized AI designed to extract key details from resumes. Given a resume, your task is to extract the following details:
    1. Full name
    2. Email address
    3. GitHub link
    4. LinkedIn profile
    5. Work experience
    6. Technical expertise
    7. Soft skills
    Return the information in JSON format only.
    '''

    # Create OpenAI client
    openai_client = OpenAI(api_key=api_key)

    # Set up message payload for the OpenAI model
    conversation = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": resume_text}
    ]

    # Get response from OpenAI API
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.0,
        max_tokens=1500
    )
    
    # Extract the response content
    extracted_data = response.choices[0].message.content

    # Return the parsed data
    return extracted_data
