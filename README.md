# Kamiwaza Assistants API

A drop-in replacement for the OpenAI Assistants API that runs on Kamiwaza's enterprise infrastructure. This API provides 100% compatibility with OpenAI's Assistants API, allowing developers to migrate by only changing their import statement and API key.

## Features

- 🔄 **Complete OpenAI Compatibility**: Implements all OpenAI Assistant API endpoints with identical request/response formats
- 🚀 **Enterprise Infrastructure**: Powered by Kamiwaza's distributed AI platform
- 🛠️ **Full Tool Support**: 
  - Code Interpreter with secure execution
  - File Search with vector store integration
  - Function Calling with parallel execution
- 📁 **Advanced File Handling**: Automatic processing, chunking, and vector search setup
- 🔒 **Enterprise Security**: Role-based access control and comprehensive authentication
- 📊 **Production Monitoring**: Built-in metrics, logging, and resource tracking

## Quick Start

```python
# Instead of OpenAI's client:
# from openai import OpenAI
# client = OpenAI()

# Use Kamiwaza's client:
from kamiwaza import KamiwazaAI
client = KamiwazaAI()

# Create an assistant (identical to OpenAI's interface)
assistant = client.beta.assistants.create(
    name="Data Analyst",
    instructions="You analyze data...",
    model="deepseek-v3",  # Maps to Kamiwaza models
    tools=[{"type": "code_interpreter"}]
)

# Create a thread
thread = client.beta.threads.create()

# Add a message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Analyze this data"
)

# Run the assistant
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id
)
```

## Installation

```bash
pip install kamiwaza-assistants
```

## API Documentation

### Core Endpoints

- **Assistants**
  - POST /v1/assistants
  - GET /v1/assistants/{assistant_id}
  - POST /v1/assistants/{assistant_id}
  - DELETE /v1/assistants/{assistant_id}
  - GET /v1/assistants

- **Threads**
  - POST /v1/threads
  - GET /v1/threads/{thread_id}
  - POST /v1/threads/{thread_id}
  - DELETE /v1/threads/{thread_id}

- **Messages**
  - POST /v1/threads/{thread_id}/messages
  - GET /v1/threads/{thread_id}/messages/{message_id}
  - POST /v1/threads/{thread_id}/messages/{message_id}
  - GET /v1/threads/{thread_id}/messages

- **Runs**
  - POST /v1/threads/{thread_id}/runs
  - GET /v1/threads/{thread_id}/runs/{run_id}
  - POST /v1/threads/{thread_id}/runs/{run_id}
  - GET /v1/threads/{thread_id}/runs
  - POST /v1/threads/{thread_id}/runs/{run_id}/cancel
  - POST /v1/threads/{thread_id}/runs/{run_id}/submit_tool_outputs

### Tool Support

#### Code Interpreter
```python
assistant = client.beta.assistants.create(
    name="Python Coder",
    tools=[{"type": "code_interpreter"}]
)
```

#### File Search
```python
# Upload and process a file
file = client.files.create(
    file=open("data.pdf", "rb"),
    purpose="assistants"
)

# Create assistant with file search
assistant = client.beta.assistants.create(
    tools=[{"type": "file_search"}],
    file_ids=[file.id]
)
```

#### Function Calling
```python
assistant = client.beta.assistants.create(
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"},
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
                }
            }
        }
    }]
)
```

## Support

For support, please contact [support@kamiwaza.ai](mailto:support@kamiwaza.ai) or open an issue in the GitHub repository.
