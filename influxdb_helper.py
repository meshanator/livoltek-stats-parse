import logging
from dataclasses import asdict
from influxdb_client import InfluxDBClient, Point, WriteOptions

logger = logging.getLogger()

class InfluxDBHelper:
    def __init__(self, influxdbHost, influxdbToken, influxdbOrg, influxdbBucket, influxdbMeasurement):
        self.influxdbHost = influxdbHost
        self.influxdbToken = influxdbToken
        self.influxdbOrg = influxdbOrg
        self.influxdbBucket = influxdbBucket
        self.influxdbMeasurement = influxdbMeasurement
        
        # Use batching and async writes for better performance
        self.client = InfluxDBClient(url=self.influxdbHost, token=self.influxdbToken, org=self.influxdbOrg)
        self.write_api = self.client.write_api(write_options=WriteOptions(batch_size=1000, flush_interval=1000, jitter_interval=200, retry_interval=5000))

    def ping(self):
        return self.client.ping()

    def push_to_influxdb_v2(self, file):
        points = []

        for line in file.livoltekLines:
            fields = asdict(line)

            # Remove fields that don't need to be written
            ts = line.date.isoformat()  # ISO 8601 is preferred
            del fields['date']

            # Create the point
            point = Point(self.influxdbMeasurement)\
                .time(ts)\
                .tag("Datetime", ts)\
                .tag("Running Status", line.runningStatus)

            # Add fields dynamically
            for field_name, field_value in fields.items():
                point = point.field(field_name, field_value)

            points.append(point)

        # Send in batches
        if points:
            logger.info("Sending batch of %d points to InfluxDB", len(points))
            self.write_api.write(bucket=self.influxdbBucket, record=points)

    def close(self):
        # Flush any remaining points in the write API before closing
        logger.info("Flushing and closing the InfluxDB client...")
        self.write_api.flush()
        self.write_api.close()
        self.client.close()
