from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


router = APIRouter(prefix='/parse', tags=['Фронтенд'])
templates = Jinja2Templates(directory='app/templates')

#Для валидации данных с фронта
class LinkRequest(BaseModel):
    link: str


@router.get('/')
async def get_students_html(request: Request):
    return templates.TemplateResponse(name='parse_EFRSB.html', context={'request': request})
