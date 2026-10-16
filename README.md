# Veida AI for Dify: image generation and photo editing, no API key

Unlimited free AI image generator. Most image plugins ask for a provider key
before they do anything; this one does not.
[Veida AI](https://veida.ai/?utm_source=dify&utm_medium=plugin) exposes an
anonymous tier, so both tools run the moment the plugin is installed.

## Tools

| Tool | What it does |
|---|---|
| `generate_image` | Prompt in, image URL out, with an aspect-ratio select |
| `edit_image` | Photo URL + instruction in, edited image URL out |

## The rule that makes edits work

Name what must **stay**, not only what changes.

> turn the jacket red, keep the same face, pose and lighting

holds the picture together. "Make it red" leaves everything else open to the
model.

## What the free tier covers

| | |
|---|---|
| Anonymous grant per call | 4 credits |
| `generate_image` | 4 credits, one run |
| `edit_image` | 4 credits, one run |
| Per-IP ceiling | 30 credits a day (about 7 runs) |

Every call mints a fresh anonymous id, so a workflow loop is not stopped after
its first image. Signed-out output is 1K with a small veida.ai mark.

Signing in on [veida.ai](https://veida.ai/pricing?utm_source=dify&utm_medium=plugin)
makes Veida AI Image v1 unlimited and opens the rest of the shelf:
[GPT Image 2](https://veida.ai/image/gpt-image-2?utm_source=dify&utm_medium=plugin)
when the picture has to carry readable text,
[GPT Image 2.5](https://veida.ai/image/gpt-image-2-5?utm_source=dify&utm_medium=plugin),
[Nano Banana 2](https://veida.ai/image/nano-banana-2?utm_source=dify&utm_medium=plugin),
and the [ChatGPT image editor](https://veida.ai/image/chatgpt-image-editor?utm_source=dify&utm_medium=plugin).
Prompts that already work are in the
[prompt library](https://veida.ai/image/prompts?utm_source=dify&utm_medium=plugin).

## Errors the tools return as text

- the content filter refused the prompt (rewrite it rather than retrying the
  same text)
- the job was still queued when the timeout ran out
- the per-IP daily ceiling is spent

## Setup and connection requirements

There is no setup: no API key, no account, no connection settings. The tools
call `https://veida.ai` over HTTPS and results are served from
`https://cdn.veida.ai`, so the only requirement is outbound network access from
your Dify instance to those two hosts.

## Source

<https://github.com/hanshs474/veida-dify-plugin> — issues and pull requests
welcome there.
