# Privacy Policy

## What this plugin sends

When a tool is invoked, the plugin sends to `https://veida.ai`:

- the prompt text you or your workflow supplied
- for `edit_image`, the image URL you supplied
- a randomly generated anonymous identifier, created fresh for **each call**

Nothing else leaves the plugin. There is no account, no API key and no login, so
no credential of yours is transmitted or stored.

## What this plugin stores

Nothing. The plugin holds no state between calls. The anonymous identifier is
generated per invocation and discarded when the call ends, so it cannot be used
to link two of your calls together.

## What the service does with it

Prompts and generated images are processed by Veida AI to produce the result, and
generated images are served from Veida AI's CDN at a public URL. Treat that URL as
public: anyone holding it can view the image. Do not send prompts or source
photos that must remain confidential.

Veida AI's own terms and privacy policy apply to that processing:
<https://veida.ai/privacy-policy>

## Contact

Issues: <https://github.com/hanshs474/veida-dify-plugin/issues>
