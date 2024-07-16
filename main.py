

import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
my_key = ""
MODEL = "gpt-4o"
client = OpenAI(api_key=my_key)

# Define categories and topics
categories = {
    "Theme Development": ["Introduction to Liquid", "Theme Structure", "Using Polaris"],
    "Back-End Development": ["Shopify APIs", "Authentication", "Webhook Handling"],
    "Database with Prisma": ["Introduction to Prisma", "Connecting to Database", "Prisma CRUD Operations"],
    "REST API": ["Introduction to REST", "Creating REST Endpoints", "Consuming REST APIs"]
}

def provide_theory_and_code(category, topic):
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"You are a Shopify development teacher. Teach the topic {topic} in {category} with theory and code."}
        ]
    )
    return completion.choices[0].message.content

def handle_user_questions():
    st.write("Ask your questions below. Type 'done' if the topic is clear.")
    user_input = st.text_input("Your question:")
    if user_input and user_input.lower() != 'done':
        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        st.write("AI Response: " + completion.choices[0].message.content)

def give_task_and_check_answer(category, topic):
    task_prompt = f"Please provide 5 tasks related to {topic} in {category}. No answers, just give me the tasks."
    completion_task = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": task_prompt}
        ]
    )
    tasks = completion_task.choices[0].message.content.split('\n')
    
    task_selected = st.selectbox("Select a task:", tasks)
    
    user_answer = st.text_area("Paste your answer here:")
    if st.button("Submit Answer"):
        if user_answer:
            feedback_prompt = f"Check the following answer for the task: '{task_selected}' and provide feedback.\nAnswer:\n{user_answer}"
            completion_feedback = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": feedback_prompt}
                ]
            )
            # Update the feedback directly in the UI
            st.write("AI Feedback:")
            st.write(completion_feedback.choices[0].message.content)

# Main app layout
st.title("AI Shopify Development Teacher")

# Display options
options = ["Teach Me", "Ask Questions", "Give Tasks"]
choice = st.sidebar.selectbox("Choose an option", options)

if choice == "Teach Me":
    st.subheader("Teach Me")
    category = st.selectbox("Select a category:", list(categories.keys()))
    topic = st.selectbox(f"Select a topic in {category}:", categories[category])
    if st.button("Teach Me"):
        explanation = provide_theory_and_code(category, topic)
        st.write(explanation)

elif choice == "Ask Questions":
    st.subheader("Ask Questions")
    handle_user_questions()

elif choice == "Give Tasks":
    st.subheader("Give Tasks")
    category = st.selectbox("Select a category:", list(categories.keys()))
    topic = st.selectbox(f"Select a topic in {category}:", categories[category])
    if st.button("Generate Tasks"):
        task_prompt = f"Please provide 5 tasks related to {topic} in {category}. No answers, just give me the tasks."
        completion_task = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": task_prompt}
            ]
        )
        tasks = completion_task.choices[0].message.content.split('\n')
        task_selected = st.selectbox("Select a task:", tasks)
        
        user_answer = st.text_area("Paste your answer here:")
        if st.button("Submit Answer"):
            if user_answer:
                feedback_prompt = f"Check the following answer for the task: '{task_selected}' and provide feedback.\nAnswer:\n{user_answer}"
                completion_feedback = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": feedback_prompt}
                    ]
                )
                # Update the feedback directly in the UI
                st.write("AI Feedback:")
                st.write(completion_feedback.choices[0].message.content)
