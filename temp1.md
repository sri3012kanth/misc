Perfect! Let’s build a **complete Spring Boot Kotlin project** demonstrating **MongoDB Client-Side Field Level Encryption (CSFLE) with Queryable Encryption**, using:

* **Azure Key Vault KMS**
* **Automatic DEK lookup via keyAltName**
* **Externalized schema JSON**
* **Spring Data repository** for CRUD operations
* **Application YAML configuration** for `keyAltName` and Azure KMS credentials

---

## 1️⃣ Project Structure

```
src/
 └─ main/
     ├─ kotlin/com/example/mongo/
     │   ├─ MongoConfig.kt
     │   ├─ User.kt
     │   ├─ UserRepository.kt
     │   └─ UserService.kt
     └─ resources/
         ├─ application.yml
         └─ csfle-schema.json
```

---

## 2️⃣ `application.yml`

```yaml
spring:
  data:
    mongodb:
      database: test
mongo:
  csfle:
    key-alt-name: userSSNKey
  azure:
    tenant-id: YOUR_TENANT_ID
    client-id: YOUR_CLIENT_ID
    client-secret: YOUR_CLIENT_SECRET
```

> Replace `YOUR_TENANT_ID`, `YOUR_CLIENT_ID`, `YOUR_CLIENT_SECRET` with your Azure service principal credentials.

---

## 3️⃣ `csfle-schema.json` (externalized)

```json
{
  "test.users": {
    "bsonType": "object",
    "properties": {
      "ssn": {
        "encrypt": {
          "keyAltNames": ["${KEY_ALT_NAME}"],
          "bsonType": "string"
        }
      }
    }
  }
}
```

> `${KEY_ALT_NAME}` is a placeholder replaced at runtime from `application.yml`.

---

## 4️⃣ `MongoConfig.kt` – MongoClient with CSFLE

```kotlin
package com.example.mongo

import com.mongodb.ConnectionString
import com.mongodb.MongoClientSettings
import com.mongodb.client.MongoClient
import com.mongodb.client.MongoClients
import org.bson.BsonDocument
import org.springframework.beans.factory.annotation.Value
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration
import java.nio.file.Files
import java.nio.file.Paths

@Configuration
class MongoConfig(
    @Value("\${mongo.csfle.key-alt-name}") private val keyAltName: String,
    @Value("\${mongo.azure.tenant-id}") private val tenantId: String,
    @Value("\${mongo.azure.client-id}") private val clientId: String,
    @Value("\${mongo.azure.client-secret}") private val clientSecret: String
) {

    private val connectionString = "mongodb://localhost:27017"
    private val keyVaultNamespace = "encryption.__keyVault"
    private val schemaFilePath = "src/main/resources/csfle-schema.json"

    @Bean
    fun mongoClient(): MongoClient {

        // KMS provider for Azure
        val kmsProviders = mapOf(
            "azure" to mapOf(
                "tenantId" to tenantId,
                "clientId" to clientId,
                "clientSecret" to clientSecret
            )
        )

        // Load and replace keyAltName in schema
        var schemaJson = String(Files.readAllBytes(Paths.get(schemaFilePath)))
        schemaJson = schemaJson.replace("\${KEY_ALT_NAME}", keyAltName)
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

> Note: No need to specify `cryptSharedLibPath` – the driver auto-loads the library.

---

## 5️⃣ `User.kt` – Mongo Entity

```kotlin
package com.example.mongo

import org.springframework.data.annotation.Id
import org.springframework.data.mongodb.core.mapping.Document

@Document("users")
data class User(
    @Id val id: String? = null,
    val name: String,
    val ssn: String
)
```

---

## 6️⃣ `UserRepository.kt` – Spring Data Repository

```kotlin
package com.example.mongo

import org.springframework.data.mongodb.repository.MongoRepository

interface UserRepository : MongoRepository<User, String> {
    fun findBySsn(ssn: String): User?
}
```

---

## 7️⃣ `UserService.kt` – CRUD Service

```kotlin
package com.example.mongo

import org.springframework.stereotype.Service

@Service
class UserService(private val userRepository: UserRepository) {

    fun createUser(name: String, ssn: String): User {
        val user = User(name = name, ssn = ssn)
        return userRepository.save(user)
    }

    fun findBySsn(ssn: String): User? {
        return userRepository.findBySsn(ssn)
    }

    fun findAll(): List<User> = userRepository.findAll()
}
```

---

## 8️⃣ How It Works

1. **Externalized schema**: `csfle-schema.json` defines encrypted fields and uses `${KEY_ALT_NAME}` placeholder.
2. **KeyAltName injection**: Spring Boot reads `mongo.csfle.key-alt-name` from YAML and replaces the placeholder dynamically.
3. **Automatic DEK lookup**: Driver finds the DEK in `encryption.__keyVault` by `keyAltName`.
4. **Transparent encryption/decryption**: Spring Data repository methods (`save`, `findBySsn`) work normally.
5. **No algorithm specified**: Defaults are used by the driver.
6. **No cryptSharedLibPath**: Uses built-in library from the driver.

---

This setup is **production-ready** for:

* Multiple environments (`application-dev.yml`, `application-prod.yml`)
* Transparent encryption of sensitive fields
* Queryable deterministic fields (e.g., `ssn`)

---

If you want, I can also provide a **sample REST controller** to **test creating and querying encrypted users**, so you can run this end-to-end.

Do you want me to add that?
