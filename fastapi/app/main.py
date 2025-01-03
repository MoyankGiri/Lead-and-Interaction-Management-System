from fastapi import FastAPI, Depends
from app.routers import leads, pocs, interactions, performance
from app.auth.auth import get_current_user, router as authrouter
from app.database import engine, Base

# Initialize database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# Authentication routes without protection
app.include_router(authrouter, prefix="/auth", tags=["Authentication"])

# All other routes with global dependency protection
app.include_router(leads.router, prefix="/leads", tags=["Leads"], dependencies=[Depends(get_current_user)])
app.include_router(pocs.router, prefix="/pocs", tags=["POCs"], dependencies=[Depends(get_current_user)])
app.include_router(interactions.router, prefix="/interactions", tags=["Interactions"], dependencies=[Depends(get_current_user)])
app.include_router(performance.router, prefix="/performance", tags=["Performance"], dependencies=[Depends(get_current_user)])