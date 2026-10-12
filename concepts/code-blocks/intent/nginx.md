# Intent: `nginx`

- Source: [`../source/nginx-index.html.md.erb`](../source/nginx-index.html.md.erb),
  cloudfoundry/docs-buildpacks (`nginx/index.html.md.erb`)
- Excerpt: Create the nginx.conf file and its subsections
  ([L39-L229](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/nginx/index.html.md.erb#L39-L229))
- Published: <https://docs.cloudfoundry.org/buildpacks/nginx/index.html>
  (copy: [`../published/nginx.html`](../published/nginx.html))
- Code file: [`nginx.code`](nginx.code); anchors: [`nginx.anchors`](nginx.anchors)

## Cases this page covers

- **Template syntax inside code**: `{{port}}`, `{{env "…"}}` and
  `{{module "…"}}` in five fences
  ([L52-L56](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/nginx/index.html.md.erb#L52-L56)),
  and in inline code and an HTML `<code>` in the prose. They are Jinja's
  and MDX's delimiters too.
- **Character references inside fences**, `&lt;file&gt;`, which the
  published page shows as written
  ([L147-L149](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/nginx/index.html.md.erb#L147-L149),
  [L167-L169](https://github.com/cloudfoundry/docs-buildpacks/blob/239e5c8676200914c4d386970f9989e46de9e969/nginx/index.html.md.erb#L167-L169)).
- **Thirteen fences with no info string** holding NGINX configuration, a
  YAML file and a GDB script; Rouge guessed JSON for the three
  `{{module …}}` lines.

## What a conversion must keep

Thirteen code blocks: eleven `nginx`, one `yaml`, one `text` in native
mode, their text exactly, `{{…}}` included. Twelve headings, eleven ids.

## Cleanup and deviations

- **Blocks 7 and 9 show `<file>`**, not `&lt;file&gt;`: the author meant
  the angle brackets. Decision (this round): character references written
  inside a fence are a defect the converted page fixes; the published
  page fails here.
- **The prose's `<code>{{port}}</code>` is written as inline code,
  `` `{{port}}` ``,** in Docusaurus, whose build stops on it otherwise
  ([raw check](../results/docusaurus-raw-check.txt)).
