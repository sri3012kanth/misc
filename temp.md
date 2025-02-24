To configure the SFTP server with certificate-based authentication using a locally generated certificate (instead of SSH key pairs), follow these steps:

---

## **1️⃣ Generate an SSL Certificate for SFTP**
We will generate a self-signed certificate and use it for authentication.

### **Generate a Key Pair & Certificate**
Run the following command in your terminal to generate a private key and public certificate:
```sh
openssl req -x509 -newkey rsa:4096 -keyout sftp_server.key -out sftp_server.crt -days 365 -nodes
```
This will create:
- **`sftp_server.key`** → Private key
- **`sftp_server.crt`** → Public certificate

---

## **2️⃣ Convert Certificate to SSH Format**
SFTP (OpenSSH) does not directly use X.509 certificates. We must convert it into an SSH key pair.

### **Generate an SSH Private Key from the SSL Key**
```sh
ssh-keygen -t rsa -b 4096 -f sftp_ssh_key -m PEM
```
This will create:
- **`sftp_ssh_key`** (private key)
- **`sftp_ssh_key.pub`** (public key)

### **Convert OpenSSH Key to X.509 Format**
```sh
ssh-keygen -s sftp_server.key -I sftp_cert -n user -V +365d sftp_ssh_key.pub
```
This signs the SSH key using our SSL certificate.

---

## **3️⃣ Setup Dockerized SFTP Server**
Create a **Dockerfile** to configure the SFTP server.

### **📌 `Dockerfile`**
```dockerfile
FROM atmoz/sftp

# Create required directories
RUN mkdir -p /home/user/.ssh /home/user/upload

# Copy keys and certificates
COPY sftp_ssh_key.pub /home/user/.ssh/authorized_keys

# Set proper permissions
RUN chmod 700 /home/user/.ssh && \
    chmod 600 /home/user/.ssh/authorized_keys

# Start the container
CMD ["/entrypoint", "user:1001:1001"]
```

---

## **4️⃣ `docker-compose.yml`**
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

## **5️⃣ Start the SFTP Server**
```sh
docker-compose up -d --build
```

---

## **6️⃣ Connect to the SFTP Server**
Copy the private key to the correct permissions:
```sh
chmod 600 sftp_ssh_key
```
Then, connect using:
```sh
sftp -i sftp_ssh_key -P 2222 user@localhost
```

---

### **✅ Features:**
✔ Uses self-signed certificates for authentication  
✔ Automates everything in Docker  
✔ No password required  

This method ensures a **secure SFTP setup with certificate-based authentication** inside Docker! 🚀
