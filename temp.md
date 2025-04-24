Here’s a ready-to-use **Confluence documentation template** for **Cosmos DB failover testing scenarios** with East and West regions, formatted with headings, tables, and sectioning that works well in Confluence:

---

### 🧪 Cosmos DB (MongoDB API) – Failover Testing Documentation

---

#### 📌 Overview
This document outlines the testing and validation scenarios for Azure Cosmos DB (MongoDB API) configured in **multi-region write mode** across **East US** and **West US** regions. The purpose is to ensure **high availability**, **seamless failover**, and **resilient event processing** via MongoDB change streams.

---

#### 🌍 Environment Details

| Component         | Configuration                                       |
|------------------|-----------------------------------------------------|
| Cosmos DB         | MongoDB API, Multi-region write, East + West US     |
| Write Regions     | Active-Active                                       |
| Consistency Level | Session                                             |
| Application       | Change stream consumer deployed in AKS (East + West)|
| Listener Strategy | Single active instance via distributed locking      |

---

### ✅ Scenario 1: Cosmos DB East Region Down – Automatic Failover

#### 🔧 Preconditions
- Cosmos DB configured with East as preferred write region
- Application actively processing in East AKS
- West Cosmos DB replica available and healthy

#### 🧪 Steps
1. Confirm Cosmos DB is routing reads/writes to East.
2. Simulate East region failure:
   - Disable via Azure CLI or simulate with NSG/network rules.
3. Wait for routing switch to West.
4. Generate insert/update operations to Cosmos DB.
5. Confirm:
   - Application picks up events from West.
   - No duplicate or missing events.
   - Change stream resumes in backup listener if needed.

#### ✅ Expected Results

| Checkpoint                         | Result |
|-----------------------------------|--------|
| Failover to West completed        | ✅     |
| Application remains available     | ✅     |
| Mongo change stream processes events | ✅  |
| No data loss or duplication       | ✅     |
| Alerts triggered appropriately    | ✅     |

---

### ✅ Scenario 2: Both Regions Online – Normal Active-Active Operation

#### 🔧 Preconditions
- Cosmos DB fully available in East and West.
- Application running in both regions (only one active processor).
- Read/write routing respects preferred regions.

#### 🧪 Steps
1. Confirm application is processing from preferred region (East).
2. Perform insert/update operations.
3. Observe MongoDB change stream events.
4. Review application logs and Cosmos DB metrics.

#### ✅ Expected Results

| Checkpoint                         | Result |
|-----------------------------------|--------|
| Preferred region selected correctly | ✅   |
| Mongo change stream stable        | ✅     |
| Data replicated between regions   | ✅     |
| Application consistent and available | ✅  |

---

### 📦 Artifacts & Logs

| Item                   | Description                                         |
|------------------------|-----------------------------------------------------|
| App Logs               | Stream start, cursor resume, region detection       |
| Cosmos DB Metrics      | RU/s usage, regional routing, failover telemetry    |
| Diagnostics            | SDK logs showing preferred region and fallbacks     |
| Test Events            | Controlled data mutations for validation            |

---

### 🧰 Recommendations

- Configure alerts for RU spikes, region routing changes, and stream lags.
- Periodically run failover drills to validate readiness.
- Ensure TTL-based lock strategy is robust for active-passive listener failover.

---

### ✅ Final Test Summary

| Scenario                           | Result |
|------------------------------------|--------|
| East region down – failover tested | ✅ Passed |
| Both regions online – stable ops   | ✅ Passed |

---

Would you like this in **Confluence wiki markup** format (for direct paste into a Confluence editor), or should I convert and export it to a **.docx** or **HTML snippet** for copy-paste convenience?
