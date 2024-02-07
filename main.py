import uvicorn
from fastapi import Request, FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from db_user_func import (add_new_user, get_user_by_email,
                                      user_exists)
from db_questions_func import get_questions, get_correct_answers

app = FastAPI()

app.mount("/static", StaticFiles(directory="static", html=True), name="static")


def get_file_response(file_path: str) -> FileResponse:
    return FileResponse(file_path)


def get_json_response(content: dict, status_code: int) -> JSONResponse:
    return JSONResponse(content=content, status_code=status_code)


@app.get("/auth/")
async def get_auth_page() -> FileResponse:
    return get_file_response("static/html/auth_page.html")


@app.get("/home/")
async def get_home_page() -> FileResponse:
    return get_file_response("static/html/home_page.html")


@app.get("/quiz/")
async def get_quiz_page() -> FileResponse:
    return get_file_response("static/html/test.html")


@app.get("/registration/")
async def get_registration_page() -> FileResponse:
    return get_file_response("static/html/registration.html")


@app.get("/login/")
async def get_login_page() -> FileResponse:
    return get_file_response("static/html/login.html")


@app.post("/add_user")
async def create_user(request: Request) -> JSONResponse:
    data = await request.json()

    name = data["name"]
    email = data["email"]
    password = data["password"]

    print(name, email, password)
    if user_exists(email):
        return get_json_response({}, 403)

    add_new_user(name=name, email=email, password=password)

    return get_json_response({}, 200)


@app.post("/find_user")
async def find_user(request: Request) -> JSONResponse:
    data = await request.json()

    email = data["email"]
    password = data["password"]

    if not user_exists(email):
        return get_json_response({}, 404)

    user = get_user_by_email(email=email)
    accepted_response = user.password.password == password
    response_json = {"id": user.id, "accepted": accepted_response}

    return get_json_response(response_json, 200)


@app.post("/submit_answers")
async def check_answers(request: Request) -> JSONResponse:
    data = await request.json()
    answers = get_correct_answers()
    amount_questions = len(answers)
    amount_correct_answers = sum([int(user_answer == correct_answer)
                                  for user_answer, correct_answer in zip(answers, data)])

    response = {"result": amount_correct_answers / amount_questions}

    return get_json_response(response, 200)


@app.get("/get_questions")
async def send_questions() -> JSONResponse:
    return get_json_response(get_questions(), 200)


@app.get("/quiz/")
async def get_quiz_page() -> FileResponse:
    return get_file_response("static/html/test.html")


if __name__ == '__main__':
    uvicorn.run('main:app', port=8000, reload=True)
