# 웹 백엔드 프레임 워크인 fastapi 모듈 불러오기
from fastapi import FastAPI, Request , Form
from fastapi.templating import Jinja2Templates
from typing_extensions import Annotated
from jinja2 import Template
from sqlalchemy import create_engine # 커넥터 연결 도구
import uvicorn

            #sql종류: //아이디:비번@아이피:포트/스키마 이름
db_connection=create_engine('mysql://root:1234@127.0.0.1:3306/test') # 커넥트 연결

'''
        #커넥터를 통해 실행하겠다(쿼리를)
query = db_connection.execute('select* from player')

        #쿼리 날려서 그 결과를 result 변수에 받아옴
result = query.fetchall()

for data in result:
    print('=========================================================================')
    print(data)
'''



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

# 화면 입력창부터 들어가기, 값을 입력하는 곳
@app.get('/test_get')
def test_get(request:Request):
    return templates.TemplateResponse('post_test.html',context={'request':request}) #request

# 값을 받는 친구
@app.post('/test_post')
def test_post(name:Annotated[str,Form()],pwd:Annotated[int,Form()]):
    print(name,pwd)

@app.get('/mysqltest')
def db_get(request:Request):
    query = db_connection.execute('select* from player') # 데이터를 다 불러오는
    result_db = query.fetchall()

    #받아온 정보를 정제해서 리스트에 담을 것 
    result=[]
    for data in result_db:
        temp = {'player_id':data[0], 'player_name':data[1]}
        result.append(temp)

    ## result [{선수id,선수이름} ,{선수id,선수이름},{선수id,선수이름},{선수id,선수이름}]

                                                    # 페이지를 jinja2로 랜더링할 때 서버 정보가 필요하다, 
                                                    # 그래서 request에는 서버에 대한 상태 정보들이 저장되어 있어서 프론트로 던진다. 
    return templates.TemplateResponse('sqltest.html',context={'request':request,'result_table':result})

@app.get('/detail')
def detail(request:Request, id:str,name:str):
    # 쿼리문 문법이 잘 실행이 안되면 mysql열어서 확인
    query = db_connection.execute('select* from player where player_id={} and player_name like '{}''.format(id,name)) # like 는 문자 비교할 때 사용
    result_db=query.fetchall
    result=[]
    for i in result_db:
        temp={'player_id':i[0],'player_name':i[1],'team_name':i[2],'height':i[-2],'weight':i[-1]}
        result.append(temp)

    return templates.TemplateResponse('detail.html',context={'request':request,'result_table':result})


if __name__ == '__main__':
                    #ip 설정,    port 설정하는 곳
    uvicorn.run(app,host='localhost',port=5000)
    

