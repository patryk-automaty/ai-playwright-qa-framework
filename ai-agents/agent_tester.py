import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from models import TestSuite

# Load OpenAI API key from .env file
load_dotenv()


def generate_test_cases(file_name: str,model_name: str ):
    """
    Generates structured test cases from a Markdown requirements file using an AI agent (GPT-4o).

    The agent acts as an expert QA Automation Engineer, analyzing business requirements
    and producing a producing a JSON test suite covering both positive (happy path) and negative
    (edge case) scenarios.

    Args:
        file_name (str): The name of the Markdown file (e.g., 'login.md')
                         located in the '../wiki/' directory.

    Returns:
        None: The generated test cases are saved as a JSON file in '../test_cases/'.
    """
    # Build the absolute path to the wiki directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(script_dir, '..', 'wiki', file_name))

    # Load the requirements from the Markdown file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            requirements = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None

    # Initialize the LLM (GPT-4o) with low temperature for consistent, deterministic output
    llm = ChatOpenAI(model=model_name, temperature=0.1)

    # Bind the LLM to the Pydantic TestSuite model for structured JSON output
    structured_llm = llm.with_structured_output(TestSuite)

    # Define the system and user prompts for the AI test case generator
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert QA Automation Engineer with years of experience. "
                   "Your task is to analyze business requirements and create precise, structured test cases."),
        ("user", "Analyze the following requirements and write test cases, covering both positive "
                 "(happy path) and negative (edge cases) scenarios.\n\n"
                 "Requirements from the file:\n{file_requirements}. ")
    ])

    # Create the chain: prompt -> LLM -> structured output
    chain = prompt | structured_llm

    print(f"Agent is reading the file: {file_path}...\n")

    # Invoke the AI agent with the raw requirements content
    response = chain.invoke({"file_requirements": requirements})

    # Convert the Pydantic model response to a formatted JSON string
    json_output = response.model_dump_json(indent=4)

    # Save the generated test cases to a JSON file (e.g., login.json)
    output_test_cases_filename = file_name.replace('.md', '.json')
    output_path = os.path.abspath(os.path.join(script_dir, '..', 'test_cases', output_test_cases_filename))

    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(json_output)
    print("===========================================\n")
    print("=== TEST CASES HAVE BEEN GENERATED ===")
    print("\n===========================================")


if __name__ == "__main__":
    # Default requirements file to process when running the script directly
    selected_file = "login.md"
    generate_test_cases(selected_file)