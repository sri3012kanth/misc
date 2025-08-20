Perfect! You want a **nested YAML structure** showing `databases → collections → indexes` with `keys` as a list of `[field, direction]` and `options` as a dict. Here’s a **Python script** that exports Cosmos DB (Mongo API) indexes in exactly that format:

---

```python
from pymongo import MongoClient
import yaml

# === Config ===
COSMOS_URI = "mongodb://<username>:<password>@<cosmos-account>.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb"
DATABASES = ["myappdb", "analyticsdb"]  # List your databases here

client = MongoClient(COSMOS_URI)

output = {"databases": {}}

for db_name in DATABASES:
    db = client[db_name]
    output["databases"][db_name] = {"collections": {}}
    
    # List collections
    for coll_name in db.list_collection_names():
        collection = db[coll_name]
        indexes = collection.list_indexes()
        index_list = []
        
        for idx in indexes:
            # Convert keys dict to list of [field, direction]
            keys = [[k, v] for k, v in idx["key"].items()]
            
            # Build options dict
            options = {}
            if idx.get("unique"):
                options["unique"] = True
            if idx.get("sparse"):
                options["sparse"] = True
            if idx.get("expireAfterSeconds") is not None:
                options["expireAfterSeconds"] = idx["expireAfterSeconds"]
            if idx.get("partialFilterExpression") is not None:
                options["partialFilterExpression"] = idx["partialFilterExpression"]
            
            index_list.append({
                "keys": keys,
                "options": options
            })
        
        output["databases"][db_name]["collections"][coll_name] = {"indexes": index_list}

# Export to YAML
with open("cosmos_indexes.yaml", "w") as f:
    yaml.dump(output, f, default_flow_style=False, sort_keys=False)

print("Indexes exported to cosmos_indexes.yaml")
```

---

### ✅ Sample Output (`cosmos_indexes.yaml`)

```yaml
databases:
  myappdb:
    collections:
      users:
        indexes:
          - keys: [ ["_id", 1] ]
            options: {}
          - keys: [ ["email", 1] ]
            options: { unique: true }
      orders:
        indexes:
          - keys: [ ["orderId", 1] ]
            options: { unique: true }
          - keys: [ ["userId", 1], ["status", 1] ]
            options: {}
  analyticsdb:
    collections:
      events:
        indexes:
          - keys: [ ["timestamp", -1] ]
            options: {}
```

---

This script handles **all indexes, including compound indexes**, and correctly maps options like `unique`, `sparse`, `expireAfterSeconds`, and `partialFilterExpression`.

If you want, I can also **make it auto-detect all databases** in your Cosmos account instead of manually listing `DATABASES`. Do you want me to do that?
