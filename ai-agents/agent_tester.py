import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load openAi api key
load_dotenv()

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

    # create prompt (instructions) for AI
    prompt = ChatPromptTemplate.from_messages([
        ("system","You are an expert QA Automation Engineer with years of experience. Your task is to analyze business requirements and create precise, structured test cases."),
        ("user", "Analyze the following requirements and write test cases, covering both positive (happy path) and negative (edge cases) scenarios.\n\nRequirements from the file:\n{file_requirements}. This is test prompt so please write only one test case")
    ])

    # create chain (connect instructions with AI model)
    chain = prompt | llm

    print(f"Agent is reading the file:{file_path}...\n")

    # invoke the AI
    response = chain.invoke({"file_requirements": requirements})

    print("=== GENERATED TEST CASES ===")
    print(response.content)
    print("\n===========================================")


if __name__ == "__main__":
    selected_file = "login.md"
    generate_test_cases(selected_file)