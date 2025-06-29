# tools.py

import os
from dotenv import load_dotenv
load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool

# Creating search tool
search_tool = SerperDevTool()

# Custom PDF Reader Tool as a CrewAI Tool
class BloodPDFTool(BaseTool):
    name: str = "Blood Test PDF Reader"
    description: str = "Reads and returns the content of a blood test PDF file given its file path."

    def _run(self, file_path: str):
        try:
            file_path = "data/blood_test_report.pdf"
            docs = PyPDFLoader(file_path=file_path).load()
            full_report = ""
            for data in docs:
                content = data.page_content
                content = content.replace("\n\n", "\n")
                full_report += content + "\n"
            return full_report
        except Exception as e:
            return f"Error reading PDF file: {str(e)}"

blood_pdf_tool = BloodPDFTool()

# Nutrition Analysis Tool (Placeholder)
class NutritionAnalysisTool(BaseTool):
    name: str = "Nutrition Analysis Tool"
    description: str = "Analyzes nutritional insights from blood report data (to be implemented)."

    def _run(self, blood_report_data: str):
        # TODO: Implement actual nutrition logic
        return "Nutrition analysis functionality to be implemented"

nutrition_analysis_tool = NutritionAnalysisTool()

# Exercise Planning Tool (Placeholder)
class ExercisePlanningTool(BaseTool):
    name: str = "Exercise Planning Tool"
    description: str = "Generates exercise plans from blood report data (to be implemented)."

    def _run(self, blood_report_data: str):
        # TODO: Implement actual exercise planning logic
        return "Exercise planning functionality to be implemented"

exercise_planning_tool = ExercisePlanningTool()

# Export the tools so they can be imported
__all__ = ["search_tool", "blood_pdf_tool", "nutrition_analysis_tool", "exercise_planning_tool"]
