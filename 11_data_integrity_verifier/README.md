## Data Integrity Verification Tool

### Project Overview

This command-line tool, written in Java, demonstrates a core cybersecurity principle: **data integrity**. It uses the **SHA-256 cryptographic hashing algorithm** to generate a unique digital fingerprint for any file. This allows for the verification of a file's integrity, ensuring that it has not been altered or tampered with. This is a critical function in cybersecurity for preventing unauthorized file modification, detecting malware, and ensuring the trustworthiness of data.

---

### Key Concepts Demonstrated

* **Data Integrity:** Ensuring that data has not been altered or destroyed in an unauthorized manner.
* **Cryptographic Hashing:** Creating a fixed-size, unique "fingerprint" of a piece of data. SHA-256 is an industry-standard algorithm.
* **File I/O:** Reading and writing files on the system, a fundamental skill for many security tools.
* **Error Handling:** Gracefully managing potential issues like file-not-found errors.

---

### How to Compile and Run the Program

**Compile the code:**

```powershell
javac FileIntegrityVerifier.java
```

**Run the program:**

```powershell
java FileIntegrityVerifier
```

---

### Example Usage

#### Generating a Hash
When you first run the tool, you can generate a hash for a file. For this example, let's assume we have a file named `important_document.txt`.

The tool will create a new file, `important_document.txt.sha256`, containing the calculated hash.

#### Verifying File Integrity
Later, you can verify the integrity of the original file. The tool will re-calculate the hash and compare it to the saved one.

* **Scenario 1: The file is unchanged.**
* **Scenario 2: The file has been modified.**

If even a single character in `important_document.txt` has changed, the new SHA-256 hash will be completely different.

---

### Code Snippet: The Hashing Logic

The core of this tool is the `calculateSha256` method. It uses Java's built-in `MessageDigest` class to perform the SHA-256 hashing.

```java
private static String calculateSha256(String filePath) throws IOException, NoSuchAlgorithmException {
    MessageDigest md = MessageDigest.getInstance("SHA-256");
    try (FileInputStream fis = new FileInputStream(filePath);
            DigestInputStream dis = new DigestInputStream(fis, md)) {
        // Read the file to update the message digest
        while (dis.read() != -1) ;
        md = dis.getMessageDigest();
    }

    StringBuilder result = new StringBuilder();
    for (byte b : md.digest()) {
        result.append(String.format("%02x", b));
    }
    return result.toString();
}
```

This method is efficient because it reads the file in chunks, allowing it to handle large files without consuming excessive memory.

### Future Improvements

**Implement other hashing algorithms (e.g., `MD5`, `SHA-512`) for comparison.**

**Add functionality to hash an entire directory of files.**

**Develop a graphical user interface (GUI) for easier use.**

---
