"""NFe na rede API."""
from fastapi import FastAPI
from mangum import Mangum


# FastAPI Config ---------------------------------------------------------------------------------------------
app = FastAPI(title="NFe na rede API", version="2022.1001")

# Handler Lambda - Mangum ------------------------------------------------------------------------------------

# app.include_router(api_router)

# Handler Lambda - Mangum ------------------------------------------------------------------------------------

handler = Mangum(app=app)

# ------------------------------------------------------------------------------------------------------------
