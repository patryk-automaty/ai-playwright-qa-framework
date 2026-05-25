import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

# Load OpenAI API key from .env file
load_dotenv()


def prepare_tests_report(file_name: str) -> None:
    """
    Reads a Playwright JSON test report, sends it to an LLM for executive analysis,
    and writes the resulting Markdown summary to reports/executive_summary.md.

    Args:
        file_name: Name of the JSON file inside the test-results/ directory.
    """
    # Resolve the absolute path to the test results file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.abspath(os.path.join(script_dir, '..', 'test-results', file_name))

    # Read the raw JSON test report from disk
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            test_result_to_report = file.read()
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return

    # Initialise the LLM — GPT-4o with low temperature for consistent, factual output
    llm = ChatOpenAI(model='gpt-4o', temperature=0.2)

    # Build a structured prompt for executive QA report generation
    prompt = ChatPromptTemplate.from_messages([
        ('system', '''You are an Executive QA Manager responsible for translating raw Playwright 
                      test-execution JSON reports into clear, business-friendly Markdown summaries 
                      for stakeholders and Product Owners.

                      Always structure your report with the following sections:
                      1. **Executive Summary** – one-paragraph high-level overview.
                      2. **Overall Status** – pass/fail rate as a percentage and a visual indicator.
                      3. **Scope of Testing** – what features / scenarios were covered.
                      4. **Detailed Failure Analysis** – for each failure: test name, error details, and 
                         potential business impact.
                      5. **Metrics** – total tests, passed, failed, skipped, duration.
                      6. **Go / No-Go Recommendation** – a clear deploy-or-not decision with rationale.

                      Use a professional but accessible tone. Avoid technical jargon where possible.''' ),
        ('user', '''Analyse the following Playwright test execution JSON report and produce the executive 
                    summary as described.

                    JSON report:
                    {test_report}''')
    ])

    # Assemble the LangChain run chain: prompt → LLM
    chain = prompt | llm

    print(f"Agent (reporter) is reading the file: {file_path}...\n")

    # Invoke the chain — returns an AIMessage object; extract .content for the string
    response = chain.invoke({"test_report": test_result_to_report})
    report_content = response.content  # 👈 FIX: extract plain text from AIMessage

    # Write the generated Markdown report to the reports/ folder
    output_path = os.path.abspath(os.path.join(script_dir, '..', 'reports', "executive_summary.md"))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print("===========================================")
    print("=== TESTS RESULTS HAVE BEEN REPORTED ===")
    print("===========================================")


if __name__ == "__main__":
    # Default report file to process when running the script directly
    selected_file = "playwright-report.json"
    prepare_tests_report(selected_file)