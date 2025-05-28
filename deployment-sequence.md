
# 📦 Deployment Sequence – Production Environment

This document outlines the production deployment sequence of modules across various platforms to ensure dependency alignment and avoid downtime.

---

## 🚀 Overall Deployment Strategy

- Ensure all pipelines pass QA/UAT.
- Validate external service dependencies.
- Pause external triggers (if applicable).
- Deploy in defined order to maintain service integrity.

---

## 🧭 Deployment Order

| Step | Module Name         | Platform              | Description                                 | Notes                                |
|------|---------------------|------------------------|---------------------------------------------|--------------------------------------|
| 1    | common-config       | Shared                 | Deploy shared config maps and secrets       | Used by all services                 |
| 2    | auth-service        | AKS                    | Authentication backend (Java)               | Ensure Key Vault access works        |
| 3    | customer-service    | GKE                    | Customer profile service                    | Depends on auth-service              |
| 4    | billing-service     | GKE                    | Handles invoicing and payment processing    | Requires customer-service to be up   |
| 5    | event-processor-fn  | Azure Functions        | Processes domain events                     | Triggered by Azure Event Grid        |
| 6    | notifier            | Google Cloud Run       | Sends notifications (email/SMS)             | Consumes Pub/Sub events              |
| 7    | reporting-fn        | Google Cloud Function  | Generates daily reports                     | Scheduled function                   |
| 8    | order-service       | AKS                    | Manages order workflows                     | Depends on billing-service           |
| 9    | api-gateway         | Google Cloud Run       | External API entrypoint                     | Should be last for traffic control   |

---

## ⚙️ Platform-Specific Notes

### 🌀 AKS Deployment Notes

- Use Helm charts for version consistency.
- Validate Key Vault integration for secrets.
- Use readiness probes to avoid traffic on cold starts.

### 🟦 Azure Functions Deployment Notes

- Use slots if available (`staging` → `production` swap).
- Rotate keys post-deploy if secrets are updated.
- Monitor with Application Insights.

### 🟩 GKE Deployment Notes

- Use rolling updates to avoid downtime.
- Validate sidecar containers (e.g., Istio, logging).
- Ensure GCR/GAR access for pulling images.

### 🟨 Google Cloud Run Deployment Notes

- Set concurrency limits to avoid overload.
- Configure IAM for service-to-service auth.
- Ensure Pub/Sub trigger permissions are in place.

---

## ✅ Post-Deployment Checklist

- [ ] Verify service health across all modules.
- [ ] Re-enable external triggers or schedulers.
- [ ] Rotate secrets if changes were made.
- [ ] Tag the deployment version in Git (or artifact repository).
- [ ] Communicate deployment completion to stakeholders.
