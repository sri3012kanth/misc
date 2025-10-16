Excellent — let’s enhance the script to include a **`list`** action that fetches and prints all Entra ID–based users in your **MongoDB vCore** instance.

We’ll support three actions now:
✅ `create` → create a user
✅ `remove` → drop a user
✅ `list` → list all users

---

### **Final Script: `mongo_user_manage.py`**

```python
import argparse
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Manage MongoDB vCore Entra ID users")
parser.add_argument("--action", required=True, choices=["create", "remove", "list"],
                    help="Action to perform: create, remove, or list users")
parser.add_argument("--user-id", help="Entra ID of the user (required for create/remove)")
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
        if not entra_user_id or not role:
            print("Error: --user-id and --role are required for creating a user")
            exit(1)

        command = {
            "createUser": entra_user_id,
            "roles": [{"role": role, "db": "admin"}],
            "customData": {"authType": "EntraID"}
        }
        result = db.command(command)
        print(f"✅ User '{entra_user_id}' created successfully with role '{role}'.")
        print(result)

    elif action == "remove":
        if not entra_user_id:
            print("Error: --user-id is required for removing a user")
            exit(1)

        command = {"dropUser": entra_user_id}
        result = db.command(command)
        print(f"🗑️  User '{entra_user_id}' removed successfully.")
        print(result)

    elif action == "list":
        users = db.command("usersInfo")["users"]
        if not users:
            print("ℹ️  No users found.")
        else:
            print(f"👥 Users in '{cosmos_account}':")
            for user in users:
                name = user.get("user")
                roles = [r["role"] for r in user.get("roles", [])]
                print(f" - {name} | Roles: {', '.join(roles) if roles else 'None'}")

except PyMongoError as e:
    print(f"❌ Error performing '{action}' on user '{entra_user_id or 'N/A'}': {e}")
```

---

### **Usage Examples**

#### 🧩 Create a user

```bash
python mongo_user_manage.py --action create --user-id user@example.com --role readWrite --cosmos-account myCosmosAccount
```

#### 🗑️ Remove a user

```bash
python mongo_user_manage.py --action remove --user-id user@example.com --cosmos-account myCosmosAccount
```

#### 👥 List all users

```bash
python mongo_user_manage.py --action list --cosmos-account myCosmosAccount
```

---

✅ **Highlights:**

* Uses Entra ID (`MONGODB-OIDC`) for connection.
* Requires no hardcoded credentials.
* Provides clean output for `list` action.

---

Would you like me to now extend it so the script **automatically retrieves the Azure AD access token using `az account get-access-token`** (so it works even from a CI/CD agent without interactive login)?
