Here's a **complete step-by-step example** to create a **Cloud Run service that is private** and make it **accessible from a GKE pod**:

---

## **1. Create a VPC Network and Subnet**

### **Create a custom VPC Network:**
```bash
gcloud compute networks create my-vpc \
    --subnet-mode=custom
```

### **Create a Subnet in the VPC:**
```bash
gcloud compute networks subnets create my-subnet \
    --network=my-vpc \
    --region=REGION \
    --range=10.0.0.0/24
```

---

## **2. Set Up GKE Cluster**

### **Create a GKE Cluster in the VPC:**
```bash
gcloud container clusters create my-gke-cluster \
    --region=REGION \
    --network=my-vpc \
    --subnetwork=my-subnet \
    --workload-pool=PROJECT_ID.svc.id.goog
```

### **Get Cluster Credentials:**
```bash
gcloud container clusters get-credentials my-gke-cluster \
    --region=REGION
```

---

## **3. Create a VPC Connector**

### **Create a VPC Connector for Cloud Run:**
```bash
gcloud compute networks vpc-access connectors create my-vpc-connector \
    --region=REGION \
    --network=my-vpc \
    --range=10.8.0.0/28
```

---

## **4. Deploy a Private Cloud Run Service**

### **Deploy a Cloud Run Service:**
```bash
gcloud run deploy my-cloud-run-service \
    --image=gcr.io/PROJECT_ID/my-image \
    --region=REGION \
    --vpc-connector=my-vpc-connector \
    --ingress=internal \
    --allow-unauthenticated
```

### **Verify the Service URL:**
```bash
gcloud run services describe my-cloud-run-service \
    --region=REGION \
    --format="value(status.url)"
```
The URL will look like this:  
`https://my-cloud-run-service-<ID>.a.run.internal`

---

## **5. Configure Private DNS for Cloud Run**

### **Create a Private DNS Zone:**
```bash
gcloud dns managed-zones create private-cloud-run \
    --dns-name="a.run.internal." \
    --visibility=private \
    --networks=my-vpc
```

---

## **6. Grant GKE Access to Cloud Run**

### **Find the GKE Node Service Account:**
```bash
gcloud container clusters describe my-gke-cluster \
    --region=REGION \
    --format="value(nodeConfig.serviceAccount)"
```

### **Grant `roles/run.invoker` Permission:**
```bash
gcloud run services add-iam-policy-binding my-cloud-run-service \
    --member=serviceAccount:<GKE_NODE_SERVICE_ACCOUNT> \
    --role=roles/run.invoker
```

---

## **7. Deploy a GKE Pod to Access Cloud Run**

### **Create a Deployment in GKE:**
Save the following YAML file as `pod-access-cloud-run.yaml`:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cloud-run-client
spec:
  replicas: 1
  selector:
    matchLabels:
      app: cloud-run-client
  template:
    metadata:
      labels:
        app: cloud-run-client
    spec:
      containers:
      - name: curl-container
        image: curlimages/curl:latest
        command: ["/bin/sh", "-c", "sleep 3600"]
        env:
        - name: CLOUD_RUN_URL
          value: "https://my-cloud-run-service-<ID>.a.run.internal"
```

### **Apply the Deployment:**
```bash
kubectl apply -f pod-access-cloud-run.yaml
```

### **Verify the Pod is Running:**
```bash
kubectl get pods
```

---

## **8. Test Access to Cloud Run**

### **Open a Shell in the Pod:**
```bash
kubectl exec -it $(kubectl get pods -l app=cloud-run-client -o jsonpath='{.items[0].metadata.name}') -- /bin/sh
```

### **Fetch the Cloud Run Service:**
Generate an identity token and call the service:
```bash
TOKEN=$(curl -H "Metadata-Flavor: Google" \
  http://metadata/computeMetadata/v1/instance/service-accounts/default/identity?audience=https://my-cloud-run-service-<ID>.a.run.internal)

curl -H "Authorization: Bearer $TOKEN" $CLOUD_RUN_URL
```

---

## **9. Debug and Verify**

- Ensure DNS is resolving the `a.run.internal` domain inside the GKE pod:
  ```bash
  nslookup my-cloud-run-service-<ID>.a.run.internal
  ```

- Ensure IAM permissions are correct for the GKE service account.

- Ensure the firewall allows communication from GKE to the VPC Connector subnet.

---

### **Considerations**
- **Scaling:** Ensure the VPC connector and Cloud Run have sufficient capacity for concurrent connections.
- **Security:** Use Workload Identity to avoid hardcoding credentials.
- **Timeouts:** Adjust timeout settings in both GKE and Cloud Run to prevent disconnections.

Let me know if you need further assistance!
