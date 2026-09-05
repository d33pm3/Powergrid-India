# Security Policy

## Supported versions

Report issues against the `main` branch of this public repository.

## What this repository must never contain

- `.env` files, API keys, access tokens, SSH keys, private certificates, OAuth credentials
- Customer or client names, records, screenshots, exports, audit findings, or internal reports
- Internal URLs, IP addresses, hostnames, or service-account names
- Private prompts, RAG source documents, vector-store exports, embeddings, or internal agent instructions

If you find any of the above in a commit, open a public issue **without pasting the secret** and rotate the credential immediately.

## Reporting a vulnerability

Open a GitHub issue titled `security:` with a description of the class of issue (do not include live secrets). For credential leaks, rotate first, then report.

## Runtime data

Workbook builds and CSV checkpoints belong in `outputs/` (gitignored). Do not commit generated `.xlsx` files.
