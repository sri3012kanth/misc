Below is a sample **step-by-step user guide / reference documentation** for using the **DocumentDB for VS Code** extension to connect to an **Azure Cosmos DB for MongoDB (vCore)** cluster using **Microsoft Entra ID (formerly Azure AD) authentication** as a user with the `readAnyDatabase` (read-only) role.

You can adapt/brand this for your organization or internal documentation.

---

## Overview & Prerequisites

### What this doc covers

* Assumes the user is already onboarded to the vCore cluster with Entra ID–based authentication and has been granted a *readOnly / readAnyDatabase* role (i.e. data-plane read access) via Entra ID.
* Shows how to authenticate locally using `az login` and then use the DocumentDB (Cosmos DB) VS Code extension to connect to the vCore cluster using the Entra ID–based auth method.
* Shows how to build the correct connection string / URI and configuration in VS Code.

### Key prerequisites & constraints

1. **vCore cluster must have Entra ID authentication enabled**
   The cluster must be configured to allow Entra ID (Microsoft Entra) authentication in addition to (or alongside) native DocumentDB/MongoDB authentication. ([Microsoft Learn][1])

2. **User identity must be added to the cluster with read access**
   You (or group) must have been added as a nonadministrative Entra ID principal on the vCore cluster with the appropriate read permission (e.g. read any database). ([Microsoft Learn][2])

3. **Tooling**

   * Azure CLI installed (or use Azure Cloud Shell)
   * VS Code installed
   * The **DocumentDB for VS Code** extension installed (version ≥ 0.3, which supports Entra ID auth for vCore) ([microsoft.github.io][3])

4. **Network connectivity**
   VS Code must be able to reach the vCore cluster endpoint over the network (firewalls, VNets, Private Link, etc.).

5. **Permissions and roles**
   Ensure you have appropriate Azure RBAC / control-plane permissions (for using `az login`, reading resource metadata, etc.).

---

## Step 1: Log in using Azure CLI (`az login`)

To acquire a valid Azure/Entra ID auth token that can be used by VS Code, you must log in via Azure CLI.

```bash
az login
```

* This opens the browser to sign in to your Entra ID user account.
* If you have multiple subscriptions or accounts, specify the correct subscription:

```bash
az login --tenant <TENANT_ID>
az account set --subscription <SUBSCRIPTION_ID>
```

* Confirm your signed in account:

```bash
az account show
```

It should display the account email / object id and the active subscription.

> **Note:** Under the hood, this gives you credentials (tokens) that VS Code and the extension can use (via Azure Identity libraries) to query the resource and get tokens for the vCore cluster.

---

## Step 2: Obtain the Entra ID–based connection URI / string for vCore

Before connecting in VS Code, you need the correct connection URI format that supports Entra ID (OIDC) authentication.

### Connection URI format for Entra ID + vCore

When using Entra ID to authenticate to Cosmos DB for MongoDB vCore, the connection URI uses the standard MongoDB connection scheme (e.g. `mongodb+srv://`), but you do **not** embed a username/password in the URI. Instead, the driver or tool must obtain a token via OIDC and send it in the MongoDB `authMechanism` (OIDC-based). ([Microsoft Learn][1])

A sample connection URI might look like:

```
mongodb+srv://<clusterName>.global.mongo.cosmos.azure.com/?authMechanism=DEFAULT
```

or

```
mongodb+srv://<clusterName>.mongo.cosmos.azure.com/?authMechanism=DEFAULT
```

Additionally, you may need parameters such as `tls=true` etc., depending on the cluster configuration.

**Important**: The extension needs to know that you’re using Entra ID (OIDC) auth rather than basic username/password auth.

In practice, the DocumentDB extension provides a connection UI where you pick **“Entra ID (Azure AD) Authentication”** (or similar) instead of entering username/password. ([Microsoft Learn][4])

You do **not** embed your credential in the connection string for Entra ID mode; instead, the extension uses your Azure identity to authenticate.

---

## Step 3: Connecting via DocumentDB for VS Code extension

Here’s a walkthrough of how to connect via the VS Code extension:

1. **Install / Ensure you have the extension**

   * In VS Code, go to Extensions (`Ctrl+Shift+X`)
   * Search for **DocumentDB for VS Code** (or “Azure Cosmos DB”) and install
   * If you already have it, ensure you have a version >= 0.3, which supports Entra ID login for vCore. ([microsoft.github.io][3])

2. **Open the Azure / Cosmos DB explorer view**
   In VS Code, open the **Azure** side-bar (Activity bar) and find the **Cosmos DB / Azure Databases** section. ([Microsoft Learn][4])

3. **Add new connection / account**

   * Click on “+ Add Account” or “Add Connection” under Cosmos DB / Azure Databases
   * In the connection dialogue, choose **Azure subscription** (this lets the extension list your Cosmos DB vCore clusters).
   * Alternatively, you may choose **Connection String** and paste a URI; but when selecting *Entra ID authentication*, you should not provide username/password — the extension will use your Azure identity.

4. **Select Entra ID / Azure AD authentication mode**

   * In the authentication dropdown, pick **Entra ID / Azure AD** (or “Azure Active Directory”) instead of **Username & Password**.
   * The extension will detect you are signed in via Azure CLI / your Azure session.

5. **Pick your vCore cluster resource**

   * The extension will list your Azure subscription(s), resource groups, and vCore clusters.
   * Expand to find your desired **Azure Cosmos DB for MongoDB (vCore)** cluster. Select it.

6. **Connection established**

   * The extension will internally acquire a token for the cluster using OIDC flows based on your signed-in Azure identity.
   * You should now see your cluster, its databases, collections, etc., and can run queries / browse data (read-only, per your role).

If the extension fails, ensure:

* You're logged in (`az login`) and subscription is correct
* Your identity is permitted on the vCore cluster (has read role)
* No network or firewall issues block access

---

## Example: Full Flow Summary

Here’s the full user flow summarized:

| Step | Action                                                          | Outcome / Check                                                  |
| ---- | --------------------------------------------------------------- | ---------------------------------------------------------------- |
| 1    | `az login` (and `az account set`)                               | You are authenticated in Azure CLI                               |
| 2    | Open VS Code → Azure / Cosmos DB extension                      | Extension sees your Azure identity                               |
| 3    | Add connection → choose your Azure subscription / vCore cluster | The extension lists vCore clusters in your subscription          |
| 4    | Select Entra ID / Azure AD auth mode                            | The extension will use OIDC to fetch token                       |
| 5    | Select cluster → connect                                        | You see the cluster, databases, and can browse / query read-only |

---

## Troubleshooting & Tips

* **Not seeing clusters?**
  Make sure your Azure CLI / VS Code session is using the correct subscription where the cluster is deployed (`az account set`).
  Also ensure your identity has at least *read* permission on the resource in Azure RBAC / role assignments.

* **Permission denied / unauthorized errors**
  Likely your Entra ID user was not properly added to the vCore cluster or assigned the proper read role. Confirm via the Azure portal or CLI that the cluster’s authentication settings include your user. ([Microsoft Learn][2])

* **Extension version compatibility**
  Only versions ≥ 0.3 support Entra ID authentication for vCore. Earlier versions only supported username/password. ([microsoft.github.io][3])

* **Networking / firewall issues**
  The extension must reach the cluster endpoint (over TLS). If the cluster is behind VNet, Private Link, or firewall rules, ensure VS Code’s machine is permitted to connect.

* **Token expiration / re-login**
  The extension may need to refresh tokens; if your Azure login session expires, re-run `az login`.

* **Logging / diagnostic**
  Use the VS Code extension’s output panel / logs to see detailed errors about authentication failures or network connectivity.

---

If you like, I can produce a polished internal documentation PDF / markdown version (with screenshots) tailored to your environment (substitution of your cluster names, etc.). Would you like me to format it as Markdown ready for your docs portal?

[1]: https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/entra-authentication?utm_source=chatgpt.com "Microsoft Entra ID authentication - Azure Cosmos DB for MongoDB ..."
[2]: https://learn.microsoft.com/en-us/azure/cosmos-db/mongodb/vcore/how-to-configure-entra-authentication?utm_source=chatgpt.com "Configure Microsoft Entra ID authentication for an Azure Cosmos DB ..."
[3]: https://microsoft.github.io/vscode-documentdb/release-notes/0.3.html?utm_source=chatgpt.com "DocumentDB for VS Code Extension v0.3"
[4]: https://learn.microsoft.com/en-us/azure/cosmos-db/visual-studio-code-extension?utm_source=chatgpt.com "Use Visual Studio Code to connect and manage Azure Cosmos DB ..."
