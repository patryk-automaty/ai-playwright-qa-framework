import questionary
import os 
import sys


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


if __name__ == '__main__':
    main()
