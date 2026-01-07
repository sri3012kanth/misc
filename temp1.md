Below is the **Kotlin version** of the same solution, fully compatible with **Spring Boot 3.x + Azure App Configuration**, supporting **label + prefix filtering** from an API.

---

## 🎯 API Goal

```
GET /config?label=prod&prefix=app.
```

Returns **only Azure App Configuration keys** that:

* match the given **label**
* start with the given **prefix**

---

## ✅ Kotlin Implementation

---

## 1️⃣ Controller (Kotlin)

```kotlin
@RestController
@RequestMapping("/config")
class AzureAppConfigController(
    private val environment: ConfigurableEnvironment
) {

    @GetMapping
    fun getConfig(
        @RequestParam label: String,
        @RequestParam prefix: String
    ): Map<String, Any?> {

        val result = sortedMapOf<String, Any?>()

        environment.propertySources.forEach { ps ->

            // Only Azure App Configuration sources
            if (isAzureAppConfigSource(ps) && labelMatches(ps, label)) {

                if (ps is EnumerablePropertySource<*>) {
                    ps.propertyNames.forEach { key ->
                        if (key.startsWith(prefix)) {
                            result[key] = ps.getProperty(key)
                        }
                    }
                }
            }
        }

        return result
    }

    private fun isAzureAppConfigSource(ps: PropertySource<*>): Boolean =
        ps.name.contains("AzureAppConfiguration", ignoreCase = true)

    private fun labelMatches(ps: PropertySource<*>, label: String): Boolean =
        ps.name.contains(label, ignoreCase = true)
}
```

---

## 🧪 Example

### Request

```
GET /config?label=prod&prefix=app.
```

### Response

```json
{
  "app.feature.enabled": true,
  "app.db.timeout": 30
}
```

---

## 🔁 Handle DEFAULT (no-label) case

Azure App Configuration default label is **`\0`**
Spring loads it as:

```
AzureAppConfigurationPropertySource(...-null)
```

### Enhanced matcher:

```kotlin
private fun labelMatches(ps: PropertySource<*>, label: String): Boolean =
    if (label.equals("default", ignoreCase = true)) {
        ps.name.contains("null", ignoreCase = true)
    } else {
        ps.name.contains(label, ignoreCase = true)
    }
```

---

## 🔒 Optional: Mask Sensitive Values

```kotlin
private fun maskIfSensitive(key: String, value: Any?): Any? =
    if (key.contains(Regex("password|secret|token|key", RegexOption.IGNORE_CASE))) {
        "****"
    } else value
```

Use while putting into result.

---

## 🧠 Why this approach works well

| Benefit              | Reason                               |
| -------------------- | ------------------------------------ |
| Azure-native         | Uses already-loaded App Config       |
| Label aware          | Each label → separate PropertySource |
| Prefix safe          | Prevents accidental leaks            |
| Zero Azure SDK calls | No latency / auth issues             |
| Refresh compatible   | Works with sentinel refresh          |

---

## ⚠️ Production Notes

* Secure this endpoint (internal use only)
* Do **not** expose secrets
* Prefer `app.*` or `feature.*` prefixes
* Enable App Config refresh

---

If you want, I can also provide:

* **Service-based abstraction**
* **Exact label resolution (not name-based)**
* **Wildcard prefix support**
* **Spring Security example**
* **Unit tests in Kotlin**

Just tell me 👍
