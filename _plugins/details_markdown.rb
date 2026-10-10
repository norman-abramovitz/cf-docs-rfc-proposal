# kramdown leaves Markdown inside an HTML block as text, so fenced code in a
# <details> block would show as raw backticks on Pages. markdown="1" tells
# kramdown to parse it; GitHub already renders it and needs no attribute.
Jekyll::Hooks.register :pages, :pre_render do |page|
  next unless page.extname == ".md"
  page.content = page.content.gsub(/^<details>/, '<details markdown="1">')
end
