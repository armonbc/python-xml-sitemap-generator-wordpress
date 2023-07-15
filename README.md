# Xml Sitemap Generator for Wordpress site (written in Python)
A simple Python script to generate local sitemap.xml for Wordpress site
- Auto-crawl links from WP REST-API
- Posts Only (Categories, Tags, Comments,etc., are not implemented yet)
#### Installation:
```
pip3 install -r requirements.txt
```

#### Modify the config in the main.py:
```
...
config = {
   # Edit your wp url here
   "full_url":"https://kinsta.com/",
   # Edit your file output here
   "output_file":"sitemap.xml",
   "url_set_config": {
        # True = original_modification |  False = now() 
        "date_val":False,
        # True = randomize |  False = 1
        "priority_val":False,
   }
}
...
```
#### Usage (or hit F5 in VS Code):
```
python3 main.py
```
#### Limitations:
- No WAF (WEB APPLICATION Firewall) Bypass. (This does not bypass anti-bot behind Cloudflare). If rate-limiting rule is enabled, you have to turn-off it from your account/server.
