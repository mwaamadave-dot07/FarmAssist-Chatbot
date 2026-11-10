
import streamlit as st
import re

# PAGE SETTINGS
st.set_page_config(
    page_title="FarmAssist",
    page_icon="🌱",
    layout="centered"
)

# PAGE TITLE
st.title("🌱 FarmAssist")
st.subheader("Agricultural Advisory Chatbot")

st.write(
    "Welcome to FarmAssist! Ask questions about crops, "
    "pests, irrigation and farming practices."
)

# FARMING KNOWLEDGE DATABASE
knowledge = {
    "tomato": """
### 🍅 TOMATO GROWING ADVICE

1. Choose a sunny place for planting.
2. Prepare soil with well-rotted compost.
3. Plant healthy tomato seedlings.
4. Water regularly, especially during dry weather.
5. Avoid keeping the soil waterlogged.
6. Support plants with stakes.
7. Check leaves regularly for pests and diseases.
""",

    "maize": """
### 🌽 MAIZE GROWING ADVICE

1. Prepare the soil before planting.
2. Plant healthy maize seeds.
3. Leave enough space between plants.
4. Water when rainfall is insufficient.
5. Control weeds early.
6. Check plants regularly for pests.
""",

    "beans": """
### 🫘 BEAN GROWING ADVICE

1. Use healthy bean seeds.
2. Plant in well-drained soil.
3. Water when the soil becomes dry.
4. Remove weeds around the plants.
5. Check leaves and pods for pests.
""",

    "irrigation": """
### 💧 IRRIGATION ADVICE

1. Check soil moisture before watering.
2. Water according to the crop and weather.
3. Water near the roots where possible.
4. Water early in the morning.
5. Avoid overwatering.
""",

    "pest": """
### 🐛 PEST MANAGEMENT ADVICE

1. Inspect leaves and stems regularly.
2. Look for holes, spots and unusual damage.
3. Identify the pest before choosing a treatment.
4. Remove badly affected plant material safely.
5. Ask an agricultural extension officer for advice
   if the problem is serious.
"""
}


# FUNCTION TO IDENTIFY AND ANSWER QUESTIONS
def get_answer(message):

    # Separate questions using question marks or new lines
    questions = re.split(r'\?|\n+', message)

    answers = []
    found_topics = set()

    for question in questions:

        q = question.lower().strip()

        if not q:
            continue

        topic = None

        # Identify tomato questions
        if any(word in q for word in ["tomato", "tomatoes"]):
            topic = "tomato"

        # Identify maize questions
        elif any(word in q for word in ["maize", "corn"]):
            topic = "maize"

        # Identify bean questions
        elif any(word in q for word in ["bean", "beans"]):
            topic = "beans"

        # Identify irrigation questions
        elif any(word in q for word in
                 ["irrigation", "irrigate", "watering", "water"]):
            topic = "irrigation"

        # Identify pest questions
        elif any(word in q for word in
                 ["pest", "insect", "insects", "bugs"]):
            topic = "pest"

        # Add the answer only if the topic has not appeared before
        if topic and topic not in found_topics:

            answers.append(knowledge[topic])

            found_topics.add(topic)

    if answers:
        return "\n\n---\n\n".join(answers)

    return (
        "I do not have enough information about that question yet. "
        "Please ask about tomatoes, maize, beans, irrigation or pests."
    )


# SHOW ALL FARMING ADVICE BUTTON
if st.button("📚 Show All Farming Advice", use_container_width=True):

    for answer in knowledge.values():
        st.markdown(answer)
        st.divider()


# QUESTION BUTTONS
st.write("### Select a farming question")

col1, col2 = st.columns(2)

with col1:

    if st.button("🍅 Growing Tomatoes", use_container_width=True):
        st.session_state.selected_question = "How can I grow tomatoes?"

    if st.button("🌽 Growing Maize", use_container_width=True):
        st.session_state.selected_question = "How do I grow maize?"

    if st.button("🫘 Growing Beans", use_container_width=True):
        st.session_state.selected_question = "How do I grow beans?"

with col2:

    if st.button("💧 Irrigation Advice", use_container_width=True):
        st.session_state.selected_question = (
            "How often should I irrigate my crops?"
        )

    if st.button("🐛 Identifying Pests", use_container_width=True):
        st.session_state.selected_question = "How can I identify pests?"


# CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []


# DISPLAY PREVIOUS MESSAGES
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# RECEIVE QUESTIONS FROM FARMERS
question = st.session_state.pop("selected_question", None)

typed_question = st.chat_input(
    "Type one or more farming questions..."
)

if typed_question:
    question = typed_question


# PROCESS QUESTIONS
if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    answer = get_answer(question)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    st.rerun()
