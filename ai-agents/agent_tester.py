import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from typing import List
from pydantic import BaseModel, Field

# Load openAi api key
load_dotenv()

# Define data structure
class TestCase(BaseModel):
    test_id: str = Field(description="Unique identifier for the test, e.g., TC-001")
    title: str = Field(description="Short, descriptive title of the test")
    description: str = Field(description="Detailed description of what is being tested")
    steps: List[str] = Field(description="List of steps to execute the test")
    expected_results: str = Field(description="The expected outcome of the test")

class TestSuite(BaseModel):
    test_cases: List[TestCase] = Field(description="List of generated test cases")

def generate_test_cases(file_name):
    # create file path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(script_dir, '..', 'wiki', file_name))

    # load the file
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            requirements = file.read()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    
    # initialize LLM
    llm = ChatOpenAI(model='gpt-4o', temperature=0.2)

    # add to LLM out sctructured data model
    structured_llm = llm.with_structured_output(TestSuite)

    # create prompt (instructions) for AI
    prompt = ChatPromptTemplate.from_messages([
        ("system","You are an expert QA Automation Engineer with years of experience. Your task is to analyze business requirements and create precise, structured test cases."),
        ("user", "Analyze the following requirements and write test cases, covering both positive (happy path) and negative (edge cases) scenarios.\n\nRequirements from the file:\n{file_requirements}. This is test prompt so please write only one test case")
    ])

    # create chain (connect instructions with AI model)
    chain = prompt | structured_llm

    print(f"Agent is reading the file:{file_path}...\n")

    # invoke the AI
    response = chain.invoke({"file_requirements": requirements})

    # convert response to json format
    json_output = response.model_dump_json(indent=4)

    # define the output path and file name 
    output_test_cases_filename = file_name.replace('.md', '.json')
    output_path = os.path.abspath(os.path.join(script_dir, '..', 'test_cases', output_test_cases_filename))

    # save output file
    with open(output_path, 'w', encoding='utf-8') as output_file:
        output_file.write(json_output)

    print("=== GENERATED TEST CASES ===")
    print(json_output)
    print("\n===========================================")


if __name__ == "__main__":
    selected_file = "login.md"
    generate_test_cases(selected_file)