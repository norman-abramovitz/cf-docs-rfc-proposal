---
title: Backing up with BOSH Backup and Restore
owner: BBR
---

## Connect to your jumpbox {#connect-to-jumpbox}

To back up a BOSH Director or BOSH deployment using BBR, you need to establish a
connection to your jumpbox in one of the ways below:

* [Option 1: Connect with SSH](#ssh)
* [Option 2: Connect with BOSH\_ALL\_PROXY](#bosh-all-proxy)

For more information about the jumpbox, see [Installing BOSH Backup and Restore](installing.html).

### Option 1: Connect with SSH {#ssh}

To connect to your jumpbox using the command line interface (CLI), run:

```bash
ssh -i PATH-TO-KEY JUMPBOX-USERNAME@JUMPBOX-ADDRESS
```

Where:

* `PATH-TO-KEY` is the local path to your private key file for the jumpbox host.
* `JUMPBOX-USERNAME` is your jumpbox username.
* `JUMPBOX-ADDRESS` is the IP address or hostname of the jumpbox.

!!! note

    If you connect to your jumpbox with SSH, you must run the BBR commands in this topic from inside your jumpbox.

### Option 2: Connect with BOSH\_ALL\_PROXY {#bosh-all-proxy}

You can use the environment variable `BOSH_ALL_PROXY` to open an SSH tunnel with
SOCKS5 to the jumpbox.
This tunnel enables you to forward requests from your local machine to the BOSH
Director through the jumpbox.
When `BOSH_ALL_PROXY` is set, the BBR CLI uses its value to forward
requests to the BOSH Director.

!!! note

    For the following procedures to work, ensure the SOCKS port is not already in use by a different tunnel or process.

To connect with `BOSH_ALL_PROXY`, follow one of the below procedures:

* **To establish the tunnel separate from the BOSH CLI:**
    1. Establish the tunnel and make it available on a local port by running:

        ```bash
        ssh -4 -D SOCKS-PORT -fNC JUMPBOX-USERNAME@JUMPBOX-ADDRESS -i JUMPBOX-KEY-FILE -o ServerAliveInterval=60
        ```

        Where:

        * `SOCKS-PORT` is the local SOCKS port.
        * `JUMPBOX-USERNAME` is your jumpbox username.
        * `JUMPBOX-ADDRESS` is the IP address or hostname of the jumpbox.
        * `JUMPBOX-KEY-FILE` is the local SSH private key for accessing the jumpbox.
    2. Provide the BOSH CLI with access to the tunnel using the `BOSH_ALL_PROXY` environment variable
    by running:

        ```bash
        export BOSH_ALL_PROXY=socks5://localhost:SOCKS-PORT
        ```

        Where `SOCKS-PORT` is your local SOCKS port.

* **To establish the tunnel using the BOSH CLI:**

    Provide the BOSH CLI with the necessary SSH credentials to create the tunnel by
    running:

    ```bash
    export BOSH_ALL_PROXY=ssh+socks5://JUMPBOX-USERNAME@JUMPBOX-ADDRESS:SOCKS-PORT?private-key=JUMPBOX-KEY-FILE
    ```

    Where:

    * `JUMPBOX-USERNAME` is your jumpbox username.
    * `JUMPBOX-ADDRESS` is the IP address or hostname of the jumpbox.
    * `SOCKS-PORT` is the local SOCKS port.
    * `JUMPBOX-KEY-FILE` is the local SSH private key for accessing the jumpbox.

!!! note

    Using <code>BOSH_ALL_PROXY</code> can result in longer backup and restore
    times due to network performance degradation.
    All operations must pass through the proxy, which can make moving backup artifacts significantly
    slower.

!!! caution

    In the BBR v1.5.0 and earlier, the tunnel created by the BOSH CLI does
    not include the <code>ServerAliveInterval</code> flag.
    This might cause your SSH connection to timeout when transferring large artifacts.
    In BBR v1.5.1, the <code>ServerAliveInterval</code> flag is included.
    For more information, see
    <a href="https://github.com/cloudfoundry-incubator/bosh-backup-and-restore/releases/tag/v1.5.1">bosh-backup-and-restore</a>
    on GitHub.
