# Residential App Deployment

This bundle is for the existing Ubuntu EC2 server. It contains no credentials or evidence images. Installation and activation are performed by the student. The cloud deployment starts with a fresh MongoDB volume and a separate demo account; local users, chat history, and the UI-created local agent are not imported. The cloud chat uses the gateway's handbook instructions with Gemini 3.6 Flash.

## Architecture

Caddy handles HTTPS and proxies to the private LibreChat API. The API stores users and chats in MongoDB using a dedicated read/write database user and sends model requests to the authenticated internal gateway. The gateway loads the private S3 handbook and Gemini SecureString in memory and calls Google's generateContent API. It refreshes handbook/key context after 60 seconds and logs JSON request outcomes to stdout. Model responses are delivered as one final SSE answer, rather than token-by-token streaming.

Only Caddy publishes host ports (80 and 443). MongoDB, LibreChat, and the gateway have no host ports. Public registration, social login, social registration, and password reset are disabled. Create the demo login through the server-side CLI before activating the public profile.

start.py retrieves app-secrets into memory through AWS CLI and passes them to Compose as process environment variables. It does not create a secret .env file. Docker administrators can inspect container environment values, so preserve restricted server and Docker access. Do not run commands that dump environments or expanded Compose configuration into screenshots or Git. Avoid rotating MongoDB passwords or credential-encryption values without migrating the stored data.

The S3 object for this bundle is deployment/residential-app-bundle.zip in sam10-residential-content-1229. The EC2 role must use the latest ../iam/runtime-access.json to read that object and both secret parameters. Upload the bundle privately through the S3 console. Evidence images remain local and are excluded from this bundle.

## Transfer to EC2

Run each command separately in Session Manager. Recheck that no existing app directory will be overwritten before extracting an updated bundle.

```bash
sudo install -d -m 0750 -o "$(id -u)" -g "$(id -g)" /opt/residential-assistant/app
```

```bash
/usr/local/bin/aws s3 cp s3://sam10-residential-content-1229/deployment/residential-app-bundle.zip /tmp/residential-app-bundle.zip --region ap-southeast-1
```

```bash
unzip /tmp/residential-app-bundle.zip -d /opt/residential-assistant/app
```

```bash
cd /opt/residential-assistant/app
```

## Start the private app

```bash
sudo python3 start.py start
```

This builds and starts MongoDB, the gateway, and LibreChat. The current Caddy setup page continues serving while these start. If startup fails, use the diagnostic commands below and share only sanitized errors. The secrets validation previously demonstrated verifies structure; a real model response through this gateway still needs testing.

## Create a demo login

```bash
sudo python3 start.py create-user
```

Enter invented profile details such as resident@example.com and Resident Demo. Use a strong unique password, and mark the fictional demo email verified when prompted. The upstream CLI can display or echo password input, so keep this terminal private and do not capture or share it. This account is separate from the local demonstration account.

## Switch the HTTPS page to the app

Only proceed after the private app is healthy and the demo user exists. Keep a copy of the working checkpoint configuration and retain certificate volumes.

```bash
sudo docker compose -f /opt/residential-assistant/https-check/compose.yaml down
```

Do not add -v. This stops the temporary proxy while preserving the named certificate volumes.

```bash
sudo python3 start.py publish
```

Open https://residential-assistant.54.179.56.26.sslip.io and sign in. Test pool hours, missing information, and unsupported bookings. Confirm sign-up is unavailable. Check gateway logs for request status, duration, version and handbook version. The deployment is complete only after a real browser login and Gemini answer succeed.

## Status and diagnostics

```bash
sudo python3 start.py status
```

```bash
sudo python3 start.py logs
```

## Roll back to the setup page

```bash
sudo python3 start.py stop
```

```bash
sudo docker compose -f /opt/residential-assistant/https-check/compose.yaml up -d
```

Preserve all volumes. Do not change secret values or delete database volumes to address an unknown startup issue.

## Verification and limits

Five offline tests cover JSON and SSE completion shapes, authorization before model access, rejecting non-text requests, and sanitizing provider errors. Run python3 gateway/test_server.py without installing boto3; the tests replace AWS/Gemini with test doubles. Python and JavaScript syntax and Compose configuration were checked locally. Real EC2 startup, the provider call, account creation, and certificate handover remain required deployment checks.

The LibreChat image is pinned to the digest already running locally. MongoDB uses version 8.0.20, boto3 uses version 1.43.126, and Caddy and Python use major/minor tags. Record final image digests before the reproducibility review. Logs rotate at 10 MiB per file with three files per service. CloudWatch ingestion, alarms, scheduled backups, automated health questions, and restore evidence are separate upcoming phases.
