Here’s a **Python script** to copy the **Data Encryption Key (DEK)** from **Cosmos DB MongoDB RU-based API** to **MongoDB vCore API**, assuming both store their DEKs in the `encryption.__keyVault` collection.

---

## ✅ Requirements

Install dependencies:

```bash
pip install pymongo dnspython
```

---

## 🐍 Python Script

```python
from pymongo import MongoClient
from bson import json_util
import json

# 🔐 Connection URIs
RU_URI = "mongodb://<username>:<password>@<ru-account>.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false"
VCORE_URI = "mongodb://<username>:<password>@<vcore-server>.mongo.cosmos.azure.com:10255/?ssl=true&retrywrites=false"

# Constants
KEY_VAULT_DB = "encryption"
KEY_VAULT_COLL = "__keyVault"
KEY_ALT_NAME = "your-key-alias"  # 🔁 Update with your DEK alias or use _id

# Step 1: Connect to RU-based Cosmos DB and read DEK
ru_client = MongoClient(RU_URI)
ru_key_vault = ru_client[KEY_VAULT_DB][KEY_VAULT_COLL]

dek_doc = ru_key_vault.find_one({"keyAltNames": KEY_ALT_NAME})

if not dek_doc:
    raise Exception(f"DEK with keyAltName '{KEY_ALT_NAME}' not found in RU Cosmos DB")

print(f"[✅] DEK document found in RU Cosmos DB: {dek_doc['_id']}")

# Step 2: Connect to vCore Cosmos DB and insert DEK
vcore_client = MongoClient(VCORE_URI)
vcore_key_vault = vcore_client[KEY_VAULT_DB][KEY_VAULT_COLL]

existing = vcore_key_vault.find_one({"_id": dek_doc["_id"]})
if existing:
    print("[ℹ️] DEK already exists in vCore. Replacing it.")
    vcore_key_vault.replace_one({"_id": dek_doc["_id"]}, dek_doc)
else:
    print("[➕] Inserting DEK into vCore Cosmos DB.")
    vcore_key_vault.insert_one(dek_doc)

print("[🎉] DEK successfully copied from RU to vCore.")

# Optional: Export to JSON (for inspection or backup)
with open("dek_backup.json", "w") as f:
    f.write(json_util.dumps(dek_doc, indent=2))

print("[📁] Backup saved to dek_backup.json")
```

---

## 📝 Notes

* You can also fetch by `_id` instead of `keyAltNames` if you prefer.
* `json_util.dumps` handles binary fields (`keyMaterial`) correctly for BSON.
* Make sure your app on vCore can still access the Azure Key Vault (KEK) to decrypt data using this DEK.

---

Would you like a version of this that pulls the DEK from Azure Key Vault directly as well, or regenerates the DEK and re-wraps it with a new KEK?
