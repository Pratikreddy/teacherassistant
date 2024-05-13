import streamlit as st
import requests
import json
import numpy as np

api_url = "http://pratikreddy.pythonanywhere.com/ta"

def send_data(input_data):
    try:
        data = json.loads(input_data)
    except json.JSONDecodeError:
        st.error("Invalid JSON input")
        return

    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        candidate_content = response_data['candidates'][0]['content']['parts'][0]['text']
        
        try:
            candidate_json = json.loads(candidate_content)
            grades = candidate_json['grades']
            ai_scores = {id_: float(score['score']) for id_, score in grades.items()}
            ai_average = np.mean(list(ai_scores.values()))

            st.write("AI Grades:", ai_scores)
            st.write(f"AI Average Score: {ai_average}")

        except json.JSONDecodeError as e:
            st.error(f"Failed to decode JSON from response: {e}")
    else:
        st.error(f"Request failed with status code {response.status_code}")

def main():
    st.title("Teachers Assistant")
    st.write("Enter the data in JSON format")

    input_data = st.text_area("Input Data")

    if st.button("Send Data"):
        send_data(input_data)

if __name__ == '__main__':
    main()
