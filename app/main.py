import logging

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.responses import PlainTextResponse
from xlwings import XlwingsError

from .api import github

# Don't expose the docs publicly
app = FastAPI(docs_url=None, redoc_url=None)

# Logging configuration
logging.basicConfig(level=logging.INFO)

# Error handling
# Only handle those Exceptions where you want the frontend to show a detailed error.
# Otherwise, it'll return a generic "Internal Server Error". Showing too many
# details may have security implications for your application.
@app.exception_handler(XlwingsError)
async def xlwings_exception_handler(request, exception):
    return PlainTextResponse(
        str(exception), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exception):
    # Return "msg" instead of {"detail": "msg"} for nicer frontend formatting
    return PlainTextResponse(str(exception.detail), status_code=exception.status_code)


# Routers
app.include_router(github.router)

# Unprotected healthcheck
@app.get("/health")
async def health():
    return {"status": "ok"}
