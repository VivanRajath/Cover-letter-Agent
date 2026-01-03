import streamlit as st
import os
from dotenv import load_dotenv
from typing import TypedDict

from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from pypdf import PdfReader


load_dotenv()


llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.4
)

DRAFT_PROMPT = """
You are a professional career assistant.

Using the resume and job description below, write a clear, concise, and role-specific cover letter.
Avoid generic statements. Keep a professional tone.

Resume:
{resume}

Job Description:
{job_description}
"""

CRITIQUE_PROMPT = """
You are reviewing a draft cover letter.

Critique it based on:
1. Alignment with the job description
2. Use of resume-specific details
3. Generic or weak phrasing
4. Tone and clarity

Return a short critique only.

Draft:
{draft}
"""

REVISION_PROMPT = """
Rewrite the cover letter using the critique below.
Make it more specific, impactful, and well-aligned with the job description.

Draft:
{draft}

Critique:
{critique}
"""


class CoverLetterState(TypedDict):
    resume: str
    job_description: str
    draft: str
    critique: str
    final_letter: str


def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def generate_draft(state: CoverLetterState):
    prompt = DRAFT_PROMPT.format(
        resume=state["resume"],
        job_description=state["job_description"]
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"draft": response.content}

def self_critique(state: CoverLetterState):
    prompt = CRITIQUE_PROMPT.format(draft=state["draft"])
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"critique": response.content}

def revise_letter(state: CoverLetterState):
    prompt = REVISION_PROMPT.format(
        draft=state["draft"],
        critique=state["critique"]
    )
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_letter": response.content}


graph = StateGraph(CoverLetterState)

graph.add_node("generate_draft", generate_draft)
graph.add_node("self_critique", self_critique)
graph.add_node("revise_letter", revise_letter)

graph.set_entry_point("generate_draft")
graph.add_edge("generate_draft", "self_critique")
graph.add_edge("self_critique", "revise_letter")
graph.add_edge("revise_letter", END)

app = graph.compile()


st.set_page_config(page_title="Cover Letter Agent", layout="wide")

st.title("Cover Letter Agent")
st.caption("Reflexion architecture · Generate → Critique → Improve")

st.subheader("Resume Input")

resume_file = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

resume_text = st.text_area(
    "Or paste your resume text",
    height=250
)

st.subheader(" Job Description")
job_description = st.text_area(
    "Paste the Job Description",
    height=250
)

if st.button("Generate Cover Letter"):
    if resume_file:
        final_resume = extract_text_from_pdf(resume_file)
    elif resume_text.strip():
        final_resume = resume_text.strip()
    else:
        st.warning("Please upload a resume PDF or paste resume text.")
        st.stop()

    if not job_description.strip():
        st.warning("Please provide the job description.")
        st.stop()

    with st.spinner("Thinking → Reflecting → Improving..."):
        result = app.invoke({
            "resume": final_resume,
            "job_description": job_description.strip()
        })

    with st.expander("Step 1: Initial Draft"):
        st.write(result["draft"])

    with st.expander("Step 2: Critique"):
        st.write(result["critique"])

    st.subheader(" Final Cover Letter")
    st.code(result["final_letter"], language='markdown')
