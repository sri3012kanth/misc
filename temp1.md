To write each Pub/Sub message to the console with a sequence number, you can use a counter to track the sequence of messages as they are processed. Below is an updated version of the Python subscriber script to include this functionality.

---

### **Python Code**

```python
import os
from google.cloud import pubsub_v1
import json
from concurrent.futures import TimeoutError

# Set up environment for Pub/Sub Emulator
os.environ["PUBSUB_EMULATOR_HOST"] = "localhost:8085"

# Pub/Sub configuration
project_id = "my-project-id"
subscription_id = "my-subscription-id"
timeout = 60.0  # Time to listen for messages (seconds)

# Global counter for sequence numbers
sequence_number = 1

def process_message_with_sequence(message, seq_num):
    """Log the message with a sequence number."""
    message_content = {
        "sequence_number": seq_num,
        "message_id": message.message_id,
        "data": message.data.decode("utf-8"),
        "attributes": message.attributes
    }

    # Print to console
    print(f"Sequence {seq_num}: {json.dumps(message_content, indent=2)}")

    # Return processed content for other uses (e.g., file writing)
    return message_content

def callback(message):
    """Callback function to process messages."""
    global sequence_number
    try:
        # Log and process message with sequence number
        process_message_with_sequence(message, sequence_number)
        sequence_number += 1

        # Acknowledge the message
        message.ack()
    except Exception as e:
        print(f"Failed to process message: {e}")
        message.nack()  # Not acknowledge the message for retry

def main():
    """Main function to subscribe to Pub/Sub and listen for messages."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    print(f"Listening for messages on {subscription_path}...")
    
    with subscriber:
        streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
        print("Subscriber started.")

        try:
            streaming_pull_future.result(timeout=timeout)  # Timeout for listener
        except TimeoutError:
            streaming_pull_future.cancel()  # Stop the subscriber
            print("Listening timeout. Stopping subscriber.")
        except Exception as e:
            print(f"An error occurred: {e}")
            streaming_pull_future.cancel()

if __name__ == "__main__":
    main()
```

---

### **Key Changes for Sequence Number**

1. **Global Counter**:
   - The variable `sequence_number` is a global counter incremented for each processed message.

2. **Logging with Sequence**:
   - The `process_message_with_sequence` function formats and logs the message to the console with the sequence number.
   - The message is printed in a structured JSON format for readability.

---

### **Sample Console Output**

When you run the script, the console output will look like this:

```
Listening for messages on projects/my-project-id/subscriptions/my-subscription-id...
Subscriber started.
Sequence 1: {
  "sequence_number": 1,
  "message_id": "1",
  "data": "Hello, Pub/Sub! Message 0",
  "attributes": {}
}
Sequence 2: {
  "sequence_number": 2,
  "message_id": "2",
  "data": "Hello, Pub/Sub! Message 1",
  "attributes": {}
}
...
```

---

### **Optional Enhancements**

- **Thread Safety**: If you have a multi-threaded environment, consider using `threading.Lock` or an `itertools` generator to manage the sequence counter safely.
- **File Output**: You can combine this logic with file writing if needed.
- **Custom Logging**: Use the `logging` module instead of `print` for better control over log levels and output formatting.

This script will log messages sequentially to the console with a unique sequence number for each message received.
