Yes! With **modern MongoDB Client-Side Field Level Encryption (CSFLE / QE)**, you can externalize the schema and even avoid hardcoding the algorithm in your Spring Boot Kotlin application. Here’s how:

---

### 1️⃣ Externalize Schema

Instead of embedding the schema in code, store it as a **JSON file** in `resources/` (e.g., `csfle-schema.json`):

```json
{
  "test.users": {
    "bsonType": "object",
    "properties": {
      "ssn": {
        "encrypt": {
          "keyAltNames": ["userSSNKey"],
          "bsonType": "string"
        }
      }
    }
  }
}
```

**Notes:**

* The driver can **infer a default algorithm** (`AEAD_AES_256_CBC_HMAC_SHA_512-Deterministic`) if you omit `algorithm`.
* The schema can now be modified without changing code.

---

### 2️⃣ Load Schema Dynamically in Kotlin

```kotlin
import com.mongodb.ConnectionString
import com.mongodb.MongoClientSettings
import com.mongodb.client.MongoClient
import com.mongodb.client.MongoClients
import org.bson.BsonDocument
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import java.nio.file.Files
import java.nio.file.Paths

@Configuration
class MongoConfig {

    private val connectionString = "mongodb://localhost:27017"
    private val keyVaultNamespace = "encryption.__keyVault"
    private val schemaFilePath = "src/main/resources/csfle-schema.json"

    @Bean
    fun mongoClient(): MongoClient {

        val kmsProviders = mapOf(
            "azure" to mapOf(
                "tenantId" to "YOUR_TENANT_ID",
                "clientId" to "YOUR_CLIENT_ID",
                "clientSecret" to "YOUR_CLIENT_SECRET"
            )
        )

        // Load schema from external JSON file
        val schemaJson = String(Files.readAllBytes(Paths.get(schemaFilePath)))
        val schemaMap = BsonDocument.parse(schemaJson)

        val autoEncryptionSettings = com.mongodb.AutoEncryptionSettings.builder()
            .keyVaultNamespace(keyVaultNamespace)
            .kmsProviders(kmsProviders)
            .schemaMap(schemaMap)
            .build()

        val settings = MongoClientSettings.builder()
            .applyConnectionString(ConnectionString(connectionString))
            .autoEncryptionSettings(autoEncryptionSettings)
            .build()

        return MongoClients.create(settings)
    }
}
```

---

### 3️⃣ Spring Data Repository & Entity (No Algorithm Needed in Code)

```kotlin
import org.springframework.data.annotation.Id
import org.springframework.data.mongodb.core.mapping.Document
import org.springframework.data.mongodb.repository.MongoRepository

@Document("users")
data class User(
    @Id val id: String? = null,
    val name: String,
    val ssn: String
)

interface UserRepository : MongoRepository<User, String> {
    fun findBySsn(ssn: String): User?
}
```

---

### ✅ Advantages of This Approach

1. **Schema externalized**: No need to modify the code to change encrypted fields.
2. **Algorithm optional**: The driver uses default deterministic encryption for queryable fields.
3. **Automatic DEK lookup**: Using `keyAltNames`, the driver fetches the DEK from `encryption.__keyVault`.
4. **Repository-friendly**: Spring Data repositories work as usual; encryption is transparent.

---

Essentially, with **externalized schema + automatic DEK lookup + no algorithm specified**, your Spring Boot Kotlin app can fully leverage **MongoDB QE/CSFLE** without touching the DEK, algorithm, or shared libraries in code.

I can prepare a **full working Spring Boot Kotlin project** demonstrating this setup with **CRUD endpoints** if you want.

Do you want me to do that?
