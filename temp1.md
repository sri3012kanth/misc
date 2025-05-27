Here is the same **application-level documentation** using **Confluence wiki markup format**, including collapsible sections (using `{expand}`), and tables to capture environment variables, secrets, service accounts, and notes for each app.

---

# 📘 Application Configuration Documentation (Confluence Format)

This page documents per-application configuration values across environments. It includes environment variables, secrets, service identities, and key operational notes.

---

## 🔹 **customer-service**

{expand\:title=🔧 Environment Variables}
|| Key || Value/Example || Description || Source ||
\| ENV | prod | Runtime environment | ConfigMap / App Settings |
\| DB\_URL | jdbc\:sqlserver://... | Database connection string | ConfigMap / App Settings |
\| API\_TIMEOUT | 5000 | Timeout in milliseconds | ConfigMap |
{expand}

{expand\:title=🔐 Secrets}
|| Secret Key || Usage || Source || Notes ||
\| DB\_PASSWORD | DB Authentication | Azure Key Vault | Referenced via CSI or App Settings |
\| JWT\_SECRET | Token Signing | Secret Manager | Injected as env var or volume |
{expand}

{expand\:title=🛡️ Service Account / Identity}
|| Platform || Service Account Name || Permissions ||
\| AKS | sa-customer-svc | Reader for Key Vault, DB |
\| Cloud Run | [customer-svc@project.iam.gserviceaccount.com](mailto:customer-svc@project.iam.gserviceaccount.com) | Pub/Sub, SecretManager Access |
{expand}

{expand\:title=📝 Notes}

* Ensure `JWT_SECRET` is rotated every 90 days
* Requires access to `customer-profile` topic in Pub/Sub
* Fails fast if `DB_URL` is incorrect
  {expand}

---

## 🔹 **order-service**

{expand\:title=🔧 Environment Variables}
|| Key || Value/Example || Description || Source ||
\| ENV | staging | Runtime environment | ConfigMap / YAML |
\| ORDER\_QUEUE | orders-topic | Pub/Sub topic name | App Setting |
{expand}

{expand\:title=🔐 Secrets}
|| Secret Key || Usage || Source || Notes ||
\| QUEUE\_TOKEN | Pub/Sub auth | Secret Manager | Least-privilege access |
{expand}

{expand\:title=🛡️ Service Account / Identity}
|| Platform || Service Account Name || Permissions ||
\| Cloud Run | [order-svc@project.iam.gserviceaccount.com](mailto:order-svc@project.iam.gserviceaccount.com) | Pub/Sub Publisher |
{expand}

{expand\:title=📝 Notes}

* Requires topic `orders-topic` to exist
* Use dead-letter topic config for error handling
* Rotate `QUEUE_TOKEN` every 30 days
  {expand}

---

## 🧩 Template for New App

Copy this block when adding a new application.

{expand\:title=🔧 Environment Variables}
|| Key || Value/Example || Description || Source ||
\| EXAMPLE\_KEY | value | Example description | ConfigMap/App Settings |
{expand}

{expand\:title=🔐 Secrets}
|| Secret Key || Usage || Source || Notes ||
\| SECRET\_NAME | Description | Key Vault / Secret Manager | Additional info |
{expand}

{expand\:title=🛡️ Service Account / Identity}
|| Platform || Service Account Name || Permissions ||
\| Platform Name | service-account-name | Role / access description |
{expand}

{expand\:title=📝 Notes}

* Notes about setup, dependencies, or conditions
  {expand}

---

Would you like a downloadable `.confluence` file or should I prepare this for direct pasting into your Confluence page editor?
