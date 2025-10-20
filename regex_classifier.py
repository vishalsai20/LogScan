import re

def classify_with_regex(log_message):
    regex_patterns = {
        r"User User\d+ logged (in|out).": "User Action",
        r"Backup (started|ended) at .*": "System Notification",
        r"Backup completed successfully.": "System Notification",
        r"System updated to version .*": "System Notification",
        r"File .* uploaded successfully by user .*": "System Notification",
        r"Disk cleanup completed successfully.": "System Notification",
        r"System reboot initiated by user .*": "System Notification",
        r"Account with ID \S+ created by User\S+.": "User Action"
    }
    for pattern, label in regex_patterns.items():
        if re.search(pattern, log_message):
            return label
    return None

if __name__ == "__main__":
    print(classify_with_regex("Backup completed successfully."))
    print(classify_with_regex("Account with ID 1 created by User1."))
    print(classify_with_regex("System restarted successfully"))
    print(classify_with_regex("mail service experiencing issues with sending"))
    print(classify_with_regex("Good Morning from IT"))
    print(classify_with_regex("User User12 logged in."))