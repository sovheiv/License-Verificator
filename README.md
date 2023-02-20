# License Verificator
Web service for verification of license keys for commercial projects


### Setup
1. `mkdir programs/License-Verificator`
1. `nano programs/License-Verificator/docker-compose.yaml`
1. `sudo nano //etc/systemd/system/license-verificator.service`
1. `sudo systemctl daemon-reload`
1. `sudo systemctl enable license-verificator.service`
1. `sudo systemctl start license-verificator.service`
1. `sudo systemctl status license-verificator.service`
