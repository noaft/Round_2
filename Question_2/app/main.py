from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# init app
app = FastAPI()

# mount at folder static for static
app.mount("/static", StaticFiles(directory="static"), name="static")

# set directory is templates
templates = Jinja2Templates(directory="templates")

# firt router 
@app.get("/")
async def page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)