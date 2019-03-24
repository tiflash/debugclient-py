import os
import re
import json
import socket
import subprocess


def launch_server(ccs_exe, workspace):
    """Launches DebugServer process

    Args:
        ccs_exe (str): full path to ccs executable
        workspace (str): full path to workspace to use

    Returns:
        (subprocess.PID, int): returns tuple containing process id and port number
    """
    server_script = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "server.js")
    )
    os.environ["DSS_SCRIPTING_ROOT"] = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "debugserver-js")
    )
    ccsexe = [
        ccs_exe,
        "-noSplash",
        "-application",
        "com.ti.ccstudio.apps.runScript",
        "-ccs.script",
    ]
    ccsexe.append(server_script)
    ccsexe.append("-ccs.rhinoArgs")

    p = subprocess.Popen(ccsexe, stdout=subprocess.PIPE)

    if p.poll() is not None:
        raise Exception("Could not start server process")

    # Wait until Debug Server has started
    line = ""
    while "PORT" not in str(line):
        line = p.stdout.readline()
    try:
        m = re.search("PORT: ([0-9]+)", str(line))
        port = int(m.group(1))
    except:
        p.terminate()
        raise Exception("Could not retrieve port from debugserver process.")

    return (p, port)


def create_socket(port, host=None, connect=True):
    """Creates and returns a socket

    Args:
        port (int): port number to use
        connect (bool, optional): whether socket should be connected (default=True)
        host (str, optional): hostname to connect to (default="localhost")

    Returns:
        socket: socket created

    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if host is None:
        host = "localhost"
    if connect:
        s.connect((host, port))
    return s


def send(s, req):
    """Sends a JSON formatted request and returns the response.

    This will wait/block until a response is received or timeout occurs

    Args:
        s (socket): socket to send request over
        req (dict): request to convert to json and send over socket

    Returns:
        dict: JSON formatted response
    """
    msg = json.dumps(req)
    s.sendall(b"%s\n" % msg.encode())

    r = bytearray()
    while b"\n" not in r:
        r.extend(s.recv(1024))

    result = json.loads(r)
    return result


def create_request(cmd, **kwargs):
    """Creates a properly formatted request dictionary

    Args:
        cmd (str): command name
        **kwargs (dict, optional): keyword arguments to specify for command

    Returns:
        dict: request formatted dictionary containing parameters
    """
    req = {"name": cmd}
    if kwargs is not None:
        req["args"] = kwargs

    return req
