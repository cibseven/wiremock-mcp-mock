"""Build the static site for GitHub Pages deployment."""
import html
import glob
import os

PAGES_URL = "https://cibseven.github.io/wiremock-mcp-mock"


def build(output_dir: str = "_site") -> None:
    os.makedirs(output_dir, exist_ok=True)

    compose = open("compose.yml").read()
    compose_escaped = html.escape(compose)

    wiremock_files = sorted(
        p.replace("\\", "/")
        for p in glob.glob("wiremock/**/*", recursive=True)
        if os.path.isfile(p)
    )
    file_links = "\n".join(
        f'      <li><a href="{f}">{f}</a></li>' for f in wiremock_files
    )

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>WireMock MCP Mock</title>
  <link rel="stylesheet" href="style.css" />
</head>
<body>
  <h1>WireMock MCP Mock</h1>
  <p>
    A WireMock-based mock server for
    <a href="https://modelcontextprotocol.io/">MCP (Model Context Protocol)</a> server testing.
    This site serves the <code>compose.yml</code> and WireMock stub files so that CI pipelines
    and developers can pull the latest mock configuration directly via HTTPS.
  </p>

  <h2>Quick Start</h2>
  <p>Download and run the mock server with Docker Compose:</p>
  <pre>curl -O {PAGES_URL}/compose.yml
docker compose up -d</pre>
  <p>The WireMock server will be available at <code>http://localhost:9090</code>.</p>

  <h2>compose.yml</h2>
  <p><a href="compose.yml">Download compose.yml</a></p>
  <pre>{compose_escaped}</pre>

  <h2>MCP Server Testing</h2>
  <p>
    To configure an MCP server or client to use this WireMock instance as a mock backend,
    point it to <code>http://localhost:9090</code> after starting the Docker Compose stack.
  </p>
  <p>In a CI pipeline you can pull the compose file from GitHub Pages and spin up the mock
  before running your MCP integration tests:</p>
  <pre>curl -O {PAGES_URL}/compose.yml
docker compose up -d
# run your MCP tests against http://localhost:9090
docker compose down</pre>

  <h2>WireMock Stub Files</h2>
  <p>All stub files are served statically from this site:</p>
  <ul>
{file_links}
  </ul>

  <h2>Source</h2>
  <p>
    <a href="https://github.com/cibseven/wiremock-mcp-mock">github.com/cibseven/wiremock-mcp-mock</a>
  </p>
</body>
</html>
"""

    with open(os.path.join(output_dir, "index.html"), "w") as fh:
        fh.write(page)


if __name__ == "__main__":
    build()
