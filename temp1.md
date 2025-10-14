Perfect — here’s the **Cloud Run–level optimization section only**, rewritten for your constraint:

> **min-instances = 0** and **max-instances = 1**,
> where cold-start performance is the **primary priority**.

You can drop this directly into your README or Confluence page.

---

## ☁️ Cloud Run-Level Optimizations (minInstances=0, maxInstances=1)

When your Cloud Run service is configured with `min-instances=0` and `max-instances=1`, **every request after idle will experience a cold start**.
These settings minimize cost but make startup speed critical.
The following configurations focus purely on **infrastructure and runtime parameters** to reduce cold-start latency and improve reliability.

---

### ⚙️ 1. Container Concurrency

**Recommended:**

```bash
--concurrency=1
```

**Reason:**

* With only one instance (`max-instances=1`), concurrency >1 can delay responses when the container is still initializing.
* Setting concurrency to 1 ensures predictable latency and sequential processing (important if duplicate-detection logic depends on ordered requests).

**Impact:**
Reduces CPU contention during initialization and prevents request queuing inside a cold container.

---

### ⚡ 2. CPU Allocation During Startup

**Recommended:**

```bash
--cpu-throttling=no
```

**Reason:**

* By default, Cloud Run throttles CPU when the service is idle.
* During a cold start, CPU availability directly impacts how fast the JVM loads and initializes Spring Boot.
* Disabling throttling ensures the container has full CPU access during startup.

**Impact:**
Typical improvement of **30–40% faster startup** (e.g., from 4.5 s → ~2.5–3.0 s).

---

### 💾 3. Memory Allocation

**Recommended:**

```bash
--memory=1Gi
```

**Reason:**

* JVMs perform more garbage collection and classloading work at startup than steady-state runtime.
* Allocating at least 1 GB prevents GC thrash and provides adequate space for metadata and code cache.

**Impact:**
Smoother cold starts and fewer GC pauses during class loading.

---

### 🧠 4. CPU Allocation

**Recommended:**

```bash
--cpu=1
```

**Reason:**

* A single vCPU is usually sufficient for sequential workloads (especially with concurrency = 1).
* Increasing CPU to 2 can marginally reduce cold-start latency but may not be cost-effective unless startup exceeds 4–5 seconds.

**Impact:**
Balanced cost and performance. Use `--cpu=2` only if profiling shows CPU-bound initialization.

---

### 🚀 5. Image Build & Startup Layer Optimization

**Recommendations:**

1. Use **layered JAR** support:

   ```bash
   ./mvnw spring-boot:build-image -Dspring-boot.build-image.layers.enabled=true
   ```

   or

   ```properties
   spring.boot.build-image.layers.enabled=true
   ```

2. **Exploded JAR deployment (you already do this)** — good choice for Cloud Run.
   It avoids archive decompression at startup.

3. **Keep base image consistent** (JDK 21, non-native):
   Avoid switching images frequently; image caching in GCP improves cold-start time.

**Impact:**
Layered/exploded JARs typically save **200–300 ms** per startup and reduce image pull time.

---

### 🌐 6. Network and DNS Optimization

**Recommendations:**

* Enable **HTTP/2** (Cloud Run defaults to it).
* Prefer **GCP Artifact Registry** over Docker Hub for images to reduce cold-start image pull latency.
* If calling other GCP services (e.g., Pub/Sub, Secret Manager), use **regional endpoints** to minimize connection setup time.

**Impact:**
Reduces external initialization delays by up to **200 ms** per service dependency.

---

### 🔍 7. Health Check Configuration

**Recommended:**
Expose a lightweight `/actuator/health` endpoint for Cloud Run to probe:

```yaml
management:
  endpoint:
    health:
      probes:
        enabled: true
  endpoints:
    web:
      exposure:
        include: health
```

Then configure Cloud Run to use it as the **readiness probe**.
Keep the probe fast — avoid any downstream calls or DB access in it.

**Impact:**
Improves reliability without extending startup time.

---

### 📈 8. JVM and Runtime Flags

**Recommended JVM options:**

```bash
JAVA_TOOL_OPTIONS="-XX:+UseG1GC -XX:MaxRAMPercentage=75.0 -Dspring.main.lazy-initialization=true -Dspring.threads.virtual.enabled=true"
```

**Reason:**

* Ensures efficient GC and heap sizing under container memory constraints.
* Works natively with JDK 21.
* Virtual threads (available in JDK 21) improve throughput even with single-instance concurrency.

**Impact:**
Stabilizes cold-start GC performance and reduces warm-up jitter.

---

### 🧾 Summary — Optimal Cloud Run Configuration

| Setting          | Recommended       | Purpose                        | Expected Impact         |
| ---------------- | ----------------- | ------------------------------ | ----------------------- |
| `min-instances`  | `0`               | Cost savings, no warm instance | Cold start every time   |
| `max-instances`  | `1`               | Sequential request flow        | Predictable processing  |
| `concurrency`    | `1`               | Avoids contention during init  | Consistent latency      |
| `cpu-throttling` | `no`              | Full CPU access during boot    | 30–40% faster startup   |
| `memory`         | `1Gi`             | Prevents GC overhead           | Smoother init           |
| `cpu`            | `1`               | Balanced cost/perf             | Adequate for single API |
| `image`          | Exploded JAR      | Skip decompression             | ~200–300 ms faster      |
| `base image`     | JDK 21 standard   | Maintains compatibility        | Stable                  |
| `registry`       | Artifact Registry | Faster pull                    | Lower latency           |

---

### ✅ Combined Expected Outcome

| Metric                           | Before (Default) | After Optimization    |
| -------------------------------- | ---------------- | --------------------- |
| JVM Warmup                       | ~4.5 s           | ~2.5–3.0 s            |
| First Request (after cold start) | ~5–6 s           | ~3–3.5 s              |
| Warm Request                     | ~100 ms          | ~100 ms               |
| Cold-start Frequency             | High (always)    | Unchanged (by design) |
| Cost                             | Lowest possible  | ✅                     |

---

Would you like me to add a **“Cost vs Performance trade-off matrix”** section next (showing the difference if min-instances = 1 or CPU = 2)?
That would help justify your choice in documentation.
