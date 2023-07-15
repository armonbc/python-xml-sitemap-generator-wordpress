# Xml Sitemap Generator for Wordpress site (written in Python)
A simple Python script to generate local sitemap.xml for Wordpress site
- Auto-crawl links from WP REST-API
- Posts Only (Categories, Tags, Comments,etc., are not implemented yet)

#### Limitations:
- No WAF (WEB APPLICATION Firewall) Bypass. (This does not bypass anti-bot behind Cloudflare). If rate-limiting rule is enabled, you have to turn-off it from your account/server.
