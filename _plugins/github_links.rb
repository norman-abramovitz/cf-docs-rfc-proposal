require "set"

# A relative link to a file or folder that the site does not publish (tool
# inputs, partials, folders without a README) would 404 on Pages. Point it
# at the GitHub view of the same path instead; on GitHub itself the link
# already works as written.
Jekyll::Hooks.register :site, :post_render do |site|
  repo = site.config["repository"]
  branch = site.config["branch"] || "main"
  published = (site.pages + site.static_files + site.documents)
    .map { |f| f.relative_path.delete_prefix("/") }.to_set
  index_names = %w[README.md index.md index.html]

  (site.pages + site.documents).each do |page|
    next unless page.output && page.output_ext == ".html"
    dir = File.dirname(page.relative_path.delete_prefix("/"))
    page.output = page.output.gsub(/\b(href|src)="([^"#?:]+)([#?][^"]*)?"/) do
      attr, target, rest = $1, $2, $3
      next $& if target.start_with?("/")
      path = File.expand_path(target, "/#{dir}").delete_prefix("/")
      source = File.join(site.source, path)
      next $& unless File.exist?(source)
      folder = File.directory?(source)
      next $& if folder ? index_names.any? { |n| published.include?(File.join(path, n)) } : published.include?(path)
      kind = attr == "src" ? "raw" : folder ? "tree" : "blob"
      %(#{attr}="https://github.com/#{repo}/#{kind}/#{branch}/#{path}#{rest}")
    end
  end
end
