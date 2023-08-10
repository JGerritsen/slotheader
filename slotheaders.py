#!/usr/bin/env python3
import os
import sys
import argparse
import requests
import threading

def save_headers(url, save_dir):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            headers = response.headers
            filename = os.path.join(save_dir, f"{url.replace('://', '_').replace('/', '_').replace('.', '_')}.headers")
            with open(filename, 'w') as f:
                for key, value in headers.items():
                    f.write(f"{key}: {value}\n")
            return True
        else:
            print(f"Failed to retrieve headers for {url}. Status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error while making the request: {e}")
        return False

def process_url(url, save_dir):
    if save_headers(url, save_dir):
        print(f"Headers saved for: {url}")

def main():
    banner = """
	⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⢠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠣⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡼⠤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣶⣾⢿⡳⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠉⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠙⢿⣿⣮⣿⣶⣄⠀⠀⠀⠀⣀⣀⣀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣶⣶⣒⣒⣿⣿⣿⣿⡿⠿⠿⠿⢿⣿⣛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣯⣽⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣷⠯⠁⠀⠀⣀⠤⠤⢄⠈⠉⢻⣷⣶⣶⣿⣿⣿⣿⣿⣿⠿⣿⣿⣿⣽⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⢛⠏⠀⠀⣀⠎⠀⠀⠀⠀⠘⢄⠀⢏⠉⣉⣏⣉⡉⠉⡏⠀⠀⠈⢋⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡌⠀⡔⠉⠀⠀⠀⠀⠺⠇⠀⢸⠀⢸⠁⠀⠀⠀⠀⠀⠃⠀⠀⠀⠘⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢇⢰⠀⠀⢀⣤⠀⠚⡠⠀⠀⡘⠠⠃⠀⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡄⢄⠀⠀⠀⠀⢸⡀⠣⡀⠀⠁⠀⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠂⠀⠀⠀⡸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠻⢀⠇⡠⢀⠀⠀⠡⠢⡈⠑⠒⠒⠒⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡰⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⣐⣒⡳⠴⠋⠀⠀⠀⠀⠀⠉⠁⠉⢇⠀⠀⠀⠀⡄⠀⠀⠀⠀⠀⠀⠀⢀⠠⠊⢀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠉⠀⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠸⡉⠀⠒⠒⠒⠂⠉⠀⠀⠀⣎⡸⣀⡖⣉⣐⠄⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣄⠀⠀⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⡀⠚⣍⠢⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠈⠑⢶⢾⠙⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣆⢉⣲⠥⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠤⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠀⡀⠀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠉⠀⠀⠀⠀⠈⠈⠉⠈⠈⠁⠂⠈⠈⠁⠉⠀⠈⠁⠈⠘⠀⠁⠈⠈⠈⠁⠀⠀⠀⠀
    """
    print(banner)
    print("Welcome to the Slothberry HTTP Headers Saver!\n")

    parser = argparse.ArgumentParser(description="Save HTTP headers of given URLs.")
    parser.add_argument("target", help="URL or filepath containing URLs")
    parser.add_argument("--save-dir", help="Directory to save headers files", default=".")
    parser.add_argument("--single-thread", help="Disable multithreading", action="store_true")
    args = parser.parse_args()

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    if os.path.isfile(args.target):
        with open(args.target, 'r') as file:
            urls = file.read().splitlines()
    else:
        urls = [args.target]

    if args.single_thread:
        for url in urls:
            process_url(url, args.save_dir)
    else:
        threads = []
        for url in urls:
            thread = threading.Thread(target=process_url, args=(url, args.save_dir))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    print("\nHeaders saved successfully!")
    print(f"Saved {len(urls)} file(s) in directory: {os.path.relpath(args.save_dir)}")

if __name__ == "__main__":
    main()
