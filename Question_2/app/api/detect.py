from fastapi import APIRouter, Request
from pydantic import BaseModel
from model.QA_model import QA_model as model
from model.combine import multi_user
router = APIRouter()

model_name = "deepset/xlm-roberta-large-squad2"
model = model(model_name, model_name)

# Define a Pydantic model to parse the incoming JSON data
class MessageData(BaseModel):
    timeMessage: str
    collectedText: str

# Define an endpoint to handle the incoming data
@router.post("/submit-data")
async def submit_data(data: MessageData):
    # Access timeMessage and collectedText from the request
    time_message = data.timeMessage
    collected_text = data.collectedText

    # For demonstration, print or process the data as needed
    print("Time Message:", time_message)
    time = time_message.split(" ")
    time = time[0] * 60 + time[1]
    messages = collected_text.split("\n")[:-1]
    print("Collected Text:", messages)
    # Return a response
    return {"status": "success", "timeMessage": time_message, "collectedText": collected_text}


# Run the FastAPI server using: uvicorn script_name:app --reload
