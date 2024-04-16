from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.login_attempt_middleware import LoginAttemptMiddleware
from app.routes.technicians_route import router as technicians_route
from app.routes.llm_query_route import router as llm_query_route
from app.routes.login_route import router as login_route
from app.routes.tickets_route import router as tickets_route
from app.routes.infographics_route import router as infographics_route
from app.routes.activity_route import router as activity_route

app = FastAPI(
    title="Rostering.AI",
    swagger_ui_parameters={"syntaxHighlight": False}
    )

app.add_middleware(LoginAttemptMiddleware)
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
app.include_router(infographics_route, prefix="/infographics", tags=["Infographics"])
app.include_router(activity_route, prefix="/activity", tags=["Activity"])

@app.get("/")
async def root():
    """
    Brief Description: This endpoint redirects users to the API documentation.

    Longer Description: This endpoint redirects users to the API documentation page ("/docs") where they can find detailed documentation about the available endpoints and how to interact with them.
    """
    return RedirectResponse(url="/docs")