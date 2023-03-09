# Kütüphaneleri import ediyoruz
from multiprocessing import context
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import PlainTextResponse,JSONResponse,RedirectResponse
from starlette.templating import Jinja2Templates #Html dosyası import etmek için 
from db import get_all_students,create_a_student,get_a_student_by_id,update_student_data,delete_student_data

templates=Jinja2Templates(directory="templates")

# asenkron fonksiyon tanımlıyoruz
async def index(request:Request):   
    #Request HTTP kanalı kitaplığıdır.ASGI kapsamına erişmek yerine doğrudan kanal alır.
    student_id = request.path_params.get("student_id") 
    #path_params = Yol parametreleri
    student_name = request.query_params.get("student_name") or "World"
    #query_params =Sorgu Parametreleri
    return PlainTextResponse(content=f"Hello {student_name}")  
    #content = Bir dize veya bayt dizisi.

async def Json_endpoint(request:Request):
    return JSONResponse(content={"Message":"Hello World"})

async def html_endpoint(request:Request):
    student_name ="JOHN DOE"
    students=get_all_students()
    context={"request":request,"name":student_name,"students":students}
    return templates.TemplateResponse("index.html",context) #Response=yanıt

async def create_students(request:Request):
    if request.method == "POST":
        #request.method = İstek yöntemine erişir.
        student_data=await request.form()
        create_a_student(student_data)
        return RedirectResponse(request.url_for('html_endpoint'),status_code=303)
    
    if input== ' ':
        create_a_student(student_data)
        return RedirectResponse(request.url_for('html_endpoint'),status_code=303)        
    
    context = {"request":request}
    return templates.TemplateResponse("create.html",context)

async def update_a_student(request:Request):
    student_id=request.path_params.get("student_id") 
    #Çerezin uygulanacağı yolların alt kümesini belirten bir dize.
    student_to_update=get_a_student_by_id(student_id)

    if request.method == "POST":
        student_update_data = await request.form()
        update_student_data(student_id,student_update_data)
        return RedirectResponse(request.url_for("html_endpoint"),status_code=303)

    context={"request":request,"student":student_to_update}
    return templates.TemplateResponse("update.html",context)
    
async def delete_student(request:Request):
    student_id = request.path_params.get("student_id") 
    delete_student_data(student_id)    

    return RedirectResponse(request.url_for('html_endpoint'),status_code=303)


# yönlendirme yapıyoruz
routes=[
    #Route("/{student_id:int}",endpoint=index),
    Route("/json",endpoint=Json_endpoint),
    Route("/",endpoint=html_endpoint),
    Route("/create_student",endpoint=create_students,methods=["GET","POST"]),
    Route("/update_student/{student_id:int}",endpoint=update_a_student,methods=["GET","POST"]),
    Route("/delete/{student_id:int}/",endpoint=delete_student)
]


app=Starlette(
    debug=True,
    routes=routes

)