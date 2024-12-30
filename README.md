# Athena with AWS Bedrock

A FastAPI application for generating SQL queries using AWS Bedrock LLMs with context awareness. The application validates SQL syntax, handles schema validation, and provides clean, consistent query outputs.

## Features

- SQL Query Generation using AWS Bedrock LLMs
- Schema-aware Query Generation 
- Query History Context
- Proper Column Qualification and Table Aliasing
- SQL Validation and Formatting
- Case-insensitive String Handling

## Prerequisites

- Python 3.x
- PDM (Python Development Manager)
- AWS Credentials
- Docker (optional)

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/yourusername/athena-with-aws-bedrock.git
cd athena-with-aws-bedrock
```

2. Install dependencies:
```bash
pdm install
```

3. Set up environment variables:
```bash
cp .env.example .env
# Add your AWS credentials and other configurations
```

4. Run the application:
```bash
make run
```

## Development

### Project Structure
```
athena-with-aws-bedrock/
├── src/
│   ├── builder/         # LLM builder implementations
│   ├── executor/        # Query execution logic
│   ├── generator/       # Query and schema generators
│   │   ├── query/      # SQL query generation
│   │   └── schema/     # Schema management
│   ├── main.py         # FastAPI application
│   ├── models.py       # Data models
│   ├── prompt.txt      # LLM prompts
│   ├── resolvers.py    # Query resolvers
│   └── schema_def.json # Schema definitions
├── tests/
├── Makefile
└── README.md
```

### Available Commands

Format code:
```bash
make format
```

Run development server:
```bash
make run
```

## Core Components

### Builder
- Handles LLM integration with AWS Bedrock
- Manages model configurations and parameters
- Provides interface for query generation

### Generator
- Query Generator: Creates SQL queries from natural language
- Schema Generator: Manages and validates database schemas
- Ensures proper table aliasing and column qualification

### Executor
- Executes generated SQL queries
- Handles query validation
- Manages query context and history

## SQL Generation Rules

1. Table Aliasing
   - Meaningful table aliases (e.g., tf for transaction_fact)
   - Every column must be fully qualified (e.g., tf.column_name)
   - Consistent alias usage across queries

2. String Handling
   - Case-insensitive comparisons using LOWER()
   - String values in uppercase
   - Special handling for tenant_id

3. Query Structure
   - Single line output without line breaks
   - Proper WHERE clause construction
   - Appropriate JOIN handling
   - Date/time handling using EXTRACT()

Example Query:
```sql
SELECT 
    tf.transaction_id, 
    tf.amount 
FROM transaction_fact tf 
WHERE 
    tf.tenant_id = '123' 
    AND LOWER(tf.status) = LOWER('COMPLETED')
```

## API Documentation

When running locally, access:
- API Documentation: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc

### Key Endpoints

- `/generate-sql`: Generate SQL from natural language
- `/validate-sql`: Validate generated SQL
- `/execute-sql`: Execute validated SQL queries

## Environment Variables

```env
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=your_region

# Bedrock Configuration
MODEL_ID=your_bedrock_model_id
MODEL_PARAMETERS={"temperature": 0, "top_p": 1}

# Application Configuration
DEBUG=True
LOG_LEVEL=INFO
```

## Makefile Commands

```makefile
format:
    pdm run black .

run:
    pdm run uvicorn src.main:app --reload
```

## Error Handling

The application handles various error scenarios:

1. Schema Validation Errors
2. SQL Syntax Errors
3. Query Execution Errors
4. AWS Bedrock API Errors

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Format your code (`make format`)
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Guidelines

- Use Black for code formatting
- Add tests for new features
- Update documentation as needed
- Follow semantic versioning

## Testing

Run tests:
```bash
pdm run pytest
```

Generate coverage report:
```bash
pdm run pytest --cov=src
```

## License

[MIT License](LICENSE)

## Acknowledgments

- AWS Bedrock team for LLM capabilities
- FastAPI framework
- Python PDM community
