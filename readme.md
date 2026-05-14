# AI-Playwright QA Framework

## Project Overview
This project is an advanced, proof-of-concept Quality Assurance framework that bridges the gap between Artificial Intelligence and UI/API Test Automation. It demonstrates a fully automated testing lifecycle: from business requirements analysis to test execution and executive reporting.

The system uses **LangGraph (OpenAI)** agents to generate and review test scenarios based on markdown requirements, executes the coded automated tests using **Playwright**, and utilizes AI again to analyze the final test reports.

The target application under test is **ParaBank** (a locally hosted banking system).

## The AI-QA Workflow
1. **Requirement Analysis:** Business rules are defined in wiki folder.
2. **AI Test Generation:** The *Agent Tester* (LangGraph) analyzes the requirements and generates structured test cases.
3. **AI Peer Review:** The *Agent Senior QA* reviews the generated cases, adding edge cases and ensuring coverage.
4. **Test Execution:** Tests are coded and executed using Playwright (TypeScript).
5. **AI Executive Reporting:** The *Agent Report Manager* analyzes Playwright's test output and generates a business-friendly summary of the quality metrics.

## Tech Stack
* **UI/API Testing:** Playwright, TypeScript, Node.js
* **AI Orchestration:** Python, LangGraph, LangChain, OpenAI API
* **Infrastructure:** Docker (Local Test Environment), GitHub Actions (CI/CD)

## Getting Started

### Prerequisites
Make sure you have the following installed on your machine:
* [Docker Desktop](https://www.docker.com/products/docker-desktop)
* [Node.js](https://nodejs.org/) (v20+)
* [Python](https://www.python.org/downloads/) (v3.10+)
* An active OpenAI API Key

### 1. Start the Target Application (ParaBank)
Run the ParaBank system locally using Docker:
```bash
docker run -d -p 8080:8080 parasoft/parabank
```
The application will be available at http://localhost:8080/parabank.

### 2. Setup the Playwright Enviroment
Install Node dependencies and Playwright browsers:
```bash
npm install
npx playwright install
```

### 3. Setup the AI Agents Enviroment
Navigate to the AI agents folder, create a virtual environment, and install required Python packages:
```bash
cd ai-agents
python -m venv venv

# On Windows:
.\venv\Scripts\activate
# On Mac/Linux:
# source venv/bin/activate

pip install -r requirements.txt
```

### 4. Configure Enviroment Variables

Create a ```.env``` file inside the ```ai-agents``` directory and add your OpenAI API key:
```
OPENAI_API_KEY=your_actual_api_key_here
```
