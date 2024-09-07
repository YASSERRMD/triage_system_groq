from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()




GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@app.get("/")
def read_root():
    return FileResponse("index.html")

@app.post("/transcribe/")
async def transcribe_audio(file: UploadFile = File(...)):
    client = Groq(api_key=GROQ_API_KEY)

    # Save the uploaded file temporarily
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())

    # Transcribe the audio file
    with open(file.filename, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            file=(file.filename, audio_file.read()),
            model="distil-whisper-large-v3-en",#"whisper-large-v3",
            response_format="verbose_json",
        )

    # Remove the temporary file
    os.remove(file.filename)
    completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
         {
            "role": "system",
            "content": """convert the statement paramedic or doctor to the strictly as per  below json schema\n\n
            
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Triage Assessment Form",
  "type": "object",
  "properties": {
    "voiceObservation": {
      "type": "string"
    },
    "patientInformation": {
      "type": "object",
      "properties": {
        "patientName": { "type": "string" },
        "age": { "type": "integer" },
        "gender": { "type": "string", "enum": ["male", "female", "other"] }
      },
      "required": ["patientName", "age", "gender"]
    },
    "abcdeAssessment": {
      "type": "object",
      "properties": {
        "airwayStatus": { "type": "string", "enum": ["clear", "obstructed", "partially obstructed"] },
        "breathingStatus": { "type": "string", "enum": ["normal", "labored", "not breathing"] },
        "circulationStatus": { "type": "string", "enum": ["normal", "weak", "absent"] },
        "disabilityStatus": { "type": "string", "enum": ["alert", "verbal", "pain", "unresponsive"] },
        "exposure": { "type": "string" }
      },
      "required": ["airwayStatus", "breathingStatus", "circulationStatus", "disabilityStatus", "exposure"]
    },
    "triageClassification": {
      "type": "object",
      "properties": {
        "triageCategory": { "type": "string", "enum": ["red", "yellow", "green", "black"] },
        "comments": { "type": "string" }
      },
      "required": ["triageCategory"]
    }
  },
  "required": ["patientInformation", "abcdeAssessment", "triageClassification"]
}

            
            
            """
        },
        {
            "role": "user",
            "content": "convert the paramedic statement to json " + transcription.text
        }
    ],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
    )

    print(completion.choices[0].message.content or "", end="")


    return {"transcription": transcription.text,"details":completion.choices[0].message.content}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)