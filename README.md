# DODNS - DigitalOcean Dynamic DNS

DigitalOcean DNS update script. Written in Python, bundled with Docker 😎

## Usage

### Docker

```
$ docker pull ghcr.io/mitchtreece/dodns
$ docker run -d --name dodns \
    -e DO_API_TOKEN="your_api_token" \
    -e DO_DOMAIN="yourdomain.com" \
    -e DO_SUBDOMAINS="your,subdomain,list" \
    mitchtreece/dodns
```

### Docker Compose

```
dodns:
    container_name: dodns-yourdomain.com
    image: ghcr.io/mitchtreece/dodns
    environment:
        - DO_API_TOKEN="your_api_token"
        - DO_DOMAIN="yourdomain.com"
        - DO_SUBDOMAINS="your,subdomain,list"
```

## Variables

- **DODNS_SCHEDULE (optional)**: The cron schedule you'd like the script to run on. Defaults to "`*/5 * * * *`" (every 5 minutes) if not specified.
- **DODNS_DRY_RUN (optional)**: (_0 || 1_) - Flag indicating if the script should be run "dry", i.e. no actual update actions will be performed.
- **DO_API_TOKEN**: Your DigitalOcean API token.
- **DO_DOMAIN**: The DigitalOcean domain you'd like to update.
- **DO_SUBDOMAINS (optional)**: Comma-separated list of subdomains you'd like updated. Defaults to "`@`" if none are specified.