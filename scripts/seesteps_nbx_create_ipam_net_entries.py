# Script that scans your network based on the defined network
# Records will be created within your enviroment, and marked as deprecated.
# It you wish for the status to be marked as active, you change this on line.52
# The following modules need to be installed, pip3 ipcalc networkscan python-netbox
# If you use https(SSL) in netbox API change port to 443
# Credit to Sasha0986 - https://gitlab.com/Sasha0986/netbox/-/tree/master/postinterfaces as I used his script as a template
# Script amended/created by SeeSteps

# Install Python module, uncomment if required
# pip install pip3
# pip install ipcalc
# pip install networkscan
# pip install python-netbox

import ipcalc
import networkscan
from netbox import netbox
import requests
import datetime

API_TOKEN = "INPUT YOUR NETBOX API TOKEN HERE"
HEADERS = {'Authorization': f'Token {API_TOKEN}', 'Content-Type': 'application/json', 'Accept': 'application/json'}
NB_URL = "http://192.168.1.2"
netbox = NetBox(host="192.168.2", port=8000, use_ssl=False, auth_token="INPUT YOUR NETBOX API TOKEN HERE")

if __name__ == '__main__':
    # Define the network to scan here
    my_network = "192.168.1.0/24"

    # Create the object
    my_scan = networkscan.Networkscan(my_network)

    # Run the scan of hosts using pings
    my_scan.run()

    # Here we define existing IP addresses in our network and write them to a list
    found_ip_in_network = [str(address) for address in my_scan.list_of_hosts_found]

    # Get all IP addresses from the prefix
    for ipaddress in ipcalc.Network(my_network):
        ip_str = str(ipaddress)

        # Check if IP address is in the network range
        if ip_str in found_ip_in_network:
            # Check if IP address exists in NetBox
            request_url = f"{NB_URL}/api/ipam/ip-addresses/?q={ipaddress}/"
            ipaddress1 = requests.get(request_url, headers=HEADERS)
            netboxip = ipaddress1.json()

            # If IP address does not exist in NetBox, create it as deprecated
            if netboxip['count'] == 0:
                netbox.ipam.create_ip_address(ip_str, status="deprecated")
        else:
            # Check if IP address exists in NetBox
            request_url = f"{NB_URL}/api/ipam/ip-addresses/?q={ipaddress}/"
            ipaddress1 = requests.get(request_url, headers=HEADERS)
            netboxip = ipaddress1.json()

            # If IP address does not exist in NetBox, create it as deprecated
            if netboxip['count'] == 0:
                netbox.ipam.create_ip_address(ip_str, status="deprecated")
