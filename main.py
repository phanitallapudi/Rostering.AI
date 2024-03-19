from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routes.technicians_route import router as technicians_route
from app.routes.llm_query_route import router as llm_query_route

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(technicians_route)
app.include_router(llm_query_route)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")