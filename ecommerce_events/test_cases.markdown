# Test Plan

## Test Cases

1. **CSV Generation**

   - **Test**: Run data_generator.py for 10 seconds
   - **Expected**: Multiple CSV files created in ecommerce_events/
   - **Actual**: [To be filled after testing]

2. **Spark File Detection**

   - **Test**: Generate 5 CSV files, run Spark job
   - **Expected**: Spark processes all files
   - **Actual**: [To be filled after testing]

3. **Data Transformations**

   - **Test**: Verify price > 0 filter
   - **Expected**: No negative prices in PostgreSQL
   - **Actual**: [To be filled after testing]

4. **PostgreSQL Writing**

   - **Test**: Check database after 1 minute of streaming
   - **Expected**: Events table populated without errors
   - **Actual**: [To be filled after testing]

5. **Performance Metrics**
   - **Test**: Monitor processing time
   - **Expected**: Processing time < 2 seconds per batch
   - **Actual**: [To be filled after testing]
