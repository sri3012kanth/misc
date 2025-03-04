In Azure API Management (APIM), you can **publish** the **Developer Portal** using the **Azure REST API**. Here’s how you can do it:

---

## **1. Get Required Authentication Details**
You need:
- **APIM Name** (e.g., `my-apim-service`)
- **Resource Group Name** (e.g., `my-resource-group`)
- **Azure Subscription ID**
- **Azure Management API Authentication** (via `Bearer` token)

---

## **2. Obtain Access Token**
You must authenticate with **Azure AD** to get a token:

```sh
az login
TOKEN=$(az account get-access-token --query accessToken --output tsv)
```

---

## **3. Publish the Developer Portal**
Use the following REST API **PUT** request:

```sh
curl -X PUT "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/portalsettings/delegation?api-version=2022-08-01"
-H "Authorization: Bearer $TOKEN"
-H "Content-Type: application/json"
-d '{
  "properties": {
    "isDelegationEnabled": true
  }
}'
```

Replace:
- `{subscriptionId}` → Your Azure Subscription ID
- `{resourceGroupName}` → Your APIM Resource Group
- `{serviceName}` → Your APIM Instance Name

---

## **4. Verify the Portal Deployment**
Run:
```sh
curl -X GET "https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.ApiManagement/service/{serviceName}/portalsettings/delegation?api-version=2022-08-01" \
-H "Authorization: Bearer $TOKEN"
```

If `isDelegationEnabled` is `true`, the portal is published.

---

## **5. Alternative: Publish via Azure CLI**
```sh
az apim update --name {serviceName} --resource-group {resourceGroupName} --set portalSettings.delegation.isDelegationEnabled=true
```

---

### **Additional Notes**
- The Developer Portal uses **delegation settings** for sign-in and subscription requests.
- If the API version **changes**, use `az rest` to check available versions:
  ```sh
  az rest --method get --uri "https://management.azure.com/providers/Microsoft.ApiManagement?api-version=2022-08-01"
  ```

Let me know if you need further clarifications! 🚀
