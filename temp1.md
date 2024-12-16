Here’s a complete example of a **change stream listener** in Kotlin Spring Boot using **customer profile documents** from a MongoDB collection and leveraging **ShedLock** with explicit **lock extension (heartbeat mechanism)**. This implementation ensures:

1. **Customer Profile Document** is used in the change stream.
2. **Lock Extension Logic**: Heartbeat explicitly extends the lock duration during processing.
3. Ensures failover with a lock timeout (`lockAtMostFor`) in case of failure.

---

### **Customer Profile Document**

```kotlin
data class CustomerProfile(
    val id: String,
    val name: String,
    val address: String,
    val phone: String,
    val email: String,
    val ssn: String,
    val dateOfBirth: String
)
```

---

### **Updated Change Stream Listener Implementation**

```kotlin
import net.javacrumbs.shedlock.spring.annotation.SchedulerLock
import net.javacrumbs.shedlock.core.LockProvider
import net.javacrumbs.shedlock.core.SimpleLock
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Service
import com.mongodb.client.MongoClient
import com.mongodb.client.MongoCollection
import com.mongodb.client.model.changestream.ChangeStreamDocument
import org.bson.Document
import java.time.Instant
import kotlin.concurrent.thread

@Service
class CustomerChangeStreamListener(
    private val mongoClient: MongoClient,
    private val lockProvider: LockProvider
) {
    private val heartbeatInterval = 10000L // 10 seconds in milliseconds
    private var heartbeatThread: Thread? = null
    private var lock: SimpleLock? = null

    /**
     * Change stream listener with ShedLock.
     * Scheduled every 5 seconds. Only one instance will execute due to ShedLock.
     */
    @Scheduled(fixedRate = 5000)
    @SchedulerLock(name = "CustomerChangeStreamListenerTask", lockAtMostFor = "PT5M", lockAtLeastFor = "PT10S")
    fun listenToCustomerChanges() {
        println("Acquired lock. Starting customer profile change stream listener.")

        // Start a new heartbeat thread to extend the lock
        startHeartbeat()

        try {
            val collection: MongoCollection<Document> = mongoClient
                .getDatabase("<database-name>")
                .getCollection("<collection-name>")

            // Open the change stream
            val changeStream = collection.watch().iterator()

            // Process changes
            while (changeStream.hasNext()) {
                val change: ChangeStreamDocument<Document> = changeStream.next()
                val customerProfile = parseCustomerProfile(change.fullDocument)
                println("Processing customer change: $customerProfile")
                // Process change (e.g., send downstream, update other systems)
                processCustomerChange(customerProfile)
            }
        } catch (ex: Exception) {
            println("Error in change stream listener: ${ex.message}")
        } finally {
            stopHeartbeat()
            println("Released lock. Stopping customer profile change stream listener.")
        }
    }

    /**
     * Parse the MongoDB document into a CustomerProfile object.
     */
    private fun parseCustomerProfile(document: Document?): CustomerProfile {
        if (document == null) {
            throw IllegalArgumentException("Change document cannot be null")
        }
        return CustomerProfile(
            id = document.getString("id"),
            name = document.getString("name"),
            address = document.getString("address"),
            phone = document.getString("phone"),
            email = document.getString("email"),
            ssn = document.getString("ssn"),
            dateOfBirth = document.getString("dateOfBirth")
        )
    }

    /**
     * Process a customer profile change.
     */
    private fun processCustomerChange(customerProfile: CustomerProfile) {
        println("Customer change detected: $customerProfile")
        // Add business logic here (e.g., update downstream systems)
    }

    /**
     * Starts the heartbeat thread to extend the lock.
     */
    private fun startHeartbeat() {
        heartbeatThread = thread(start = true) {
            while (!Thread.currentThread().isInterrupted) {
                try {
                    Thread.sleep(heartbeatInterval)
                    extendLock()
                } catch (e: InterruptedException) {
                    Thread.currentThread().interrupt()
                    println("Heartbeat thread interrupted.")
                } catch (e: Exception) {
                    println("Error during heartbeat: ${e.message}")
                }
            }
        }
    }

    /**
     * Stops the heartbeat thread.
     */
    private fun stopHeartbeat() {
        heartbeatThread?.interrupt()
        heartbeatThread = null
        lock?.unlock()
        lock = null
    }

    /**
     * Explicitly extend the lock during processing.
     */
    private fun extendLock() {
        val newLock = lockProvider.lock("CustomerChangeStreamListenerTask", Instant.now().plusMillis(heartbeatInterval))
        if (newLock != null) {
            lock?.unlock()
            lock = newLock
            println("Lock extended successfully.")
        } else {
            println("Failed to extend lock.")
        }
    }
}
```

---

### **Key Enhancements**
1. **Heartbeat-Driven Lock Extension**:
   - The `extendLock` method explicitly re-acquires the lock before it expires to prevent lock release during processing.
   - `lockProvider.lock` extends the lock by adding `heartbeatInterval` to the current timestamp.

2. **Customer Profile Parsing**:
   - Processes MongoDB documents into `CustomerProfile` objects for easy downstream handling.

3. **Failover Handling**:
   - If the lock expires (`lockAtMostFor`), another instance will acquire the lock automatically.

4. **Graceful Shutdown**:
   - Ensures the heartbeat thread is stopped and the lock is released when the listener terminates.

---

### **Testing**

1. **Multi-Instance Test**:
   - Deploy two instances of the application.
   - Confirm only one instance processes change streams at any time.

2. **Failure Test**:
   - Simulate failure of the active instance (kill the process).
   - Verify that the lock is released, and the other instance starts processing after acquiring the lock.

3. **Idle Test**:
   - Let the system run without changes to ensure the lock is held correctly and extended via heartbeat.

---

### **Deployment in Kubernetes**
Would you like assistance with creating Kubernetes manifests (e.g., `Deployment`, `Service`, `ConfigMap`, etc.) for deploying this application?
