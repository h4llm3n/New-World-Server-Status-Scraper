# New-World-Server-Status-Scraper

![example](https://i.imgur.com/Rj4a2EB.png)

 Requirements:
-  python
-  pip

Install script dependencies:
```
pip install -r requirements.txt
```

Update the Discord webhook URL variable in server_status.py to post to that channel.

Schedule script to run every x minutes (cron):
```
python3 server_status.py
```
