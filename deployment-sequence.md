# 📦 Project Dependencies & Pre-Requisites

This document outlines the key dependencies and required services for successful deployment of the application stack across environments (AKS, GKE, Azure Functions, Google Cloud Run).

---

## 🧱 Prerequisite Summary Table

| Dependency Type   | Name / Resource                     | Applies To       | Owner / Team     | Notes                                              |
|-------------------|--------------------------------------|------------------|------------------|----------------------------------------------------|
| 🔐 Secret Store    | Azure Key Vault: `my-app-kv`         | All Envs         | Security Team    | Must exist before app deployment                   |
| 🪪 Identity         | Managed Identity: `app-mi`           | Prod / Staging   | IAM Admins       | Needs access to Key Vault, Storage                 |
| 📦 External API     | `customer-profile-service`           | All Envs         | Integration Team | Must be reachable over VNet                        |
| 📊 Database         | CosmosDB: `customer-db`              | Prod             | DBA Team         | Indexed for customerId                             |
| 🪝 Event Trigger    | Pub/Sub Topic: `order-topic`         | GCP / Cloud Run  | Platform Team    | Required for async order processing                |

---

## 🔐 Azure Key Vault: `my-app-kv`

<details>
<summary>Details</summary>

- **Type**: Azure Key Vault  
- **Required For**: Storing `DB_PASSWORD`, `JWT_SECRET`  
- **Access Control**: Managed Identity `app-mi` must have `get` and `list` permissions  
- **Environment**: All (Dev, Staging, Prod)  
- **Reference**: Vault URI must be configured in app settings  

</details>

---

## 📦 Dependency: `customer-profile-service`

<details>
<summary>Details</summary>

- **Interface**: REST (v1)  
- **Base URL**: `https://profile.internal/api/v1`  
- **Auth**: Internal token (shared secret)  
- **Availability**: Must be reachable in all environments  
- **Owner**: Integration Team  

</details>

---

## 🪪 Managed Identity: `app-mi`

<details>
<summary>Details</summary>

- **Purpose**: Used to access Azure Key Vault and Cosmos DB  
- **Environment**: Staging, Prod  
- **Permissions Required**:  
  - Key Vault: `get`, `list`  
  - Cosmos DB: read/write access  

</details>

---

## 📊 Cosmos DB: `customer-db`

<details>
<summary>Details</summary>

- **Type**: Azure Cosmos DB for MongoDB API  
- **Environment**: Production  
- **Key Usage**: Customer profile storage  
- **Indexes**: Must include `customerId`, `email` for performance  
- **Owner**: DBA Team  

</details>

---

## 🪝 Pub/Sub Topic: `order-topic`

<details>
<summary>Details</summary>

- **Platform**: Google Cloud Pub/Sub  
- **Used By**: Order service running in Cloud Run  
- **Access**: Publisher rights for `order-service@project.iam.gserviceaccount.com`  
- **Environment**: All  
- **Notes**: Configure dead-letter topic and retry policy  

</details>

---

## 🚦 Pre-deployment Checklist

| Item                         | Status       | Verified By |
|------------------------------|--------------|--------------|
| Key Vault Exists             | ✅ Complete  | DevOps       |
| Managed Identity Assigned    | 🕒 In Progress | Security     |
| External App Reachable       | ⏳ Pending   | Network      |
| Secret Reference Validated   | ✅ Complete  | Developer    |

---

> ℹ️ This document should be reviewed before each major deployment. Use pull requests to update dependency records as needed.
