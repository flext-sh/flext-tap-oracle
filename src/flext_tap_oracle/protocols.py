"""Singer Oracle tap protocols for FLEXT ecosystem."""

from typing import Protocol, runtime_checkable

from flext_core import FlextProtocols, FlextResult


class FlextTapOracleProtocols(FlextProtocols):
    """Singer Oracle tap protocols extending FlextProtocols with Oracle database extraction interfaces.

    This class provides protocol definitions for Singer Oracle tap operations including
    Oracle database connectivity, schema discovery, data extraction, and performance optimization.
    """

    @runtime_checkable
    class OracleConnectionProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle database connection operations."""

        def establish_connection(
            self,
            connection_config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Establish connection to Oracle database.

            Args:
                connection_config: Oracle connection configuration

            Returns:
                FlextResult[dict[str, object]]: Connection details or error

            """
            ...

        def test_connection(
            self, connection_config: dict[str, object]
        ) -> FlextResult[bool]:
            """Test Oracle database connectivity.

            Args:
                connection_config: Oracle connection configuration

            Returns:
                FlextResult[bool]: Connection test result or error

            """
            ...

        def close_connection(self) -> FlextResult[bool]:
            """Close Oracle database connection.

            Returns:
                FlextResult[bool]: Connection close status or error

            """
            ...

        def validate_credentials(
            self, connection_config: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Validate Oracle credentials and permissions.

            Args:
                connection_config: Oracle connection configuration

            Returns:
                FlextResult[dict[str, object]]: Validation results or error

            """
            ...

    @runtime_checkable
    class SchemaDiscoveryProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle schema discovery operations."""

        def discover_schemas(
            self, discovery_config: dict[str, object]
        ) -> FlextResult[list[dict[str, object]]]:
            """Discover available Oracle schemas.

            Args:
                discovery_config: Schema discovery configuration

            Returns:
                FlextResult[list[dict[str, object]]]: Discovered schemas or error

            """
            ...

        def discover_tables(
            self,
            schema_name: str,
            discovery_config: dict[str, object],
        ) -> FlextResult[list[dict[str, object]]]:
            """Discover tables in Oracle schema.

            Args:
                schema_name: Name of Oracle schema
                discovery_config: Table discovery configuration

            Returns:
                FlextResult[list[dict[str, object]]]: Discovered tables or error

            """
            ...

        def discover_views(
            self,
            schema_name: str,
            discovery_config: dict[str, object],
        ) -> FlextResult[list[dict[str, object]]]:
            """Discover views in Oracle schema.

            Args:
                schema_name: Name of Oracle schema
                discovery_config: View discovery configuration

            Returns:
                FlextResult[list[dict[str, object]]]: Discovered views or error

            """
            ...

        def discover_columns(
            self,
            schema_name: str,
            table_name: str,
            discovery_config: dict[str, object],
        ) -> FlextResult[list[dict[str, object]]]:
            """Discover columns in Oracle table or view.

            Args:
                schema_name: Name of Oracle schema
                table_name: Name of table or view
                discovery_config: Column discovery configuration

            Returns:
                FlextResult[list[dict[str, object]]]: Discovered columns or error

            """
            ...

        def discover_primary_keys(
            self,
            schema_name: str,
            table_name: str,
        ) -> FlextResult[list[str]]:
            """Discover primary key columns for Oracle table.

            Args:
                schema_name: Name of Oracle schema
                table_name: Name of table

            Returns:
                FlextResult[list[str]]: Primary key column names or error

            """
            ...

    @runtime_checkable
    class DataExtractionProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle data extraction operations."""

        def extract_table_data(
            self,
            schema_name: str,
            table_name: str,
            extraction_config: dict[str, object],
        ) -> FlextResult[list[dict[str, object]]]:
            """Extract data from Oracle table.

            Args:
                schema_name: Name of Oracle schema
                table_name: Name of table
                extraction_config: Data extraction parameters

            Returns:
                FlextResult[list[dict[str, object]]]: Extracted data or error

            """
            ...

        def extract_incremental_data(
            self,
            schema_name: str,
            table_name: str,
            replication_key: str,
            replication_value: object,
            extraction_config: dict[str, object],
        ) -> FlextResult[list[dict[str, object]]]:
            """Extract incremental data from Oracle table.

            Args:
                schema_name: Name of Oracle schema
                table_name: Name of table
                replication_key: Column used for incremental extraction
                replication_value: Last extracted value
                extraction_config: Extraction parameters

            Returns:
                FlextResult[list[dict[str, object]]]: Incremental data or error

            """
            ...

        def execute_custom_query(
            self,
            query: str,
            parameters: dict[str, object] | None = None,
        ) -> FlextResult[list[dict[str, object]]]:
            """Execute custom SQL query on Oracle database.

            Args:
                query: SQL query to execute
                parameters: Query parameters

            Returns:
                FlextResult[list[dict[str, object]]]: Query results or error

            """
            ...

        def get_table_row_count(
            self, schema_name: str, table_name: str
        ) -> FlextResult[int]:
            """Get row count for Oracle table.

            Args:
                schema_name: Name of Oracle schema
                table_name: Name of table

            Returns:
                FlextResult[int]: Row count or error

            """
            ...

    @runtime_checkable
    class TypeMappingProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle to Singer type mapping operations."""

        def map_oracle_type_to_singer(
            self, oracle_type: str, column_metadata: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Map Oracle data type to Singer JSON schema type.

            Args:
                oracle_type: Oracle data type name
                column_metadata: Additional column metadata

            Returns:
                FlextResult[dict[str, object]]: Singer type definition or error

            """
            ...

        def convert_oracle_value(
            self,
            value: object,
            oracle_type: str,
            conversion_config: dict[str, object],
        ) -> FlextResult[object]:
            """Convert Oracle value to Singer-compatible format.

            Args:
                value: Oracle database value
                oracle_type: Oracle data type
                conversion_config: Conversion configuration

            Returns:
                FlextResult[object]: Converted value or error

            """
            ...

        def handle_special_types(
            self,
            value: object,
            oracle_type: str,
            handling_config: dict[str, object],
        ) -> FlextResult[object]:
            """Handle Oracle special types (CLOB, BLOB, XMLType, etc.).

            Args:
                value: Oracle special type value
                oracle_type: Oracle data type
                handling_config: Special type handling configuration

            Returns:
                FlextResult[object]: Handled value or error

            """
            ...

        def validate_type_compatibility(
            self, oracle_type: str, singer_type: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate Oracle to Singer type mapping compatibility.

            Args:
                oracle_type: Oracle data type
                singer_type: Singer type definition

            Returns:
                FlextResult[bool]: Compatibility status or error

            """
            ...

    @runtime_checkable
    class StreamGenerationProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Singer stream generation from Oracle objects."""

        def generate_table_stream(
            self,
            schema_name: str,
            table_name: str,
            stream_config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Generate Singer stream for Oracle table.

            Args:
                schema_name: Name of Oracle schema
                table_name: Name of table
                stream_config: Stream configuration

            Returns:
                FlextResult[dict[str, object]]: Stream definition or error

            """
            ...

        def generate_view_stream(
            self,
            schema_name: str,
            view_name: str,
            stream_config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Generate Singer stream for Oracle view.

            Args:
                schema_name: Name of Oracle schema
                view_name: Name of view
                stream_config: Stream configuration

            Returns:
                FlextResult[dict[str, object]]: Stream definition or error

            """
            ...

        def generate_custom_stream(
            self,
            stream_name: str,
            query: str,
            stream_config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Generate Singer stream for custom SQL query.

            Args:
                stream_name: Name for the custom stream
                query: SQL query for data extraction
                stream_config: Stream configuration

            Returns:
                FlextResult[dict[str, object]]: Stream definition or error

            """
            ...

        def determine_replication_method(
            self,
            schema_name: str,
            table_name: str,
            replication_config: dict[str, object],
        ) -> FlextResult[str]:
            """Determine optimal replication method for Oracle table.

            Args:
                schema_name: Name of Oracle schema
                table_name: Name of table
                replication_config: Replication configuration

            Returns:
                FlextResult[str]: Replication method (FULL_TABLE, INCREMENTAL) or error

            """
            ...

    @runtime_checkable
    class PerformanceProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle tap performance optimization operations."""

        def optimize_query_performance(
            self, query: str, optimization_config: dict[str, object]
        ) -> FlextResult[str]:
            """Optimize Oracle query for performance.

            Args:
                query: Original SQL query
                optimization_config: Optimization parameters

            Returns:
                FlextResult[str]: Optimized query or error

            """
            ...

        def configure_connection_pooling(
            self, pool_config: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Configure Oracle connection pooling for performance.

            Args:
                pool_config: Connection pooling configuration

            Returns:
                FlextResult[dict[str, object]]: Pool configuration result or error

            """
            ...

        def monitor_extraction_performance(
            self, performance_metrics: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Monitor Oracle extraction performance metrics.

            Args:
                performance_metrics: Performance monitoring data

            Returns:
                FlextResult[dict[str, object]]: Performance analysis or error

            """
            ...

        def optimize_batch_processing(
            self, batch_config: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Optimize batch processing for Oracle extraction.

            Args:
                batch_config: Batch processing configuration

            Returns:
                FlextResult[dict[str, object]]: Optimization results or error

            """
            ...

    @runtime_checkable
    class ValidationProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle data validation operations."""

        def validate_data_integrity(
            self,
            schema_name: str,
            table_name: str,
            validation_rules: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate Oracle data integrity.

            Args:
                schema_name: Name of Oracle schema
                table_name: Name of table
                validation_rules: Data validation rules

            Returns:
                FlextResult[dict[str, object]]: Validation results or error

            """
            ...

        def check_data_consistency(
            self,
            extracted_data: list[dict[str, object]],
            consistency_config: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Check consistency of extracted Oracle data.

            Args:
                extracted_data: Extracted data to validate
                consistency_config: Consistency check configuration

            Returns:
                FlextResult[dict[str, object]]: Consistency check results or error

            """
            ...

        def detect_data_anomalies(
            self,
            data: list[dict[str, object]],
            anomaly_config: dict[str, object],
        ) -> FlextResult[list[dict[str, object]]]:
            """Detect anomalies in Oracle data.

            Args:
                data: Oracle data to analyze
                anomaly_config: Anomaly detection configuration

            Returns:
                FlextResult[list[dict[str, object]]]: Detected anomalies or error

            """
            ...

        def validate_schema_changes(
            self,
            schema_name: str,
            table_name: str,
            previous_schema: dict[str, object],
        ) -> FlextResult[dict[str, object]]:
            """Validate Oracle schema changes against previous state.

            Args:
                schema_name: Name of Oracle schema
                table_name: Name of table
                previous_schema: Previous schema definition

            Returns:
                FlextResult[dict[str, object]]: Schema change validation or error

            """
            ...

    @runtime_checkable
    class MonitoringProtocol(FlextProtocols.Domain.Service, Protocol):
        """Protocol for Oracle tap monitoring operations."""

        def track_extraction_metrics(
            self, extraction_id: str, metrics: dict[str, object]
        ) -> FlextResult[bool]:
            """Track Oracle extraction metrics.

            Args:
                extraction_id: Extraction identifier
                metrics: Extraction metrics data

            Returns:
                FlextResult[bool]: Metric tracking success status

            """
            ...

        def monitor_connection_health(
            self, connection_config: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Monitor Oracle connection health status.

            Args:
                connection_config: Connection monitoring configuration

            Returns:
                FlextResult[dict[str, object]]: Health status or error

            """
            ...

        def get_extraction_status(
            self, extraction_id: str
        ) -> FlextResult[dict[str, object]]:
            """Get Oracle extraction status.

            Args:
                extraction_id: Extraction identifier

            Returns:
                FlextResult[dict[str, object]]: Extraction status or error

            """
            ...

        def create_monitoring_dashboard(
            self, dashboard_config: dict[str, object]
        ) -> FlextResult[dict[str, object]]:
            """Create monitoring dashboard for Oracle tap operations.

            Args:
                dashboard_config: Dashboard configuration

            Returns:
                FlextResult[dict[str, object]]: Dashboard creation result or error

            """
            ...

    # Convenience aliases for easier downstream usage
    TapOracleConnectionProtocol = OracleConnectionProtocol
    TapOracleSchemaDiscoveryProtocol = SchemaDiscoveryProtocol
    TapOracleDataExtractionProtocol = DataExtractionProtocol
    TapOracleTypeMappingProtocol = TypeMappingProtocol
    TapOracleStreamGenerationProtocol = StreamGenerationProtocol
    TapOraclePerformanceProtocol = PerformanceProtocol
    TapOracleValidationProtocol = ValidationProtocol
    TapOracleMonitoringProtocol = MonitoringProtocol


__all__ = [
    "FlextTapOracleProtocols",
]
