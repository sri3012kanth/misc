Got it! We can make the **Cosmos DB account** a command-line parameter as well, so nothing is hardcoded. Here's the updated script:

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
parser.add_argument("--cosmos-account", required=True, help="Cosmos DB vCore account name")

args = parser.parse_args()

entra_user_id = args.user_id
action = args.action
role = args.role
cosmos_account = args.cosmos_account

# MongoDB vCore connection URI with Entra ID auth
mongo_uri = f"mongodb+srv://{cosmos_account}.mongo.cosmos.azure.com:10255/?authMechanism=MONGODB-OIDC&tls=true"

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
python mongo_user_manage.py --action create --user-id user@example.com --role readWrite --cosmos-account myCosmosAccount
```

**Remove a user:**

```bash
python mongo_user_manage.py --action remove --user-id user@example.com --cosmos-account myCosmosAccount
```

---

✅ Now **all inputs** (action, user ID, role, Cosmos account) are fully parameterized.

If you want, I can **add Azure CLI OIDC token automation** next so the script can run completely hands-free. This is especially useful for CI/CD or scheduled scripts.

Do you want me to add that?
