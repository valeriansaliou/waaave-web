## Compass configuration file
## Copyright 2013, Waaave
## Author: Valerian Saliou valerian@valeriansaliou.name

# Inspired from: https://gist.github.com/timkelty/1595176

# General
output_style = (environment == :production) ? :compressed : :expanded
relative_assets = true
project_path = File.dirname(__FILE__) + '/'

# Sass Paths
http_path = '/'
http_javascripts_path = http_path
http_stylesheets_path = http_path
http_images_path = http_stylesheets_path
http_fonts_path = http_stylesheets_path

# Sass Directories
css_dir = 'build/'
sass_dir = 'src/'
javascripts_dir = 'src/'
fonts_dir = ''

images_dir = 'src/'
generated_images_dir = 'build/'