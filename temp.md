Great — thanks for the clarifications. I’ll tailor the plan to these constraints:

* you **need actuator** for GCP health checks (so don’t remove it),
* you **cache request IDs** to dedupe (so caching must remain),
* you **must produce a JAR** in your pipeline and the Docker image will use an **exploded JAR** (not native image / Graal), and
* the runtime JDK image is the organization’s **jdk 21** base.

Below are concrete, prioritized optimizations (with exact edits you can paste), why each matters for cold-start, trade-offs, and the expected effect. I won’t suggest native-image since that’s off the table; instead we focus on faster JVM startup and minimal spring boot work at startup.

---

# Immediate, high-impact changes (do these first)

## 1) Enable lazy initialization (very high impact, low risk)

Why: prevents Spring from creating and initializing lots of beans at boot. For a single API that only needs a small set of beans, lazy init can cut boot time dramatically. Since you use actuator, the health endpoint will still initialize what it needs.

**Add to `src/main/resources/application.properties`:**

```properties
# defer bean creation until first use
spring.main.lazy-initialization=true

# keep actuator minimal (only what Cloud Run needs)
management.endpoints.web.exposure.include=health
management.endpoint.health.show-details=never
```

**If you prefer YAML:**

```yaml
spring:
  main:
    lazy-initialization: true

management:
  endpoints:
    web:
      exposure:
        include: health
  endpoint:
    health:
      show-details: never
```

Expected effect: large reduction in startup. Trade-off: slightly longer first-request time for beans that are created on demand — acceptable for single-endpoint services.

---

## 2) Remove / exclude unnecessary auto-configurations (high impact)

Why: many auto-configurations run checks and create beans even if unused (JPA, DB, messaging, etc.). Excluding them avoids startup work. Keep actuator and caching auto-configs you need.

**In your `Application.kt` (or main class), add exclusions for things you do not use.** Example Kotlin:

```kotlin
@SpringBootApplication(
  exclude = [
    // exclude things you don't use:
    DataSourceAutoConfiguration::class,
    HibernateJpaAutoConfiguration::class,
    // If not using JMS:
    JmsAutoConfiguration::class,
    // If not using mail:
    MailSenderAutoConfiguration::class
    // add more exclusions as required
  ]
)
class Application
```

**Alternative** (in `application.properties`) — but class-level is clearer:

```properties
spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration,org.springframework.boot.autoconfigure.orm.jpa.HibernateJpaAutoConfiguration
```

Which auto-configs to exclude depends on your dependencies; common candidates:

* `DataSourceAutoConfiguration`, `HibernateJpaAutoConfiguration` (if no DB)
* `MongoAutoConfiguration` (if you don't use Mongo client autoconfig)
* `JmxAutoConfiguration`
* `TaskSchedulingAutoConfiguration` (if you don’t schedule tasks)

Expected effect: moderate-to-large. Trade-off: ensure you do not exclude an auto-config you actually need.

---

## 3) Limit component scanning & only register required beans (moderate impact)

Why: scanning wide package trees forces Spring to inspect many classes. Restrict the scan to only app packages.

**In `Application.kt`:**

```kotlin
@SpringBootApplication
@ComponentScan(basePackages = ["com.jeniusbank.yourservice"]) // change to your package only
class Application
```

If you have configuration classes in other packages, explicitly import them.

Expected effect: moderate, especially with many libraries present.

---

## 4) Switch to WebFlux (Netty) if you don’t need Servlet API (moderate → large)

Why: `spring-boot-starter-web` (Tomcat) pulls servlet plumbing — WebFlux with Reactor Netty tends to start faster and has smaller runtime footprint for small services.

**Changes to `build.gradle.kts`:**

* Remove servlet starter:

```kotlin
// remove or comment out:
implementation("org.springframework.boot:spring-boot-starter-web")
```

* Add webflux:

```kotlin
implementation("org.springframework.boot:spring-boot-starter-webflux")
```

**Controller changes (minimal):**
Existing controllers with `@RestController` and `@PostMapping` typically work unchanged on WebFlux if you accept simple request bodies. Consider `suspend` functions if you prefer Kotlin coroutines:

```kotlin
@RestController
class EventController {
  @PostMapping("/event")
  suspend fun receive(@RequestBody body: String) {
    // process body (dedupe using cache)
  }
}
```

Notes/trade-offs:

* If your code depends on servlet APIs (filters, `HttpServletRequest`, `ServletContext`), you’ll need changes.
* For simple string JSON body processing, migration is straightforward.

Expected effect: moderate-to-large reduction in startup time.

---

# JVM/runtime-level optimizations (easy to apply in Docker)

## 5) Use startup-friendly JVM flags (low effort, noticeable)

Add these flags to the JVM command to speed startup:

* `-XX:TieredStopAtLevel=1` — limits JIT optimization tiers so JVM spends less time compiling during startup (improves startup at cost of some steady throughput).
* `-Djava.security.egd=file:/dev/./urandom` — avoids blocking entropy acquisition on some images.
* `-XX:+HeapDumpOnOutOfMemoryError` (optional for diagnostics only).
* `-XX:MaxRAMPercentage=<value>` to limit heap relative to container memory (avoid OOM from oversized default).
* `-XX:+UseParallelGC` or `-XX:+UseG1GC` — G1 is default on modern JDKs; keep default unless testing shows otherwise.

**Example ENTRYPOINT (exploded jar approach)** — place in your Dockerfile runtime stage:

```dockerfile
ENTRYPOINT ["java",
  "-XX:TieredStopAtLevel=1",
  "-Dspring.main.lazy-initialization=true",
  "-Djava.security.egd=file:/dev/./urandom",
  "-XX:MaxRAMPercentage=70.0",
  "-jar","/app/exploded/spring-app.jar"]
```

(Adjust `/app/exploded/spring-app.jar` to your exploded jar location; if you run classes directly from exploded directories, adapt accordingly.)

Expected effect: moderate startup improvement. Measure to confirm the throughput trade-off is acceptable.

---

## 6) Use layered/exploded JAR properly & avoid unnecessary classpath scanning (moderate)

You said pipeline creates a JAR and the image copies exploded JAR. Two tips:

* Use **Spring Boot layered JAR** (or exploded layout) so container can reuse layers (not strictly faster startup, but speeds re-deploys and layer caching).
* Ensure your exploded layout does not include build-time tools (large `node_modules`, test resources). Only copy `build/libs/*.jar` and `build/dependencies` if using exploded.

**Dockerfile snippet for exploded jar (multi-stage)**

```dockerfile
# builder stage
FROM eclipse-temurin:21-jdk as builder
WORKDIR /workspace
COPY . .
RUN ./gradlew bootJar -x test

# final stage (exploded)
FROM eclipse-temurin:21-jdk as runtime
WORKDIR /app
# copy only what is needed
COPY --from=builder /workspace/build/libs/yourapp.jar /app/yourapp.jar
# If your pipeline explodes jar already, copy that exploded directory:
# COPY --from=builder /workspace/build/exploded /app/exploded
ENTRYPOINT ["java","-XX:TieredStopAtLevel=1","-Dspring.main.lazy-initialization=true","-Djava.security.egd=file:/dev/./urandom","-jar","/app/yourapp.jar"]
```

Tip: if the pipeline produces exploded jar content (a directory with `BOOT-INF/classes` and `BOOT-INF/lib`), start the JVM with `-cp` pointing to the `BOOT-INF/classes` and all jars in `BOOT-INF/lib` — avoid re-wrapping as a fat jar at runtime.

Expected effect: neutral to moderate on cold start; biggest benefit is smaller image & faster container startup times from caching.

---

# Spring-level compile-time and build-time optimizations

## 7) Use Spring (AOT) optimizations for faster JVM start (compatible with JVM)

Why: Spring AOT (ahead-of-time processing) can precompute reflection metadata, proxies, and bean descriptors at build time — reducing runtime reflection costs without using Graal native image. This works on the JVM and is allowed given your constraint.

**Gradle quick setup (add to `build.gradle.kts`)**

```kotlin
plugins {
  id("org.springframework.boot") version "3.4.10" // match your project
  id("io.spring.dependency-management") version "1.1.2"
  id("org.springframework.experimental.aot") version "1.1.0" // check latest compatible
  kotlin("jvm") version "2.0.21"
}

dependencies {
  // your existing deps...
  implementation("org.springframework.boot:spring-boot-starter-webflux") // or web
  // Add spring context indexer to speed component scanning
  implementation("org.springframework:spring-context-indexer")
}
```

**Build with AOT generation** (example Gradle tasks)

```bash
./gradlew clean bootJar
./gradlew generateAot // plugin generates AOT artifacts
# then package the AOT-optimized jar
./gradlew bootJar
```

Notes:

* Exact plugin name/version may vary by Spring Boot version. Use the Spring Boot docs matching your Spring Boot version.
* AOT for JVM reduces runtime reflection and proxy creation overhead.

Expected effect: moderate improvement in cold-start. Trade-off: slightly more complex build and need to test generated artifacts.

---

## 8) Use `spring-context-indexer` to reduce classpath scanning (small but easy)

Why: indexer helps Spring discover candidate components faster at startup.

**Add to `build.gradle.kts`**:

```kotlin
dependencies {
  compileOnly("org.springframework:spring-context-indexer")
}
```

This creates `META-INF/spring.components` at compile time.

Expected effect: small but cumulative.

---

# Caching/deduplication notes (because you cache request IDs)

You mentioned you cache request JSON ids for dedupe. That cache must remain accessible quickly after start. Two tips:

* **Use an external cache (Redis, Memorystore)** for dedupe if you need dedupe across instances or failover. External caches don’t increase service boot time.
* **If you keep an in-memory cache (Caffeine)**, ensure creation is lazy (bean creation for the cache can be delayed by lazy-init) and that the cache implementation isn’t heavy at start.

If you keep in-memory caching, declare the cache bean with `@Lazy` so it doesn’t initialize until first request:

```kotlin
@Configuration
class CacheConfig {
  @Bean
  @Lazy
  fun idCache(): Cache<String, Boolean> {
    return Caffeine.newBuilder()
      .maximumSize(100_000)
      .expireAfterWrite(Duration.ofMinutes(10))
      .build()
  }
}
```

This keeps startup work minimal and still provides caching once requests come in.

---

# Observability & measurement (must do after each change)

Add startup timing and a simple endpoint to show JVM args and bean counts — this helps confirm each change improves startup.

**Add to `Application.kt`:**

```kotlin
fun main(args: Array<String>) {
  val start = System.nanoTime()
  val ctx = runApplication<Application>(*args)
  val elapsed = (System.nanoTime() - start) / 1_000_000
  println("Application started in ${elapsed} ms; beans=${ctx.beanDefinitionCount}")
}
```

Cloud Run: deploy and measure cold start time (time from request to 200 OK for first request). Record numbers before/after each change.

---

# Quick prioritized checklist (what to do, in order)

1. Add `spring.main.lazy-initialization=true` and limit `management.endpoints.web.exposure.include=health`. Deploy and measure.
2. Exclude unnecessary auto-configs (DataSource, JPA, Mongo, JMS if unused). Deploy and measure.
3. Restrict `@ComponentScan` to your package. Deploy and measure.
4. Replace `starter-web` with `starter-webflux` if you can (simple single-endpoint app) — migrate controller if needed. Deploy and measure.
5. Add JVM flags (`-XX:TieredStopAtLevel=1`, `-Djava.security.egd=...`, `-XX:MaxRAMPercentage`), rebuild image and deploy.
6. Add `spring-context-indexer` and enable Spring AOT generation in Gradle; regenerate jar and deploy.
7. If still not fast enough, consider AppCDS or more advanced class-data-sharing steps with your JDK21 image (I can give exact commands once you confirm the JDK image vendor/version).

---

# Example diffs / snippets to paste

**`application.properties`**

```properties
spring.main.lazy-initialization=true
management.endpoints.web.exposure.include=health
management.endpoint.health.show-details=never
```

**`build.gradle.kts` (snippets)**

```kotlin
plugins {
  id("org.springframework.boot") version "3.4.10"
  id("io.spring.dependency-management") version "1.1.2"
  kotlin("jvm") version "2.0.21"
  id("org.springframework.experimental.aot") version "1.1.0" // optional
}

dependencies {
  implementation("org.springframework.boot:spring-boot-starter-webflux")
  implementation("com.github.ben-manes.caffeine:caffeine:3.2.2") // if caching
  compileOnly("org.springframework:spring-context-indexer")
  // remove org.jetbrains.kotlin:kotlin-reflect if you can
}
```

**`Application.kt`**

```kotlin
@SpringBootApplication
@ComponentScan(basePackages = ["com.jeniusbank.yourservice"])
class Application

fun main(args: Array<String>) {
  val start = System.nanoTime()
  val ctx = runApplication<Application>(*args)
  val elapsed = (System.nanoTime() - start) / 1_000_000
  println("Started in ${elapsed} ms; beans=${ctx.beanDefinitionCount}")
}
```

**Docker ENTRYPOINT example**

```dockerfile
ENTRYPOINT ["java",
  "-XX:TieredStopAtLevel=1",
  "-Dspring.main.lazy-initialization=true",
  "-Djava.security.egd=file:/dev/./urandom",
  "-XX:MaxRAMPercentage=70.0",
  "-jar","/app/yourapp.jar"]
```

---

# Expected numbers (very approximate)

* baseline: **3–6s** cold start (typical Spring Boot on Cloud Run depending on app)
* after lazy init + exclude + component-scan limit: **~30–60% reduction** (1.5–4s)
* after WebFlux + JVM flags: further **20–40% reduction**
* after AOT JVM optimizations: another improvement (depends), could bring you near **~1s–2s** cold starts for a small app on JDK21.

Exact numbers depend on your dependencies; measure after each change.

---

# Final notes & next steps I can produce now (pick any — I’ll produce without waiting)

* A concrete **Gradle `build.gradle.kts` diff** for your repository (I can generate the file edits assuming the dependencies shown in your screenshots).
* A **Dockerfile** for your exploded-jar pipeline with the exact commands to produce the final image (matching your build steps).
* A **short checklist + CI/CD snippet** for Cloud Build / GitHub Actions to build the jar, run AOT generation, and produce the image.
* **AppCDS commands** tuned to JDK21 (I will provide exact commands if you tell me the JDK vendor & full version string — e.g., `Eclipse Temurin 21.0.2+...` — but I can also give general commands that work for most JDK21 builds).

Which of those would you like me to generate now? I’ll produce the chosen artifact immediately.
