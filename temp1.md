Got it — here’s a **focused list of Cloud Run console configuration updates** you can apply directly in the **GCP Cloud Run UI** for **fast readiness detection and optimized cold-start**, without touching your application code:

---

## 🛠 Cloud Run Console Settings for Optimized Readiness Probe

| Setting                               | Recommended Value                                | Notes / Purpose                                                           |
| ------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------- |
| **Min Instances**                     | `0`                                              | Keep cost minimal; container starts on-demand.                            |
| **Max Instances**                     | `1`                                              | Only one instance active at a time.                                       |
| **Container Concurrency**             | `1`                                              | Ensures sequential request handling; avoids contention during cold-start. |
| **CPU Allocation**                    | `1` vCPU                                         | Enough for a single API; reduces cold-start delays.                       |
| **CPU Throttling**                    | **Disabled**                                     | Ensures full CPU during cold-start for faster JVM initialization.         |
| **Memory**                            | `1 GiB`                                          | Prevents GC pressure during startup.                                      |
| **Startup Probe / Health Check Path** | `/actuator/health/readiness`                     | Detects readiness as early as possible.                                   |
| **Startup Probe Interval**            | `1 second`                                       | Probe frequently to minimize detection delay.                             |
| **Startup Probe Timeout**             | `4 seconds`                                      | Fails fast if container not yet ready.                                    |
| **Startup Probe Failure Threshold**   | `5`                                              | Allow 5 attempts before restart (~5 seconds).                             |
| **Readiness Probe Path**              | `/actuator/health/readiness`                     | Continuous health verification after startup.                             |
| **Readiness Probe Interval**          | `5 seconds`                                      | Check app health regularly.                                               |
| **Readiness Probe Timeout**           | `3 seconds`                                      | Fail fast if unhealthy.                                                   |
| **Startup CPU Boost**                 | Enabled (`run.googleapis.com/startup-cpu-boost`) | Gives temporary CPU burst during startup to reduce cold-start time.       |

---

### 🔹 Notes for GCP Console

1. Open your **Cloud Run service** → **Edit & Deploy New Revision**.
2. Under **Container, CPU & Memory**, set:

   * CPU: `1 vCPU`
   * Memory: `1 GiB`
   * CPU always allocated → toggle **ON**
3. Under **Autoscaling / Instances**, set:

   * Minimum instances: `0`
   * Maximum instances: `1`
4. Under **Container Concurrency**, set: `1`
5. Under **Advanced settings → Health checks / Probes**:

   * Startup Probe:

     * HTTP path: `/actuator/health/readiness`
     * Period: `1s`
     * Timeout: `4s`
     * Failure threshold: `5`
   * Readiness Probe:

     * HTTP path: `/actuator/health/readiness`
     * Period: `5s`
     * Timeout: `3s`
6. Enable **Startup CPU Boost** via **Annotations**:

   ```
   run.googleapis.com/startup-cpu-boost = true
   ```

---

This configuration ensures **Cloud Run detects readiness as early as possible**, minimizes cold-start latency, and avoids unnecessary restarts.

If you want, I can create a **ready-to-copy screenshot-style table + step-by-step UI guide** for the console so someone can just apply these settings visually. Do you want me to do that?
