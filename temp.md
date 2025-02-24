To configure **Public Key Authentication** and set the `AuthorizedKeysFile` correctly inside a Docker container running an SFTP server, follow these steps:

---

## **1️⃣ Modify SSH Configuration in the Docker Container**
Since OpenSSH inside the container controls authentication, we need to explicitly enable **public key authentication**.

### **Create a Custom `sshd_config` File**
Inside your project directory, create `sshd_config` with the following content:

📌 **`sshd_config`**
```plaintext
# Enable public key authentication
PubkeyAuthentication yes

# Set the file where SSH looks for authorized keys
AuthorizedKeysFile /home/%u/.ssh/authorized_keys

# Disable password authentication
PasswordAuthentication no

# Allow root login only with keys (optional, improves security)
PermitRootLogin prohibit-password

# Use the standard port for SSH (inside the container)
Port 22
```

---

## **2️⃣ Modify Dockerfile to Use the Custom Config**
Now, update the **Dockerfile** to copy this config into the container.

📌 **`Dockerfile`**
```dockerfile
FROM atmoz/sftp

# Create required directories
RUN mkdir -p /home/user/.ssh /etc/ssh

# Copy the custom SSH configuration file
COPY sshd_config /etc/ssh/sshd_config

# Copy public key for authentication
COPY sftp_ssh_key.pub /home/user/.ssh/authorized_keys

# Set permissions
RUN chmod 700 /home/user/.ssh && \
    chmod 600 /home/user/.ssh/authorized_keys && \
    chown -R user:user /home/user/.ssh

# Expose SFTP Port
EXPOSE 22

# Start SSHD
CMD ["/entrypoint", "user:1001:1001"]
```

---

## **3️⃣ Modify `docker-compose.yml`**
Ensure your `docker-compose.yml` correctly maps volumes and ports.

📌 **`docker-compose.yml`**
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

## **4️⃣ Build and Start the SFTP Server**
```sh
docker-compose up -d --build
```

---

## **5️⃣ Verify SSH Configuration Inside the Container**
After starting the container, connect to it:
```sh
docker exec -it sftp_server sh
```
Then check if the SSH configuration is applied correctly:
```sh
grep "PubkeyAuthentication" /etc/ssh/sshd_config
grep "AuthorizedKeysFile" /etc/ssh/sshd_config
```
Expected output:
```
PubkeyAuthentication yes
AuthorizedKeysFile /home/%u/.ssh/authorized_keys
```

If correct, restart SSH inside the container:
```sh
service ssh restart
```

---

## **6️⃣ Test SFTP Connection**
On your local machine, connect using:
```sh
sftp -i sftp_ssh_key -P 2222 user@localhost
```
If everything is set up correctly, it should authenticate without asking for a password.

---

## **✅ Summary**
✔ **Enabled** Public Key Authentication (`PubkeyAuthentication yes`)  
✔ **Set `AuthorizedKeysFile`** to `/home/%u/.ssh/authorized_keys`  
✔ **Disabled Password Authentication** for security  
✔ **Configured Everything in Docker** for automation  

Now your **SFTP server in Docker fully supports public key authentication!** 🚀 Let me know if you need any tweaks!
