# A model of how the book renders code blocks: each page's Markdown through
# Redcarpet with the book's options, and each code block through Rouge as
# middleman-syntax does it. Writes one row per code block Redcarpet finds.
#
# Usage:
#   GEM_HOME=DIR ruby book-render.rb REPOS_DIR SHAS RENDERED.csv [WORK_DIR]
#
# Needs the gems redcarpet 3.2.3 and rouge 1.11.1 in GEM_HOME
# (gem install --no-document redcarpet -v 3.2.3; rouge -v 1.11.1): the
# newest releases that bookbindery 9.12.1 (redcarpet ~> 3.2.3) and
# middleman-syntax 2.1.0 (rouge ~> 1.0) allow. On Ruby 3.5 and later also
# the gem cgi, which Rouge 1.x needs for CGI.parse.
#
# WORK_DIR, if given, receives two trees: md/<repo>/<file>, each page's
# Markdown after the ERB step below (commonmark-render.mjs reads it), and
# html/<repo>/<page>.html, each rendered page body, for comparison with the
# published pages.
#
# What it models, with the source lines it follows:
#   - Markdown options: tables, autolink, smartypants, fenced_code_blocks
#     (bookbinder master_middleman/config.rb L11-L16, v9.12.0 tag), plus
#     no_intra_emphasis: no source found sets it, but the published pages
#     behave as if it were set (an underscore inside a word is never
#     emphasis there; see the survey README)
#   - SmartyPants as a mixin of the renderer (middleman-core 3.4.1
#     renderers/redcarpet.rb L24-L29)
#   - block_code -> Rouge::Lexer.find_fancy(language, code) || PlainText,
#     css_class "highlight <lexer tag>" (middleman-syntax 2.1.0
#     redcarpet_code_renderer.rb L6-L8, highlighter.rb L7-L16)
#
# What it does not model: ERB is replaced, not run. `<%= vars.name %>`
# becomes the value from the book's template_variables.yml (nothing for an
# empty or undefined name); every other ERB tag, partial calls included,
# becomes nothing. Front matter is removed. Reads files only.
require 'csv'
require 'yaml'
require 'fileutils'
begin; gem 'cgi'; rescue Gem::LoadError; end
require 'cgi'
require 'redcarpet'
require 'rouge'

abort File.read(__FILE__)[/\A(#.*\n)+/] unless [3, 4].include?(ARGV.size)
repos, shas, out_csv, work = ARGV
BOOK = 'docs-book-cloudfoundry'
sha = File.readlines(shas).map(&:split).reject(&:empty?).to_h { |l| [l[0], l[1]] }
vars = YAML.safe_load(File.read(File.join(repos, BOOK, 'config/template_variables.yml')))['template_variables']

class BookHTML < Redcarpet::Render::HTML
  include Redcarpet::Render::SmartyPants
  attr_accessor :blocks

  def block_code(code, language)
    lexer = Rouge::Lexer.find_fancy(language, code) || Rouge::Lexers::PlainText
    @blocks << [language, lexer.tag, code]
    Rouge::Formatters::HTML.new(css_class: "highlight #{lexer.tag}").format(lexer.lex(code))
  end
end

renderer = BookHTML.new
md = Redcarpet::Markdown.new(renderer, tables: true, autolink: true, fenced_code_blocks: true,
                                      no_intra_emphasis: true)

def save(path, text)
  FileUtils.mkdir_p(File.dirname(path))
  File.write(path, text)
end

rows = []
sha.keys.sort.each do |repo|
  next if repo == 'docs-bosh' # bosh.io, built with MkDocs
  root = File.join(repos, repo)
  Dir.glob('**/*', base: root).sort.each do |rel|
    next unless rel =~ /\.(md|markdown)(\.erb)?\z/
    next if rel.split('/').any? { |p| %w[.git node_modules vendor].include?(p) }
    next if !rel.include?('/') && rel =~ /\.md\z/ # root Markdown files: no site publishes them
    src = File.read(File.join(root, rel), encoding: 'UTF-8').scrub
    src = src.sub(/\A---\n.*?\n---\n/m, '')
    src = src.gsub(/<%=\s*vars\.(\w+)\s*-?%>/) { vars[$1].to_s }
    src = src.gsub(/<%.*?%>/m, '')
    renderer.blocks = []
    html = md.render(src)
    if work
      save(File.join(work, 'md', repo, rel), src)
      save(File.join(work, 'html', repo, rel.sub(/(\.html)?\.(md|markdown)(\.erb)?\z/, '') + '.html'), html)
    end
    renderer.blocks.each_with_index do |(lang, tag, code), i|
      first = code.lines.map(&:strip).reject(&:empty?).first.to_s[0, 80]
      rows << [repo, rel, i + 1, lang.to_s, tag, code.lines.size, first]
    end
  end
end

CSV.open(out_csv, 'w') do |csv|
  csv << %w[repo file n language lexer lines first_line]
  rows.each { |r| csv << r }
end
puts "#{rows.size} code blocks rendered by the model"
puts rows.group_by { |r| r[4] }.map { |k, v| "  #{k} #{v.size}" }.sort_by { |s| -s.split.last.to_i }
