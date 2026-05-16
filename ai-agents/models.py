from typing import List
from pydantic import BaseModel, Field

# Define data structure
class TestCase(BaseModel):
    test_id: str = Field(description="Unique identifier for the test, e.g., TC-001")
    title: str = Field(description="Short, descriptive title of the test")
    description: str = Field(description="Detailed description of what is being tested")
    steps: List[str] = Field(description="List of steps to execute the test")
    expected_results: str = Field(description="The expected outcome of the test")

class TestSuite(BaseModel):
    test_cases: List[TestCase] = Field(description="List of generated test cases")