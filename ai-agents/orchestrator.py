import questionary
import os
import sys

# Ensure the ai-agents directory is on the path for sibling imports
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

import agent_tester
import agent_qa_reviewer
import agent_report_manager


def _check_api_key() -> bool:
    """Warn the user if OPENAI_API_KEY is not set."""
    from dotenv import load_dotenv
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("  OPENAI_API_KEY not found in environment or .env file.")
        print("   Create an .env file in the ai-agents/ folder with:\n")
        print("       OPENAI_API_KEY=sk-...\n")
        return False
    return True


def _resolve_file_path(agent_choice: str, file_name: str) -> str | None:
    """Return the absolute path to the file for the given agent, or None if missing."""
    subdir_map = {
        "tester": ("wiki", file_name),                          # login.md
        "reviewer": ("test_cases", file_name),                  # login.json
        "reporter": ("test-results", file_name),                # playwright-report.json
    }
    subdir, fname = subdir_map[agent_choice]
    path = os.path.abspath(os.path.join(_SCRIPT_DIR, "..", subdir, fname))
    if not os.path.isfile(path):
        print(f"File not found: {path}")
        return None
    return path


def _describe_file_format(agent_choice: str) -> str:
    """Return a user-friendly hint about which file to enter."""
    hints = {
        "tester": "the requirements filename (e.g. login.md) from the wiki/ folder",
        "reviewer": "the test-case filename (e.g. login.json) from the test_cases/ folder",
        "reporter": "the results filename (e.g. playwright-report.json) from the test-results/ folder",
    }
    return hints.get(agent_choice, "the target filename")


def main() -> None:
    print(" Welcome to the AI-Playwright QA Framework CLI\n")

    # ── API key guard ──────────────────────────────────────────
    if not _check_api_key():
        sys.exit(1)

    while True:
        # ── Agent selection ────────────────────────────────────
        agent_choice = questionary.select(
            "Select the AI Agent you want to run:",
            choices=[
                questionary.Choice("1. Agent Tester (Generate tests from requirements)", value="tester"),
                questionary.Choice("2. Agent Senior QA (Review test cases)", value="reviewer"),
                questionary.Choice("3. Agent Report Manager (Analyze Playwright results)", value="reporter"),
                questionary.Choice("Exit", value="exit"),
            ],
            style=questionary.Style([("highlighted", "fg:green bold")]),
        ).ask()

        if agent_choice is None or agent_choice == "exit":
            print("Goodbye!")
            sys.exit(0)

        # ── Model selection ────────────────────────────────────
        model_choice = questionary.select(
            "Select the LLM for this task:",
            choices=[
                questionary.Choice("Basic (gpt-4o-mini)", value="gpt-4o-mini"),
                questionary.Choice("Advanced (gpt-4o)", value="gpt-4o"),
            ],
        ).ask()

        if model_choice is None:
            sys.exit(0)

        # ── File selection with context-aware hint ────────────
        hint = _describe_file_format(agent_choice)
        file_name = questionary.text(
            f"Enter {hint}"
        ).ask()

        if not file_name or not file_name.strip():
            print("File name cannot be empty.")
            continue

        file_name = file_name.strip()

        # ── Pre-flight validation ─────────────────────────────
        resolved = _resolve_file_path(agent_choice, file_name)
        if resolved is None:
            continue

        print(f"\nStarting process...")
        print(f"   Agent: {agent_choice}")
        print(f"   Model: {model_choice}")
        print(f"   File:  {resolved}\n")

        # ── Route to the selected agent ────────────────────────
        try:
            if agent_choice == "tester":
                agent_tester.generate_test_cases(file_name, model_choice)
            elif agent_choice == "reviewer":
                agent_qa_reviewer.review_test_cases(file_name, model_choice)
            elif agent_choice == "reporter":
                agent_report_manager.prepare_tests_report(file_name, model_choice)
        except Exception as e:
            print(f"An error occurred during agent execution: {e}")

        # ── Offer another run ──────────────────────────────────
        again = questionary.confirm("Would you like to run another task?").ask()
        if not again:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
