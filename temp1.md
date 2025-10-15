Perfect! We can extend the same script to **support both creating and removing a user** using a `--action` parameter (`create` or `remove`). Here's the updated script:

---

### **Python Script: `mongo_user_manage.py`**

```python
import argparse
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Manage MongoDB vCore Entra ID users")
parser.add_argument("--action", required=True, choices=["create", "remove"], help="Action to perform: create or remove a user")
parser.add_argument("--user-id", required=True, help="Entra ID of the user")
parser.add_argument("--role", help="Role to assign (required for create)")

args = parser.parse_args()

entra_user_id = args.user_id
action = args.action
role = args.role

# MongoDB vCore connection URI with Entra ID auth
# Replace <YOUR_COSMOS_ACCOUNT> with your Cosmos DB vCore cluster
mongo_uri = "mongodb+srv://<YOUR_COSMOS_ACCOUNT>.mongo.cosmos.azure.com:10255/?authMechanism=MONGODB-OIDC&tls=true"

try:
    client = MongoClient(mongo_uri)
    db = client['admin']

    if action == "create":
        if not role:
            print("Error: --role is required for creating a user")
            exit(1)

        command = {
            "createUser": entra_user_id,
            "roles": [{"role": role, "db": "admin"}],
            "customData": {"authType": "EntraID"}
        }
        result = db.command(command)
        print(f"User '{entra_user_id}' created successfully with role '{role}': {result}")

    elif action == "remove":
        command = {
            "dropUser": entra_user_id
        }
        result = db.command(command)
        print(f"User '{entra_user_id}' removed successfully: {result}")

except PyMongoError as e:
    print(f"Error performing action '{action}' on user '{entra_user_id}': {e}")
```

---

### **Usage Examples**

**Create a user:**

```bash
python mongo_user_manage.py --action create --user-id user@example.com --role readWrite
```

**Remove a user:**

```bash
python mongo_user_manage.py --action remove --user-id user@example.com
```

---

✅ This single script now handles **both creation and removal** of Entra ID–based MongoDB users.

If you want, I can also **add automatic OIDC token retrieval from Azure CLI**, so you won’t have to manage tokens manually—this makes automation fully hands-free. Do you want me to add that?
