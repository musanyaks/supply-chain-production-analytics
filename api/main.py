from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import inventory, production, procurement

app = FastAPI(title="Supply Chain Analytics API", version="1.0.0")

# Enable CORS so Streamlit can talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory.router, prefix="/api", tags=["Inventory"])
app.include_router(production.router, prefix="/api", tags=["Production"])
app.include_router(procurement.router, prefix="/api", tags=["Procurement"])

@app.get("/health")
def health_check():
    return {"status": "healthy"}
