<!-- mcp-name: io.github.rafapra3008/lu-mcp-server -->

# lu-mcp-server

[![PyPI](https://img.shields.io/pypi/v/lu-mcp-server.svg)](https://pypi.org/project/lu-mcp-server/)
[![Tests](https://img.shields.io/badge/tests-25%20passed-brightgreen.svg)](tests/)
[![Glama](https://glama.ai/mcp/servers/@rafapra3008/lu-mcp-server/badge)](https://glama.ai/mcp/servers/@rafapra3008/lu-mcp-server)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)

MCP server for [Lingua Universale](https://github.com/rafapra3008/cervellaswarm) protocol verification.

Verify AI agent communication with session types -- mathematical proofs, not trust.

## Install

```bash
pip install lu-mcp-server
```

## Configure

### Claude Code

```bash
claude mcp add lu-mcp-server -- lu-mcp-server
```

### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "lu-mcp-server": {
      "command": "lu-mcp-server"
    }
  }
}
```

### Cursor / Windsurf

Add to your MCP settings:

```json
{
  "lu-mcp-server": {
    "command": "lu-mcp-server"
  }
}
```

## Tools

### `lu_load_protocol`

Parse a `.lu` protocol definition and extract its structure.

### `lu_verify_message`

Check if a message is valid in the context of an ongoing session.

### `lu_check_properties`

Verify formal safety properties (always terminates, no deadlock, etc.).

### `lu_list_templates`

Browse 20 standard library protocols across 5 categories.

## Example

```
protocol OrderProcessing:
    roles: customer, warehouse, payment
    customer asks warehouse to check availability
    warehouse returns stock status to customer
    when customer decides:
        in_stock:
            customer asks payment to process order
            payment returns confirmation to customer
        out_of_stock:
            customer sends cancellation to warehouse
    properties:
        always terminates
        no deadlock
        all roles participate
```

## Links

- [Playground](https://rafapra3008.github.io/cervellaswarm/) -- try LU in your browser
- [PyPI](https://pypi.org/project/cervellaswarm-lingua-universale/) -- core package
- [VS Code](https://marketplace.visualstudio.com/items?itemName=cervellaswarm.lingua-universale) -- editor extension

## License

Apache 2.0
