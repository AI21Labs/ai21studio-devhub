import streamlit as st
import requests


# Main function - sending a completion request to Jurassic-1 models
def generate_text_j1(input_text, temp=0, model="grande"):
    """
        Send a completion request to one of Jurassic-1 models

        Arguments:
        - input_text   : The prompt you want to feed into the model (string)
        - temp         : Temperature, any value between 0-1 (float)
        - model        : jumbo, grande or large (string; default is grande)

        Returns:
        - text         : the completion text (if the request was successful)
        - json         : full response json
    """

    if model not in ["large", "grande", "jumbo"]:
        print("model must be jumbo, grande or large!")
        return

    model_url = f"https://api.ai21.com/studio/v1/j1-{model}/complete"
    api_key = st.secrets['api-key']
    ## Send the completion request
    response = requests.post(model_url,
                             headers={"Authorization": api_key},
                             json={
                                 "prompt": input_text,
                                 "numResults": 1,
                                 "maxTokens": 200,
                                 "temperature": temp,
                                 "topKReturn": 0,
                                 "topP": 0.9,
                                 "stopSequences": ["##"]
                             }
                             )

    if response.status_code != 200:
        raise Exception(f"Completion request failed with status {response.status_code}")

    return response.json()["completions"][0]["data"]["text"]


# Generate a prompt given a role and highlights
def create_prompt(role, highlights):
    """
        Creates a prompt for a completion request to produce CV profile

        Arguments:
        - role         : what is the profession of the candidate
        - highlights   : what are the skills and ambitions of the candidate

        Returns:
        - prompt       : a full prompt, including few shot examples
    """

    few_shot_prompt = "Write a winning Business management CV profile incorporating the following features:\n1. Logical mind\n2. Problem solver\n3. 2 years of experience in management\n4. Eager to learn\n\nProfile:\nI have a clear, logical mind with a practical approach to problem-solving and a drive to see things through to completion. I have more than 2 years of experience in managing and leading teams across multiple sectors. I am eager to learn, I enjoy overcoming challenges, and I have a genuine interest in Business Management and making organisations successful.\n\n##\n\nWrite a winning  IT CV profile incorporating the following features:\n1. Experience IT professional\n2. Record designing websites, networking and managing databases\n3. Excellent interpersonal skills\n4. Looking for a challenge\n\nProfile:\nI am a highly competent IT professional with a proven track record in designing websites, networking and managing databases. I have strong technical skills as well as excellent interpersonal skills, enabling me to interact with a wide range of clients. I am eager to be challenged in order to grow and further improve my IT skills. My greatest passion is in life is using my technical know-how to benefit other people and organisations.\n\n##\n\nWrite a winning Student CV profile incorporating the following features:\n1. Hard-worker\n2. Ambitious\n3. Interested in the transport and logistics industry\n4.  Second year BA Logistics and Supply Chain Management at Aston University\n5. Communication skills\n6. Looking for a part time-position\n\nProfile:\nI am a hardworking and ambitious individual with a great passion for the transport and logistics industry. I am currently in my second year of studying BA Logistics and Supply Chain Management at Aston University. I have excellent communication skills, enabling me to effectively communicate with a wide range of people. I am seeing a part-time position in the industry in which I can put into practice my knowledge and experience, ultimately benefiting the operations of the organisation that I work for.\n\n##\n\nWrite a winning Manager CV profile incorporating the following features:\n1. Energetic\n2. Ambitious\n3. Responsible\n4. Three years experience in management\n5. Excellent in working with others\n6. Improved the performance, operations and productivity of my team by 35%.\n\nProfile:\nI am an energetic, ambitious person who has developed a mature and responsible approach to any task that I undertake, or situation that I am presented with. As a graduate with three years’ experience in management, I am excellent in working with others to achieve a certain objective on time and with excellence. In my previous role, I improved the performance, operations and productivity of my team by 35%.\n\n##\n\nWrite a winning Sales Executive CV profile incorporating the following features:\n1. Energetic and ambitious\n2. 6 years of selling experience\n3. Love working in a team\n4. Independent \n5. MBA from the Hebrew University in Jerusalem\n\nProfile:\nI am an energetic and ambitious person who has developed a mature and responsible approach to any task that I undertake, or situation that I am presented with. I am sales executive with 6 years of experience in selling and negotiating. I am independent, love working in a team, and I am looking for a challenging position where I can use my skills and knowledge to benefit the company\n\n##\n\n"
    current_input = f"Write a winning {role} incorporating the following features:\n"
    skills_str = ""
    for i in range(len(highlights)):
        if highlights[i]:
            skills_str += f"{i + 1:d}. {highlights[i]}\n"
    return few_shot_prompt + current_input + skills_str + "\nProfile:"


st.title("CV Profile Generator")
st.header("Using AI21 Studio")
st.subheader("Enter a role and up to 4 skills:")

MAX_HIGHLIGHTS = 4

role = st.text_input("Role", value="Software Engineer", max_chars=30)
highlights = [
    st.text_input(f"Highlight #{n + 1:d} (experience / skill / ambition / etc.)", max_chars=60)
    for n in range(MAX_HIGHLIGHTS)
]

input_text = create_prompt(role, highlights)

if st.button(label="Generate"):
    st.write(generate_text_j1(input_text=input_text, temp=0.5, model="jumbo"))
