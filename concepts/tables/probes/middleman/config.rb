require 'ostruct'
require 'yaml'

# The Markdown engine and options the published book sets
set :markdown_engine, :redcarpet
set :markdown, layout_engine: :erb,
               tables: true,
               autolink: true,
               smartypants: true,
               fenced_code_blocks: true,
               with_toc_data: true,
               no_intra_emphasis: true

# The book's variables, read the way the book reads them: an undefined name
# is nil and renders as nothing
TEMPLATE_VARIABLES = YAML.load_file(File.expand_path('../../source/template_variables.yml', __dir__))['template_variables']

helpers do
  def vars
    OpenStruct.new(TEMPLATE_VARIABLES)
  end
end
