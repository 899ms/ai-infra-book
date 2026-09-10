<!-- 从 claude-api-pricing.html 迁移的资料快照；原始 HTML SHA-256: db976b73de9f59d003ae80035e893da4e9c64170f3f832235c2ef0bac4dc9d94。 -->

[Models & pricing](/docs/en/models/overview)Lifecycle and reference

# Pricing

Copy page



Learn about Anthropic's pricing structure for models and features

Copy page



This page provides detailed pricing information for Anthropic's models and features. All prices are in USD.

For the most current pricing information, visit [claude.com/pricing](https://claude.com/pricing).

## Model pricing

The following table shows pricing for all Claude models:

| Model | Base input tokens | 5m cache writes | 1h cache writes | Cache hits and refreshes | Output tokens |
|----|----|----|----|----|----|
| Claude Fable 5.1 | \$10 / MTok | \$12.50 / MTok | \$20 / MTok | \$0.25 / MTok¹ | \$50 / MTok |
| Claude Mythos 5.1 ([limited availability](https://anthropic.com/glasswing)) | \$10 / MTok | \$12.50 / MTok | \$20 / MTok | \$0.25 / MTok¹ | \$50 / MTok |
| Claude Fable 5 | \$10 / MTok | \$12.50 / MTok | \$20 / MTok | \$1 / MTok | \$50 / MTok |
| Claude Mythos 5 ([limited availability](https://anthropic.com/glasswing)) | \$10 / MTok | \$12.50 / MTok | \$20 / MTok | \$1 / MTok | \$50 / MTok |
| Claude Opus 5 | \$5 / MTok | \$6.25 / MTok | \$10 / MTok | \$0.50 / MTok | \$25 / MTok |
| Claude Opus 4.8 | \$5 / MTok | \$6.25 / MTok | \$10 / MTok | \$0.50 / MTok | \$25 / MTok |
| Claude Opus 4.7 | \$5 / MTok | \$6.25 / MTok | \$10 / MTok | \$0.50 / MTok | \$25 / MTok |
| Claude Opus 4.6 | \$5 / MTok | \$6.25 / MTok | \$10 / MTok | \$0.50 / MTok | \$25 / MTok |
| Claude Opus 4.5 | \$5 / MTok | \$6.25 / MTok | \$10 / MTok | \$0.50 / MTok | \$25 / MTok |
| Claude Opus 4.1 ([retired, except on Bedrock and Google Cloud](/docs/en/about-claude/model-deprecations)) | \$15 / MTok | \$18.75 / MTok | \$30 / MTok | \$1.50 / MTok | \$75 / MTok |
| Claude Opus 4 ([retired, except on Google Cloud](/docs/en/about-claude/model-deprecations)) | \$15 / MTok | \$18.75 / MTok | \$30 / MTok | \$1.50 / MTok | \$75 / MTok |
| Claude Sonnet 5 | \$2 / MTok | \$2.50 / MTok | \$4 / MTok | \$0.20 / MTok | \$10 / MTok |
| Claude Sonnet 4.6 | \$3 / MTok | \$3.75 / MTok | \$6 / MTok | \$0.30 / MTok | \$15 / MTok |
| Claude Sonnet 4.5 | \$3 / MTok | \$3.75 / MTok | \$6 / MTok | \$0.30 / MTok | \$15 / MTok |
| Claude Sonnet 4 ([retired, except on Bedrock and Google Cloud](/docs/en/about-claude/model-deprecations)) | \$3 / MTok | \$3.75 / MTok | \$6 / MTok | \$0.30 / MTok | \$15 / MTok |
| Claude Haiku 4.5 | \$1 / MTok | \$1.25 / MTok | \$2 / MTok | \$0.10 / MTok | \$5 / MTok |
| Claude Haiku 3.5 ([retired, except on Bedrock and Google Cloud](/docs/en/about-claude/model-deprecations)) | \$0.80 / MTok | \$1 / MTok | \$1.60 / MTok | \$0.08 / MTok | \$4 / MTok |

*^(1 Cache hits and refreshes on Claude Fable 5.1 and Claude Mythos 5.1 are priced at 0.025x the base input price. All other models use the standard 0.1x multiplier.)*



The \$2/\$10 per million input/output token pricing for Claude Sonnet 5, announced at launch as introductory pricing through August 31, 2026, is now the standard price. The previously scheduled increase to \$3/\$15 per million input/output tokens on September 1, 2026 will not occur.



MTok = Million tokens. The "Base Input Tokens" column shows standard input pricing, the "5m Cache Writes", "1h Cache Writes", and "Cache Hits & Refreshes" columns are specific to [prompt caching](#prompt-caching), and "Output Tokens" shows output pricing. See [prompt caching pricing](#prompt-caching) for an explanation of the cache columns and pricing multipliers.



Claude 4.7 and later models and Claude Mythos Preview use a newer tokenizer that contributes to their improved performance on a wide range of tasks. This tokenizer produces approximately 30% more tokens for the same text. The exact increase depends on the content and workload shape. Claude Sonnet 4.6 and earlier models use the previous tokenizer.

For Claude Platform on AWS pricing, see [Claude Platform on AWS pricing](#claude-platform-on-aws-pricing).

## Cloud platform pricing

This section covers partner-operated cloud platforms, where the cloud provider invoices you. For Anthropic-operated cloud platforms billed through a marketplace, see [Claude Platform on AWS pricing](#claude-platform-on-aws-pricing) and [Claude in Microsoft Foundry pricing](#claude-in-microsoft-foundry-pricing).

Claude models are available on [Amazon Bedrock](/docs/en/build-with-claude/claude-in-amazon-bedrock) and [Google Cloud](/docs/en/build-with-claude/claude-on-vertex-ai). For official pricing, visit:

- [Amazon Bedrock pricing](https://aws.amazon.com/bedrock/pricing/)
- [Google Cloud pricing](https://cloud.google.com/vertex-ai/generative-ai/pricing#claude-models)



**Regional and multi-region endpoint pricing for Claude 4.5 models and beyond**

Starting with Claude Sonnet 4.5, Haiku 4.5, and Opus 4.5:

- **Bedrock** offers two endpoint types: global endpoints (dynamic routing for maximum availability) and regional endpoints (guaranteed data routing through specific geographic regions).
- **Google Cloud** offers three endpoint types: global endpoints, multi-region endpoints (dynamic routing within a geographic area), and regional endpoints.

Regional and multi-region endpoints include a 10% premium over global endpoints. The Claude API (first-party) is global by default; for first-party data residency options and pricing, see [Data residency pricing](#data-residency-pricing).

**Scope:** This pricing structure applies to Claude Sonnet 4.5, Haiku 4.5, Opus 4.5, and all future models. Earlier models (Claude Opus 4.1 and prior releases) retain their existing pricing.

For implementation details and code examples:

- [Amazon Bedrock global vs regional endpoints](/docs/en/build-with-claude/claude-in-amazon-bedrock#regions) for Opus 4.7, Haiku 4.5, and later models, or [the legacy integration](/docs/en/build-with-claude/claude-on-amazon-bedrock-legacy#global-vs-regional-endpoints) for all other models on Bedrock
- [Google Cloud global, multi-region, and regional endpoints](/docs/en/build-with-claude/claude-on-vertex-ai#global-multi-region-and-regional-endpoints)

## Claude Platform on AWS pricing

[Claude Platform on AWS](/docs/en/build-with-claude/claude-platform-on-aws) bills through AWS Marketplace using Claude Consumption Units (CCUs). Anthropic rates your token usage in USD at standard per-model, per-feature rates, applies any negotiated discount, converts the result to CCUs at \$0.01 per CCU, and reports the CCU quantity to AWS Marketplace hourly. Your AWS bill shows a single CCU line item.

| Concept | Details |
|:---|:---|
| **Billing unit** | Claude Consumption Unit (CCU) |
| **CCU price** | \$0.01 per CCU (fixed; discounts apply at token-to-CCU conversion, not to the CCU price) |
| **Conversion** | Token usage rated in USD at standard per-model, per-feature rates (same as [Claude API pricing](#model-pricing)), then converted to CCUs at \$0.01 per CCU |
| **Billing cadence** | Hourly metering to AWS Marketplace; monthly invoices |
| **Payment model** | Arrears only (postpaid); no prepaid credits |
| **Discounts** | Applied as fewer CCUs metered |
| **Tax** | Pre-tax metering; AWS Marketplace handles tax |
| **Cost visibility** | Real-time breakdown in the Claude Console (access through the AWS Console); AWS Cost Explorer shows aggregated CCU |



**Claude Consumption Units.** If Customer accesses the Services through certain Marketplace Platforms (e.g., Claude Platform on AWS), usage will be invoiced in Claude Consumption Units ("CCU") rather than per MTok. A CCU is a unit of measure used solely for Marketplace Platform invoicing. One hundred (100) CCU represents \$1.00 USD of fees owed for the Services, calculated at the applicable prices on [claude.com/pricing#api](https://claude.com/pricing#api), after application of any discounts.

### Inference geography

For Claude 4.6 and later models, using `inference_geo: "us"` applies a 1.1x pricing multiplier. `inference_geo: "global"` (default) uses standard pricing. See [Data residency](/docs/en/manage-claude/data-residency) for details.

### Private offers

When you sign up on the AWS Console **Claude Platform on AWS** service page, the AWS Console looks up any private offer associated with your account and prompts you to accept it in AWS Marketplace. Contact your Anthropic account representative for private offer terms.



If you have an existing Amazon Bedrock private offer, contact your Anthropic or AWS account representative before getting started with Claude Platform on AWS to ensure your discounts are applied correctly. Discounts cannot be applied retroactively to usage incurred before your private offer is accepted.

## Claude in Microsoft Foundry pricing

[Claude in Microsoft Foundry](/docs/en/build-with-claude/claude-in-microsoft-foundry) bills through the Azure Marketplace using Claude Consumption Units (CCUs). Anthropic rates your token usage in USD at standard per-model, per-feature rates, applies any negotiated discount, converts the result to CCUs at \$0.01 per CCU, and reports the CCU quantity to the Azure Marketplace hourly. Your Azure bill shows a single CCU line item.

| Concept | Details |
|:---|:---|
| **Billing unit** | Claude Consumption Unit (CCU) |
| **CCU price** | \$0.01 per CCU (fixed; discounts apply at token-to-CCU conversion, not to the CCU price) |
| **Conversion** | Token usage rated in USD at standard per-model, per-feature rates (same as [Claude API pricing](#model-pricing)), then converted to CCUs at \$0.01 per CCU |
| **Billing cadence** | Hourly metering to the Azure Marketplace; monthly invoices |
| **Payment model** | Arrears only (postpaid); no prepaid credits |
| **Discounts** | Applied as fewer CCUs metered |
| **Tax** | Pre-tax metering; Azure Marketplace handles tax |
| **Cost visibility** | Azure Cost Management shows aggregated CCU |



**Claude Consumption Units.** If Customer accesses the Services through certain Marketplace Platforms (e.g., Claude Platform on AWS, Claude in Microsoft Foundry), usage will be invoiced in Claude Consumption Units ("CCU") rather than per MTok. A CCU is a unit of measure used solely for Marketplace Platform invoicing. One hundred (100) CCU represents \$1.00 USD of fees owed for the Services, calculated at the applicable prices on [claude.com/pricing#api](https://claude.com/pricing#api), after application of any discounts.

### Inference geography

Deployments hosted on Azure can use the US Data Zone Standard deployment type, which keeps inference within the United States. This is equivalent to `inference_geo: "us"` on the Claude API and applies the same 1.1x pricing multiplier. See [Data residency](/docs/en/manage-claude/data-residency) for details.

## Feature-specific pricing

### Prompt caching

Prompt caching reduces costs and latency by reusing previously processed portions of your prompt across API calls. Instead of reprocessing the same large system prompt, document, or conversation history on every request, the API reads from cache at a fraction of the standard input price.

There are two ways to enable prompt caching:

- **Automatic caching:** Add a single `cache_control` field at the top level of your request. The system automatically manages cache breakpoints as conversations grow. This is the recommended starting point for most use cases.
- **Explicit cache breakpoints:** Place `cache_control` directly on individual content blocks for fine-grained control over exactly what gets cached.

Prompt caching uses the following pricing multipliers relative to base input token rates:

| Cache operation | Multiplier | Duration |
|:---|:---|:---|
| 5-minute cache write | 1.25x base input price | Cache valid for 5 minutes |
| 1-hour cache write | 2x base input price | Cache valid for 1 hour |
| Cache read (hit) | 0.1x base input price (0.025x on Claude Fable 5.1 and Claude Mythos 5.1) | Same duration as the preceding write |

Cache write tokens are charged when content is first stored. Cache read tokens are charged when a subsequent request retrieves the cached content. A cache hit costs 10% of the standard input price, which means caching pays off after one cache read for the 5-minute duration (1.25x write), or after two cache reads for the 1-hour duration (2x write). On Claude Fable 5.1 and Claude Mythos 5.1, a cache hit costs 2.5% of the standard input price (\$0.25 USD per million tokens).

These multipliers stack with other pricing modifiers, including the Batch API discount and data residency.

For implementation details, supported models, and code examples, see [Prompt caching](/docs/en/build-with-claude/prompt-caching).

### Data residency pricing

For Claude 4.6 and later models, specifying US-only inference through the `inference_geo` parameter incurs a 1.1x multiplier on all token pricing categories, including input tokens, output tokens, cache writes, and cache reads. Global routing (the default) uses standard pricing.

This applies to the Claude API (first-party) and Claude Platform on AWS. On Claude in Microsoft Foundry, the same 1.1x multiplier applies to deployments that use the US Data Zone Standard deployment type (see [Inference geography](#foundry-inference-geography)). Partner-operated platforms (Bedrock and Google Cloud) have independent regional pricing. See [Bedrock](https://aws.amazon.com/bedrock/pricing/) and [Google Cloud](https://cloud.google.com/vertex-ai/generative-ai/pricing#claude-models) for details. Earlier models do not support the `inference_geo` parameter and always use standard pricing; requests that include the parameter on these models return a 400 error.

For more information, see [Data residency](/docs/en/manage-claude/data-residency).

### Fast mode pricing

[Fast mode](/docs/en/build-with-claude/fast-mode), in research preview, provides significantly faster output for Claude Opus 5 and Claude Opus 4.8 at premium pricing. Fast mode pricing applies across the full context window, including requests over 200k input tokens. Fast mode is available on the Claude API (first-party) only; it is not available on Claude Platform on AWS or partner-operated cloud platforms.

| Model                           | Input       | Output      |
|:--------------------------------|:------------|:------------|
| Claude Opus 5 / Claude Opus 4.8 | \$10 / MTok | \$50 / MTok |

Fast mode is not available on Claude Opus 4.7 (requests with `speed: "fast"` return an error) or Claude Opus 4.6 (requests run at standard speed and are billed at standard rates). See [Fast mode](/docs/en/build-with-claude/fast-mode#supported-models).

Fast mode pricing stacks with other pricing modifiers:

- [Prompt caching multipliers](#prompt-caching) apply on top of fast mode pricing
- [Data residency](/docs/en/manage-claude/data-residency) multipliers apply on top of fast mode pricing

Fast mode is not available with the [Batch API](#batch-processing).

For more information, see [Fast mode](/docs/en/build-with-claude/fast-mode).

### Batch processing

The Batch API allows asynchronous processing of large volumes of requests with a 50% discount on both input and output tokens.

| Model | Batch input | Batch output |
|----|----|----|
| Claude Fable 5.1 | \$5 / MTok | \$25 / MTok |
| Claude Mythos 5.1 ([limited availability](https://anthropic.com/glasswing)) | \$5 / MTok | \$25 / MTok |
| Claude Fable 5 | \$5 / MTok | \$25 / MTok |
| Claude Mythos 5 ([limited availability](https://anthropic.com/glasswing)) | \$5 / MTok | \$25 / MTok |
| Claude Opus 5 | \$2.50 / MTok | \$12.50 / MTok |
| Claude Opus 4.8 | \$2.50 / MTok | \$12.50 / MTok |
| Claude Opus 4.7 | \$2.50 / MTok | \$12.50 / MTok |
| Claude Opus 4.6 | \$2.50 / MTok | \$12.50 / MTok |
| Claude Opus 4.5 | \$2.50 / MTok | \$12.50 / MTok |
| Claude Opus 4.1 ([retired, except on Bedrock and Google Cloud](/docs/en/about-claude/model-deprecations)) | \$7.50 / MTok | \$37.50 / MTok |
| Claude Opus 4 ([retired, except on Google Cloud](/docs/en/about-claude/model-deprecations)) | \$7.50 / MTok | \$37.50 / MTok |
| Claude Sonnet 5 | \$1 / MTok | \$5 / MTok |
| Claude Sonnet 4.6 | \$1.50 / MTok | \$7.50 / MTok |
| Claude Sonnet 4.5 | \$1.50 / MTok | \$7.50 / MTok |
| Claude Sonnet 4 ([retired, except on Bedrock and Google Cloud](/docs/en/about-claude/model-deprecations)) | \$1.50 / MTok | \$7.50 / MTok |
| Claude Haiku 4.5 | \$0.50 / MTok | \$2.50 / MTok |
| Claude Haiku 3.5 ([retired, except on Bedrock and Google Cloud](/docs/en/about-claude/model-deprecations)) | \$0.40 / MTok | \$2 / MTok |

For more information about batch processing, see [Batch processing](/docs/en/build-with-claude/batch-processing).

### Long context pricing

Claude 4.6 and later models and [Claude Mythos Preview](https://anthropic.com/glasswing) include the full [1M token context window](/docs/en/build-with-claude/context-windows) at standard pricing. (A 900k-token request is billed at the same per-token rate as a 9k-token request.) Prompt caching and batch processing discounts apply at standard rates across the full context window.

### Tool use pricing

Tool use requests are priced based on:

1.  The total number of input tokens sent to the model (including in the `tools` parameter)
2.  The number of output tokens generated
3.  For server-side tools, additional usage-based pricing (for example, web search charges per search performed)

Client-side tools are priced the same as any other Claude API request, although server-side tools can incur additional charges based on their specific usage.

The additional tokens from tool use come from:

- The `tools` parameter in API requests (tool names, descriptions, and schemas)
- `tool_use` content blocks in API requests and responses
- `tool_result` content blocks in API requests

When you use `tools`, the API also automatically includes a special system prompt for the model that enables tool use. The number of tool use tokens required for each model is listed in the following table (excluding the additional tokens listed earlier). Note that the table assumes at least 1 tool is provided. If no `tools` are provided, then a tool choice of `none` uses 0 additional system prompt tokens.

[TABLE]

These token counts are added to your normal input and output tokens to calculate the total cost of a request.

For current per-model prices, refer to the [model pricing](#model-pricing) section.

For more information about tool use implementation and best practices, see [Tool use](/docs/en/agents-and-tools/tool-use/overview).

### Specific tool pricing

#### Bash tool

The bash tool definition adds the following input tokens to your request. This is in addition to the per-model [tool use system prompt](/docs/en/agents-and-tools/tool-use/overview#pricing) that applies whenever any tool is present.

| Model | Additional input tokens |
|----|----|
| Claude Opus 5, Claude Opus 4.8, and Claude Opus 4.7 | 325 tokens |
| Claude Opus 4.6, Claude Sonnet 4.6, and earlier | 244 tokens |

Additional tokens are consumed by:

- Command outputs (stdout/stderr)
- Error messages
- Large file contents

See [tool use pricing](#tool-use-pricing) for complete pricing details.

#### Code execution tool

**Code execution is free when used with web search or web fetch.** When `web_search_20260209` (or later) or `web_fetch_20260209` (or later) is included in your API request, there are no additional charges for code execution tool calls beyond the standard input and output token costs.

When used without these tools, code execution is billed by execution time, tracked separately from token usage:

- Execution time has a minimum of 5 minutes
- Each organization receives **1,550 free hours** of usage per month
- Additional usage beyond 1,550 hours is billed at **\$0.05 USD per hour, per container**
- If files are included in the request, execution time is billed even if the tool is not called, because files are preloaded onto the container

Code execution usage is tracked in the response:

``` shiki
{
  "usage": {
    "input_tokens": 105,
    "output_tokens": 239,
    "server_tool_use": {
      "code_execution_requests": 1
    }
  }
}
```



#### Text editor tool

The text editor tool uses the same pricing structure as other tools used with Claude. It follows the standard input and output token pricing based on the Claude model you're using.

In addition to the base tokens, the following additional input tokens are needed for the text editor tool:

| Tool                                | Additional input tokens |
|-------------------------------------|-------------------------|
| `text_editor_20250429` (Claude 4.x) | 700 tokens              |

See [tool use pricing](#tool-use-pricing) for complete pricing details.

#### Web search tool

Web search usage is charged in addition to token usage:

``` shiki
{
  "usage": {
    "input_tokens": 105,
    "output_tokens": 6039,
    "cache_read_input_tokens": 7123,
    "cache_creation_input_tokens": 7345,
    "server_tool_use": {
      "web_search_requests": 1
    }
  }
}
```



Web search is available on the Claude API for **\$10 per 1,000 searches**, plus standard token costs for search-generated content. Web search results retrieved throughout a conversation are counted as input tokens, in search iterations executed during a single turn and in subsequent conversation turns.

Each web search counts as one use, regardless of the number of results returned. If an error occurs during web search, the web search will not be billed.

#### Web fetch tool

Web fetch usage has **no additional charges** beyond standard token costs:

``` shiki
{
  "usage": {
    "input_tokens": 25039,
    "output_tokens": 931,
    "cache_read_input_tokens": 0,
    "cache_creation_input_tokens": 0,
    "server_tool_use": {
      "web_fetch_requests": 1
    }
  }
}
```



The web fetch tool is available on the Claude API at **no additional cost**. You only pay standard token costs for the fetched content that becomes part of your conversation context.

To protect against inadvertently fetching large content that would consume excessive tokens, use the `max_content_tokens` parameter to set appropriate limits based on your use case and budget considerations.

Example token usage for typical content:

- Average web page (10 kB): ~2,500 tokens
- Large documentation page (100 kB): ~25,000 tokens
- Research paper PDF (500 kB): ~125,000 tokens

#### Computer use tool

Computer use follows the standard [tool use pricing](/docs/en/agents-and-tools/tool-use/overview#pricing). When using the computer use tool:

**Toolset definition overhead:** Declaring `computer_toolset_20260801` with its default members adds about 4,500 input tokens to a request (about 4,520 on Claude Fable 5, Claude Mythos 5, Claude Opus 5, and Claude Opus 4.8, and about 4,590 on Claude Sonnet 5), which covers the member tool definitions and the tool use system prompt. Disabling `zoom` with `configs` removes about 410 of those tokens. The exact count for a request is reported in the response `usage`, and you can estimate it in advance with the [token counting endpoint](/docs/en/build-with-claude/token-counting).

**Earlier tool versions:** The following figures apply to the `computer_20251124` and `computer_20250124` tool versions, not to `computer_toolset_20260801`:

- System prompt overhead: 466–499 tokens added to the system prompt
- Tool definition: about 735 input tokens per tool definition (measured with `computer_20250124`)

**Additional token consumption:**

- Screenshot and zoom images returned in tool results, billed as image input (see [Vision pricing](/docs/en/build-with-claude/vision#evaluate-image-size))
- Tool execution results returned to Claude



If you're also using bash or text editor tools alongside computer use, those tools have their own token costs as documented in their respective pages.

#### Browser use tool

Browser use follows the standard [tool use pricing](/docs/en/agents-and-tools/tool-use/overview#pricing). When using the browser use tool:

**Toolset definition overhead:** Declaring `browser_toolset_20260801` with its default members adds about 6,600 input tokens to a request (about 6,610 on Claude Fable 5, Claude Mythos 5, Claude Opus 5, and Claude Opus 4.8, and about 6,670 on Claude Sonnet 5), which covers the member tool definitions and the tool use system prompt. Enabling all four optional members adds about 880 tokens, and disabling members with `configs` reduces the count. The exact count for a request is reported in the response `usage`, and you can estimate it in advance with the [token counting endpoint](/docs/en/build-with-claude/token-counting).

**Additional token consumption:**

- Screenshot and zoom images returned in tool results, billed as image input (see [Vision pricing](/docs/en/build-with-claude/vision#evaluate-image-size))
- Text tool results returned to Claude, such as accessibility trees, page text, and console or network entries



If you also use the computer use tool, bash tool, text editor tool, or your own tools alongside browser use, those tools have their own token costs as documented on their respective pages.

## Claude Managed Agents pricing

[Claude Managed Agents](/docs/en/managed-agents/overview) is billed on two dimensions: tokens and session runtime.

### Tokens

All tokens consumed by a Claude Managed Agents session are billed at the rates shown in [Model pricing](#model-pricing). [Prompt caching](#prompt-caching) multipliers apply identically. Web search triggered inside a session incurs the standard \$10 per 1,000 searches. On [Claude Platform on AWS](#claude-platform-on-aws-pricing), session token and runtime charges convert to Claude Consumption Units at the standard rate. [Fast mode](#fast-mode-pricing) premium pricing applies when an agent's `model.speed` is set to `"fast"`.

The [data residency multiplier](#data-residency-pricing) also applies: when an agent's `model.inference_geo` is pinned to `"us"`, tokens consumed by sessions running that agent are billed at 1.1x the standard rates, the same multiplier that applies to US-only inference on the Messages API.

The following Messages API modifiers do **not** apply to Claude Managed Agents sessions:

| Modifier | Why it doesn't apply |
|----|----|
| [Batch API discount](#batch-processing) | Sessions are stateful and interactive. There is no batch mode. |
| [Cloud platform pricing](#cloud-platform-pricing) | Not available on partner-operated cloud platforms. |

### Session runtime

| SKU             | Rate                    | Metering                  |
|-----------------|-------------------------|---------------------------|
| Session runtime | \$0.08 per session-hour | `running` status duration |

Runtime is measured to the millisecond and accrues only while the session's status is `running`. Time spent `idle` (waiting for your next message or a tool confirmation), `rescheduling`, or `terminated` does not count toward runtime.



Session runtime replaces the [code execution](#code-execution-tool) container-hour billing model when using Claude Managed Agents. You are not separately billed for container hours on top of session runtime.

### Worked example

A one-hour coding session using Claude Opus 5 that consumes 50,000 input tokens and 15,000 output tokens:

| Line item       | Calculation               | Cost        |
|-----------------|---------------------------|-------------|
| Input tokens    | 50,000 × \$5 / 1,000,000  | \$0.25      |
| Output tokens   | 15,000 × \$25 / 1,000,000 | \$0.375     |
| Session runtime | 1.0 hour × \$0.08         | \$0.08      |
| **Total**       |                           | **\$0.705** |

If prompt caching is active and 40,000 of the input tokens are cache reads:

| Line item             | Calculation                    | Cost        |
|-----------------------|--------------------------------|-------------|
| Uncached input tokens | 10,000 × \$5 / 1,000,000       | \$0.05      |
| Cache read tokens     | 40,000 × \$5 × 0.1 / 1,000,000 | \$0.02      |
| Output tokens         | 15,000 × \$25 / 1,000,000      | \$0.375     |
| Session runtime       | 1.0 hour × \$0.08              | \$0.08      |
| **Total**             |                                | **\$0.525** |



Example calculation for processing 10,000 support tickets:

- Average ~3,700 tokens per conversation
- Using Claude Haiku 4.5 at \$1/MTok input, \$5/MTok output
- Total cost: ~\$37.00 per 10,000 tickets

For a detailed walkthrough of this calculation, see the [customer support agent guide](/docs/en/about-claude/use-case-guides/customer-support-chat).

## Additional pricing considerations

### Cost optimization strategies

When building agents with Claude:

1.  **Use appropriate models:** Choose Haiku for simple tasks, Sonnet for most production workloads, and Opus for the most complex reasoning
2.  **Implement prompt caching:** Reduce costs for repeated context
3.  **Batch operations:** Use the Batch API for non-time-sensitive tasks
4.  **Monitor usage patterns:** Track token consumption to identify optimization opportunities



For high-volume agent applications, contact the [enterprise sales team](https://claude.com/contact-sales) for custom pricing arrangements.

### Rate limits

Rate limits vary by usage tier and affect how many requests you can make:

- **Start tier:** Entry-level limits for getting started
- **Build tier:** Increased limits for growing applications
- **Scale tier:** Highest standard limits for production workloads

For detailed rate limit information, see [Rate limits](/docs/en/api/rate-limits).

For limits beyond the Scale tier or custom pricing arrangements, [contact the sales team](https://claude.com/contact-sales).

### Volume discounts

Volume discounts may be available for high-volume users. These are negotiated on a case-by-case basis.

- Standard usage tiers use the pricing shown in [Model pricing](#model-pricing)
- Enterprise customers can [contact sales](mailto:sales@anthropic.com) for custom pricing
- Academic and research discounts may be available

### Enterprise pricing

For enterprise customers with specific needs:

- Custom rate limits
- Volume discounts
- Dedicated support
- Custom terms

Contact the sales team at <sales@anthropic.com> or through the [Claude Console](/settings/limits) to discuss enterprise pricing options.

## Billing and payment

- Billing is based on actual monthly usage
- All payments are in USD
- Credit card and invoicing options available
- Usage tracking available in the [Claude Console](/)

## Frequently asked questions

### How is token usage calculated?

Tokens are pieces of text that models process. As a rough estimate, 1 token is approximately 4 characters or 0.75 words in English. The exact count varies by language and content type.

### Are there free tiers or trials?

New users receive a small amount of free credits to test the API. [Contact sales](mailto:sales@anthropic.com) for information about extended trials for enterprise evaluation.

### How do discounts stack?

Batch API and prompt caching discounts can be combined. For example, using both features together provides significant cost savings compared to standard API calls. See [prompt caching pricing](#prompt-caching) for how the multipliers interact.

### What payment methods are accepted?

Major credit cards are accepted for standard accounts. Enterprise customers can arrange invoicing and other payment methods.

For additional questions about pricing, contact <support@anthropic.com>.

Was this page helpful?





- [Model pricing](#model-pricing)
- [Cloud platform pricing](#cloud-platform-pricing)
- [Claude Platform on AWS pricing](#claude-platform-on-aws-pricing)
- [Inference geography](#inference-geography)
- [Private offers](#private-offers)
- [Claude in Microsoft Foundry pricing](#claude-in-microsoft-foundry-pricing)
- [Inference geography](#foundry-inference-geography)
- [Feature-specific pricing](#feature-specific-pricing)
- [Prompt caching](#prompt-caching)
- [Data residency pricing](#data-residency-pricing)
- [Fast mode pricing](#fast-mode-pricing)
- [Batch processing](#batch-processing)
- [Long context pricing](#long-context-pricing)
- [Tool use pricing](#tool-use-pricing)
- [Specific tool pricing](#specific-tool-pricing)
- [Claude Managed Agents pricing](#claude-managed-agents-pricing)
- [Tokens](#tokens)
- [Session runtime](#session-runtime)
- [Worked example](#worked-example)
- [Additional pricing considerations](#additional-pricing-considerations)
- [Cost optimization strategies](#cost-optimization-strategies)
- [Rate limits](#rate-limits)
- [Volume discounts](#volume-discounts)
- [Enterprise pricing](#enterprise-pricing)
- [Billing and payment](#billing-and-payment)
- [Frequently asked questions](#frequently-asked-questions)
- [How is token usage calculated?](#how-is-token-usage-calculated)
- [Are there free tiers or trials?](#are-there-free-tiers-or-trials)
- [How do discounts stack?](#how-do-discounts-stack)
- [What payment methods are accepted?](#what-payment-methods-are-accepted)

[](/docs/en/home)

![](data:image/svg+xml;base64,PHN2ZyBkYXRhLWNkcz0iU3BhcmsiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld2JveD0iMCAwIDEwMCAxMDAiIHdpZHRoPSIyNiIgaGVpZ2h0PSIyNiIgZmlsbD0idmFyKC0tY2RzLWNsYXksICNkOTc3NTcpIiBjbGFzcz0ic2hyaW5rLTAiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJtMTkuNiA2Ni41IDE5LjctMTEgLjMtMS0uMy0uNWgtMWwtMy4zLS4yLTExLjItLjNMMTQgNTNsLTkuNS0uNS0yLjQtLjVMMCA0OWwuMi0xLjUgMi0xLjMgMi45LjIgNi4zLjUgOS41LjYgNi45LjRMMzggNDkuMWgxLjZsLjItLjctLjUtLjQtLjQtLjRMMjkgNDFsLTEwLjYtNy01LjYtNC4xLTMtMi0xLjUtMi0uNi00LjIgMi43LTMgMy43LjMuOS4yIDMuNyAyLjkgOCA2LjFMMzcgMzZsMS41IDEuMi42LS40LjEtLjMtLjctMS4xTDMzIDI1bC02LTEwLjQtMi43LTQuMy0uNy0yLjZjLS4zLTEtLjQtMi0uNC0zbDMtNC4yTDI4IDBsNC4yLjZMMzMuOCAybDIuNiA2IDQuMSA5LjNMNDcgMjkuOWwyIDMuOCAxIDMuNC4zIDFoLjd2LS41bC41LTcuMiAxLTguNyAxLTExLjIuMy0zLjIgMS42LTMuOCAzLTJMNjEgMi42bDIgMi45LS4zIDEuOC0xLjEgNy43TDU5IDI3LjFsLTEuNSA4LjJoLjlsMS0xLjEgNC4xLTUuNCA2LjktOC42IDMtMy41TDc3IDEzbDIuMy0xLjhoNC4zbDMuMSA0LjctMS40IDQuOS00LjQgNS42LTMuNyA0LjctNS4zIDcuMS0zLjIgNS43LjMuNGguN2wxMi0yLjYgNi40LTEuMSA3LjYtMS4zIDMuNSAxLjYuNCAxLjYtMS40IDMuNC04LjIgMi05LjYgMi0xNC4zIDMuMy0uMi4xLjIuMyA2LjQuNiAyLjguMmg2LjhsMTIuNiAxIDMuMyAyIDEuOSAyLjctLjMgMi01LjEgMi42LTYuOC0xLjYtMTYtMy44LTUuNC0xLjNoLS44di40bDQuNiA0LjUgOC4zIDcuNUw4OSA4MC4xbC41IDIuNC0xLjMgMi0xLjQtLjItOS4yLTctMy42LTMtOC02LjhoLS41di43bDEuOCAyLjcgOS44IDE0LjcuNSA0LjUtLjcgMS40LTIuNiAxLTIuNy0uNi01LjgtOC02LTktNC43LTguMi0uNS40LTIuOSAzMC4yLTEuMyAxLjUtMyAxLjItMi41LTItMS40LTMgMS40LTYuMiAxLjYtOCAxLjMtNi40IDEuMi03LjkuNy0yLjZ2LS4ySDQ5TDQzIDcybC05IDEyLjMtNy4yIDcuNi0xLjcuNy0zLTEuNS4zLTIuOEwyNCA4NmwxMC0xMi44IDYtNy45IDQtNC42LS4xLS41aC0uM0wxNy4yIDc3LjRsLTQuNy42LTItMiAuMi0zIDEtMSA4LTUuNVoiIC8+PC9zdmc+)

Claude Platform Docs

[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNyIgaGVpZ2h0PSIxNyIgdmlld2JveD0iMCAwIDE3IDE3IiBmaWxsPSJub25lIiBjbGFzcz0idy1bMTZweF0gaC1bMTZweF0iPjxwYXRoIGQ9Ik0xMC4wNTggNy4yOTAyM0wxNS45MDYxIDAuNTE4Nzk5SDE0LjUyMDNMOS40NDI0MSA2LjM5ODM0TDUuMzg2NzMgMC41MTg3OTlIMC43MDg5ODRMNi44NDE5NyA5LjQwOTdMMC43MDg5ODQgMTYuNTEwNkgyLjA5NDg3TDcuNDU3MjMgMTAuMzAxNkwxMS43NDAzIDE2LjUxMDZIMTYuNDE4MUwxMC4wNTc3IDcuMjkwMjNIMTAuMDU4Wk04LjE1OTg3IDkuNDg4MDNMNy41Mzg0NyA4LjYwMjdMMi41OTQyMiAxLjU1ODAxSDQuNzIyODVMOC43MTI5MiA3LjI0MzNMOS4zMzQzMiA4LjEyODYzTDE0LjUyMDkgMTUuNTE4NkgxMi4zOTIzTDguMTU5ODcgOS40ODgzN1Y5LjQ4ODAzWiIgZmlsbD0iY3VycmVudENvbG9yIiAvPjwvc3ZnPg==)](https://x.com/claudeai)[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNyIgaGVpZ2h0PSIxNyIgdmlld2JveD0iMCAwIDk3Ni45OCAxMDgyIiBmaWxsPSJub25lIiBjbGFzcz0idy1bMTZweF0gaC1bMTZweF0iPjxwYXRoIGQ9Ik03NzAuMzUsNTAwLjM1Yy0xLjM1LTE1Ni44NS04Ni4zOS0yNTEuMzctMjMwLjAyLTI1MS4zNy05NS44NywwLTE3Ni41LDQzLjM2LTIxOC44NSwxMTIuNDdsOTIuODIsNjQuNzFjMjQuMDUtMzcuOTQsNTcuMjUtNjkuNDUsMTE4LjIzLTY5LjQ1LDY4Ljc3LDAsMTA0LjM0LDM4LjI4LDExNC41LDEwOS40Mi0zMy4yLTUuMDgtNjYuNC03Ljc5LTEwMC42MS03Ljc5LTE4NS42NSwwLTI3My4wNSw4NC4wMi0yNzMuMDUsMTk1LjEzczg3LjQsMTc5LjU1LDIxNi4xNCwxNzkuNTVjMTQxLjI3LDAsMjI1LjYyLTk1LjE5LDI2MC4xOC0yMTMuMDksMzUuOTEsMTYuMjYsNjAuNjQsNTQuMiw2MC42NCwxMTEuMTIsMCwxNTIuNDUtMTc1LjgyLDIzNS40NS0zMjQuODgsMjM1LjQ1LTIxOS44NiwwLTM2My41LTE0NC4zMi0zNjMuNS0zNzkuMDgsMC0yODcuNjIsMTkwLjA1LTQ3MS45MSw0NDUuNDgtNDcxLjkxLDE3MS40MiwwLDI1Ni4xMSw3NS4yMSwzMTMuNywxNzYuMTZsOTQuODYtNjYuNEM5MTMuMzEsOTQuNSw3NzMuNCwxLDU2My4zNiwxLDIyOC42NSwxLDEsMjM4LjQ4LDEsNTgzLjAxYzAsMzE1LjA2LDIyMi45MSw0OTcuOTksNDg4LjUxLDQ5Ny45OSwyMTkuNTIsMCw0NDEuNDItMTI4LjA1LDQ0MS40Mi0zNDcuMjQsMC0xMTQuNS02NS43Mi0xOTAuMzktMTYwLjU4LTIzMy40MWgwWk00ODUuNDQsNzE4Ljg1Yy00OC40NCwwLTkxLjEzLTIzLjA0LTkxLjEzLTY1LjM4LDAtNjYuNzQsODEuOTgtODcuMDYsMTYyLjI3LTg3LjA2LDMwLjQ5LDAsNjAuMywyLjAzLDg2LjcyLDcuNzktMTguOTcsODYuNzItNzUuMjEsMTQ0LjY2LTE1Ny44NywxNDQuNjZoMFoiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)](https://www.threads.com/@claudeai)[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNyIgdmlld2JveD0iMCAwIDE2IDE3IiBmaWxsPSJub25lIiBjbGFzcz0idy1bMTZweF0gaC1bMTZweF0iPjxwYXRoIGQ9Ik0xMy45NjM5IDAuNjY0Nzk1QzE0LjkyNzYgMC42NjQ5MiAxNS43MDg4IDEuNDQ2MTYgMTUuNzA5IDIuNDA5OTFWMTQuNjI4N0MxNS43MDg5IDE1LjU5MjUgMTQuOTI3NyAxNi4zNzM3IDEzLjk2MzkgMTYuMzczOEgxLjc0NTEyQzAuNzgxMzYxIDE2LjM3MzYgMC4wMDAxMjQ3MDEgMTUuNTkyNCAwIDE0LjYyODdWMi40MDk5MUMwLjAwMDE4MjI3OCAxLjQ0NjE5IDAuNzgxMzk3IDAuNjY0OTc3IDEuNzQ1MTIgMC42NjQ3OTVIMTMuOTYzOVpNMi40MDcyMyAxNC4xOTIxSDQuNzVWNi42Mjc2OUgyLjQwNzIzVjE0LjE5MjFaTTEwLjc3NDQgNi4zOTcyMkM5LjE2OTM2IDYuMzk3MjIgOC40OTQxNCA3LjY0NzIyIDguNDk0MTQgNy42NDcyMlY2LjYyNzY5SDYuMjQ3MDdWMTQuMTkyMUg4LjQ5NDE0VjEwLjIyMTRDOC40OTQxNCA5LjE1NzU4IDguOTgzNTcgOC41MjQxNyA5LjkyMDkgOC41MjQxN0MxMC43ODI1IDguNTI0MTggMTEuMTk2MyA5LjEzMjg2IDExLjE5NjMgMTAuMjIxNFYxNC4xOTIxSDEzLjUyNzNWOS40MDMwOEMxMy41MjczIDcuMzc2OSAxMi4zNzg3IDYuMzk3MjQgMTAuNzc0NCA2LjM5NzIyWk0zLjU2NzM4IDIuODQ2NDRDMi44MDIxNiAyLjg0NjQ0IDIuMTgxNjQgMy40NzExOCAyLjE4MTY0IDQuMjQxOTRDMi4xODE2NiA1LjAxMjY5IDIuODAyMTcgNS42Mzc0NSAzLjU2NzM4IDUuNjM3NDVDNC4zMzI0OCA1LjYzNzMxIDQuOTUyMTMgNS4wMTI2IDQuOTUyMTUgNC4yNDE5NEM0Ljk1MjE1IDMuNDcxMjcgNC4zMzI0OSAyLjg0NjU4IDMuNTY3MzggMi44NDY0NFoiIGZpbGw9ImN1cnJlbnRDb2xvciIgLz48L3N2Zz4=)](https://www.linkedin.com/showcase/claude)[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNyIgaGVpZ2h0PSIxMiIgdmlld2JveD0iMCAwIDE3IDEyIiBmaWxsPSJub25lIiBjbGFzcz0idy1bMTZweF0gaC1bMTZweF0iPjxwYXRoIGQ9Ik02Ljk1NzcyIDguMzM2MTJWMy42NjU0OUwxMS4wNjM3IDYuMDAxMDdMNi45NTc3MiA4LjMzNjEyWk0xNi4wOTA1IDIuMTk1MjJDMTUuOTA1MSAxLjUxMzc3IDE1LjM4MTMgMC45ODY4MzcgMTQuNzE1NiAwLjgwMDM2OEwxNC43MDE0IDAuNzk3MjI1QzEzLjAyOSAwLjU4NDU2NyAxMS4wOTQ2IDAuNDYzMDQ4IDkuMTMxNDQgMC40NjMwNDhDOC45MzE4OCAwLjQ2MzA0OCA4LjczMjg0IDAuNDY0MDk2IDguNTM0MzIgMC40NjY3MTVMOC41NjQ3IDAuNDY2MTkxQzguMzk2MDQgMC40NjQwOTYgOC4xOTc1MiAwLjQ2MjUyNCA3Ljk5Nzk2IDAuNDYyNTI0QzYuMDM0OCAwLjQ2MjUyNCA0LjA5OTQgMC41ODQwNDMgMi4xOTk2MiAwLjgxOTIyNUwyLjQyNjk0IDAuNzk2MTc4QzEuNzQ3NTkgMC45ODYzMTMgMS4yMjM4IDEuNTEyNzIgMS4wNDIwNCAyLjE4MDU1TDEuMDM4OSAyLjE5NDE3QzAuODI5Mzg1IDMuMjk4ODQgMC43MDk5NjEgNC41NzAwOCAwLjcwOTk2MSA1Ljg2OTA3QzAuNzA5OTYxIDUuOTE1MTcgMC43MDk5NjEgNS45NjEyNiAwLjcxMDQ4NSA2LjAwNjgzVjUuOTk5NUMwLjcxMDQ4NSA2LjAzODI2IDAuNzA5OTYxIDYuMDg0MzUgMC43MDk5NjEgNi4xMzA0NEMwLjcwOTk2MSA3LjQyOTQ0IDAuODI5OTA5IDguNzAwMTUgMS4wNTg4IDkuOTMyNjNMMS4wMzg5IDkuODA0ODJDMS4yMjQzMiAxMC40ODYzIDEuNzQ4MTEgMTEuMDEzMiAyLjQxMzg1IDExLjE5OTdMMi40Mjc5OSAxMS4yMDI4QzQuMTAwNDUgMTEuNDE1NSA2LjAzNDggMTEuNTM3IDcuOTk3OTYgMTEuNTM3QzguMTk3IDExLjUzNyA4LjM5NjA0IDExLjUzNTkgOC41OTUwOCAxMS41MzMzTDguNTY0NyAxMS41MzM4QzguNzMzMzYgMTEuNTM1OSA4LjkzMjQgMTEuNTM3NSA5LjEzMTQ0IDExLjUzNzVDMTEuMDk1MSAxMS41Mzc1IDEzLjAzIDExLjQxNiAxNC45Mjk4IDExLjE4MDhMMTQuNzAyNSAxMS4yMDM5QzE1LjM4MjMgMTEuMDE0MyAxNS45MDYxIDEwLjQ4NzMgMTYuMDg4NCA5LjgxOTQ5TDE2LjA5MTUgOS44MDU4N0MxNi4zMDA1IDguNzAxMiAxNi40MiA3LjQyOTk2IDE2LjQyIDYuMTMxNDlDMTYuNDIgNi4wODU0IDE2LjQyIDYuMDM5MyAxNi40MTk0IDUuOTkzNzRWNi4wMDA1NEMxNi40MTk0IDUuOTYxNzggMTYuNDIgNS45MTU2OSAxNi40MiA1Ljg2OTZDMTYuNDIgNC41NzA2IDE2LjMgMy4yOTk4OSAxNi4wNzExIDIuMDY3NDFMMTYuMDkwNSAyLjE5NTIyWiIgZmlsbD0iY3VycmVudENvbG9yIiAvPjwvc3ZnPg==)](https://www.youtube.com/@anthropic-ai)[![](data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNyIgaGVpZ2h0PSIxNyIgdmlld2JveD0iMCAwIDE3IDE3IiBmaWxsPSJub25lIiBjbGFzcz0idy1bMTZweF0gaC1bMTZweF0iPjxnIGNsaXAtcGF0aD0idXJsKCNjbGlwMF82NV8xMTgzKSI+PHBhdGggZD0iTTUuMDE5NzMgMC43MTk0ODRDNC4xODQwMSAwLjc1ODkxMyAzLjYxMzMgMC44OTIyODQgMy4xMTQzOCAxLjA4ODMzQzIuNTk4MDIgMS4yODk1NyAyLjE2MDM2IDEuNTU5NjEgMS43MjQ5MSAxLjk5NjYzQzEuMjg5NDUgMi40MzM2NiAxLjAyMTMgMi44NzE2MyAwLjgyMTQ3OCAzLjM4ODc3QzAuNjI4MDk5IDMuODg4NzkgMC40OTcwODUgNC40NTk5OCAwLjQ2MDE2OSA1LjI5NjE3QzAuNDIzMjUzIDYuMTMyMzcgMC40MTUwODQgNi40MDExNSAwLjQxOTE2OCA4LjUzNDEzQzAuNDIzMjUzIDEwLjY2NzEgMC40MzI2NzggMTAuOTM0NSAwLjQ3MzIwNyAxMS43NzI0QzAuNTEzMTA5IDEyLjYwOCAwLjY0NjAwNyAxMy4xNzg1IDAuODQyMDU3IDEzLjY3NzZDMS4wNDM2IDE0LjE5NCAxLjMxMzMzIDE0LjYzMTUgMS43NTA1MSAxNS4wNjcxQzIuMTg3NyAxNS41MDI3IDIuNjI1MzUgMTUuNzcwMiAzLjE0Mzc1IDE1Ljk3MDNDMy42NDMzIDE2LjE2MzQgNC4yMTQ2NCAxNi4yOTUgNS4wNTA2OCAxNi4zMzE2QzUuODg2NzIgMTYuMzY4MyA2LjE1NTgxIDE2LjM3NjcgOC4yODgxNyAxNi4zNzI3QzEwLjQyMDUgMTYuMzY4NiAxMC42ODkgMTYuMzU5MSAxMS41MjY4IDE2LjMxOTRDMTIuMzY0NSAxNi4yNzk3IDEyLjkzMjEgMTYuMTQ1OCAxMy40MzEzIDE1Ljk1MDdDMTMuOTQ3NyAxNS43NDg3IDE0LjM4NTUgMTUuNDc5NCAxNC44MjA4IDE1LjA0MjFDMTUuMjU2MSAxNC42MDQ3IDE1LjUyNDEgMTQuMTY2NSAxNS43MjM4IDEzLjY0OUMxNS45MTczIDEzLjE0OTUgMTYuMDQ4OCAxMi41NzgxIDE2LjA4NTEgMTEuNzQyN0MxNi4xMjE3IDEwLjkwNDMgMTYuMTMwMyAxMC42MzY2IDE2LjEyNjIgOC41MDM5N0MxNi4xMjIxIDYuMzcxMyAxNi4xMTI1IDYuMTAzOTMgMTYuMDcyOCA1LjI2NjMyQzE2LjAzMzEgNC40Mjg3MSAxNS45IDMuODU5ODkgMTUuNzA0MSAzLjM2MDVDMTUuNTAyMyAyLjg0NDE0IDE1LjIzMjggMi40MDY5NSAxNC43OTU4IDEuOTcxMDNDMTQuMzU4OCAxLjUzNTEgMTMuOTIwMiAxLjI2NzI2IDEzLjQwMjkgMS4wNjgwN0MxMi45MDMgMC44NzQ2ODkgMTIuMzMyIDAuNzQyODkgMTEuNDk2IDAuNzA2NzU5QzEwLjY1OTkgMC42NzA2MjggMTAuMzkwOCAwLjY2MTM2IDguMjU3NjkgMC42NjU0NDRDNi4xMjQ1NSAwLjY2OTUyOSA1Ljg1NzUgMC42Nzg2NCA1LjAxOTczIDAuNzE5NDg0Wk01LjExMTQ3IDE0LjkxODZDNC4zNDU2NiAxNC44ODUzIDMuOTI5ODQgMTQuNzU4MSAzLjY1MjczIDE0LjY1MTZDMy4yODU3NiAxNC41MTAyIDMuMDI0MzYgMTQuMzM5MyAyLjc0ODIgMTQuMDY1OEMyLjQ3MjAzIDEzLjc5MjMgMi4zMDIzNyAxMy41Mjk5IDIuMTU5MTEgMTMuMTYzOEMyLjA1MTUgMTIuODg2NiAxLjkyMTkgMTIuNDcxMyAxLjg4NjA4IDExLjcwNTVDMS44NDcxMiAxMC44Nzc4IDEuODM4OTYgMTAuNjI5MiAxLjgzNDQgOC41MzIyNEMxLjgyOTg0IDYuNDM1MjQgMS44Mzc4NiA2LjE4NzAzIDEuODc0MTQgNS4zNTkwMUMxLjkwNjgyIDQuNTkzODIgMi4wMzQ4NSA0LjE3NzUzIDIuMTQxMiAzLjkwMDU3QzIuMjgyNTggMy41MzMxNCAyLjQ1Mjg3IDMuMjcyMjEgMi43MjY5OSAyLjk5NjJDMy4wMDExMSAyLjcyMDE5IDMuMjYyNjcgMi41NTAyMiAzLjYyOTE2IDIuNDA2OTVDMy45MDU5NiAyLjI5ODg4IDQuMzIxMzEgMi4xNzAzOCA1LjA4NjgxIDIuMTMzOTNDNS45MTUxNSAyLjA5NDY2IDYuMTYzMzUgMi4wODY4IDguMjYwMDUgMi4wODIyNUMxMC4zNTY3IDIuMDc3NjkgMTAuNjA1NiAyLjA4NTU1IDExLjQzNDIgMi4xMjE5OUMxMi4xOTk0IDIuMTU1MjkgMTIuNjE1OSAyLjI4MjA3IDEyLjg5MjUgMi4zODkwNUMxMy4yNTk2IDIuNTMwNDMgMTMuNTIwOSAyLjcwMDI0IDEzLjc5NjkgMi45NzQ4NEMxNC4wNzI5IDMuMjQ5NDMgMTQuMjQzIDMuNTEwMDUgMTQuMzg2MyAzLjg3NzMzQzE0LjQ5NDUgNC4xNTMzMyAxNC42MjMgNC41Njg1MyAxNC42NTkxIDUuMzM0NUMxNC42OTg2IDYuMTYyODQgMTQuNzA3NSA2LjQxMTIgMTQuNzExMyA4LjUwNzc0QzE0LjcxNTEgMTAuNjA0MyAxNC43MDc3IDEwLjg1MzMgMTQuNjcxNCAxMS42ODFDMTQuNjM3OSAxMi40NDY4IDE0LjUxMSAxMi44NjI4IDE0LjQwNDMgMTMuMTQwMkMxNC4yNjMgMTMuNTA3IDE0LjA5MjUgMTMuNzY4NiAxMy44MTgyIDE0LjA0NDRDMTMuNTQ0IDE0LjMyMDMgMTMuMjgyNyAxNC40OTAyIDEyLjkxNjEgMTQuNjMzNUMxMi42Mzk2IDE0Ljc0MTQgMTIuMjIzOCAxNC44NzAyIDExLjQ1ODkgMTQuOTA2N0MxMC42MzA1IDE0Ljk0NTYgMTAuMzgyMyAxNC45NTM4IDguMjg0ODcgMTQuOTU4NEM2LjE4NzM5IDE0Ljk2MjkgNS45Mzk5NyAxNC45NTQ0IDUuMTExNjMgMTQuOTE4Nk0xMS41MTQ3IDQuMzIxMTFDMTEuNTE1IDQuNTA3NTQgMTEuNTcwNiA0LjY4OTY5IDExLjY3NDQgNC44NDQ1MkMxMS43NzgyIDQuOTk5MzYgMTEuOTI1NyA1LjExOTkyIDEyLjA5OCA1LjE5MDk2QzEyLjI3MDQgNS4yNjIwMSAxMi40NiA1LjI4MDM0IDEyLjY0MjcgNS4yNDM2NEMxMi44MjU1IDUuMjA2OTQgMTIuOTkzMyA1LjExNjg2IDEzLjEyNDkgNC45ODQ3OUMxMy4yNTY1IDQuODUyNzIgMTMuMzQ2IDQuNjg0NiAxMy4zODIgNC41MDE2OEMxMy40MTggNC4zMTg3NyAxMy4zOTkgNC4xMjkyNyAxMy4zMjczIDMuOTU3MTdDMTMuMjU1NiAzLjc4NTA3IDEzLjEzNDUgMy42MzgwOCAxMi45NzkzIDMuNTM0ODFDMTIuODI0MSAzLjQzMTU0IDEyLjY0MTcgMy4zNzY2MiAxMi40NTUzIDMuMzc2OTlDMTIuMjA1NCAzLjM3NzQ5IDExLjk2NTkgMy40NzcyMyAxMS43ODk1IDMuNjU0MjhDMTEuNjEzMSAzLjgzMTMyIDExLjUxNDIgNC4wNzExOCAxMS41MTQ3IDQuMzIxMTFaTTQuMjM5NzggOC41MjY5QzQuMjQ0MTcgMTAuNzU0NSA2LjA1MzIzIDEyLjU1NjEgOC4yODAzMSAxMi41NTE5QzEwLjUwNzQgMTIuNTQ3NiAxMi4zMTAzIDEwLjczODcgMTIuMzA2MSA4LjUxMTE5QzEyLjMwMTggNi4yODM2NCAxMC40OTIzIDQuNDgxNSA4LjI2NDkyIDQuNDg1OUM2LjAzNzUyIDQuNDkwMjkgNC4yMzU1MyA2LjI5OTY3IDQuMjM5NzggOC41MjY5Wk01LjY1NDU0IDguNTI0MDdDNS42NTM1MSA4LjAwNjI0IDUuODA2MDcgNy40OTk3MyA2LjA5MjkxIDcuMDY4NTlDNi4zNzk3NSA2LjYzNzQ2IDYuNzg4IDYuMzAxMDYgNy4yNjYwMyA2LjEwMTk1QzcuNzQ0MDUgNS45MDI4NCA4LjI3MDM5IDUuODQ5OTQgOC43Nzg0NyA1Ljk0OTk2QzkuMjg2NTYgNi4wNDk5OCA5Ljc1MzU4IDYuMjk4NDIgMTAuMTIwNSA2LjY2Mzg2QzEwLjQ4NzQgNy4wMjkzIDEwLjczNzYgNy40OTUzMyAxMC44Mzk3IDguMDAzMDJDMTAuOTQxNyA4LjUxMDcgMTAuODkwOSA5LjAzNzI1IDEwLjY5MzcgOS41MTYwNkMxMC40OTY1IDkuOTk0ODcgMTAuMTYxNyAxMC40MDQ0IDkuNzMxNjkgMTAuNjkzQzkuMzAxNjkgMTAuOTgxNSA4Ljc5NTc5IDExLjEzNjEgOC4yNzc5NiAxMS4xMzcxQzcuOTM0MTEgMTEuMTM3OCA3LjU5MzQ5IDExLjA3MDggNy4yNzU1NiAxMC45Mzk5QzYuOTU3NjIgMTAuODA5IDYuNjY4NTkgMTAuNjE2NyA2LjQyNDk3IDEwLjM3NEM2LjE4MTM2IDEwLjEzMTQgNS45ODc5MyA5Ljg0MzEgNS44NTU3NCA5LjUyNTY4QzUuNzIzNTQgOS4yMDgyNyA1LjY1NTE4IDguODY3OTIgNS42NTQ1NCA4LjUyNDA3WiIgZmlsbD0iY3VycmVudENvbG9yIiAvPjwvZz48ZGVmcz48Y2xpcHBhdGggaWQ9ImNsaXAwXzY1XzExODMiPjxyZWN0IHdpZHRoPSIxNS43MDkxIiBoZWlnaHQ9IjE1LjcwOTEiIGZpbGw9IndoaXRlIiB0cmFuc2Zvcm09InRyYW5zbGF0ZSgwLjQxODIxMyAwLjY2NDc5NSkiIC8+PC9jbGlwcGF0aD48L2RlZnM+PC9zdmc+)](https://instagram.com/claudeai)





### Solutions

- [AI agents](https://claude.com/solutions/agents)
- [Code modernization](https://claude.com/solutions/code-modernization)
- [Coding](https://claude.com/solutions/coding)
- [Customer support](https://claude.com/solutions/customer-support)
- [Financial services](https://claude.com/solutions/financial-services)
- [Government](https://claude.com/solutions/government)
- [Higher education](https://claude.com/solutions/education)
- [K-12 teachers](https://claude.com/solutions/teachers)
- [Life sciences](https://claude.com/solutions/life-sciences)

### Partners

- [Claude on AWS](https://claude.com/partners/amazon-bedrock)
- [Claude on Google Cloud](https://claude.com/partners/google-cloud-vertex-ai)

### Learn

- [Blog](https://claude.com/blog)
- [Courses](https://claude.com/resources/courses)
- [Use cases](https://claude.com/resources/use-cases)
- [Connectors](https://claude.com/partners/mcp)
- [Customer stories](https://claude.com/customers)
- [Engineering at Anthropic](https://www.anthropic.com/engineering)
- [Events](https://www.anthropic.com/events)
- [Powered by Claude](https://claude.com/partners/powered-by-claude)
- [Service partners](https://claude.com/partners/services)
- [Startups program](https://claude.com/programs/startups)

### Company

- [Anthropic](https://www.anthropic.com/company)
- [Careers](https://www.anthropic.com/careers)
- [Economic Futures](https://www.anthropic.com/economic-futures)
- [Research](https://www.anthropic.com/research)
- [News](https://www.anthropic.com/news)
- [Responsible Scaling Policy](https://www.anthropic.com/news/announcing-our-updated-responsible-scaling-policy)
- [Security and compliance](https://trust.anthropic.com)
- [Transparency](https://www.anthropic.com/transparency)

### Learn

- [Blog](https://claude.com/blog)
- [Courses](https://claude.com/resources/courses)
- [Use cases](https://claude.com/resources/use-cases)
- [Connectors](https://claude.com/partners/mcp)
- [Customer stories](https://claude.com/customers)
- [Engineering at Anthropic](https://www.anthropic.com/engineering)
- [Events](https://www.anthropic.com/events)
- [Powered by Claude](https://claude.com/partners/powered-by-claude)
- [Service partners](https://claude.com/partners/services)
- [Startups program](https://claude.com/programs/startups)

### Help and security

- [Availability](https://www.anthropic.com/supported-countries)
- [Status](https://status.claude.com/)
- [Support](https://support.claude.com/)
- [Discord](https://www.anthropic.com/discord)

### Terms and policies

- [Privacy policy](https://www.anthropic.com/legal/privacy)
- [Responsible disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)
- [Terms of service: Commercial](https://www.anthropic.com/legal/commercial-terms)
- [Terms of service: Consumer](https://www.anthropic.com/legal/consumer-terms)
- [Usage policy](https://www.anthropic.com/legal/aup)
