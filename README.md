# Veida — image generation with no API key

A Dify tool provider that generates images from a prompt with **nothing to configure**.
No API key, no account, no card. It calls the anonymous tier of
[Veida](https://veida.ai/?utm_source=dify&utm_medium=plugin), which meters the free allowance against an identifier the
plugin invents rather than an account you register.

## Tools

| Tool | What it does |
|---|---|
| `generate_image` | Prompt → image URL. Returns both an image message and the URL as text. |

That is the whole surface, on purpose. See below for what is deliberately missing.

## What the free tier actually covers

Every number here was read out of the running service, not estimated:

- A signed-out caller is granted **4 credits**, and one text-to-image run costs **4**.
  That is one image per caller, so the plugin mints a **fresh caller per call** — a
  workflow is not limited to a single run.
- A ceiling of **30 credits per IP per day** sits on top: roughly **7 images a day** from
  one machine, however many callers it invents. When it is spent, the tool returns a
  readable message instead of failing silently.
- Free output is **1K and watermarked**. Signing in removes the mark and opens the rest of
  the shelf — [GPT Image 2](https://veida.ai/image/gpt-image-2?utm_source=dify&utm_medium=plugin),
  [Nano Banana 2](https://veida.ai/image/nano-banana-2?utm_source=dify&utm_medium=plugin),
  [Seedream 5.0 Lite](https://veida.ai/image/seedream-5-lite?utm_source=dify&utm_medium=plugin). What each tier costs is on
  the [pricing page](https://veida.ai/pricing?utm_source=dify&utm_medium=plugin).

## What this plugin deliberately does not do

- 🔴 **No edit tool.** Editing an existing image runs on a model that costs **30 credits**
  against a 4-credit anonymous grant, so an anonymous edit can never be paid for. A tool
  that always fails is worse than a tool that is not there. For edits, sign in and use the
  [image editor](https://veida.ai/image/nano-banana-2-lite?utm_source=dify&utm_medium=plugin) or the
  [ChatGPT image editor](https://veida.ai/image/chatgpt-image-editor?utm_source=dify&utm_medium=plugin).
- **No video tool.** This site does not serve video at all.

## Errors the tool returns as text

Rather than raising, the tool answers with a sentence a workflow can branch on:

- the anonymous allowance for this caller is spent
- the per-IP daily ceiling is spent — try tomorrow, or sign in
- the prompt was refused by the content filter — rewrite it rather than retrying the same text
- still queued after the timeout

## Writing prompts that work

Name the light, the material and the composition. "A product photo of a mug" gives the
model nothing; "matte black ceramic mug on pale oak, soft window light from the left,
shallow depth of field" gives it a picture. Worked examples are in the
[prompt library](https://veida.ai/image/prompts?utm_source=dify&utm_medium=plugin), and finished output is in the
[showcase](https://veida.ai/showcases?utm_source=dify&utm_medium=plugin).

The same engine backs the
[ChatGPT image generator](https://veida.ai/image/chatgpt-image-generator?utm_source=dify&utm_medium=plugin) and the
[free AI image generator](https://veida.ai/image?utm_source=dify&utm_medium=plugin) pages in a browser.

## Setup

Install and use it. `credentials_for_provider` is empty and `_validate_credentials` is a
no-op, because there is no credential — asking for one would block a setup that is already
correct.

## Source

<https://github.com/hanshs474/veida-dify-plugin>

MIT.
