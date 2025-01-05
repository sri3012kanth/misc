To directly listen to changes as entities instead of using raw `Document` objects and manually converting them, you can leverage Spring Data's `DefaultMessageListenerContainer` and its support for type-safe listeners.

Here’s how you can listen to changes as entities:

---

### **Updated Implementation**

#### 1. **Entity Class**

Define your entity with the necessary annotations:

```kotlin
import org.springframework.data.annotation.Id
import org.springframework.data.mongodb.core.mapping.Document

@Document(collection = "custom_collection")
data class CustomEntity(
    @Id val id: String? = null,
    val name: String,
    val value: String,
    val entityType: String
)
```

---

#### 2. **Service with Type-Safe Listener**

Use `DefaultMessageListenerContainer` to listen to changes and directly map them to your entity class (`CustomEntity`):

```kotlin
import org.springframework.data.mongodb.core.ChangeStreamOptions
import org.springframework.data.mongodb.core.MongoTemplate
import org.springframework.data.mongodb.core.messaging.DefaultMessageListenerContainer
import org.springframework.data.mongodb.core.messaging.Message
import org.springframework.data.mongodb.core.messaging.MessageListener
import org.springframework.data.mongodb.core.messaging.SubscriptionRequest
import org.springframework.stereotype.Service
import javax.annotation.PostConstruct

@Service
class EntityChangeStreamService(private val mongoTemplate: MongoTemplate) {

    private lateinit var listenerContainer: DefaultMessageListenerContainer

    @PostConstruct
    fun init() {
        listenerContainer = DefaultMessageListenerContainer(mongoTemplate)
        listenerContainer.start()

        println("DefaultMessageListenerContainer started for entity change stream.")

        val options = ChangeStreamOptions.builder()
            .filter(
                org.springframework.data.mongodb.core.query.Criteria.where("fullDocument.entityType")
                    .`is`("specific_entity")
            )
            .returnFullDocumentOnUpdate()
            .build()

        val subscriptionRequest = SubscriptionRequest.builder()
            .collection("custom_collection")
            .options(options)
            .publishTo(entityMessageListener())
            .build()

        listenerContainer.register(subscriptionRequest)

        println("Change stream subscription created for entity: CustomEntity")
    }

    private fun entityMessageListener(): MessageListener<CustomEntity, CustomEntity> {
        return MessageListener { message: Message<CustomEntity, CustomEntity> ->
            handleEntityChange(message.body)
        }
    }

    private fun handleEntityChange(entity: CustomEntity?) {
        if (entity != null) {
            println("Change detected for entity: $entity")
            // Process the change event (e.g., save to a different collection, trigger downstream processing, etc.)
        } else {
            println("No entity found in the change event.")
        }
    }

    fun stopListener() {
        listenerContainer.stop()
        println("Stopped DefaultMessageListenerContainer.")
    }
}
```

---

### **How It Works**

1. **Change Stream Options**:
   - Configures the change stream to filter based on the `entityType` field.
   - Ensures the listener gets the full document (`returnFullDocumentOnUpdate`).

2. **Entity Listener**:
   - The `MessageListener` is configured with type parameters (`CustomEntity, CustomEntity`).
   - The `message.body` directly maps to the `CustomEntity`.

3. **Type Mapping**:
   - Spring Data MongoDB automatically maps the MongoDB document to the `CustomEntity` using the `MongoTemplate` and registered converters.

4. **Lifecycle Management**:
   - The container starts on application initialization (`@PostConstruct`) and stops gracefully when required.

---

### **Advantages of Direct Entity Mapping**

- **Simplicity**: Avoids manual conversion from `Document` to `CustomEntity`.
- **Type Safety**: Ensures the change stream data aligns with the expected entity structure.
- **Spring Ecosystem**: Leverages Spring's default `MongoConverter` for seamless mapping.

---

### **Testing**

1. Insert a document into the collection:
   ```javascript
   db.custom_collection.insertOne({
       "name": "Test Entity",
       "value": "100",
       "entityType": "specific_entity"
   })
   ```

2. Update a document:
   ```javascript
   db.custom_collection.updateOne(
       { "entityType": "specific_entity" },
       { $set: { "value": "200" } }
   )
   ```

3. Delete a document:
   ```javascript
   db.custom_collection.deleteOne({ "entityType": "specific_entity" })
   ```

---

### **Output Example**

For the above operations, the service logs would look like this:

```
DefaultMessageListenerContainer started for entity change stream.
Change stream subscription created for entity: CustomEntity
Change detected for entity: CustomEntity(id=64b8b8b8b8b8b8b8b8b8b8, name=Test Entity, value=100, entityType=specific_entity)
Change detected for entity: CustomEntity(id=64b8b8b8b8b8b8b8b8b8b8, name=Test Entity, value=200, entityType=specific_entity)
```

---

### **Notes**

1. **Mapping Requirements**:
   - Ensure your MongoDB document structure matches the `CustomEntity` class fields.

2. **Error Handling**:
   - Add exception handling in `handleEntityChange` for cases where the mapping fails.

3. **Extensibility**:
   - Extend the filtering logic in `ChangeStreamOptions` to include more criteria or stages if required.

Let me know if you'd like further clarifications or enhancements!
