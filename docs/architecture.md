# AWS Infrastructure Design

Initial deployment, November 8, 2026. Based on deployment configuration, launch-form screenshots, service-health output, runtime access tests, and the student's successful browser chat. Final running-instance security and storage settings still need auditing. This diagram describes the current application; CloudWatch ingestion, alarms, backup jobs, and scheduled checks are not yet implemented.

```mermaid
flowchart LR
    Resident[Resident browser]
    Gemini[Google Gemini API\ngemini-3.6-flash]
    Operator[Student operator]
    subgraph AWS["AWS Singapore — ap-southeast-1"]
        SSM[Systems Manager\nSession Manager]
        Parameters[Parameter Store\nSecureString secrets]
        S3[Private S3 content\nsam10-residential-content-1229]
        subgraph EC2["EC2 — residential-assistant-server"]
            Launcher[Startup script\nAWS CLI]
            Caddy[Caddy\nHTTPS on 443, redirect on 80]
            API[LibreChat\nprivate port 3080]
            Gateway[Resident gateway\nprivate port 8000]
            Mongo[MongoDB\nprivate port 27017]
            Logs[Docker JSON logs\nrequest duration, result, version]
        end
    end
    Resident -->|HTTPS| Caddy
    Caddy --> API
    API -->|Authenticated internal request| Gateway
    Gateway -->|Question + handbook| Gemini
    Gemini -->|Answer| Gateway
    Gateway --> API
    API --> Caddy
    Caddy --> Resident
    API <-->|Accounts and conversations| Mongo
    Gateway -->|Read handbook| S3
    Gateway -->|Read Gemini key| Parameters
    Launcher -->|Read app secrets into memory| Parameters
    Launcher -->|Start containers with runtime environment| API
    Launcher --> Mongo
    Gateway --> Logs
    Operator --> SSM
    SSM --> EC2
```

Only Caddy publishes app-stack host ports. MongoDB uses a dedicated application user. The runtime EC2 role supplies AWS credentials; no static AWS access key is included in the bundle. Model-provider authentication is handled by the gateway using the Gemini parameter. The handbook and model key are cached in memory for up to 60 seconds. JSON request logs are written to the gateway container's stdout with local Docker rotation.

The hostname is residential-assistant.54.179.56.26.sslip.io. sslip.io supplies DNS, and Caddy obtained a public certificate. Certificate data is retained in the existing named Caddy volume. The documentation website will be a separate GitHub Pages deployment.

A single host was chosen to keep cost and operational scope manageable. This is a deliberate availability trade-off: failure of that host interrupts the app and database. The next priority is detecting failure and proving recovery.
