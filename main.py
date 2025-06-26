from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    return {
        "rows": len(df),
        "columns": list(df.columns)
    }
