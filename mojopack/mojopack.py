#!/usr/bin/env python3

import os
import requests
import argparse
from urllib.parse import urljoin
from tqdm import tqdm

def list_directories(repo_url, owner, repo_name):
    """
    List all directories under the specified GitHub repository.
    """
    api_url = urljoin(repo_url, f"repos/{owner}/{repo_name}/contents")
    response = requests.get(api_url)
    contents = response.json()

    directories = []
    for content in contents:
        if content['type'] == 'dir':
            directories.append(content['name'])

    return directories

def install_directory(repo_url, owner, repo_name, directory_name, target_path):
    """
    Install the specified directory from the GitHub repository.
    """
    api_url = urljoin(repo_url, f"repos/{owner}/{repo_name}/contents/{directory_name}")
    response = requests.get(api_url)
    contents = response.json()

    os.makedirs(target_path, exist_ok=True)
    for content in contents:
        file_path = os.path.join(target_path, content['name'])
        if content['type'] == 'file':
            file_url = content['download_url']
            file_response = requests.get(file_url, stream=True)
            total_size = int(file_response.headers.get('content-length', 0))
            block_size = 1024
            with tqdm(total=total_size, unit='iB', unit_scale=True) as progress:
                with open(file_path, 'wb') as file:
                    for chunk in file_response.iter_content(chunk_size=block_size):
                        if chunk:
                            file.write(chunk)
                            progress.update(len(chunk))
        elif content['type'] == 'dir':
            os.makedirs(file_path, exist_ok=True)
            install_directory(repo_url, owner, repo_name, f"{directory_name}/{content['name']}", file_path)

def search_directories(repo_url, owner, repo_name, search_term):
    """
    Search for directories that match the given search term.
    """
    directories = list_directories(repo_url, owner, repo_name)
    matching_directories = [d for d in directories if search_term.lower() in d.lower()]
    return matching_directories

if __name__ == "__main__":
    repo_url = "https://api.github.com"
    owner = "modularml"
    repo_name = "mojo"

    parser = argparse.ArgumentParser(description="Manage packages in a GitHub repository.")
    parser.add_argument("action", choices=["list", "install", "search"], help="Action to perform.")
    parser.add_argument("name", nargs="?", help="Name of the directory to install or search for.")
    args = parser.parse_args()

    if args.action == "list":
        directories = list_directories(repo_url, owner, repo_name)
        print("Directories in the repository:")
        for directory in directories:
            print(f"- {directory}")

    elif args.action == "install":
        if args.name:
            target_path = os.path.join(os.getcwd(), args.name)
            install_directory(repo_url, owner, repo_name, args.name, target_path)
            print(f"Installed {args.name} to {target_path}")
        else:
            print("Please provide a directory name to install.")

    elif args.action == "search":
        if args.name:
            matching_directories = search_directories(repo_url, owner, repo_name, args.name)
            if matching_directories:
                print(f"Directories matching '{args.name}':")
                for directory in matching_directories:
                    print(f"- {directory}")
            else:
                print(f"No directories found matching '{args.name}'.")
        else:
            print("Please provide a search term.")