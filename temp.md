To set up **Python logging** similar to **Spring Boot**, you can use Python’s built-in `logging` module and configure it for structured, customizable output. Here's how you can set it up:

---

## **1. Basic Logging Setup**
```python
import logging

# Basic configuration
logging.basicConfig(
    level=logging.INFO,  # Set logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",  # Log format
    datefmt="%Y-%m-%d %H:%M:%S"  # Date format
)

# Example logger
logger = logging.getLogger("myApp")  # Similar to package name in Spring Boot

def sample_function():
    logger.debug("Debug message for tracing")
    logger.info("Informational message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical error message")

if __name__ == "__main__":
    sample_function()
```

**Sample Output:**
```
2025-02-04 15:30:01 - INFO - myApp - Informational message
2025-02-04 15:30:01 - WARNING - myApp - Warning message
2025-02-04 15:30:01 - ERROR - myApp - Error message
2025-02-04 15:30:01 - CRITICAL - myApp - Critical error message
```

---

## **2. Advanced Configuration with Logging Levels**
Create a **logging configuration file** (e.g., `logging.conf`):

```ini
[loggers]
keys=root,myApp

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter,detailedFormatter

[logger_root]
level=WARNING
handlers=consoleHandler

[logger_myApp]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=myApp
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=detailedFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=INFO
formatter=detailedFormatter
args=("app.log", "a")

[formatter_simpleFormatter]
format=%(levelname)s - %(message)s

[formatter_detailedFormatter]
format=%(asctime)s - %(levelname)s - %(name)s - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

### **Using the Configuration in Code**
```python
import logging
import logging.config

# Load configuration from file
logging.config.fileConfig("logging.conf")

# Get logger
logger = logging.getLogger("myApp")

def sample_function():
    logger.debug("Debugging details")
    logger.info("Application started")
    logger.warning("Low disk space")
    logger.error("Failed to connect to database")
    logger.critical("Application crash")

if __name__ == "__main__":
    sample_function()
```

---

## **3. Logging in Cloud Run**
When running in **Google Cloud Run**, structured logging can be enabled for better integration with **Cloud Logging**:

### **Structured Logging (JSON Format)**
```python
import logging
import json
import sys

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record, self.datefmt),
            "severity": record.levelname,
            "message": record.getMessage(),
            "name": record.name,
            "module": record.module,
            "funcName": record.funcName,
        }
        return json.dumps(log_entry)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("myApp")
logger.handlers[0].setFormatter(JsonFormatter())

# Sample log messages
logger.info("Service started successfully")
logger.error("Error processing request")
```

**Output in Cloud Logging:**
```json
{
  "timestamp": "2025-02-04 15:30:01",
  "severity": "INFO",
  "message": "Service started successfully",
  "name": "myApp",
  "module": "main",
  "funcName": "<module>"
}
```

---

## **4. Comparison with Spring Boot Logging**
- **Spring Boot**: Uses Logback/SLF4J, supports different log levels and structured logging (JSON, XML).
- **Python**: Uses `logging` module, configurable for various handlers (console, file, HTTP), supports JSON formatting.

## **Summary**
- Configure Python logging to mimic Spring Boot with `logging` or `logging.config`.
- Use **JSON formatting** for structured logging in **Cloud Run** or other cloud services.
- Utilize **configuration files** for reusable, centralized logging settings.

Would you like examples for specific use cases or log message formats? 🚀
