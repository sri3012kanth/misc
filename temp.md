Here's a fully automated setup using Docker and Docker Compose that ensures key generation, permissions, and configurations are handled inside the container.

---

## **1️⃣ Directory Structure**
```
sftp-server/
│── docker-compose.yml
│── Dockerfile
│── sftp_setup.sh
│── sftp_key (generated automatically)
│── sftp_key.pub (generated automatically)
```

---

## **2️⃣ `Dockerfile` (Automates Key Setup & Permissions)**
```dockerfile
FROM atmoz/sftp

# Create user and directories
RUN mkdir -p /home/user/.ssh /home/user/upload \
    && chmod 700 /home/user/.ssh /home/user/upload

# Copy script to setup SSH keys and set permissions
COPY sftp_setup.sh /sftp_setup.sh
RUN chmod +x /sftp_setup.sh

# Execute script on container startup
CMD ["/bin/sh", "-c", "/sftp_setup.sh && exec /entrypoint user:1001:1001"]
```

---

## **3️⃣ `sftp_setup.sh` (Automates Key Generation & Permissions)**
```sh
#!/bin/sh

# Generate SSH key pair if not exists
if [ ! -f "/home/user/.ssh/sftp_key" ]; then
    ssh-keygen -t rsa -b 4096 -f /home/user/.ssh/sftp_key -q -N ""
fi

# Set permissions
chmod 700 /home/user/.ssh
chmod 600 /home/user/.ssh/sftp_key
chmod 644 /home/user/.ssh/sftp_key.pub

# Ensure authorized_keys exists
cat /home/user/.ssh/sftp_key.pub > /home/user/.ssh/authorized_keys
chmod 600 /home/user/.ssh/authorized_keys
```

---

## **4️⃣ `docker-compose.yml` (Automates Deployment)**
```yaml
version: "3.8"

services:
  sftp:
    build: .
    container_name: sftp_server
    ports:
      - "2222:22"
    volumes:
      - ./sftp_data:/home/user/upload
    restart: always
```

---

## **5️⃣ Deploy & Connect**
### **🚀 Build & Run**
```sh
docker-compose up -d --build
```

### **🔑 Fetch Generated Private Key**
```sh
docker cp sftp_server:/home/user/.ssh/sftp_key .
chmod 600 sftp_key
```

### **🔗 Connect to SFTP Server**
```sh
sftp -i sftp_key -P 2222 user@localhost
```

---

### **✅ Features:**
✅ Automated SSH key generation  
✅ Correct permissions handled inside Docker  
✅ One-command deployment  
✅ Persistent SFTP storage  

This is a **fully automated** SFTP test server running on Docker! 🚀
