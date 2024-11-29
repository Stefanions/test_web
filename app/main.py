from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
from fastapi.staticfiles import StaticFiles
from app.pages.router import router as router_pages
from pydantic import BaseModel
import time
import subprocess
import asyncio
import json


def run_scrapy_spider(url):
    project_directory = 'sp_EFRSB_parse'
    command = ['scrapy', 'crawl', 'bargaining_new', '-a', f'param={url}']
    process = subprocess.Popen(command, cwd=project_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode == 0:
        try:
            output = json.loads(stdout.decode('utf-8'))
            for i in output:
                return output
        except json.JSONDecodeError:
            return False
    else:
        return False
# Инициализация подключение
app = FastAPI()
app.include_router(router_pages)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Настройка папки с шаблонами
templates = Jinja2Templates(directory="app/templates")

#Для валидации данных с фронта
class LinkRequest(BaseModel):
    link: str

@app.get("/", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

@app.post("/parse_scrapy")
async def process_link(data: LinkRequest):
    result = run_scrapy_spider(data.link)

    # result = [item for item in result if (item.get('final_price') is not None)]
    
    #Обрабатываем result
    for i in result:
        i['date'] = i['date'].split("— ")[1]
    #Убираем где нет победителя
    all(word in text for word in words)
    result = [item for item in result if ((key_word in item.get('description')) and (item.get('winner')))]
    #Получаем среднюю цену
    av = 0
    for el in result:
        if (el.get("final_price")) is not None:
            av += float(el.get("final_price").replace(" ", "").replace("₽", "").replace(",", "."))
        else:
            av += float(el.get("start_price").replace(" ", "").replace("₽", "").replace(",", "."))
            el['final_price'] = el['start_price']

    av = round(av/len(result), 2)

    #Получаем краткую сводку
    summary = {"av": av}



    return {"result": result, "summary": summary}