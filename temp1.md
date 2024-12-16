Here’s a fully updated version of the change stream listener application with the following features:

1. **Configuration-Driven Durations**:
   - All time durations like `lockAtMostFor`, `lockAtLeastFor`, and `heartbeatInterval` are read from `application.yaml`.

2. **Modular Structure**:
   - Separate classes for configuration, change stream listener, heartbeat mechanism, and MongoDB handling.

3. **Improved Resilience**:
   - Handles both idle and failover scenarios effectively.

---

### **Application Configuration (`application.yaml`)**

```yaml
app:
  mongo:
    database: customer-db
    collection: customer-profile
  lock:
    lockAtMostFor: PT5M         # Lock maximum duration: 5 minutes
    lockAtLeastFor: PT10S       # Lock minimum duration: 10 seconds
    heartbeatInterval: PT10S    # Heartbeat interval: 10 seconds
```

---

### **Code Implementation**

#### **Application Configuration**

```kotlin
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.context.annotation.Configuration
import java.time.Duration

@Configuration
@ConfigurationProperties(prefix = "app")
class AppConfig {
    lateinit var mongo: MongoConfig
    lateinit var lock: LockConfig
}

class MongoConfig {
    lateinit var database: String
    lateinit var collection: String
}

class LockConfig {
    lateinit var lockAtMostFor: Duration
    lateinit var lockAtLeastFor: Duration
    lateinit var heartbeatInterval: Duration
}
```

---

#### **Customer Profile Model**

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

#### **Change Stream Listener**

```kotlin
import com.mongodb.client.MongoClient
import com.mongodb.client.MongoCollection
import com.mongodb.client.model.changestream.ChangeStreamDocument
import net.javacrumbs.shedlock.core.LockProvider
import net.javacrumbs.shedlock.spring.annotation.SchedulerLock
import org.bson.Document
import org.springframework.scheduling.annotation.Scheduled
import org.springframework.stereotype.Service

@Service
class ChangeStreamListener(
    private val mongoClient: MongoClient,
    private val appConfig: AppConfig,
    private val heartbeatManager: HeartbeatManager,
    private val lockProvider: LockProvider
) {
    @Scheduled(fixedRate = 5000) // Check every 5 seconds
    @SchedulerLock(
        name = "CustomerChangeStreamListenerTask",
        lockAtMostFor = "#{@appConfig.lock.lockAtMostFor}",
        lockAtLeastFor = "#{@appConfig.lock.lockAtLeastFor}"
    )
    fun listenToCustomerChanges() {
        println("Acquired lock. Starting change stream listener.")

        // Start the heartbeat
        heartbeatManager.start()

        try {
            val collection = getCustomerProfileCollection()
            val changeStream = collection.watch().iterator()

            while (changeStream.hasNext()) {
                val change: ChangeStreamDocument<Document> = changeStream.next()
                val customerProfile = parseCustomerProfile(change.fullDocument)
                println("Processing customer change: $customerProfile")
                processCustomerChange(customerProfile)
            }
        } catch (ex: Exception) {
            println("Error in change stream listener: ${ex.message}")
        } finally {
            heartbeatManager.stop()
            println("Released lock. Stopping change stream listener.")
        }
    }

    private fun getCustomerProfileCollection(): MongoCollection<Document> {
        return mongoClient
            .getDatabase(appConfig.mongo.database)
            .getCollection(appConfig.mongo.collection)
    }

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

    private fun processCustomerChange(customerProfile: CustomerProfile) {
        println("Customer change detected: $customerProfile")
        // Add business logic here
    }
}
```

---

#### **Heartbeat Manager**

```kotlin
import net.javacrumbs.shedlock.core.LockProvider
import net.javacrumbs.shedlock.core.SimpleLock
import org.springframework.stereotype.Component
import java.time.Instant
import kotlin.concurrent.thread

@Component
class HeartbeatManager(
    private val lockProvider: LockProvider,
    private val appConfig: AppConfig
) {
    private var heartbeatThread: Thread? = null
    private var lock: SimpleLock? = null

    fun start() {
        heartbeatThread = thread(start = true) {
            while (!Thread.currentThread().isInterrupted) {
                try {
                    Thread.sleep(appConfig.lock.heartbeatInterval.toMillis())
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

    fun stop() {
        heartbeatThread?.interrupt()
        heartbeatThread = null
        lock?.unlock()
        lock = null
    }

    private fun extendLock() {
        val newLock = lockProvider.lock(
            "CustomerChangeStreamListenerTask",
            Instant.now().plusMillis(appConfig.lock.heartbeatInterval.toMillis())
        )
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

### **Spring Boot Main Class**

```kotlin
import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import org.springframework.scheduling.annotation.EnableScheduling

@SpringBootApplication
@EnableScheduling
class ChangeStreamApp

fun main(args: Array<String>) {
    runApplication<ChangeStreamApp>(*args)
}
```

---

### **Dependencies (`build.gradle.kts`)**

```kotlin
dependencies {
    implementation("org.springframework.boot:spring-boot-starter-data-mongodb")
    implementation("org.springframework.boot:spring-boot-starter-scheduling")
    implementation("net.javacrumbs.shedlock:shedlock-spring:5.5.0")
    implementation("net.javacrumbs.shedlock:shedlock-provider-mongo:5.5.0")
}
```

---

### **Summary of Features**

1. **Configuration Flexibility**: 
   - Timeouts (`lockAtMostFor`, `lockAtLeastFor`, `heartbeatInterval`) are read from `application.yaml`.

2. **Heartbeat Mechanism**:
   - Ensures the lock is extended periodically.
   - Gracefully handles interruptions or failures.

3. **Failover Support**:
   - `ShedLock` ensures that only one instance processes the change stream.
   - If an instance fails, another automatically picks up.

4. **MongoDB-Driven Change Streams**:
   - Parses `CustomerProfile` changes and allows business logic integration.

5. **Resilience and Scalability**:
   - Modular design makes it easy to test and extend.

Let me know if you'd like assistance with Kubernetes deployment for this application!
