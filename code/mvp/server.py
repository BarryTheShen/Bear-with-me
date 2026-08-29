"""Local ASGI entrypoint for the modular MVP API."""

from .api import create_app

app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("code.mvp.server:app", host="0.0.0.0", port=8000, reload=False)
