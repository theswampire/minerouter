# minerouter

This is a prototype for a Minecraft reverse-proxy written in Python.

## Usage
There are no external dependencies, therefore you start the server just by running `minerouter`:
```commandline
$ python minerouter
```
Make sure to be in the parent folder of the `__main__.py` file. If not, substitute `minerouter` with `__main__.py`.

If you prefer a containerized setup, minerouter is available on `ghcr.io/theswampire/minerouter`.

### Configuration
You can configure following aspects:
- Incoming Socket: HOST, PORT
- Upstream Servers: 
  - Domain/IP String to identify the origin server. It uses the server address field of the [handshake](https://wiki.vg/Protocol#Handshaking) packet.
  - Actual address of the origin server.
- Experimental Features
  - "COMPLETE_PACKETS": Read entire Minecraft-Packets before passing it further.

#### Commandline Interface
There are CLI options which you can look up with `-h` or `--help`:
```commandline
$ python minerouter -h
```

#### JSON-File
Create a file named `config.json` in the same directory as the `minerouter` directory:
```json
{
  "upstream_config": {
    "mc1.example.com": "11.1.11.1",
    "mc2.example.com": "12.1.1.1:6969",
    "mc3.example.com": "[::1]:26",
    "mc4.example.com": "backend_server_domain"
  },
  # Optional
  "system_config": {
    "COMPLETE_PACKETS": false
  }
}
```
Note that if you provide an IPv6 address, use the bracket notation like `mc4.example.com`.

If you prefer storing your config in another location, you can specify a path to your configuration file with the `--config` argument.
