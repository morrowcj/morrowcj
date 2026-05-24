Source for this info: https://gist.github.com/luckygoswami/3f7cd9a2a7787314d44290941f0665f3

#### **Title:** 🔑 How to Import and Configure an Existing GPG Key on a New System

#### **Description:**

Step-by-step guide to transfer and set up an old GPG key (for Git commit signing) on a new machine.

---

### **1. Export Keys from Old System**

_(Skip if you already have the key files)_

#### **Export Private Key:**

```bash
gpg --export-secret-keys --armor YOUR_KEY_ID > private-key.asc
```

- Replace `YOUR_KEY_ID` with your key’s fingerprint or email.

#### **Export Public Key:**

```bash
gpg --export --armor YOUR_KEY_ID > public-key.asc
```

#### **Export Trust DB (Optional):**

```bash
gpg --export-ownertrust > trustdb.txt
```

---

### **2. Transfer Files to New System**

Copy these files to the new machine:

- `private-key.asc`
- `public-key.asc` (optional, if needed)
- `trustdb.txt` (optional)

---

### **3. Import Keys on New System**

#### **Install GPG**

- **Linux:** `sudo apt install gnupg`
- **Mac:** `brew install gnupg`
- **Windows:** [GPG4Win](https://gpg4win.org/)

#### **Open Bash in the same directory as your keys**

#### **Import Private Key:**

```bash
gpg --import private-key.asc
```

#### **Import Public Key (if separate):**

```bash
gpg --import public-key.asc
```

#### **Import Trust DB (Optional):**

```bash
gpg --import-ownertrust trustdb.txt
```

---

### **4. Verify Imported Keys**

```bash
gpg --list-secret-keys --keyid-format LONG
```

Check if your key appears.

---

### **5. Configure Git to Use GPG**

#### **Set Key for Git:**

```bash
git config --global user.signingkey YOUR_KEY_ID
```

#### **Enable Commit Signing:**

```bash
git config --global commit.gpgsign true
```

#### **Enable Tag Signing (Optional):**

```bash
git config --global tag.gpgsign true
```

#### **Set GPG Program Path on Windows (Optional):**

```bash
git config --global gpg.program "C:\Program Files (x86)\GnuPG\bin\gpg.exe"
```

---

### **7. Add GPG Key to GitHub**

_(Skip if the key already exists in GitHub account)_

1. Get your public key:
   ```bash
   gpg --armor --export YOUR_KEY_ID
   ```
2. Paste it at:  
   **GitHub → Settings → SSH and GPG Keys → New GPG Key**

---

✅ **Done!** Your old GPG key is now active on the new system.

