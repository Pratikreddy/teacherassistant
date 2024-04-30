import streamlit as st
import requests
import json

# Streamlit widgets to get user input
question = st.text_input("Question")
OutOf = st.text_input("Out of")
expected_answer = st.text_input("Correct Answer")
batch_student_answers = st.text_area("Batch Student Answers (JSON format)")
batch_student_ids = st.text_area("Batch Student IDs (JSON format)")

if st.button('Submit'):
    try:
        batch_student_answers = json.loads(batch_student_answers)
        batch_student_ids = json.loads(batch_student_ids)
    except json.JSONDecodeError as e:
        st.error(f"Error decoding JSON: {str(e)}")
        st.stop()

    expected_format = {
        "grades": {id_: {"score": "int"} for id_ in batch_student_ids}
    }

    system_instructions = f"""you are a teacher who needs to grade student answers relative to the CorrectAnswer out of {OutOf} given by the teacher. Please focus only on the score out of the total points possible.
    question = {question}
    OutOf = {OutOf}
    expected = {expected_answer}
    student answers = {json.dumps(batch_student_answers)}
    expected format = {json.dumps(expected_format)}
    please adhere to the expected json format with great attention. please Be a little lenient in awarding .5 marks for attempting the topics or using the correct keywords. Display a little leniency in giving marks.
    """

    payload = {
    "contents": [
        {
            "parts": [
                {"text": system_instructions},
                {"text": json.dumps(expected_format)},
                {"text": "strict rules : Kindly follow keys and ID's very efficiently as they are non changeable entities, Always output only json object and no other trailing or leading characters."}
            ]
        }
    ],
    "generationConfig": {
        "response_mime_type": "application/json"}
    }

    headers = {"Content-Type": "application/json"}
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key=AIzaSyC8tc7m4TkAmfOx9cu_bckCc62ZgVDzSBQ"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        try:
            generated_data = json.loads(response.text)
            st.json(generated_data)
        except json.JSONDecodeError as e:
            st.error(f"Failed to decode JSON: {str(e)}")
        except KeyError as e:
            st.error(f"Key error in processing response data: {str(e)}")
    else:
        st.error(f"Failed to contact API: {response.status_code}")
