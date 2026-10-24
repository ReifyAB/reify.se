require "fileutils"
require "time"

def slugify(text)
  text.downcase.strip.gsub(/\s+/, "-").gsub(/[^\w-]/, "")
end

def write_new(path, content)
  abort "#{path} already exists" if File.exist?(path)
  FileUtils.mkdir_p(File.dirname(path))
  File.write(path, content)
  puts "Created #{path}"
end

desc "Serve the site locally with live reload"
task :serve do
  sh "bundle exec jekyll serve --livereload"
end

desc "Build the site into _site"
task :build do
  sh "bundle exec jekyll build"
end

# rake post title="My Post" [date=2026-10-24] [tags=talks,programming]
desc "Create a new blog post"
task :post do
  title = ENV.fetch("title") { abort 'Usage: rake post title="My Post"' }
  date = ENV["date"] ? Time.parse(ENV["date"]) : Time.now
  tags = ENV.fetch("tags", "").split(",").map(&:strip)
  write_new "_posts/#{date.strftime('%Y-%m-%d')}-#{slugify(title)}.md", <<~MD
    ---
    title: "#{title}"
    tagline: ""
    tags: [#{tags.join(', ')}]
    ---

    Intro paragraph, shown on the blog index.

    <!-- more -->

    The rest of the post.
  MD
end

# rake page title="Services" [nav=3]
desc "Create a new page, optionally listed in the main navigation"
task :page do
  title = ENV.fetch("title") { abort 'Usage: rake page title="Services" [nav=3]' }
  nav = ENV["nav"] ? "nav_order: #{ENV['nav']}\n" : ""
  write_new "#{slugify(title)}.md", <<~MD
    ---
    title: "#{title}"
    #{nav}---

    Page content goes here.
  MD
end
