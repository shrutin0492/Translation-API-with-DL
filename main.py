from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, validator
import tasks
app=FastAPI()

languages=["English","French","German","Romanian"]

class Translation(BaseModel):
    text: str
    base_lang: str
    final_lang: str

    @validator('base_lang','final_lang')
    def valid_lang(cls,lang):
        if lang not in languages:
            raise ValueError("Invalid language")
        return lang



## Route 1: /
## Test of everything is working
## {"message":"Hello world"}
@app.get("/")
def get_root():
    return {"message":"Hello world"}

## Route 2: /translate
## Take in a translation request, and store it to the db
## Return a translation id
@app.post("/translate")
def post_translation(t: Translation, background_tasks: BackgroundTasks):
    # Store the translation
    # Run translation in background
    t_id=tasks.store_translation(t)
    background_tasks.add_task(tasks.run_translation, t_id)
    return {"task_id":t_id}

## Route 3: /results
## Take in a translation id
## Return the translated text
@app.get("/results")
def get_translation(t_id:int):
    return {"translation":tasks.find_translation(t_id)}