"""Starts the screen.     uvicorn server:app --reload      then open http://127.0.0.1:8000
Set OFFLINE=1 to run from your files without Neo4j."""
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse
import service


from offline_graph import OfflineGraph; G = OfflineGraph()

app = FastAPI(title="India import shock")
@app.get("/api/options")
def options(): return service.options(G)
@app.get("/api/scenario")
def scenario(country: str, hs: str = "all", sev: float = 1.0, asof: int | None = None): return service.scenario(G, country, hs, sev, asof)
@app.get("/")
def home(): return FileResponse(Path(__file__).parent / "static" / "index.html")
