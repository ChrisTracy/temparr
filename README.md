# temparr

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
      - HOST_URL=<host_url>
      - API_KEY=<api_key>
      - TEMPORARY_FOLDER=<temporary_folder>
      - KEEP_TIME=<keep_time>
      - RECURRENCE=<recurrence>
    restart: unless-stopped
```

3. Bring up your stack by running

```bash
docker-compose up -d
```
