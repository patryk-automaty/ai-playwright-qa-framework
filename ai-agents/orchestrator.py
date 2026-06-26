import questionary
import os 
import sys
import agent_tester
import agent_qa_reviewer

def main():
    print("Welcome to the AI-Playwright QA Framework CLI \n")
    
    agent_choice = questionary.select(
        "Select the AI Agent you want to run:",
        choices=[
            questionary.Choice("1. Agent Tester (Generate tests from requirements)", value="tester"),
            questionary.Choice("2. Agent Senior QA (Review test cases)", value= "reviewer"),
            questionary.Choice("3. Agent Report Manager (Analyze Playwright results)", value="reporter"),
            questionary.Choice("Exit", value="exit")
        ],
            style=questionary.Style([('highlighted', 'fg:green bold')])).ask()

    if agent_choice == "exit" or agent_choice is None:
        print("Exiting the program")
        sys.exit(0)

    model_choice = questionary.select(
        "Select the LLM for this task:",
        choices=[
            questionary.Choice("Basic (gpt-4o-mini)", value="gpt-4o-mini"),
            questionary.Choice("Advanced (gpt-4o)", value='gpt-4o')
        ]
    ).ask()

    if model_choice is None:
        sys.exit(0)

    file_name = questionary.text("Enter the exact target file name").ask()

    if file_name is None or file_name.strip() == "":
        print("Wrong file name")
        sys.exit(1)

    print(f"\n Starting process...")
    print(f"Model: {model_choice}")
    print(f"File: {file_name}\n")

    try:
        if agent_choice == "tester":
            print(f"[SIMULATION] -> Called generate_test_cases('{file_name}', '{model_choice}')")
            agent_tester.generate_test_cases(file_name, model_choice)
        elif agent_choice == "reviewer":
            print(f"[SIMULATION] -> Called review_test_cases('{file_name}', '{model_choice}')")
            agent_qa_reviewer.review_test_cases(file_name, model_choice)
        elif agent_choice == "reporter":
            print(f"[SIMULATION] -> Called prepare_tests_report('{file_name}', '{model_choice}')")
            
        
    except Exception as e:
        print(f"An error occurred during Agent execution {e}")


if __name__ == '__main__':
    main()
