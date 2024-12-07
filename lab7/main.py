import re


def extract_bytes(entry: str) -> int:
    """Extract the number of bytes sent from the given entry"""
    return int(re.findall(r"\d{3} (\d*) ", entry)[0])


def sum_bytes_sent_and_received(nginx_log_path: str) -> int:
    """Calculate the total number of bytes sent and received in the log file of nginx"""
    with open(nginx_log_path, "r") as f:
        bytes_sum = sum(extract_bytes(line) for line in f)
    return bytes_sum


def main():
    nginx_log_path = "2017_05_07_nginx.txt"
    print(sum_bytes_sent_and_received(nginx_log_path))


if __name__ == "__main__":
    main()
