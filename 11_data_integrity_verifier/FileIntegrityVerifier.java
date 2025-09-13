import java.util.*;
import java.util.Scanner;
import java.io.FileInputStream;
import java.io.IOException;
import java.security.DigestInputStream;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;


public class FileIntegrityVerifier {
    // The main method serves as the entry point for the program
	public static void main(String[] args) {   
        Scanner scanner = new Scanner(System.in);

        while (true) { //This creates an infinite loop to keep the menu running
            System.out.println("\n--- File Integrity Verifier ---");
            System.out.println("1. Generate SHA-256 hash for a file");
            System.out.println("2. Verify file integrity");
            System.out.println("3. Exit");
            System.out.print("Choose an option (1-3): ");
            
            int choice;
            try {
                choice = Integer.parseInt(scanner.nextLine());
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a number between 1 and 3.");
                continue; // Skips the rest of the Loop and starts from the top
            }

            switch (choice) {
                case 1:
                    //System.out.println("Generate hash functionality coming soon...");
                    generateHash(scanner); // Replaces the "coming soon" placeholder
                    break;
                case 2:
                    //System.out.println("Verify integrity functionality coming soon...");
                    verifyIntegrity(scanner); // Replaces the "coming soon" placeholder
                    break;
                case 3:
                    System.out.println("Exiting the program. Goodbye!");
                    scanner.close(); // Important close the scanner to prevent resource leaks
                    return; // This exits the main method, ending the program
                default:
                    System.out.println("Invalid choice. Please select a valid option (1-3).");
            }
        }
    }

    //Orchestrates the hash generation process
    private static void generateHash(Scanner scanner) {
        System.out.print("Enter the file path to generate the hash for: ");
        String filePath = scanner.nextLine();

        try {
            String hash = calculateSha256(filePath); // Call our core logic
            System.out.println("SHA-256 Hash: " + hash);
            saveHashToFile(filePath, hash); // Save te hash for later
        } catch (IOException | NoSuchAlgorithmException e) {
            System.err.println("Error generating hash: " + e.getMessage());
        }
    }

    // Orchestrates the verification process
    private static void verifyIntegrity(Scanner scanner) {
        System.out.print("Enter the file path to verify: ");
        String filePath = scanner.nextLine();
        String hashFilePath = filePath + ".sha256"; // Assuming the hash is stored in a .sha256 file

        try { 
            if (!Files.exists(Paths.get(hashFilePath))) {
                System.out.println("Error: No hash file found for " + filePath);
                System.out.println("Would you like to generate a hash file now? (y/n): ");
                String response = scanner.nextLine();
                if (response.equalsIgnoreCase("y")) {
                    generateHash(scanner); // Call the hash generation method
                } else {
                    System.out.println("Verification aborted.");
                }
                return;
            }
    
            String storedHash = new String(Files.readAllBytes(Paths.get(hashFilePath))).trim();
            String currentHash = calculateSha256(filePath).trim(); // Recalculate the hash

            System.out.println("Stored Hash: " + storedHash);
            System.out.println("Current Hash: " + currentHash);

            if (storedHash.equals(currentHash)) {
                System.out.println("\n[SUCCESS] File integrity verified. The file has not been modified");
            } else {
                System.out.println("\n[WARNING] File integrity check FAILED. The file may have been tampered with.");
            }
        } catch (IOException | NoSuchAlgorithmException e) {
            System.err.println("Error verifying integrity: " + e.getMessage());
        }
    }

    // Core logic for calculating the SHA-256 hash of a file
    private static String calculateSha256(String filePath) throws IOException, NoSuchAlgorithmException {
        // 1. Get an instance of the SHA-256 algorithm
        MessageDigest md = MessageDigest.getInstance("SHA-256");

        // 2. Set up streams to read the file and feed it to the algorithm
        // This is a "try-with-resources" block, which automatically closes the streams
        try (FileInputStream fis = new FileInputStream(filePath);
            DigestInputStream dis = new DigestInputStream(fis, md)) {
            
            // 3. Read the file. The DigestInputStream does the hashing automatically.
            while (dis.read() != -1) ; // This loop reads the file until the end

            // 4. Get the resulting hash digest from the MessageDigest instance
            md = dis.getMessageDigest();
        }

        // 5. Convert the byte array into a hexadecimal string
        StringBuilder sb = new StringBuilder();
        for (byte b : md.digest()) {
            sb.append(String.format("%02x", b));
        }
        return sb.toString();
    }

    // A helper method for writing the hash to a file
    private static void saveHashToFile(String originalFilePath, String hash) throws IOException {
        Path hashFilePath = Paths.get(originalFilePath + ".sha256");
        Files.write(hashFilePath, hash.getBytes());
        System.out.println("Hash saved to: " + hashFilePath);
    } 
}

// End of FileIntegrityVerifier.java

// This Java program is a command-line tool for verifying file integrity using SHA-256 hashing.
// It allows users to generate a hash for a file and save it, and later verify the file's integrity by comparing the current hash with the stored hash.
// The program demonstrates key cybersecurity concepts such as data integrity, cryptographic hashing, and secure file handling.
// Key features include:
// - User-friendly menu for generating hashes and verifying integrity
// - SHA-256 hashing algorithm for secure and reliable hashing
// - File I/O operations for reading files and saving hashes
// - Error handling for common issues like file not found or invalid input

// The program is structured with clear methods for each functionality, making it easy to understand and maintain.
/*
* Example Interaction:
*
*    --- File Integrity Verifier ---
*    1. Generate SHA-256 hash for a file
*    2. Verify file integrity
*    3. Exit
*    Choose an option (1-3): 1
*    Enter the file path to generate the hash for: ~/File_Integrity_Verifier/README.txt
*    SHA-256 Hash: d92c54d829c05e8a5391c526c79785dae7377a2996cf41bd60521cdcfb266a16
*    Hash saved to: ~/File_Integrity_Verifier/README.txt.sha256
*
*    --- File Integrity Verifier ---
*    1. Generate SHA-256 hash for a file
*    2. Verify file integrity
*    3. Exit
*    Choose an option (1-3): 2
*    Enter the file path to verify: ~/File_Integrity_Verifier/README.txt
*    Stored Hash: d92c54d829c05e8a5391c526c79785dae7377a2996cf41bd60521cdcfb266a16
*    Current Hash: d92c54d829c05e8a5391c526c79785dae7377a2996cf41bd60521cdcfb266a16
*
*    [SUCCESS] File integrity verified. The file has not been modified
*
*    --- File Integrity Verifier ---
*    1. Generate SHA-256 hash for a file
*    2. Verify file integrity
*    3. Exit
*    Choose an option (1-3): 3
*    Exiting the program. Goodbye!
*/