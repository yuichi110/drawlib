# FastAPI Best Practices (`python/frameworks/fastapi`)

## 1. Async Event-Loop Safety
- Never invoke blocking synchronous I/O (`time.sleep()`, `requests.get()`, `urllib.request.urlopen()`, blocking `subprocess.run()`, or synchronous ORM calls) inside `async def` route handlers—either use `httpx.AsyncClient` / `asyncio.sleep` or define the route with plain `def` so FastAPI runs it in a threadpool.

## 2. Explicit Schemas & Dependency Injection
- Declare typed `response_model=...` or explicit Pydantic return annotations on route handlers so OpenAPI contracts and output serialization filtering remain deterministic.
- Use `Depends(...)` with `Annotated[Service, Depends(get_service)]` for database sessions, auth principals, and external clients instead of module-level mutable singletons.

## 3. Lifespan & Error Boundaries
- Manage startup/shutdown resources via `FastAPI(lifespan=...)` async context managers rather than deprecated `@app.on_event("startup" | "shutdown")`.
- Separate HTTP routers (`api/`), domain services (`services/`), and persistence repositories (`repositories/`).
