# Cover Letter Agent

## Agent a Day Challenge - Agent #2

This project is part of the "Agent a Day Challenge," a personal challenge to build one new AI agent every day. This is Agent #2: a specialized agent for writing high-quality cover letters.

## Overview

The Cover Letter Agent helps users generate tailored cover letters by analyzing their resume and the specific job description. Instead of a simple one-shot generation, this tool uses a multi-step process to ensure the output is professional, specific, and impactful.


## Live Demo
[Try the Live Agent](https://cover-letter-agent-j5eh8ubaso3butzmbqqzx7.streamlit.app/)

## Architecture: Reflexion

This agent is built using the **Reflexion Architecture**. This is a pattern where the AI recursively critiques and improves its own output. The workflow consists of three distinct steps:

1.  **Generate Draft**: The agent writes an initial cover letter based on the provided resume and job description.
2.  **Self-Critique**: The agent acts as a strict reviewer, analyzing the draft for general phrasing, lack of detail, or tone issues.
3.  **Refine & Polish**: The agent rewrites the letter, incorporating the feedback from the critique phase to produce a superior final version.

This iterative process mimics human drafting and editing, resulting in significantly better quality than a standard prompt.

## Features

-   **PDF Resume Support**: Upload your resume directly as a PDF.
-   **Text Input**: Option to paste resume text manually.
-   **Transparent Reasoning**: View the initial draft and the AI's self-critique to understand the improvements.
-   **One-Click Copy**: Easily copy the final formatted cover letter.

## Installation

1.  Clone the repository.
2.  Create a virtual environment.
3.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Create a `.env` file and add your Groq API key:
    ```
    GROQ_API_KEY=your_api_key_here
    ```

## Usage

Run the Streamlit application:

```bash
streamlit run main.py
```

## Technologies

-   **LangGraph**: For orchestrating the stateful multi-step workflow.
-   **LangChain**: For LLM interactions.
-   **Streamlit**: For the user interface.
-   **Groq API**: Powered by Llama 3.3 70b for fast and high-quality inference.
