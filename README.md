# wiremock-mcp-mock

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-live-blue)](https://cibseven.github.io/wiremock-mcp-mock/)

A WireMock-based mock server for [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server testing.  
The repository serves as a self-hosted, publicly accessible mock reference — the `compose.yml` and all WireMock stub files are accessible as static files via **GitHub Pages** at:

> **https://cibseven.github.io/wiremock-mcp-mock/**

## Usage

### Download and run with Docker Compose

```bash
curl -O https://cibseven.github.io/wiremock-mcp-mock/compose.yml
docker compose up -d
```

The WireMock server will be available at `http://localhost:9090`.

### Configure an MCP server

Point your MCP server or client to `http://localhost:9090` after starting the Docker Compose stack.

### Use in CI pipelines

```bash
curl -O https://cibseven.github.io/wiremock-mcp-mock/compose.yml
docker compose up -d
# run your MCP integration tests against http://localhost:9090
docker compose down
```

## WireMock Stub Structure

```
wiremock/
├── __files/          # Response body files (JSON)
│   ├── tool0-response.json
│   └── ...
└── mappings/         # Request/response mapping definitions
    ├── mapping-tool0.json
    └── ...
```

Each mapping in `mappings/` matches a `POST /tools/toolN` request and returns the corresponding `__files/toolN-response.json` body.

## compose.yml

```yaml
services:
  wiremock:
    image: wiremock/wiremock:3.13.2
    container_name: wiremock-mcp-mock
    ports:
      - "9090:8080"
    volumes:
      - ./wiremock:/home/wiremock
    restart: unless-stopped
```
