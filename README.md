# Healthcare & Insurance Document Assistant

A Streamlit retrieval-augmented generation (RAG) starter for searching approved healthcare and insurance documents. It stores original uploads in Azure Blob Storage, indexes text chunks in Azure AI Search, creates embeddings with Azure OpenAI, and answers questions with citations.

> **Safety and privacy:** This is a document-search demo, not a medical device or source of medical advice. It does not provide diagnosis or treatment. Do not upload protected health information (PHI) unless your organization has approved the Azure services, contracts, access controls, retention, and deployment for that use. The project does not itself establish HIPAA compliance. Use synthetic or public sample documents for demos.

This starter has no user authentication, role-based access, or per-user/tenant index isolation. Do not expose it to sensitive documents or users without adding and validating your organization's identity and authorization controls.

## Architecture

1. Upload a PDF, TXT, or Markdown file in the Streamlit sidebar.
2. The app extracts text, splits it into overlapping chunks, stores the original in Blob Storage, and indexes chunks in Azure AI Search.
3. Questions retrieve up to four relevant chunks. Azure OpenAI generates an answer constrained to those excerpts, with source labels.

The Azure AI Search index is created by the LangChain Azure Search integration on first use. Configure the embedding deployment and search service before indexing documents.

## Requirements

- Python 3.11+
- Azure OpenAI resource with chat and embedding model deployments
- Azure AI Search service
- Azure Storage account with permission to create/use a blob container

## Run locally

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` with your Azure resource endpoints, keys, deployment names, API version, and container. Keep `.env` private; it is excluded from Git. Then start the app:

```powershell
streamlit run app.py
```

On macOS/Linux, activate the environment with `source .venv/bin/activate`.

## Push to GitHub

Create an empty repository on GitHub, then run these commands from this project directory:

```powershell
git init
git add .
git commit -m "Build healthcare document assistant"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repository>.git
git push -u origin main
```

GitHub stores the source code; it does not run this Streamlit app by itself. The included GitHub Actions workflow runs tests on pushes and pull requests.

## Deploy the demo

For a demo with synthetic/public documents, push the repository and create an app from it in [Streamlit Community Cloud](https://share.streamlit.io/). Add each variable from `.env.example` under the app's **Secrets** settings (TOML format, for example `AZURE_OPENAI_ENDPOINT = "https://..."`) before launch. Never commit `.env` or paste secrets into source files.

For organizational or PHI workflows, deploy within an organization-approved Azure environment instead. Review identity-based access, network restrictions, encryption, audit logging, retention, and applicable contractual requirements before use. Do not use the public demo deployment for PHI.

## Notes

- The first upload creates the configured Azure AI Search index. Choose a unique index name for this app.
- The default upload size limit is 20 MB. Supported file types are PDF, TXT, and Markdown; scanned PDFs without extractable text are not OCR-processed.
- Answers can be incomplete or outdated. Verify care and coverage decisions with qualified professionals and the insurer.
- Azure credentials are loaded from environment variables; errors are displayed in the app and logged to the server output.
