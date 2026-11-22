# AI CareerCompass — Streamlit deployment

## Deploy on Streamlit Community Cloud
1. Push this folder to a GitHub repository.
2. Sign in to https://share.streamlit.io using GitHub.
3. Choose **Create app**, select the repository and branch.
4. Set the main file path to `streamlit_app.py`.
5. Deploy. Streamlit will install packages from `requirements.txt`.

## Run locally
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Current implementation and limitations
The prototype currently uses an explainable keyword-overlap baseline. The master prompt is included as a prompt-design specification, but no live LLM API is connected yet. Do not describe the score as an AI/hiring decision. PDF and TXT resume uploads are supported. Avoid uploading sensitive personal information.
