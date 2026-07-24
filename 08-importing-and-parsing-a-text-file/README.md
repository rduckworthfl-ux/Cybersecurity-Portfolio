# Algorithm for Automated Access Control

## Project Description

This project focuses on maintaining an up-to-date access control list (ACL) for employees permitted to view restricted healthcare content. In this scenario, access is managed by an allow-list of IP addresses.

To ensure security and compliance with patient data privacy, this file must be regularly updated to remove access for employees who have changed roles or left the organization. I developed a Python script that automates this process by cross-referencing the current allow-list against a "remove list" of unauthorized IP addresses, ensuring that only active, authorized personnel retain access.

## Scenario & Strategy

The goal is to sanitize the `allow_list.txt` file by removing specific IP addresses identified in a `remove_list`. The algorithm follows these core steps:

1. **Ingest** the current allow-list from a text file.
2. **Convert** the file data into a list format for processing.
3. **Iterate** through the data to identify and remove unauthorized IP addresses.
4. **Update** the original file with the sanitized list.

## Code Walkthrough

### 1. Define Variables and Open the File

First, I assigned the filename `allow_list.txt` to the `import_file` variable and defined the `remove_list` containing the IP addresses that needed to be revoked.

I used the `with` statement to open the file. This is a best practice in Python as it acts as a context manager, ensuring the file closes properly even if an error occurs during execution.

```python
import_file = "allow_list.txt"
remove_list = ["192.168.97.225", "192.168.158.170", "192.168.201.40", "192.168.58.57"]

with open(import_file, "r") as file:
    # Logic proceeds here

```

### 2. Read and Parse the Data

Once the file was open, I used the `.read()` method to convert the file contents into a single string. To manipulate individual IP addresses, I then used the `.split()` method. This converted the string into a list (`ip_addresses`), where each element represented one IP address.

```python
    ip_addresses = file.read()
    ip_addresses = ip_addresses.split()

```

### 3. Iterate and Remove Unauthorized Access

I implemented a `for` loop to iterate through the newly created `ip_addresses` list. Inside the loop, I used an `if` statement to check if the current `element` (IP address) existed in the `remove_list`.

If a match was found, I applied the `.remove()` method to delete that specific IP address from the `ip_addresses` list.

```python
    for element in ip_addresses:
        if element in remove_list:
            ip_addresses.remove(element)

```

### 4. Update the Source File

After the list was sanitized, I needed to write the changes back to the file. First, I used the `.join()` method to convert the list back into a string, using a newline character or space as the separator.

Finally, I opened the file again using `with open(import_file, "w")`. The `"w"` argument indicates "write" mode, which completely overwrites the existing file content with the updated, secure data.

```python
ip_addresses = "\n".join(ip_addresses)

with open(import_file, "w") as file:
    file.write(ip_addresses)

```

## Summary

This algorithm automates the critical task of managing network access permissions. By reading the current `allow_list.txt`, converting it into a manipulatable list, and iteratively removing unauthorized IP addresses, the script ensures that the access control file remains accurate and secure. Utilizing Python's file handling capabilities makes this security operation efficient, repeatable, and less prone to human error than manual updates.
