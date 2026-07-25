# Security Policy

## Supported Versions

The following versions of Ashwas AI are currently supported with security updates:

| Version | Supported |
| ------- | --------- |
| 2.0.x   | Yes       |
| < 2.0   | No        |

## Reporting a Vulnerability

If you discover a potential security vulnerability in this project, please do not report it publicly via GitHub issues. Instead, report it privately to our security team.

We aim to acknowledge receipt of reports within 48 hours and provide a fix or mitigation plan within 7 days.

## Security Practices

* **No Hardcoded Secrets:** All credentials, including the `GEMINI_API_KEY`, are fetched dynamically from system environment variables.
* **Privacy-First Architecture:** Emotional check-ins and recovery metrics are stored entirely in client-side local storage to guarantee user privacy.
* **Input Validation:** All user inputs are sanitized on both client and server before passing to large language models to prevent prompt injections.
* **Crisis Safety Guardrails:** Key threat indicators (e.g. self-harm keyword match) bypass LLMs and trigger immediate emergency alerts.
