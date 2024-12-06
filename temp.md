In Terraform, you can capture the value of an output variable or resource attribute, then use it to configure additional resources dynamically. Here's how you can achieve that:

---

### **1. Capturing an Output Variable Value**
Define an **output** in your module or Terraform configuration to capture a specific value:

```hcl
output "captured_name" {
  value = google_cloud_run_service.example_service.name
}
```

When you apply your Terraform configuration, you can reference this output programmatically in subsequent configurations or resources.

---

### **2. Using the Captured Output**
You can use the captured value directly as an input for another resource. Here's an example:

#### Example: Capture a Cloud Run Service Name and Use It in a Pub/Sub Subscription
```hcl
resource "google_cloud_run_service" "example_service" {
  name     = "my-cloud-run-service"
  location = "us-central1"

  template {
    spec {
      containers {
        image = "gcr.io/my-project/my-image:latest"
      }
    }
  }
}

resource "google_pubsub_topic" "example_topic" {
  name = "example-topic"
}

# Create a subscription with the captured name as part of its ID
resource "google_pubsub_subscription" "example_subscription" {
  name  = "${google_cloud_run_service.example_service.name}-subscription"
  topic = google_pubsub_topic.example_topic.name
}

output "captured_service_name" {
  value = google_cloud_run_service.example_service.name
}
```

---

### **3. Using Variables for Dynamic Configuration**
If you're working with multiple configurations, you can combine the output into a variable to dynamically configure resources:

```hcl
variable "cloud_run_service_name" {
  description = "Name of the Cloud Run service"
  type        = string
}

resource "google_cloud_run_service_iam_member" "invoker" {
  service  = var.cloud_run_service_name
  location = "us-central1"
  role     = "roles/run.invoker"
  member   = "serviceAccount:my-service-account@my-project.iam.gserviceaccount.com"
}
```

To pass the captured value:
```hcl
module "dynamic_resources" {
  source = "./modules/resource_module"

  cloud_run_service_name = google_cloud_run_service.example_service.name
}
```

---

### **4. Dynamically Configure Additional Resources**
If you want to append or modify a value for new resources:
```hcl
# Example appending a suffix to the captured name
resource "google_storage_bucket" "example_bucket" {
  name     = "${google_cloud_run_service.example_service.name}-bucket"
  location = "US"
}
```

---

### **5. Viewing the Captured Output**
To view an output value after `terraform apply`, run:
```bash
terraform output captured_name
```

If you only need the raw value for scripting, use:
```bash
terraform output -raw captured_name
```

---

### **Summary**
- Use resource attributes or module outputs to capture values.
- Use dynamic names by interpolating captured values with `${}`.
- Pass outputs to variables for modular or multi-stage configurations.
- Use the `-raw` option if you only need the variable value directly for external usage. 

Let me know if you need a more specific example!
