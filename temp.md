To generate and configure **SSH RSA certificates** for your SFTP server running in the Docker container (using the `atmoz/sftp` image), follow these steps:

### **Steps to Generate and Configure RSA SSH Keys for SFTP**

#### **1. Generate SSH RSA Key Pair (Private and Public Keys)**

You can generate an RSA key pair (private and public keys) using `ssh-keygen`. Here's how:

1. **Generate RSA Key Pair**:
   On your local machine, use the following command to generate an RSA key pair with a 2048-bit key length (you can adjust the bit length as needed):

   ```sh
   ssh-keygen -t rsa -b 2048 -f ~/.ssh/sftp_rsa_key
   ```

   This will generate two files:
   - `~/.ssh/sftp_rsa_key`: Private key (keep it secure).
   - `~/.ssh/sftp_rsa_key.pub`: Public key (you will copy this to the Docker container).

2. **Set Proper Permissions for the Private Key** (Local machine):
   Make sure the private key file has the correct permissions:

   ```sh
   chmod 600 ~/.ssh/sftp_rsa_key
   ```

#### **2. Copy the Public Key to the Docker Container**

1. **Copy the Public Key** into the container’s `/home/user/.ssh/authorized_keys`:

   First, copy the public key (`sftp_rsa_key.pub`) from your local machine to the Docker container. You can do this by using the `docker cp` command:

   ```sh
   docker cp ~/.ssh/sftp_rsa_key.pub <container_name_or_id>:/home/user/.ssh/authorized_keys
   ```

   Make sure the `.ssh` directory exists and has the correct permissions:

   ```sh
   docker exec -it <container_name_or_id> sh
   chmod 700 /home/user/.ssh
   chmod 600 /home/user/.ssh/authorized_keys
   ```

#### **3. Configure `sshd_config` for RSA Key Authentication**

Next, make sure the `sshd_config` file is set to allow RSA authentication.

1. **Update the `sshd_config`**:
   Ensure that the `sshd_config` file inside the container supports `ssh-rsa` key authentication. Here’s how you can modify or append the relevant settings in the `sshd_config`:

   - **Ensure RSA keys are enabled:**

     ```bash
     # Ensure ssh-rsa is supported
     PubkeyAcceptedAlgorithms ssh-rsa
     AuthorizedKeysFile .ssh/authorized_keys
     ```

2. **Restart SSH Service**:
   After making changes to the `sshd_config` file, restart the SSH service inside the container to apply the changes. If you are using the default `atmoz/sftp` image, it might not expose a direct `ssh` service to restart, but you can restart the container:

   ```sh
   docker restart <container_name_or_id>
   ```

#### **4. Connect Using the Private Key**

Finally, you can use the private key to authenticate with the SFTP server.

1. **Use SFTP to Connect**:

   ```sh
   sftp -i ~/.ssh/sftp_rsa_key -P 2222 user@localhost
   ```

   Replace `localhost` with the container's actual hostname or IP if necessary, and ensure that the private key (`sftp_rsa_key`) has the correct permissions.

---

### **Summary:**
1. **Generate an RSA Key Pair** using `ssh-keygen` on your local machine.
2. **Copy the Public Key** (`sftp_rsa_key.pub`) to the Docker container and place it in `/home/user/.ssh/authorized_keys`.
3. **Configure `sshd_config`** to support `ssh-rsa` by ensuring the relevant `PubkeyAcceptedAlgorithms` and `AuthorizedKeysFile` settings are correct.
4. **Restart the SSH service** by restarting the container.
5. **Connect using the private key** with the `-i` option in the `sftp` command.

After following these steps, you should be able to authenticate using the generated RSA key pair and securely transfer files via SFTP.
