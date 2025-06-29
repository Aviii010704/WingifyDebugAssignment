# main.py

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio

from crewai import Crew, Process
from agents import doctor, verifier, nutritionist, exercise_specialist
from task import help_patients, nutrition_analysis, exercise_planning, verification
from database import init_db, save_file_and_analysis  # Import database functions

app = FastAPI(title="Blood Test Report Analyser")

# Initialize the database
init_db()

def run_crew(query: str, file_path: str = "data/sample.pdf"):
    """Run the entire agent crew on the uploaded blood test report"""

    medical_crew = Crew(
        agents=[doctor, verifier, nutritionist, exercise_specialist],
        tasks=[
            verification,
            help_patients,
            nutrition_analysis,
            exercise_planning
        ],
        process=Process.sequential
    )

    # ✅ FIXED: Make sure the file_path is included in inputs
    result = medical_crew.kickoff(inputs={"query": query, "file_path": file_path})
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if not query:
            query = "Summarise my Blood Test Report"
        
        response = run_crew(query=query.strip(), file_path=file_path)
        status = "success"
        
        # Save to database
        save_file_and_analysis(
            filename=file.filename,
            stored_path=file_path,
            size=os.path.getsize(file_path),
            query=query,
            output=str(response),
            status=status
        )
        
        return {
            "status": status,
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        status = "error"
        # Optionally save error to DB (output=str(e))
        save_file_and_analysis(
            filename=file.filename if file else "unknown",
            stored_path=file_path,
            size=os.path.getsize(file_path) if os.path.exists(file_path) else 0,
            query=query,
            output=str(e),
            status=status
        )
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
