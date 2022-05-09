from fastapi import FastAPI, HTTPException, Request, Form
from brandgenerator import generate_keywords, generate_snippet
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

app = FastAPI()


templates = Jinja2Templates(directory="templates")


max_input_length = 12
# snippet
@app.get("/generate_snippet")
async def generate_snippet_api(prompt: str):
    validate_input_length(prompt)
    snippet = generate_snippet(prompt)
    return snippet

# keywords
@app.get("/generate_keywords")
async def generate_keywords_api(prompt: str):
    validate_input_length(prompt)
    keywords = generate_keywords(prompt)
    print(keywords)
    return keywords

# calling both keywords and brand tag
@app.get("/generate_brand")
async def generate_brand_api(prompt: str):
    validate_input_length(prompt)
    snippet = generate_snippet(prompt)
    keywords = generate_keywords(prompt)
    
  
    return (f"Snippet: {snippet}, keywords: {keywords}")


# checking length of the input
def validate_input_length(prompt: str):
    if len(prompt) >= max_input_length:
        raise HTTPException(status_code=400, detail=f"Submitted input '{prompt}', is too long. Input length must be under {max_input_length} charcters!")


@app.get("/index", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html",{'request': request})

@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, prompt:Optional[str]):

    if validate_input_length(prompt):
        return templates.TemplateResponse("index.html", {'error':"Long Input"})
   
    snippet = generate_snippet(prompt)
    keywords = generate_keywords(prompt)
    
    print("printing snippet..")
    context = {"request":request, 'snippet':snippet,'keywords':keywords}

    return templates.TemplateResponse("index.html", context)