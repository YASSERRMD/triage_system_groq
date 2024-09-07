# Triage Assessment System

This is a FastAPI application that provides a system for transcribing audio files and converting the transcription into a JSON object that follows a specific schema. The system uses the Groq API for audio transcription and a language model for text-to-JSON conversion.

## Setup

1. Clone the repository:

```bash
git clone https://github.com/yourusername/triage-assessment-system.git
cd triage-assessment-system
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root directory and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

Replace `your_groq_api_key_here` with your actual Groq API key.

## Usage

1. Run the FastAPI application:

```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:8000`.

3. Use the provided interface to upload an audio file and view the transcription and the JSON object converted from the transcription.

## JSON Schema

The JSON schema used for converting the transcription is as follows:

```json
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
```

