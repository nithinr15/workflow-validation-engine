from fastapi import FastAPI
from typing import List, Dict
from validator import validate_records
from simulator import simulate_workflow
from integration import fetch_external_data
from rules import RULES
from fastapi import UploadFile, File
import csv
import io
from fastapi.responses import FileResponse
import json

app = FastAPI(title="Workflow Validation Engine")

@app.get("/")
def home():
    return {"message": "Workflow Validator API Running"}

@app.post("/validate")
async def validate(data: List[Dict]):
    return await validate_records(data)

@app.post("/simulate")
def simulate(data: List[Dict]):
    return simulate_workflow(data)

@app.get("/fetch-and-validate")
async def fetch_and_validate():
    data = fetch_external_data()

    if isinstance(data, dict) and data.get("error"):
        return data

    validation_result = await validate_records(data)
    simulation_result = simulate_workflow(data)

    return {
        "source": "external_api",
        "records_fetched": len(data),
        "validation": validation_result,
        "simulation": simulation_result
    }

@app.get('/rules')
def update_rules(new_rules: List[Dict]):
    global RULES
    RULES.clear()
    RULES.extend(new_rules)
    print("RULES", RULES)

    return {
        "message": "Rules updated successfully",
        "total_rules": len(RULES)
    }

@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    content = await file.read()
    decoded = content.decode("utf-8")

    reader = csv.DictReader(io.StringIO(decoded))

    records = []
    for row in reader:
        records.append({
            "email": row.get("email"),
            "status": row.get("status"),
            "history": row.get("history", "").split("|")  # pipe-separated
        })

    validation_result = await validate_records(records)
    simulation_result = simulate_workflow(records)

    return {
        "records_processed": len(records),
        "validation": validation_result,
        "simulation": simulation_result
    }

@app.post("/export-report")
async def export_report(data: List[Dict]):
    validation_result = await validate_records(data)
    simulation_result = simulate_workflow(data)

    report = {
        "validation": validation_result,
        "simulation": simulation_result
    }

    file_path = "report.json"

    with open(file_path, "w") as f:
        json.dump(report, f, indent=4)

    return FileResponse(
        path=file_path,
        filename="validation_report.json",
        media_type="application/json"
    )

