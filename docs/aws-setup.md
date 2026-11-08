# AWS Server Setup Record

Date: November 8, 2026, Asia/Manila. Student performed AWS console configuration and server installation, with Codex guidance. This record documents observed results and identifies settings still requiring live verification.

## Server and access

- Instance name: residential-assistant-server.
- Region: ap-southeast-1 (Singapore), confirmed by the Session Manager URL.
- Selected instance type: m7i-flex.large, 2 vCPUs and 8 GiB memory.
- Selected operating system: Ubuntu Server 24.04 LTS, x86 architecture.
- Actual system reports Ubuntu 24.04.5 LTS, 7.6 GiB memory and a roughly 29 GiB root filesystem with 27 GiB available.
- Management connection: AWS Systems Manager Session Manager, with session user ssm-user.
- [Observed server environment](evidence/aws-server-environment.png).

## Launch configuration

The following settings were observed in launch-form screenshots. Capture the actual running instance settings before treating them as verified post-launch controls.

| Setting | Observed configuration |
|---|---|
| Compute | m7i-flex.large; displayed Linux rate $0.1197 per hour |
| Storage | 30 GiB gp3, 3000 IOPS, 125 MiB/s, encryption selected, delete on termination enabled |
| Network | Public IPv4 enabled; SSH from My IP; HTTP and HTTPS from the internet |
| Instance profile | ResidentialAssistantEC2Role |
| Shutdown behavior | Stop |
| Termination protection | Enabled |
| Stop protection | Disabled |
| Detailed EC2 monitoring | Disabled |
| Instance metadata | Enabled, IMDSv2 required, response hop limit 2 |
| User data | Empty |

The EC2 role creation form showed the managed policies AmazonSSMManagedInstanceCore and CloudWatchAgentServerPolicy. Application-specific S3 and Parameter Store permissions remain to be configured. The operator setup role was guided as ResidentialProjectSetupRole with an exact-user, MFA-required trust policy and AdministratorAccess for setup. Its final trust policy, attachments, and successful role switch have not been independently inspected. Budget creation, MFA completion, tags, and CloudTrail still need final evidence.

## Docker installation

The student installed Docker Engine using its official Ubuntu apt repository and enabled the service. Verified screenshot results were Docker Engine 29.9.3, Docker Compose v5.7.0, and a successful hello-world run.

[Docker installation verification](evidence/aws-docker-verification.png).

Commands used, with each code block run in the Session Manager shell:

```bash
sudo apt-get update
sudo apt-get install -y ca-certificates curl git
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc
```

```bash
sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: noble
Components: stable
Architectures: $(dpkg --print-architecture)
Signed-By: /etc/apt/keyrings/docker.asc
EOF
```

```bash
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl enable --now docker
sudo docker --version
sudo docker compose version
sudo docker run --rm hello-world
```

One initial curl command was incomplete because it ended at -o without an output filename. Re-running the full command with /etc/apt/keyrings/docker.asc corrected that input error. This setup correction is not being claimed as the assessed operational incident.

Source: https://docs.docker.com/engine/install/ubuntu/

## Remaining deployment work

### HTTPS preparation

Selected hostname: residential-assistant.54.179.56.26.sslip.io. The student ran the HTTPS checkpoint files in ../deployment/https-check/ on EC2. A Caddy log screenshot showed successful certificate issuance and a browser screenshot showed the deployment-in-progress response. This proves the temporary endpoint checkpoint; resident AI application deployment remains pending. Preserve the named Caddy data volume when replacing this page with the app proxy to retain certificates. If the EC2 public IP changes, update the hostname and configuration. The initial image reference is caddy:2; record and pin the selected digest for the final deployment.

### Content and runtime key checkpoint

The student created /sam10/residential/gemini-api-key as a Standard SecureString and attached ResidentialRuntimeAccess to ResidentialAssistantEC2Role. After installing AWS CLI, the student verified the EC2 identity uses this role and downloaded s3://sam10-residential-content-1229/handbook/resident-handbook.md successfully. An initial 403 was traced to the handbook being uploaded at the bucket root instead of the permitted handbook/ path. Uploading it to that path corrected the error without broadening permissions. At the student's request, the successful S3-download screenshot was not added to the evidence folder; this result is recorded as text only.

The student also retrieved the parameter with decryption while displaying only Name, Type and Version using a CLI query. The returned metadata showed the expected parameter name, SecureString, and version 1. This verifies decrypted retrieval, not that the key is accepted by Gemini. No secret value was displayed. Bucket versioning and private-access settings still need final evidence.

The original policy at ../deployment/iam/runtime-access.json was attached to ResidentialAssistantEC2Role, with positive runtime tests observed for the intended handbook object and Gemini parameter. Negative access tests are still pending. The local policy has now been updated to allow both the Gemini parameter and /sam10/residential/app-secrets, including updating its explicit-deny exception. Applying this revision in AWS and testing the second parameter remain pending. It explicitly denies parameter reads outside those two parameters because AmazonSSMManagedInstanceCore already permits broad GetParameter/GetParameters access. This restriction must be updated deliberately when adding further application parameters. Planned CloudWatch agent configuration will be stored locally rather than read from additional parameters. Session Manager's messaging and instance-management permissions remain attached.

The student reported creating /sam10/residential/app-secrets as a SecureString containing the generated database, JWT, and credential-encryption values. Its contents were not shared with Codex and have not been validated. Do not regenerate these values after the app starts using them without a planned rotation/migration.

This policy contains resource identifiers, not the API key. It uses the account ID observed in the student's console screenshots. Recheck the account and region before attachment. The parameter uses the default AWS-managed SSM key; any later custom KMS key will require separately reviewed key permissions. This policy does not yet grant backup writes to S3.

- Prepare the application deployment definition and export the local agent configuration without credentials.
- Create versioned private S3 content storage and secure Parameter Store settings with scoped runtime access.
- Transfer the application configuration, deploy the resident gateway and app, and arrange the HTTPS endpoint.
- Verify login, resident handbook answers, request logging, actual security settings, and baseline measurements.
- Preserve a diagram and six-pillar review describing what is actually deployed.

The student downloaded the app bundle and ran start.py start on EC2. The resulting terminal screenshot confirmed residential-mongodb-1, residential-gateway-1, and residential-api-1 all healthy. The gateway's successful startup also confirms it could load the handbook and Gemini parameter; a real provider answer still needs testing. Next create the separate cloud demo user and hand over Caddy from the temporary page to LibreChat. Public login and end-to-end AI response have not yet been demonstrated. This milestone is recorded as text; no screenshot was added to the evidence folder.
