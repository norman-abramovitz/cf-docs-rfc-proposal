---
title: Using an external file system (volume services)
owner: Core Services
---

Here are instructions to help you read and write to a mounted file system from your apps.
In <%= vars.app_runtime_first %>, a volume service provides a volume so your app can read
or write to a reliable, persistent file system.

<% include "native/_external_vol_win_note.md" %>



## <a id='nfs'></a> Create and use NFS volume services

This section describes how to use the NFS volume service.

<%= vars.app_runtime_abbr %> offers two NFS volume services:

* `nfs`: This volume service provides support for NFS volumes using both v3 and v4.x protocols.

* `nfs-legacy` (deprecated): Although it is deprecated, this volume service is still available due to the difficulty of retiring services. If you use this service, it performs exactly the same mount as the `nfs` service. For information about migrating to `nfs`, see [Migrate `nfs-legacy` Services to `nfs`](#migrate).

Both services offer a single plan called `Existing`.

!!! note

    NFS is not available on Windows systems.

### <a id='create-nfs'></a> Create an NFS volume service

To create an NFS volume service using the `Existing` plan of the `nfs` service:


1. Create an NFS volume service. Run:

    ```
    cf create-service nfs Existing SERVICE-INSTANCE-NAME -c '{"share":"SERVER/SHARE", "version":"NFS-PROTOCOL"}'
    ```

    Where:

    * `SERVICE-INSTANCE-NAME` is a name you provide for this NFS volume service instance.
    * `SERVER/SHARE` is the NFS address of your server and share.

        !!! important

            Omit the `:` that usually follows the server name in the address.

    * (Optional) `NFS-PROTOCOL` is the NFS protocol you want to use. For example, to use NFSv4, set the version to `4.1`. Valid values are `3`, `4.0`, `4.1` or `4.2`. If you do not specify a `version`, the protocol version used is negotiated between client and server at mount time. This usually causes the latest available version to be used.

    !!! important

        nfs-volume versions `v7.1.45 - v7.1.47` ship with a recent version of nfs-utils (a dependency of nfs-volume-service). Recent versions of nfs-utils have stricter option parsing. This leads to an issue with environments that configured the `vers=3.0` mount option.<br>
        NFSv3 does not utilize a MINOR version, but NFSv4 introduced MINOR versions that can be specified.<br>
        This has been mitigated by adding auto-correction logic to the nfsdriver process available with nfs-volume `>= v7.1.48`.


2. Confirm that the NFS volume service appears in your list of services. Run:

    ```
    cf services
    ```

