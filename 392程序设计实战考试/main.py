from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
import pandas as pd
import matplotlib.pyplot as plt
import tempfile

from starlette.staticfiles import StaticFiles

app = FastAPI()


@app.post("/analyze/salary_by_district")
async def salary_by_district(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    # 检查列是否存在
    if 'district' not in df.columns or 'salary' not in df.columns:
        raise HTTPException(status_code=400, detail="缺少 'district' 或 'salary' 列")

    result = df.groupby('district')['salary'].agg(
        平均薪资='mean',
        最低薪资='min',
        最高薪资='max'
    ).reset_index()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        result.to_excel(tmp.name, index=False)
        temp_path = tmp.name

    return FileResponse(temp_path, filename="薪资统计.xlsx")


@app.post("/analyze/company_count_chart")
async def company_count_chart(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)

    # 去重
    count = df.groupby('district')['companyId'].nunique().sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    count.plot(kind='bar', color='steelblue')
    plt.xlabel('district')
    plt.ylabel('company')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
        plt.savefig(tmp.name)
        temp_path = tmp.name
    plt.close()

    return FileResponse(temp_path, filename="companynums.png")
app.mount("/", StaticFiles(directory=".", html=True), name="static")
