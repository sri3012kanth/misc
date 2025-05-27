# 📘 Application Configuration Documentation

This documentation captures configuration values used by individual applications across environments. Each section details environment variables, secrets, service accounts, and operational notes.

---

## 🔹 customer-service

<details>
<summary>🔧 Environment Variables</summary>

| Key         | Value/Example              | Description               | Source                    |
|-------------|----------------------------|---------------------------|---------------------------|
| ENV         | prod                       | Runtime environment       | ConfigMap / App Settings  |
| DB_URL      | jdbc:sqlserver://...       | Database connection string| ConfigMap / App Settings  |
| API_TIMEOUT | 5000                       | Timeout in milliseconds   | ConfigMap                 |

</details>

<details>
<summary>🔐 Secrets</summary>

| Secret Key   | Usage             | Source            | Notes                                |
|--------------|------------------|-------------------|--------------------------------------|
| DB_PASSWORD  | DB Authentication| Azure Key Vault   | Referenced via CSI or App Settings   |
| JWT_SECRET   | Token Signing    | Secret Manager    | Injected as env var or volume        |

</details>

<details>
<summary>🛡️ Service Account / Identity</summary>

| Platform  | Service Account Name                              | Permissions                          |
|-----------|---------------------------------------------------|--------------------------------------|
| AKS       | sa-customer-svc                                   | Reader for Key Vault, DB             |
| Cloud Run | customer-svc@project.iam.gserviceaccount.com      | Pub/Sub, SecretManager Access        |

</details>

<details>
<summary>📝 Notes</summary>

- Ensure `JWT_SECRET` is rotated every 90 days  
- Requires access to `customer-profile` topic in Pub/Sub  
- Fails fast if `DB_URL` is incorrect  

</details>

---

## 🔹 order-service

<details>
<summary>🔧 Environment Variables</summary>

| Key          | Value/Example  | Description          | Source               |
|--------------|----------------|----------------------|----------------------|
| ENV          | staging        | Runtime environment  | ConfigMap / YAML     |
| ORDER_QUEUE  | orders-topic   | Pub/Sub topic name   | App Setting          |

</details>

<details>
<summary>🔐 Secrets</summary>

| Secret Key   | Usage         | Source         | Notes                        |
|--------------|---------------|----------------|------------------------------|
| QUEUE_TOKEN  | Pub/Sub auth  | Secret Manager | Least-privilege access       |

</details>

<details>
<summary>🛡️ Service Account / Identity</summary>

| Platform  | Service Account Name                             | Permissions           |
|-----------|--------------------------------------------------|------------------------|
| Cloud Run | order-svc@project.iam.gserviceaccount.com        | Pub/Sub Publisher      |

</details>

<details>
<summary>📝 Notes</summary>

- Requires topic `orders-topic` to exist  
- Use dead-letter topic config for error handling  
- Rotate `QUEUE_TOKEN` every 30 days  

</details>

---

## 🧩 Template for New App

<details>
<summary>🔧 Environment Variables</summary>

| Key           | Value/Example | Description         | Source                   |
|---------------|----------------|---------------------|--------------------------|
| EXAMPLE_KEY   | value          | Example description | ConfigMap / App Settings |

</details>

<details>
<summary>🔐 Secrets</summary>

| Secret Key   | Usage        | Source                    | Notes                  |
|--------------|--------------|---------------------------|------------------------|
| SECRET_NAME  | Description  | Key Vault / Secret Manager| Additional info        |

</details>

<details>
<summary>🛡️ Service Account / Identity</summary>

| Platform      | Service Account Name     | Permissions              |
|---------------|--------------------------|---------------------------|
| Platform Name | service-account-name     | Role / access description |

</details>

<details>
<summary>📝 Notes</summary>

- Notes about setup, dependencies, or conditions

</details>
