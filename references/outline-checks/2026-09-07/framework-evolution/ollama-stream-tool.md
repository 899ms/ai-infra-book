<!-- 从 ollama-stream-tool.html 迁移的资料快照；原始 HTML SHA-256: fda3cf53f6c56581e823c1b9b068eb14c78c545f1cf16e11c18399f0139f9143。 -->

[![Ollama](/public/ollama.png)](/)

[Models](/search) [Docs](/docs) [Pricing](/pricing)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibXQtMC4yNSBtbC0xLjUgaC01IHctNSBmaWxsLWN1cnJlbnQiIHZpZXdib3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgPHBhdGggZD0ibTguNSAzYzMuMDM3NTY2MSAwIDUuNSAyLjQ2MjQzMzg4IDUuNSA1LjUgMCAxLjI0ODMyMDk2LS40MTU4Nzc3IDIuMzk5NTA4NS0xLjExNjY0MTYgMy4zMjI1NzExbDQuMTQ2OTcxNyA0LjE0NzA5ODhjLjI5Mjg5MzIuMjkyODkzMi4yOTI4OTMyLjc2Nzc2NyAwIDEuMDYwNjYwMi0uMjY2MjY2Ni4yNjYyNjY1LS42ODI5MzAzLjI5MDQ3MjYtLjk3NjU0MTguMDcyNjE4MWwtLjA4NDExODQtLjA3MjYxODEtNC4xNDcwOTg4LTQuMTQ2OTcxN2MtLjkyMzA2MjYuNzAwNzYzOS0yLjA3NDI1MDE0IDEuMTE2NjQxNi0zLjMyMjU3MTEgMS4xMTY2NDE2LTMuMDM3NTY2MTIgMC01LjUtMi40NjI0MzM5LTUuNS01LjUgMC0zLjAzNzU2NjEyIDIuNDYyNDMzODgtNS41IDUuNS01LjV6bTAgMS41Yy0yLjIwOTEzOSAwLTQgMS43OTA4NjEtNCA0czEuNzkwODYxIDQgNCA0IDQtMS43OTA4NjEgNC00LTEuNzkwODYxLTQtNC00eiIgLz4KICAgIDwvc3ZnPg==)

[Sign in](/signin) [Download](/download)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTMuNzUgNi43NWgxNi41TTMuNzUgMTJoMTYuNW0tMTYuNSA1LjI1aDE2LjUiIC8+CiAgICAgICAgPC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTYgMThMMTggNk02IDZsMTIgMTIiIC8+CiAgICAgICAgPC9zdmc+)

[Models](/search) [Download](/download) [Docs](/docs) [Pricing](/pricing) [Sign in](/signin)

# Streaming responses with tool calling

## May 28, 2025

![Ollama now has upgraded tool support](/public/blog/streaming-responses.png)

Ollama now supports streaming responses with tool calling. This enables all chat applications to stream content and also call tools in real time.

**Models that support using tools:**

- [Qwen 3](https://ollama.com/library/qwen3)
- [Devstral](https://ollama.com/library/devstral)
- [Qwen2.5](https://ollama.com/library/qwen2.5) and [Qwen2.5-coder](https://ollama.com/library/qwen2.5-coder)
- [Llama 3.1](https://ollama.com/library/llama3.1)
- [Llama 4](https://ollama.com/library/llama4)
- and [more tool calling models](https://ollama.com/search?c=tools).

#### Example of simple tool calling (weather)

#### Example of web search

### Get started

Download the latest version of [Ollama](https://ollama.com/download)

### cURL

An example of Ollama using the weather tool to answer the prompt *What is the weather today in Toronto?*

``` bash
curl http://localhost:11434/api/chat -d '{
  "model": "qwen3",
  "messages": [
    {
      "role": "user",
      "content": "What is the weather today in Toronto?"
    }
  ],
  "stream": true,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "Get the current weather for a location",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The location to get the weather for, e.g. San Francisco, CA"
            },
            "format": {
              "type": "string",
              "description": "The format to return the weather in, e.g. 'celsius' or 'fahrenheit'",
              "enum": ["celsius", "fahrenheit"]
            }
          },
          "required": ["location", "format"]
        }
      }
    }
  ]
}'
```

#### Output

``` bash
...
{
  "model": "qwen3",
  "created_at": "2025-05-27T22:54:57.641643Z",
  "message": {
    "role": "assistant",
    "content": "celsius"
  },
  "done": false
}
 {
  "model": "qwen3",
  "created_at": "2025-05-27T22:54:57.673559Z",
  "message": {
    "role": "assistant",
    "content": "</think>"
  },
  "done": false
}
{
  "model": "qwen3",
  "created_at": "2025-05-27T22:54:58.100509Z",
  "message": {
    "role": "assistant",
    "content": "",
    "tool_calls": [
      {
        "function": {
          "name": "get_current_weather",
          "arguments": {
            "format": "celsius",
            "location": "Toronto"
          }
        }
      }
    ]
  },
  "done": false
}
...
```

### Python

Install the latest version of the Ollama [Python library](https://github.com/ollama/ollama-python):

``` bash
pip install -U ollama
```

An example of Ollama using a mathematical function:

``` python
# Define the python function
def add_two_numbers(a: int, b: int) -> int:
  """
  Add two numbers

  Args:
    a (set): The first number as an int
    b (set): The second number as an int

  Returns:
    int: The sum of the two numbers
  """
  return a + b
  
from ollama import chat, ChatResponse 
messages = [{'role': 'user', 'content': 'what is three minus one?'}]

response: ChatResponse = chat(
  model='qwen3',
  messages=messages,
  tools=[add_two_numbers], # Python SDK supports passing tools as functions
  stream=True
)

for chunk in response:
    # Print model content
  print(chunk.message.content, end='', flush=True)
  # Print the tool call
  if chunk.message.tool_calls:
    print(chunk.message.tool_calls)
```

#### Output

``` python
<think>
Okay, the user is asking ...
</think>

[ToolCall(function=Function(name='add_two_numbers', arguments={'a': 3, 'b': 1}))]
```

### JavaScript

Install the latest version of the Ollama [JavaScript library](https://github.com/ollama/ollama-js):

    npm i ollama

An example of Ollama using a mathematical function:

``` js
import ollama from 'ollama';

# Describe the tool schema
const addTool = {
    type: 'function',
    function: {
        name: 'addTwoNumbers',
        description: 'Add two numbers together',
        parameters: {
            type: 'object',
            required: ['a', 'b'],
            properties: {
                a: { type: 'number', description: 'The first number' },
                b: { type: 'number', description: 'The second number' }
            }
        }
    }
};

async function run(model: string) {
    const messages = [{ role: 'user', content: 'What is 2 plus 3?' }];
    console.log('Question:', messages[0].content);

    for await (const chunk of await ollama.chat({
        model: model,
        messages: messages,
        tools: [addTool],
        stream: true
    })) {
        if (chunk.message.tool_calls) {
            // Print tool calls from the response
            for (const tool of chunk.message.tool_calls) {
                console.log('Tool call:', tool);
            }
        } else {
                // Print content from model
            process.stdout.write(chunk.message.content);
        }
    }
}

run('qwen3').catch(console.error);
```

#### Output:

``` js
Question: What is 2 plus 3?
<think>
Okay, the user is asking...
</think>
Tool call: {
  function: {
    name: "addTwoNumbers",
    arguments: {
      a: 2,
      b: 3,
    },
  },
}
```

### How tool parsing works in Ollama

#### Background

We’ve built a new parser that focuses on understanding the structure of a tool call rather than simply looking for JSON.

Previously, when tools were passed into the model, the system had to wait until the entire output was generated and then parse it as JSON to determine whether it contained a tool call or normal content. Users had to wait for the *complete* generation before seeing any streamed token. This approach was reliable against malformed output, but blocked streaming because a tool call might occur at any point in the text.

Ollama supports a wide range of models, some trained with tool-specific tokens and some without. The parsing logic would needs to stream user content while being able to detect, suppress, and parse the tool call tokens.

#### Incremental Parser

The new parser directly references each model’s template to understand the prefix of the tool call. This is necessary for Ollama to understand and separate the tool calls and content.

When a model is not directly trained on tool usage directly (trained with a prefix/tool token), it may still be able to output valid tool calls based on the sheer amount of knowledge it has. In this case, the parser is able to handle the partial prefixes output by the model and correctly separate tool calls and content.

Some models also elect to output a tool call *without* a prefix, even though they were trained on using a prefix for calling tools. Empirically, this behavior happens at the start of a model output only. To address this, the parser can fallback to parsing JSON as a tool call when it recognizes the start of a JSON. If the JSON does not match the tool call format for the model, the JSON will be returned.

#### Accuracy

In some cases, a model will reference the tool call it made previously when the results are passed into the model. Previously, this would return in multiple extra tool calls. By implementing prefix matching and correctly managing states where JSON is parsed to detect tool calls, tool calling reliability should be improved.

Previously, a model output like the example below would result in two tool calls instead of one:

``` python
[TOOL_CALL] [{"name":"get_conditions","arguments":{"city":"Sydney"}}]
 To get the current weather conditions for Sydney, we can use the function `get_conditions`. 
 However, I don't have real-time data access. Let's assume that the API will return the information:

 [{"name":"get_conditions","arguments":{"city":"Sydney"}}]
```

#### Model Context Protocol (MCP)

With the improvements, developers can now stream chat content and tool calls when using Ollama with MCP (Model Context Protocol). Anecdotally, using a context window of 32k or higher improves the performance of tool calling and also the result of the tool call.

#### Example increasing the context window in Ollama to use 32k

Please note, memory usage increases with a longer context window.

##### cURL

``` sh
curl -X POST "http://localhost:11434/api/chat" -d '{
  "model": "llama3.2",
  "messages": [
    {
      "role": "user",
      "content": "why is the sky blue?"
    }
  ],
  "options": {
    "num_ctx": 32000 # Update context window here
  }
}'
```

### Reference

[Tool Streaming Pull Request](https://github.com/ollama/ollama/pull/10415)

© 2026 Ollama

[Download](/download) [Blog](/blog) [Docs](https://docs.ollama.com) [GitHub](https://github.com/ollama/ollama) [Discord](https://discord.com/invite/ollama) [X (Twitter)](https://twitter.com/ollama) [Support](mailto:support@ollama.com) [Careers](https://jobs.ashbyhq.com/ollama) [Privacy](/privacy) [Terms](/terms)

- [Blog](/blog)
- [Download](/download)
- [Docs](https://docs.ollama.com)

&nbsp;

- [GitHub](https://github.com/ollama/ollama)
- [Discord](https://discord.com/invite/ollama)
- [X (Twitter)](https://twitter.com/ollama)
- [Meetups](https://lu.ma/ollama)
- [Careers](https://jobs.ashbyhq.com/ollama)
- [Privacy](/privacy)
- [Terms](/terms)

© 2026 Ollama Inc.
