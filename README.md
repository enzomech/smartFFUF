# smartFFUF

A custom python layer above the great FFUF tool, this is configured for my personal environment, you should modify it in order to adapt the script to your usage.


So basically I started to develop this tool for a pentest box which was polluted by a lot of not worthy hidden files, so the main idea was to add an output filter, called baseline response filtering, to remove results with a precise content inside the body of the file. Then I just embedded the script around this main idea, here is now the actual features.

## Requirements

One-shot installation (Debian / Kali / Parrot)
```
sudo apt update && sudo apt install -y ffuf python3 python3-pip && pip3 install requests tqdm
```
This installs everything needed to run smartFFUF.

### Dependencies explained

#### ffuf
The core web fuzzer used to enumerate hidden files and directories.

#### python3
Interpreter used to run the smartFFUF script.

#### python3-pip
Python package manager used to install required Python libraries.

### Python libraries used

#### requests
Used to send HTTP requests and retrieve responses for post-filtering.

#### tqdm
Used to display a progress bar during the filtering phase.

### Optional (but recommended)

#### SecLists wordlists
As this is a very personal tool and is configured with a path to my generic wordlist, smartFFUF is configured by default to use:
```
/usr/share/wordlists/seclists/Discovery/Web-Content/big.txt
```
If you don’t have SecLists installed, you can either:

Modify the ```DEFAULT_WORDLIST = ""``` value on the top part of the script.
You can also install it, or provide your own wordlist with -w.

On Kali / Parrot / Exegol, SecLists is usually already present.

## Main command

```
Python smartFFUF.py <IP>
```

You can use the ```-h``` argument to open the help menu anytime with the list of possible arguments.

This will launch the FFUF tool without really much added value, the only different thing is that you get a ```urlsFiltered.txt``` file with the filtered results. (in this case without filter so...).

```urlsFiltered.txt``` keep only the wanted results inside the file, here you have the name, the status code and the length of the fuzzed hidden file.

## Arguments

The script is meant to launch easily but ofc you can (and probably want) to use some args too.

### Baseline response filtering

This is the main feature intended for this script, you just have to add the text you want to remove results with this text in it. Here is an example :

```
Python smartFFUF.py <IP> -x "<title>301 Moved Permanently</title>"
```

### Status code exclusion

This will remove any results with the unwanted status code. It just uses the FFUF native argument to do so, for better performances.

```
Python smartFFUF.py <IP> -fc 403
```

### Wordlist

This changes the default wordlist used for the script, only for this instance of command.

```
Python smartFFUF.py <IP> -w /my/pretty/wordlist.txt
```

### Json output file

You can simply ask to get a filtered JSON output file if you want to use this format for further manipulation of the data. The file will simply be the "urlsFiltered.json" in addition to the "urlsFiltered.txt" file and won't replace it.

```
Python smartFFUF.py <IP> -json
```

### Header modification

```
Python smartFFUF.py <IP> -H "My_Header"
```

The argument is directly forwarded to FFUF and also reused internally by the Python layer for post-filtering requests.

You can use this option with any header supported by FFUF, for example:

-H "Host: congolexicomatisation.fr"
-H "Authorization: Bearer TOKEN"
-H "Cookie: PHPSESSID=1234"
-H "X-Forwarded-For: 127.0.0.1"
