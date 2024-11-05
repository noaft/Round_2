from fastapi import APIRouter, Request
from pydantic import BaseModel

router = APIRouter()

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
    print("Collected Text:", collected_text)

    # Return a response
    return {"status": "success", "timeMessage": time_message, "collectedText": collected_text}

# Run the FastAPI server using: uvicorn script_name:app --reload
