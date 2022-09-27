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
- experimental Features
  - "COMPLETE_PACKETS": Read entire Minecraft-Packets before passing it further.

#### Commandline Interface
There are CLI options which you can look it up with `-h` or `--help`:
```commandline
$ python minerouter -h
```

#### JSON-File
Create a file named `config.json` in the same directory as the `minerouter` directory:
```json
{
  "upstream_config": {
    "mc1.example.com": [
      "10.0.1.1",
      25565
    ],
    "mc2.example.com": [
      "10.0.1.2",
      25565
    ]
  },
  # Optional
  "system_config": {
    "COMPLETE_PACKETS": false
  }
}
```
If you prefer storing your config in another location, you can specify a path to your configuration file with the `--config` argument.
