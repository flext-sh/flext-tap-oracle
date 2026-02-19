# FLEXT-Tap-Oracle

<!-- TOC START -->

- [🚀 Key Features](#-key-features)
- [📦 Installation](#-installation)
- [🛠️ Usage](#-usage)
  - [Connection Settings](#connection-settings)
  - [Table Selection](#table-selection)
- [🏗️ Architecture](#-architecture)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

<!-- TOC END -->

[![Singer SDK](https://img.shields.io/badge/singer--sdk-compliant-brightgreen.svg)](https://sdk.meltano.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-Tap-Oracle** extracts data from Oracle Databases (19c+), enabling reliable ELT for critical business applications. It provides full table replication, incremental updates, and schema discovery.

Part of the [FLEXT](https://github.com/flext-sh/flext) ecosystem.

## 🚀 Key Features

- **Database Support**: Oracle 19c, 21c, 23c via `python-oracledb`.
- **Replication Styles**: Full Table (`FULL_TABLE`) and Incremental (`INCREMENTAL`) sync modes.
- **Schema Discovery**: Automatically maps Oracle types (`NUMBER`, `DATE`, `CLOB`) to Singer schema.
- **Performance**: Adjustable fetch size (`batch_size`) and connection pooling for optimized throughput.
- **Security**: Supports Wallet (mTLS) and Username/Password authentication.

## 📦 Installation

To usage in your Meltano project, add the extractor to your `meltano.yml`:

```yaml
plugins:
  extractors:
    - name: tap-oracle
      pip_url: flext-tap-oracle
      config:
        host: ${ORACLE_HOST}
        service_name: ${ORACLE_SERVICE}
        username: ${ORACLE_USER}
        password: ${ORACLE_PASSWORD}
```

## 🛠️ Usage

### Connection Settings

Standard configuration for TNS connectivity:

```json
{
  "host": "oracle.example.com",
  "port": 1521,
  "service_name": "ORCL",
  "user": "etl_user",
  "password": "secure_password",
  "batch_size": 10000
}
```

### Table Selection

Filter streams to specific tables or schemas:

```json
{
  "schema_include": ["HR", "SALES"],
  "table_include": ["EMPLOYEES", "ORDERS"],
  "table_exclude": ["TEMP_LOGS"]
}
```

## 🏗️ Architecture

Adheres to Singer Spec for maximum compatibility:

- **State Management**: Tracks replication keys (e.g., `updated_at`, `id`) for resumes.
- **Type Conversion**: Explicit handling of Oracle-specific types like `XMLType` or `JSON`.
- **Error Handling**: Retry logic for transient network issues.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on adding support for new data types or improving performance.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
