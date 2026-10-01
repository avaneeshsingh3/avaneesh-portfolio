# Avaneesh Singh Portfolio

A professional personal portfolio for Avaneesh Singh, built with Python and Streamlit. It presents technical skills, projects, education, certifications, continuous learning, innovation work, a resume, and contact details in a responsive single-page experience.

## Built with

- Python
- Streamlit
- HTML
- CSS

## Features

- Modern responsive dark design
- About and technical skills
- IntelliAir Pro featured project with live demo
- Additional projects, education, certifications, and continuous learning
- Innovation and technical work
- Resume preview and download when `assets/resume.pdf` is present
- Contact form with safe, explicit delivery status

## Local installation

```bash
git clone <repository-url>
cd portfolio
pip install -r requirements.txt
streamlit run app.py
```

## Configure your details

Edit the configuration block at the top of `app.py` before deploying:

- `GITHUB_URL`
- `EMAIL`
- `INTELLAIR_GITHUB_URL`
- `CERTIFICATE_URLS`

The IntelliAir Pro live-demo URL is already configured. No API keys, credentials, or private tokens are included in this project.

## Assets

These optional files are already supported and safely fall back when absent:

```text
assets/profile.jpg
assets/resume.pdf
images/intelliair-pro.png
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and push this `portfolio` project to it. Do not commit secrets or `.streamlit/secrets.toml`.
2. Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
3. Select **Create app**, choose the repository, branch, and `app.py` as the entry point.
4. Click **Deploy**. Streamlit installs packages from `requirements.txt` automatically.
5. Add public assets to the repository. Store any future secret values in the Community Cloud Secrets settings rather than in the code.

## Run command

```bash
streamlit run app.py
```
