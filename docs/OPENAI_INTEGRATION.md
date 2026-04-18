# OpenAI Integration Notes

This backend uses the OpenAI Responses API for tool-calling.

## Why there are two modes

Remote MCP mode is the production target because it lets the model call the formal MCP server directly. That requires a public MCP endpoint, which is ideal in deployment but awkward in local development.

To keep local development usable, the backend also supports OpenAI function calling with app-side tools that mirror the same MCP contract.

## Production recommendation

- Use `OPENAI_MODEL=gpt-4.1`
- Deploy the MCP server publicly over streamable HTTP
- Set `OPENAI_TOOL_MODE=remote_mcp`
- Set `OPENAI_MCP_SERVER_URL` to the public `/mcp` endpoint

## Local recommendation

- Use `OPENAI_TOOL_MODE=function_fallback`
- Keep the MCP server running separately for parity and testing
- Switch to `remote_mcp` once the MCP server is deployed publicly

## Official references used

- Responses API overview: https://platform.openai.com/docs/api-reference/responses
- Responses guide and tool use: https://platform.openai.com/docs/guides/responses
- Remote MCP tool support: https://platform.openai.com/docs/guides/tools-connectors-mcp
