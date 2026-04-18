FROM python:3.13-slim

WORKDIR /app
COPY mcp_server/requirements.txt /app/mcp_server/requirements.txt
RUN pip install --no-cache-dir -r /app/mcp_server/requirements.txt

COPY mcp_server /app/mcp_server
COPY shared /app/shared

EXPOSE 9000
CMD ["python", "-m", "mcp_server.server"]
