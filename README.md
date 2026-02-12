# ModelPark Python SDK

Python SDK for the [ModelPark](https://modelpark.app/) CLI — publish, manage, and access ML apps via secure tunnels.

The SDK provides two interfaces:

- **`ModelPark`** — Python wrapper around the ModelPark Go CLI (apps run in the background by default)
- **`APIManager`** — Direct HTTP client for calling published ModelPark apps

## Prerequisites

Install the ModelPark CLI binary from [GitHub Releases](https://github.com/model-park/cli/releases). The Python package does **not** bundle the CLI — it must be installed separately and available on your `PATH`.

## Installation

```bash
pip install modelpark
```

## Quick Start

### CLI Wrapper

```python
from modelpark import ModelPark

mp = ModelPark()

# Authenticate
mp.login(token="your_token")

# Serve an already-running local app (background)
mp.serve(name="my-app", port=8000)

# Or run a command and tunnel it (background)
mp.run(name="my-streamlit", command_args="streamlit run app.py", framework="streamlit")

# List running apps
mp.ls()

# View logs
mp.logs("my-app")

# Stop / kill
mp.stop("my-app")
mp.kill("my-streamlit")

mp.logout()
```

### API Access

```python
from modelpark import APIManager

api = APIManager()

user_credentials = {"username": "your_username", "password": "your_password"}
app_name = "my-app"

# Simple API call
response = api.make_api_call(app_name, user_credentials, request_payload={"key": "value"})

# With password-protected app
response = api.make_api_call(app_name, user_credentials, password="secret", expire="7d")

# With file upload
response = api.make_api_call(app_name, user_credentials, audio_file_path="./audio.m4a")

# Reuse access token for multiple calls
auth_token = api.get_auth_token(user_credentials)
access_token = api.get_access_token(app_name, auth_token)
response = api.make_api_call_with_access_token(app_name, access_token, request_payload={"key": "value"})
```

## API Reference

### `ModelPark` — CLI Wrapper

| Method | Description |
|--------|-------------|
| `login(token=None, email=None)` | Authenticate with token or email |
| `run(name, command_args, port=None, access=None, framework=None)` | Run a command and expose it via tunnel (background) |
| `serve(name, port, access=None, framework=None)` | Tunnel an already-running local port (background) |
| `ls()` | List running apps |
| `logs(name, follow=False)` | View logs for an app |
| `stop(name)` | Stop a running app |
| `kill(name)` | Kill a running app |
| `status()` | Show CLI status |
| `version()` | Show SDK and CLI version |
| `logout()` | Log out |

### `APIManager` — Direct HTTP API

| Method | Description |
|--------|-------------|
| `get_auth_token(user_credentials)` | Get an authentication token |
| `get_access_token(app_name, auth_token, password=None, expire=None)` | Get an access token for an app |
| `make_api_call(app_name, user_credentials, ...)` | Full API call (auth + access + request) |
| `make_api_call_with_access_token(app_name, access_token, ...)` | API call with a pre-obtained access token |

## Migration from v0.1.x

| v0.1.x | v0.2.0 | Notes |
|--------|--------|-------|
| `ModelPark(clear_cache=True)` | `ModelPark()` | CLI installed separately, no auto-download |
| `mp.login(username=..., password=...)` | `mp.login(token=...)` or `mp.login(email=...)` | Token-based auth |
| `mp.init(port=...)` | *(removed)* | No process manager needed |
| `mp.register(port, name, access)` | `mp.serve(name, port, access)` | Background by default |
| `mp.register(port, name, file_path, framework)` | `mp.run(name, command_args, framework)` | Background by default |
| `mp.run_with_streamlit_and_register(...)` | `mp.run(name, "streamlit run app.py", framework="streamlit")` | Unified run command |
| `mp.register_port(name, port, access)` | `mp.serve(name, port, access)` | Renamed |
| `mp.stop()` | `mp.stop("app-name")` | Now requires app name |
| `mp.kill(name=..., all=True)` | `mp.kill("app-name")` | Kill by name |
| *(none)* | `mp.logs("app-name", follow=True)` | New — view/follow logs |
| App URL: `myapp-proxy.modelpark.app` | `myapp.modelpark.app` | Simplified URLs |

## License

MIT
