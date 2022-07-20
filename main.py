import requests, time

Domain = "exampledomain.com"
Host = "@" # @ points to your domain if you want to update a subdomain write that here example: if your domain is test.example.com write test here
Password = "exmaple password" # this isn't your namecheap password its your dynamic dns password
Interval = 5 # how much to wait between checks (in minutes)

# Don't touch these
FirstRun = True
PreviousIp = ""
Ip = ""

def GetIP():
    IP = requests.get("https://api64.ipify.org")
    return IP.content.decode('utf-8')

def UpdateDDNS(ip, password, host, domain):
    uri = f"https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain}&password={password}&ip={ip}"
    update = requests.get(uri)
    if "<Done>true</Done>" in update.content.decode('utf-8'):
        print(f"[LOG] IP update Sucessful! {domain} now points to: {ip}")
        return
    else:
        PreviousIp == "Err"
        print(f"[ERROR] IP update Failed!Retrying automatically next update cycle!\n[ERROR] Double Check your password or domain and try again manually!(maybe namecheap is down?)")
        return

def WaitForNextUpdate(interval):
    if FirstRun:
        return
    else:
        print(f"[LOG] Waiting for {interval} minutes until next check")
        time.sleep(interval*60)
        return

def main(Domain, Host, Password, Interval):
    global Ip
    global PreviousIp
    global FirstRun
    while True:
        WaitForNextUpdate(Interval)
        if FirstRun:
            Ip = GetIP()
            UpdateDDNS(Ip, Password, Host, Domain)
            PreviousIp = Ip
            FirstRun = False
        else:
          Ip = GetIP()
          if Ip == PreviousIp:
            print("[LOG] No ip change Detected! No update Necessary")
          elif Ip != PreviousIp:
            print("[LOG] ip changed! Updating now!")
            UpdateDDNS(Ip, Password, Host, Domain)

                

if __name__ == "__main__":
    main(Domain, Host, Password, Interval)