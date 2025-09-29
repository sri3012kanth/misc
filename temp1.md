Perfect 👍 I’ll merge both drafts into a **clean, simple documentation** with headings, findings, limitations, and conclusion.

Here’s the final version you can use:

---

# Evaluation of MongoDB Automated Field-Level Encryption (FLE) in Azure Cosmos DB for MongoDB vCore

## Objective

Assess feasibility of replacing the current **custom field-level encryption** (annotation-based with Spring PreUpdate and PostFetch listeners) with **MongoDB Automated Field-Level Encryption (FLE)** in Azure Cosmos DB for MongoDB vCore.

---

## POC Findings

1. **Library Dependency (`mongo_crypt_shared_v1`)**

   * Automated FLE requires the native `mongo_crypt_shared_v1` shared library.
   * Applications must configure `LD_LIBRARY_PATH` / `DYLD_LIBRARY_PATH` or ship the library inside Docker images.
   * This adds DevOps overhead and runtime fragility, compared to the current pure-Java solution.

2. **Operational Complexity**

   * Each encryption/decryption call invokes the native library.
   * In containerized/cloud environments, extra steps are required to bundle and maintain the library.
   * Azure VCore does not abstract this away—the burden remains on the client application.

3. **Refactoring Effort**

   * Existing code already implements encryption/decryption through annotations and entity listeners.
   * Migrating to Automated FLE only replaces current logic without adding significant functional benefit.
   * Minimal business advantage for high refactoring cost.

4. **Cloud Constraints**

   * Azure Cosmos DB vCore **does not ship or manage `mongo_crypt_shared_v1`**.
   * Automated FLE works only if the client application provides and configures the library.
   * Azure currently offers only **server-side encryption at rest** (service-managed or customer-managed keys).

---

## Official Limitations of Automated FLE (per MongoDB Documentation)

* **Unsupported operations** – Limited support for certain query/update operators and aggregation stages.
* **Arrays** – Queries on encrypted array fields may behave unexpectedly.
* **Views** – Queries on views referencing encrypted fields may produce incorrect results.
* **Collation** – Collations are not applied to encrypted fields.
* **Unique indexes** – Randomized encryption prevents true uniqueness enforcement.
* **Sharding** – Encrypted fields cannot reliably be used as shard keys.
* **Immutable schema** – Query type of an encrypted field must be set at creation and cannot change.
* **Diagnostic redaction** – Logs and diagnostics hide encrypted fields, limiting visibility.
* **Enterprise-only feature** – Full Automated FLE requires MongoDB Enterprise/Atlas and is not included in Community builds.
* **Native dependency** – Requires the `mongo_crypt_shared_v1` shared library or fallback to `mongocryptd`.

---

## Challenges / Issues Identified

* Extra **system-level dependency** not present in current implementation.
* Increased **DevOps complexity** for Docker and Kubernetes deployments.
* No **native Azure support** for client-side FLE libraries.
* Minimal **functional improvement** compared to existing custom encryption.
* Potential **vendor lock-in** to MongoDB-specific implementation.
* Reduced **observability** due to query/operator restrictions and redacted logs.

---

## Recommendation

* **Retain current custom encryption (Spring annotations + entity listeners)** as the production approach.
* **Monitor MongoDB and Azure** for future improvements (e.g., managed Automated FLE without client library).
* Keep encryption logic **abstracted** in the codebase to allow future migration if FLE matures.
* Reassess Automated FLE adoption only if Azure or MongoDB provides **fully managed support** that eliminates client dependency on native libraries.

---

## Conclusion

The POC shows that **Automated FLE in Azure VCore is not a feasible solution today**:

* It requires a native library (`mongo_crypt_shared_v1`) that Azure does not ship or manage.
* It introduces **higher operational complexity** without clear business benefits.
* The existing **custom encryption solution remains more portable, maintainable, and cloud-friendly**.

For now, the **custom approach should remain the standard**, with Automated FLE revisited when Azure provides built-in support.

---

Would you like me to also make a **one-page executive summary version** (very concise, for leadership/non-technical readers) alongside this detailed doc?
