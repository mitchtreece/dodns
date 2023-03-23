# Digitalocean DNS

# TODO

- Remove hardcoded info from script (token, domain, etc)
- Make GitHub repo public

# Content

Pick one of the options below using the following settings:

* **DO_API_TOKEN:** The token you generate in DigitalOcean's API settings.
* **DO_DOMAIN:** The domain your subdomain is registered at. (i.e. `foo.com` for `home.foo.com`)
* **DO_SUBDOMAINS:** Subdomain to use. (name in A record) (i.e. `home` for `home.foo.com`). Multiple subdomains must be separated by commas `,`

* **SLEEP_INTERVAL:** Polling time in seconds. (default: 300)
* **REMOVE_DUPLICATES:** If set to `"true"`, removes extra DNS records if more than one A record is found on a subdomain. *Note that if this is not enabled, the script will NOT update subdomains with more than one A record* (default: false)

### Docker

```
$ docker pull mitchtreece/dodns
$ docker run -d --name dodns \
    -e DO_API_TOKEN="your_api_token" \
    -e DO_DOMAIN="yourdomain.com" \
    -e SUBDOMAINS="your,subdomain,list" \
    -e SLEEP_INTERVAL=2 \
    -e REMOVE_DUPLICATES="true" \
    mitchtreece/dodns
```

### Docker Compose

TODO
