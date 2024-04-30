from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

@app.route('/myapi', methods=['POST'])
def my_api_endpoint():
    data = request.json
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent?key="
    question = data.get("question")
    OutOf = data.get("OutOf")
    expected_answer = data.get("CorrectAnswer")
    batch_student_answers = data.get("batch_student_answers")
    batch_student_ids = data.get("batch_student_ids")

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
        "response_mime_type": "application/json"}}


    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)

    try:
        generated_data = json.loads(response.text)
    except json.JSONDecodeError as e:
        return jsonify({"error": "Failed to decode JSON.", "details": str(e)})
    except KeyError as e:
        return jsonify({"error": "Key error in processing response data.", "details": str(e)})

    if 'error' in generated_data:
        return jsonify({"error": "API error response.", "details": generated_data['error']})

    # Assuming the API returns the expected format directly
    return jsonify(generated_data)
