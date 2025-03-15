def summery_message(body, subject,model):
    """
    Summarizes an email and categorizes each distinct part as Complaint, Question, or Appreciation.

    Parameters:
    - body: str, the body of the email
    - subject: str, the subject of the email
    - model: an instance of the language model capable of generating content based on the prompt

    Returns:
    - response: str, the generated summary and categorized intents from the model
    """
    prompt = (
        f"You are given an email with the following details:\n"
        f"**Subject**: {subject}\n"
        f"**Body**: {body}\n\n"
        f"Your task is to:\n"
        f"1. Identify and summarize each distinct request, issue, or statement in the email.\n"
        f"2. Categorize each part into one of the following intent types:\n"
        f"   - Complaint (e.g., reporting a problem or expressing dissatisfaction)\n"
        f"   - Question (e.g., requesting information or clarification)\n"
        f"   - Appreciation (e.g., expressing gratitude or positive feedback)\n\n"
        f"If an email contains multiple intents, separate them clearly.\n\n"
        f"**Response Format:**\n"
        f"- \"[Extracted statement]\" : [Category]\n\n"
        f"**Example Output:**\n"
        f"- \"Give me the list of employees from London\" : Question\n"
        f"- \"I have a complaint that I got a broken product\" : Complaint\n\n"
        f"Ensure that no intent is overlooked, and classify each distinct part of the email correctly."
    )
    
    # Generate content using the model
    response = model.generate_content(prompt)
    # print(f'response :: {response}')
    return response.text

def parse_categorized_response(response):
    """
    Parses the categorized response into a structured list.

    Parameters:
    - response: str, the generated categorized response with multiple intents.

    Returns:
    - List of dictionaries with 'statement' and 'category'.
    """
    parsed_data = []
    
    # Split response into individual lines
    lines = response.split("\n")
    
    for line in lines:
        if line.strip():  # Ignore empty lines
            parts = line.split(" : ")  # Split statement and category
            if len(parts) == 2:
                statement = parts[0].strip().strip('-').strip('"')  # Clean statement
                category = parts[1].strip()  # Clean category
                parsed_data.append({"statement": statement, "category": category})
    
    return parsed_data


def classify_email(summary):
    """
    Extracts and returns the category from a summary dictionary.
    
    Parameters:
    - summary: dict, containing 'statement' and 'category'.
    
    Returns:
    - str: The extracted category if found, otherwise None.
    """
    if not isinstance(summary, dict):
        return None  # Ensure input is a dictionary
    
    category = summary.get("category")  # Extract category directly
    
    if isinstance(category, str):
        return category.lower()
    
    return None  # Return None if category is missing or invalid

