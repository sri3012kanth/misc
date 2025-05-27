Sure! Here's the documentation regenerated in **Markdown (.md) format**, with tables and collapsible sections using standard Markdown syntax and details inside collapsible blocks using HTML `<details>` tags for expand/collapse behavior (commonly supported on GitHub, GitLab, and many markdown viewers).

```markdown
# 🔁 Platform Configuration Mapping

---

## 🔧 General Mapping Table

| Config Type          | AKS                          | Azure Functions                  | Cloud Run                    | GKE                              |
|----------------------|------------------------------|---------------------------------|------------------------------|---------------------------------|
| Environment Variables | ConfigMap / Helm             | App Settings                   | `gcloud` CLI / YAML           | ConfigMap / Helm                |
| Secrets              | Azure Key Vault + CSI Driver | Azure Key Vault via App Settings| Google Secret Manager         | GCP Secret Manager / K8s Secrets |
| Trigger Mechanism     | K8s Eventing / Custom Controller | HTTP / Timer / Event Grid      | Pub/Sub / Eventarc            | Pub/Sub / Cloud Run              |
| Identity & Access     | Pod Identity / Workload Identity | Managed Identity              | Service Account               | Workload Identity               |

---

## 🟦 Azure AKS

<details>
<summary>Environment Variables</summary>

| Source    | Use                 | Tool            |
|-----------|---------------------|-----------------|
| ConfigMap | Non-sensitive config| kubectl / Helm  |
| Secret    | Sensitive values    | K8s Secret / CSI driver |

</details>

<details>
<summary>Secrets</summary>

- Use **Azure Key Vault** to store sensitive information  
- Integrate via **Secrets Store CSI Driver**  
- Access using **Pod Identity** or **Workload Identity**

</details>

<details>
<summary>Service Accounts & IAM</summary>

- Map Kubernetes ServiceAccounts to Azure AD  
- Use RBAC for vault, storage, etc.  
- Grant least privilege to resources via RBAC roles

</details>

---

## ⚡ Azure Functions

<details>
<summary>Environment Variables</summary>

| Setting     | Value                      | Source         |
|-------------|----------------------------|----------------|
| DB_URL      | `jdbc:sqlserver://...`     | App Settings   |
| SECRET_KEY  | `@Microsoft.KeyVault(...)` | Key Vault Reference |

</details>

<details>
<summary>Secrets</summary>

- Secrets stored in **Azure Key Vault**  
- Use **Key Vault Reference Syntax** inside App Settings  
- Authenticate using **System/User-assigned Managed Identity**

</details>

<details>
<summary>Service Identity</summary>

- Use **Managed Identity** to access Key Vault, Storage, etc.  
- Permissions assigned at resource or group level

</details>

---

## ☁️ Google Cloud Run (Pub/Sub Trigger)

<details>
<summary>Environment Variables</summary>

| Name       | Value                  | Set Method                    |
|------------|------------------------|-------------------------------|
| ENV        | prod                   | `gcloud run deploy --set-env-vars` |
| SECRET_KEY | Pulled from Secret Manager | Env or Volume              |

</details>

<details>
<summary>Secrets</summary>

- Use **Google Secret Manager**  
- Inject secrets as env variables or mounted volume  
- Grant `roles/secretmanager.secretAccessor` to service account

</details>

<details>
<summary>Pub/Sub Trigger</summary>

- Trigger via **Eventarc** or direct **Pub/Sub subscription**  
- Grant required permissions: `pubsub.subscriber`, `run.invoker`

</details>

<details>
<summary>Service Accounts</summary>

- Each Cloud Run service uses its own **GCP Service Account**  
- Authenticate with Pub/Sub, Secret Manager, Cloud Logging, etc.

</details>

---

## 🐳 GKE (Google Kubernetes Engine)

<details>
<summary>Environment Variables</summary>

| Source     | Use                         |
|------------|-----------------------------|
| ConfigMap  | Non-sensitive values (BASE_URL, ENV) |
| Secret     | Sensitive data (passwords, API keys) |

</details>

<details>
<summary>Secrets</summary>

- Use **Kubernetes Secrets** or **Google Secret Manager**  
- Recommended: Use **Workload Identity** to access GCP secrets securely  
- Optionally sync with controller for auto updates

</details>

<details>
<summary>Service Accounts & IAM</summary>

- Use **Workload Identity** to link K8s SA ↔ GCP SA  
- GCP IAM grants access to Cloud APIs  
- K8s RBAC for namespace-level restrictions

</details>

---

## 🔐 Security & Identity Matrix

| Platform        | Identity Mechanism           | Secret Storage                  | Least Privilege Strategy          |
|-----------------|-----------------------------|--------------------------------|----------------------------------|
| AKS             | Pod Identity / Workload Identity | Azure Key Vault             | Use AD roles with minimal access |
| Azure Functions | Managed Identity             | Azure Key Vault                | Resource-level RBAC              |
| Cloud Run       | GCP Service Account          | Secret Manager                 | Per-service IAM roles            |
| GKE             | Workload Identity            | Secret Manager / K8s Secret    | GCP IAM + K8s RBAC               |

---

**Notes:**  
- Use tables for clear comparisons  
- Use collapsible `<details>` blocks to keep the page clean and easy to navigate  
- This Markdown format works well in many Markdown renderers (GitHub, GitLab, VSCode preview, etc.)

---

If you want, I can also provide a `.md` file you can download and import to your repo or wiki. Let me know!
```
