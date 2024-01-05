# 웹 백엔드 프레임 워크인 fastapi 모듈 불러오기
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from jinja2 import Template
import uvicorn

#fastAPI 객체 생성
app=FastAPI()

templates = Jinja2Templates(directory='templates') # html이 작성된 코드를 불러와서 렌더링 할꺼야

@app.get('') # fastAPI 객체에 url주소 매핑 정의 (예: http://231.28.13.23:5000)
def hello(): # 사용자가 http://231.28.13.23:5000 url 쳤을때 실행되는 함수
    return {'message : 안녕하세요 fastapi입니다'} # 메세지 return

@app.get('/test')
def test(request:Request):
    print(Request)
    return templates.TemplateResponse('test.html',context={'request':request,'a':2}) # test.html 웹 스크립트를 열꺼야. 
    # html을 열려면 context인자를 꼭 쓰고 request를 통해 서버 정보를 전달한다. a라는 변수에 2를 넣어서 웹 화면에 던져보는코드


@app.get('/getinfo/{name}/{gender}')
def getinfofn(request: Request , name:str, gender:str):
    print(name, gender)
    return templates.TemplateResponse('test.html',context={'request':request, 'name':name ,'gender': gender})

@app.get('/teamname/{name1}/{name2}')
def teamname(request:Request, name1:str, name2:str):
    return templates.TemplateResponse('team.html',context={'request':request, 'name1':name1 ,'name2': name2})


if __name__ == '__main__':
                    #ip 설정,    port 설정하는 곳
    uvicorn.run(app,host='localhost',port=5000)
    

