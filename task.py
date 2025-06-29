# task.py

from crewai import Task
from agents import doctor, verifier, nutritionist, exercise_specialist
from tools import blood_pdf_tool

# Verification Task
verification = Task(
    description="Verify that the uploaded file is a valid blood test report and contains the necessary medical data. Check for completeness and proper formatting.",
    expected_output="""Provide a verification report including:
- Confirmation that the file is a blood test report
- Assessment of data completeness
- Identification of any missing or unclear information
- Overall quality assessment of the report""",
    agent=verifier,
    tools=[blood_pdf_tool],
    async_execution=False,
)

# Help Patients Task
help_patients = Task(
    description="Analyze the blood test report and provide comprehensive medical insights for the query: {query}. Focus on interpreting the results and providing evidence-based recommendations.",
    expected_output="""Provide a detailed medical analysis including:
- Interpretation of key blood test parameters
- Identification of any abnormal values
- Medical context and potential health implications
- Recommendations for follow-up actions
- Professional medical advice based on the results""",
    agent=doctor,
    tools=[blood_pdf_tool],
    async_execution=False,
)

# Nutrition Analysis Task
nutrition_analysis = Task(
    description="Analyze the blood test results from a nutritional perspective and provide dietary recommendations based on the findings.",
    expected_output="""Provide nutritional analysis including:
- Dietary recommendations based on blood test results
- Specific foods to include or avoid
- Supplement recommendations if appropriate
- Meal planning suggestions
- Lifestyle dietary changes""",
    agent=nutritionist,
    tools=[blood_pdf_tool],
    async_execution=False,
)

# Exercise Planning Task
exercise_planning = Task(
    description="Create a safe and effective exercise plan based on the blood test results and overall health profile.",
    expected_output="""Provide exercise recommendations including:
- Safe exercise types based on health status
- Intensity and frequency guidelines
- Precautions and contraindications
- Progressive training recommendations
- Monitoring and adjustment strategies""",
    agent=exercise_specialist,
    tools=[blood_pdf_tool],
    async_execution=False,
)
