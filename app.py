import streamlit as st
import pandas as pd
import pickle
import base64


# ---------------- Page Settings ----------------

st.set_page_config(
    page_title="GradeVision AI",
    page_icon="🤖",
    layout="wide"
)



# ---------------- Background Image ----------------

def get_base64(file):

    with open(file, "rb") as image:

        return base64.b64encode(
            image.read()
        ).decode()



background = get_base64("ai_background.jpg")



# ---------------- Modern AI CSS ----------------


st.markdown(f"""

<style>


.stApp {{

    background-image:

    linear-gradient(
        rgba(5,10,25,0.78),
        rgba(5,10,25,0.78)
    ),

    url("data:image/jpg;base64,{background}");

    background-size:cover;

    background-position:center;

    background-attachment:fixed;

}}



h1 {{

    text-align:center;

    color:#00e5ff;

}}



h2,h3 {{

    color:#8be9fd;

}}



.card {{

    background:rgba(255,255,255,0.035);

    padding:25px;

    border-radius:20px;

    border:1px solid rgba(255,255,255,0.12);

    backdrop-filter:blur(8px);

    -webkit-backdrop-filter:blur(8px);

    box-shadow:
    0 8px 32px rgba(0,0,0,0.25);

    margin-bottom:20px;

}}



.stButton button {{

    width:100%;

    height:55px;

    border-radius:15px;

    background:

    linear-gradient(
        90deg,
        #0066ff,
        #00e5ff
    );

    color:white;

    font-size:20px;

    font-weight:bold;

}}


div[data-testid="stMetric"] {{

    background:rgba(255,255,255,0.04);

    border-radius:20px;

    padding:20px;

    border:1px solid rgba(255,255,255,0.10);

    backdrop-filter:blur(10px);

    -webkit-backdrop-filter:blur(10px);

}}



</style>

""",
unsafe_allow_html=True)



# ---------------- Header ----------------


st.markdown("""

<div class="card">

<h1>🤖 GradeVision AI</h1>

<center>

Machine Learning Student Score Prediction

<br>

Powered by Random Forest Algorithm

</center>

</div>

""",
unsafe_allow_html=True)




# ---------------- Load Model ----------------


with open(
    "student_score_model.pkl",
    "rb"
) as file:

    model = pickle.load(file)



with open(
    "columns.pkl",
    "rb"
) as file:

    columns = pickle.load(file)




# ---------------- Student Information ----------------


st.markdown("""

<div class="card">

<h3>👤 Student Information</h3>

</div>

""",
unsafe_allow_html=True)



col1,col2,col3 = st.columns(3)



with col1:

    school = st.selectbox(
        "🏫 School",
        ["GP","MS"]
    )


    age = st.number_input(
        "🎂 Age",
        15,
        22,
        17
    )



with col2:

    sex = st.selectbox(
        "👤 Gender",
        ["M","F"]
    )


    address = st.selectbox(
        "🌍 Address",
        ["U","R"]
    )



with col3:

    higher = st.selectbox(
        "🎓 Higher Education?",
        ["yes","no"]
    )


    internet = st.selectbox(
        "🌐 Internet Access",
        ["yes","no"]
    )




# ---------------- Academic Information ----------------


st.markdown("""

<div class="card">

<h3>📚 Academic Information</h3>

</div>

""",
unsafe_allow_html=True)



col1,col2,col3 = st.columns(3)



with col1:

    studytime = st.number_input(
        "⏰ Study Time",
        1,
        4,
        2
    )



with col2:

    failures = st.number_input(
        "❌ Previous Failures",
        0,
        4,
        0
    )



with col3:

    absences = st.number_input(
        "📅 Absences",
        0,
        100,
        0
    )





# ---------------- Previous Grades ----------------


st.markdown("""

<div class="card">

<h3>📊 Previous Grades</h3>

</div>

""",
unsafe_allow_html=True)



col1,col2 = st.columns(2)



with col1:

    G1 = st.number_input(
        "First Period Grade (G1)",
        0,
        20,
        10
    )



with col2:

    G2 = st.number_input(
        "Second Period Grade (G2)",
        0,
        20,
        10
    )




# ---------------- Prediction ----------------


if st.button("🚀 Run AI Prediction"):


    input_data = pd.DataFrame(

        0,

        index=[0],

        columns=columns

    )



    values = {

        "age":age,

        "studytime":studytime,

        "failures":failures,

        "absences":absences,

        "G1":G1,

        "G2":G2

    }



    for key,value in values.items():

        if key in input_data.columns:

            input_data[key] = value




    choices = {

        f"school_{school}":1,

        f"sex_{sex}":1,

        f"address_{address}":1,

        f"higher_{higher}":1,

        f"internet_{internet}":1

    }



    for key,value in choices.items():

        if key in input_data.columns:

            input_data[key] = value





    prediction = model.predict(input_data)[0]




    if prediction >= 18:

        status = "🌟 Excellent Student"


    elif prediction >= 15:

        status = "🔥 Good Performance"


    elif prediction >= 10:

        status = "📚 Needs Improvement"


    else:

        status = "⚠️ Low Performance"




    st.markdown("---")



    st.metric(

        "🎓 AI Predicted Final Score",

        f"{prediction:.2f} / 20"

    )


    st.success(status)