---
title: Backing up with BOSH Backup and Restore
owner: BBR
---

## Clean up after a failed backup {#manual-clean}

If your backup process fails, it might leave the BBR backup directory on the instance, causing any
subsequent attempts to backup to fail. In addition, BBR might not have run the post-backup scripts, leaving the instance in a locked state.

Follow the steps below to use the BBR cleanup script after a failed backup attempt.

1. If the BOSH Director backup failed, run:

    ```bash
    bbr director \
    --private-key-path PATH-TO-PRIVATE-KEY \
    --username USER-NAME \
    --host BOSH-DIRECTOR-IP \
    backup-cleanup
    ```

    For example:

    ```console
    $ bbr director \
    --private-key-path bosh.pem \
    --username bosh \
    --host bosh.example.com \
    backup-cleanup
    ```

1. If the BOSH deployment backup failed, run:

    ```bash
    BOSH_CLIENT_SECRET=BOSH-CLIENT-SECRET \
    bbr deployment \
    --target BOSH-TARGET \
    --username BOSH-CLIENT \
    --deployment BOSH-DEPLOYMENT \
    --ca-cert PATH-TO-BOSH-CA-CERTIFICATE \
    backup-cleanup
    ```

    For example:

    ```console
    $ BOSH_CLIENT_SECRET=p455w0rd \
    bbr deployment \
    --target bosh.example.com \
    --username jumpbox \
    --deployment cf-acceptance-0 \
    --ca-cert bosh.ca.crt \
    backup-cleanup
    ```
