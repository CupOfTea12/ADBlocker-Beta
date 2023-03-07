import tkinter as tk
import os
import requests

# Define the function to download the blocklist
def download_blocklist():
    # Download the blocklist from a URL
    blocklist_url = 'https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts'
    response = requests.get(blocklist_url)

    # Save the blocklist to a file
    with open('blocklist.txt', 'wb') as blocklist_file:
        blocklist_file.write(response.content)

# Define the function to block ads
def block_ads():
    # Download the blocklist if it hasn't been downloaded yet
    if not os.path.exists('blocklist.txt'):
        download_blocklist()

    # Get the path to the hosts file
    if os.name == 'nt':  # Windows
        hosts_path = r'C:\Windows\System32\drivers\etc\hosts'
    else:  # Unix-like systems
        hosts_path = '/etc/hosts'

    # Read the blocklist file
    with open('blocklist.txt', 'r') as blocklist_file:
        blocklist = blocklist_file.read()

    # Add the blocklist entries to the hosts file
    with open(hosts_path, 'a') as hosts_file:
        hosts_file.write('\n# Ad Blocker\n')
        for line in blocklist.splitlines():
            if not line.startswith('#'):
                parts = line.split()
                if len(parts) >= 2:
                    ip, domain = parts[:2]
                    hosts_file.write(f'{ip} {domain}\n')

    # Display a message saying that ads have been blocked
    result_label.config(text="Ads have been blocked. Please restart your browser for the changes to take effect.")

# Create the GUI window
root = tk.Tk()
root.title("Ad Blocker")

# Create the button to block ads
block_button = tk.Button(root, text="Block Ads", command=block_ads)
block_button.pack(side=tk.LEFT)

# Create the label to display the result
result_label = tk.Label(root, text="")
result_label.pack(side=tk.BOTTOM)

# Start the GUI event loop
root.mainloop()
