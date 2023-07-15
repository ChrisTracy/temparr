# Temparr

This project comes as a pre-built docker image that enables you to remove movies from Radarr after a specified number of days. It works based on a root folder that you specify.

## Quick Setup

1. Install Docker and Docker-Compose

- [Docker Install documentation](https://docs.docker.com/install/)
- [Docker-Compose Install documentation](https://docs.docker.com/compose/install/)

2. Create a docker-compose.yml file similar to this:

```yml
version: '3'

services:
  movie-management:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - HOST_URL=<radarr_url>
      - API_KEY=<radarr_api_key>
      - TEMPORARY_FOLDER=<radarr_root_folder>
      - KEEP_TIME=<keep_time_in_days>
      - RECURRENCE=<recurrence_in_minutes>
    restart: unless-stopped
```

3. Bring up your stack by running

```bash
docker-compose up -d
```
