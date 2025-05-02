# Project Overview: Real-Time Ecommerce Data Pipeline

## System Components

1. **Data Generator**: Python script generating simulated e-commerce events (views, purchases) as CSV files
2. **Spark Structured Streaming**: Processes incoming CSV files in real-time
3. **PostgreSQL Database**: Stores processed events with proper indexing
4. **Monitoring**: Tracks performance metrics (throughput, latency)

## Data Flow

1. Events generated every 2 seconds → Saved as CSV files
2. Spark monitors input directory → Reads new CSV files
3. Spark applies transformations → Cleans and formats data
4. Processed data → Written to PostgreSQL
5. Metrics collected → Performance monitoring

## Architecture Benefits

- Scalable: Spark handles large-scale streaming
- Reliable: Checkpointing ensures fault tolerance
- Efficient: Indexed PostgreSQL tables optimize queries
