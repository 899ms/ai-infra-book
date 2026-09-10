<!-- 从 blog-thinking.html 迁移的资料快照；原始 HTML SHA-256: 6ec3371fb18854d8703fc61f5b2c2f280aa415af3e86c92adf12c90f9989152e。 -->

[![Ollama](/public/ollama.png)](/)

[Models](/search) [Docs](/docs) [Pricing](/pricing)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0ibXQtMC4yNSBtbC0xLjUgaC01IHctNSBmaWxsLWN1cnJlbnQiIHZpZXdib3g9IjAgMCAyMCAyMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KICAgICAgPHBhdGggZD0ibTguNSAzYzMuMDM3NTY2MSAwIDUuNSAyLjQ2MjQzMzg4IDUuNSA1LjUgMCAxLjI0ODMyMDk2LS40MTU4Nzc3IDIuMzk5NTA4NS0xLjExNjY0MTYgMy4zMjI1NzExbDQuMTQ2OTcxNyA0LjE0NzA5ODhjLjI5Mjg5MzIuMjkyODkzMi4yOTI4OTMyLjc2Nzc2NyAwIDEuMDYwNjYwMi0uMjY2MjY2Ni4yNjYyNjY1LS42ODI5MzAzLjI5MDQ3MjYtLjk3NjU0MTguMDcyNjE4MWwtLjA4NDExODQtLjA3MjYxODEtNC4xNDcwOTg4LTQuMTQ2OTcxN2MtLjkyMzA2MjYuNzAwNzYzOS0yLjA3NDI1MDE0IDEuMTE2NjQxNi0zLjMyMjU3MTEgMS4xMTY2NDE2LTMuMDM3NTY2MTIgMC01LjUtMi40NjI0MzM5LTUuNS01LjUgMC0zLjAzNzU2NjEyIDIuNDYyNDMzODgtNS41IDUuNS01LjV6bTAgMS41Yy0yLjIwOTEzOSAwLTQgMS43OTA4NjEtNCA0czEuNzkwODYxIDQgNCA0IDQtMS43OTA4NjEgNC00LTEuNzkwODYxLTQtNC00eiIgLz4KICAgIDwvc3ZnPg==)

[Sign in](/signin) [Download](/download)

![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTMuNzUgNi43NWgxNi41TTMuNzUgMTJoMTYuNW0tMTYuNSA1LjI1aDE2LjUiIC8+CiAgICAgICAgPC9zdmc+) ![](data:image/svg+xml;base64,PHN2ZyBjbGFzcz0iaC04IHctOCIgZmlsbD0ibm9uZSIgdmlld2JveD0iMCAwIDI0IDI0IiBzdHJva2Utd2lkdGg9IjEuNSIgc3Ryb2tlPSJjdXJyZW50Q29sb3IiIGFyaWEtaGlkZGVuPSJ0cnVlIj4KICAgICAgICAgIDxwYXRoIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIgZD0iTTYgMThMMTggNk02IDZsMTIgMTIiIC8+CiAgICAgICAgPC9zdmc+)

[Models](/search) [Download](/download) [Docs](/docs) [Pricing](/pricing) [Sign in](/signin)

# Thinking

## May 30, 2025

![illustration of Ollama thinking](https://files.ollama.com/ollama_thinking.png)

Ollama now has the ability to enable or disable thinking. This gives users the flexibility to choose the model’s thinking behavior for different applications and use cases.

When thinking is enabled, the output will separate the model’s thinking from the model’s output. When thinking is disabled, the model will not think and directly output the content.

**Models that support thinking:**

- [DeepSeek R1](https://ollama.com/library/deepseek-r1)
- [Qwen 3](https://ollama.com/library/qwen3)
- more will be added under [thinking models](https://ollama.com/search?c=thinking).

### Thinking in action

#### Enable thinking in DeepSeek R1

In the CLI, thinking is enabled by default.

This can be useful in getting the model to think through different viewpoints to arrive at more accurate answer.

^(The model shown is the 8 billion parameter DeepSeek-R1-0528 Qwen 3 distilled model. This video is not sped up.)

#### Disable thinking in DeepSeek R1

In the CLI, thinking is disabled using `/set nothink` followed by the prompt.

This is useful in getting answers fast out of the model.

^(The model shown is the 8 billion parameter DeepSeek-R1-0528 Qwen 3 distilled model. This video is not sped up.)

### Get started

Download the latest version of [Ollama](https://ollama.com/download).

### CLI

From the Ollama CLI, thinking can be enabled or disabled:

**Enable thinking**

     --think

**Disable thinking**

    --think=false

#### Interactive sessions

When chatting inside an interactive session, thinking can be enabled or disabled:

**Enable thinking**

    /set think

**Disable thinking**

    /set nothink

#### Scripting

For scripting, a `--hidethinking` command is available. This helps users who want to use thinking models but simply want to see the answer.

**Example:**

    ollama run deepseek-r1:8b --hidethinking "is 9.9 bigger or 9.11?"

### API

Both of Ollama’s [generate API](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-completion) (`/api/generate`) and [chat API](https://github.com/ollama/ollama/blob/main/docs/api.md#generate-a-chat-completion) (`/api/chat`) have been updated to support thinking.

There is a new `think` parameter that can be set to `true` or `false` for enabling a model’s thinking process. When the `think` parameter is set to true, the output will separate the model’s thinking from the model’s output. This can help users craft new application experiences like animating the thinking process via a graphical interface, or for NPCs in games to have a thinking bubble before the output. When the `think` parameter is set to false, the model will not think and directly output the content.

#### Example using Ollama’s chat API with thinking enabled

    curl http://localhost:11434/api/chat -d '{
      "model": "deepseek-r1",
      "messages": [
        {
          "role": "user",
          "content": "how many r in the word strawberry?"
        }
      ],
      "think": true,
      "stream": false
    }'

**Output**

``` json
{"model":"deepseek-r1",
"created_at":"2025-05-29T09:35:56.836222Z",
"message":
    {"role": "assistant",
    "content": "The word \"strawberry\" contains **three** instances of the letter 'R' ..."
    "thinking": "First, the question is: \"how many r in the word  strawberry?\" I need to count the number of times the letter 'r' appears in the word \"strawberry\". Let me write down the word:...",
    "done_reason":"stop",
    "done":true,
    "total_duration":47975065417,
    "load_duration":29758167,
    "prompt_eval_count":10,
    "prompt_eval_duration":174191542,
    "eval_count":2514,
    "eval_duration":47770692833
    }
}
```

^(Output is truncated for brevity.)

### Python library

Please update to the latest Ollama [Python library](https://github.com/ollama/ollama-python).

``` python
pip install ollama
```

#### Example of enabling thinking

``` python
from ollama import chat

messages = [
  {
    'role': 'user',
    'content': 'What is 10 + 23?',
  },
]

response = chat('deepseek-r1', messages=messages, think=True)

print('Thinking:\n========\n\n' + response.message.thinking)
print('\nResponse:\n========\n\n' + response.message.content)
```

Please visit the [Ollama Python library](https://github.com/ollama/ollama-python) for more information about its usage. More [examples](https://github.com/ollama/ollama-python/tree/main/examples) are available.

### JavaScript library

Please update to the latest Ollama [JavaScript library](https://github.com/ollama/ollama-js).

``` js
npm i ollama
```

#### Example of enabling thinking

``` js
import ollama from 'ollama'

async function main() {
  const response = await ollama.chat({
    model: 'deepseek-r1',
    messages: [
      {
        role: 'user',
        content: 'What is 10 + 23',
      },
    ],
    stream: false,
    think: true,
  })

  console.log('Thinking:\n========\n\n' + response.message.thinking)
  console.log('\nResponse:\n========\n\n' + response.message.content + '\n\n')
}

main()
```

#### Example of streaming responses with thinking

``` js
import ollama from 'ollama'

async function main() {
  const response = await ollama.chat({
    model: 'deepseek-r1',
    messages: [
      {
        role: 'user',
        content: 'What is 10 + 23',
      },
    ],
    stream: true,
    think: true,
  })

  let startedThinking = false
  let finishedThinking = false

  for await (const chunk of response) {
    if (chunk.message.thinking && !startedThinking) {
      startedThinking = true
      process.stdout.write('Thinking:\n========\n\n')
    } else if (chunk.message.content && startedThinking && !finishedThinking) {
      finishedThinking = true
      process.stdout.write('\n\nResponse:\n========\n\n')
    }

    if (chunk.message.thinking) {
      process.stdout.write(chunk.message.thinking)
    } else if (chunk.message.content) {
      process.stdout.write(chunk.message.content)
    }
  }
}

main()
```

Please visit the [Ollama JavaScript library](https://github.com/ollama/ollama-python) for more information about its usage. More [examples](https://github.com/ollama/ollama-js/tree/main/examples) are available.

### Reference

- [GitHub](https://github.com/ollama/ollama/pull/10584/)

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
