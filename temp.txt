h1. 🔁 Platform Configuration Mapping

----

h2. 🔧 General Mapping Table

|| Config Type || AKS || Azure Functions || Cloud Run || GKE ||
| Environment Variables | ConfigMap / Helm | App Settings | gcloud CLI / YAML | ConfigMap / Helm |
| Secrets | Azure Key Vault + CSI Driver | Azure Key Vault via App Settings | Google Secret Manager | GCP Secret Manager / Kubernetes Secrets |
| Trigger Mechanism | K8s Eventing / Custom Controller | HTTP / Timer / Event Grid | Pub/Sub / Eventarc | Pub/Sub / Cloud Run |
| Identity & Access | Pod Identity / Workload Identity | Managed Identity | Service Account | Workload Identity |

----

h2. 🟦 Azure AKS

{expand:title=🔧 Environment Variables}
|| Source || Use || Tool ||
| ConfigMap | Non-sensitive config | kubectl / Helm |
| Secret | Sensitive values | K8s Secret / CSI driver |
{expand}

{expand:title=🔐 Secrets}
* Use *Azure Key Vault* to store sensitive information  
* Integrate via *Secrets Store CSI Driver*  
* Access using *Pod Identity* or *Workload Identity*  
{expand}

{expand:title=🛡️ Service Accounts & IAM}
* Map Kubernetes ServiceAccounts to Azure AD  
* Use RBAC for vault, storage, etc.  
* Grant least privilege to resources via RBAC roles  
{expand}

----

h2. ⚡ Azure Functions

{expand:title=🔧 Environment Variables}
|| Setting || Value || Source ||
| DB_URL | jdbc:sqlserver://... | App Settings |
| SECRET_KEY | @Microsoft.KeyVault(...) | Key Vault Reference |
{expand}

{expand:title=🔐 Secrets}
* Secrets stored in *Azure Key Vault*  
* Use *Key Vault Reference Syntax* inside App Settings  
* Authenticate using *System/User-assigned Managed Identity*  
{expand}

{expand:title=🛡️ Service Identity}
* Use *Managed Identity* to access Key Vault, Storage, etc.  
* Permissions assigned at resource or group level  
{expand}

----

h2. ☁️ Google Cloud Run (Pub/Sub Trigger)

{expand:title=🔧 Environment Variables}
|| Name || Value || Set Method ||
| ENV | prod | gcloud run deploy --set-env-vars |
| SECRET_KEY | Pulled from Secret Manager | Env or Volume |
{expand}

{expand:title=🔐 Secrets}
* Use *Google Secret Manager*  
* Inject secrets as env variables or mounted volume  
* Grant roles/secretmanager.secretAccessor to service account  
{expand}

{expand:title=📩 Pub/Sub Trigger}
* Trigger via *Eventarc* or direct *Pub/Sub subscription*  
* Grant required permissions: pubsub.subscriber, run.invoker  
{expand}

{expand:title=🛡️ Service Accounts}
* Each Cloud Run service uses its own *GCP Service Account*  
* Authenticate with Pub/Sub, Secret Manager, Cloud Logging, etc.  
{expand}

----

h2. 🐳 Google Kubernetes Engine (GKE)

{expand:title=🔧 Environment Variables}
|| Source || Use ||
| ConfigMap | Non-sensitive values (BASE_URL, ENV) |
| Secret | Sensitive data (passwords, API keys) |
{expand}

{expand:title=🔐 Secrets}
* Use *Kubernetes Secrets* or *Google Secret Manager*  
* Recommended: Use *Workload Identity* to access GCP secrets securely  
* Optionally sync with controller for auto updates  
{expand}

{expand:title=🛡️ Service Accounts & IAM}
* Use *Workload Identity* to link K8s SA ↔ GCP SA  
* GCP IAM grants access to Cloud APIs  
* K8s RBAC for namespace-level restrictions  
{expand}

----

h2. 🔐 Security & Identity Matrix

|| Platform || Identity Mechanism || Secret Storage || Least Privilege Strategy ||
| AKS | Pod Identity / Workload Identity | Azure Key Vault | Use AD roles with minimal access |
| Azure Functions | Managed Identity | Azure Key Vault | Resource-level RBAC |
| Cloud Run | GCP Service Account | Secret Manager | Per-service IAM roles |
| GKE | Workload Identity | Secret Manager / K8s Secret | GCP IAM + K8s RBAC |
