Got it! You want a **Python script** that uses **`--` style command-line parameters** instead of positional arguments. Here's an updated version using `argparse`:

---

### **Python Script: `create_mongo_user.py`**

```python
import argparse
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Parse command-line arguments using -- notation
parser = argparse.ArgumentParser(description="Create a new MongoDB vCore Entra ID user")
parser.add_argument("--user-id", required=True, help="Entra ID of the new user")
parser.add_argument("--role", required=True, help="Role to assign to the new user (e.g., readWrite, dbAdmin)")
args = parser.parse_args()

entra_user_id = args.user_id
role = args.role

# MongoDB vCore connection URI with Entra ID auth
# Replace <YOUR_COSMOS_ACCOUNT> with your Cosmos DB vCore cluster
mongo_uri = "mongodb+srv://<YOUR_COSMOS_ACCOUNT>.mongo.cosmos.azure.com:10255/?authMechanism=MONGODB-OIDC&tls=true"

try:
    # Connect using OIDC (Entra ID)
    client = MongoClient(mongo_uri)
    db = client['admin']

    # Command to create user with Entra ID authentication
    command = {
        "createUser": entra_user_id,
        "roles": [{"role": role, "db": "admin"}],
        "customData": {"authType": "EntraID"}
    }

    result = db.command(command)
    print(f"User '{entra_user_id}' created successfully with role '{role}': {result}")

except PyMongoError as e:
    print(f"Error creating user: {e}")
```

---

### **Usage Example**

```bash
python create_mongo_user.py --user-id user@example.com --role readWrite
```

---

This way, the script is **flexible and self-documenting**.

If you want, I can make an **enhanced version that automatically retrieves the OIDC token from Azure CLI**, so the script can run without manually setting any tokens. This is the typical approach for **Entra ID automation**.

Do you want me to do that next?
