from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.technicians_route import router as technicians_route
from app.routes.llm_query_route import router as llm_query_route
from app.routes.login_route import router as login_route
from app.routes.tickets_route import router as tickets_route

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(technicians_route, prefix="/technicians", tags=["Technicians"])
app.include_router(llm_query_route, prefix="/llm", tags=["LLM"])
app.include_router(login_route, tags=["Authenticate"])
app.include_router(tickets_route, prefix="/tickets", tags=["Tickets"])

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")