# hailmary

Pass files and folders around a local network.

## Installation

#### *Note: This repo must be cloned to every device that you want to transmit files to and from.*

After cloning the repo, run 
<pre>
pip install -r requirements.txt
</pre>

## Usage

### Server

Start the server by running `hailmary_server.py`.<br>
You will need to set the uppermost directory a client can get files from.<br>
This can be done manually in `homecloud_config.toml` or by passing it as
an argument to the `-s/--serving_directory` switch of `hailmary_server.py`.<br>
e.g. `>hailmary_server.py -s c:\users\username\documents` will only allow
clients to receive files from below the 'documents' directory level.<br>

### Clients

Other devices on the local network can then use the `hailmary.py` script
to request and download files from the device running the `hailmary_server.py`.<br>
The script has a simple command line interface.<br>
Running `>hailmary.py -h` produces:
<pre>
usage: hailmary.py [-h] [-w WRITE_DIR] [-i [INCLUDES ...]] [-e [EXCLUDES ...]] [-s] [paths ...]

positional arguments:
  paths

options:
  -h, --help            show this help message and exit
  -w WRITE_DIR, --write_dir WRITE_DIR
  -i [INCLUDES ...], --includes [INCLUDES ...]
                        List of glob patterns to use when including files to be transferred.
  -e [EXCLUDES ...], --excludes [EXCLUDES ...]
                        List of glob patterns to use when excluding files to be transferred.
  -s, --serving_directory
                        Contact the server and return the serving directory.
</pre>

Assuming the serving directory is `c:\users\username\documents`, The command
<pre>
>hailmary.py reports results -w ../info -i *.txt *.docx -e *notes.*
</pre>
will download every `.txt` and `.docx` file in `c:\users\username\documents\reports` and `c:\users\username\documents\results`
except any file with a name that ends in `notes` with any extension type.<br>
The files will then be written to a folder named `info` in the parent directory of this file (will be created if it doesn't exist.).<br>
If the requested resource doesn't exist or isn't in a sub directory of the serving directory, it will be ignored.