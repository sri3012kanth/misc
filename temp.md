Perfect — let’s enhance your cleanup script to:
✅ delete files/folders older than 10 minutes,
✅ count how many it deleted, and
✅ log the count + timestamp to a file (so you can confirm it’s running).

---

## 🧾 Updated Script: `~/cleanup_old_files.sh`

```bash
#!/bin/bash
# ================================
# Cleanup Script with Logging
# ================================

# Folder to clean
TARGET_DIR="/path/to/your/folder"

# Log file path
LOG_FILE="$HOME/cleanup_log.txt"

# Current timestamp
NOW=$(date '+%Y-%m-%d %H:%M:%S')

# Find and delete files/folders older than 10 minutes, count them
COUNT=$(find "$TARGET_DIR" -mindepth 1 -mmin +10 | wc -l)
find "$TARGET_DIR" -mindepth 1 -mmin +10 -exec rm -rf {} \; 2>/dev/null

# Log output
echo "[$NOW] Deleted $COUNT items from $TARGET_DIR" >> "$LOG_FILE"
```

---

### 🧩 What it does

* `find "$TARGET_DIR" -mindepth 1 -mmin +10`
  → Lists all files and subfolders older than 10 minutes.
* `wc -l`
  → Counts how many.
* `rm -rf {}`
  → Deletes them (quietly, ignoring errors).
* `echo ... >> "$LOG_FILE"`
  → Appends a line to the log like:

  ```
  [2025-10-06 13:45:02] Deleted 7 items from /Users/sri/Downloads/temp
  ```

---

### 🔧 Setup once

1. Save the script:

   ```bash
   nano ~/cleanup_old_files.sh
   ```
2. Paste the above code.
3. Make it executable:

   ```bash
   chmod +x ~/cleanup_old_files.sh
   ```

---

### 🧭 Optional: Run every 5 minutes via cron

```bash
crontab -e
```

Add:

```bash
*/5 * * * * /Users/yourname/cleanup_old_files.sh >/dev/null 2>&1
```

---

### ✅ Check log anytime

```bash
cat ~/cleanup_log.txt
```

Example output:

```
[2025-10-06 13:00:01] Deleted 3 items from /Users/sri/Downloads/temp
[2025-10-06 13:05:01] Deleted 0 items from /Users/sri/Downloads/temp
[2025-10-06 13:10:01] Deleted 5 items from /Users/sri/Downloads/temp
```

---

Would you like me to modify it to **keep only the last N log lines** (say last 100 entries) so the file doesn’t grow too large?
