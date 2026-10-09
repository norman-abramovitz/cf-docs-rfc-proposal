import ejsPlugin from "@11ty/eleventy-plugin-ejs";

export default function (eleventyConfig) {
  // EJS is a plugin since Eleventy 3; Markdown pages run through it first,
  // then through markdown-it.
  eleventyConfig.addPlugin(ejsPlugin);
  eleventyConfig.addGlobalData("layout", "page.ejs");
  // The copied source pages are git-ignored, and Eleventy skips git-ignored
  // files by default.
  eleventyConfig.setUseGitIgnore(false);
  return {
    dir: { input: "src", output: "_site" },
    markdownTemplateEngine: "ejs",
  };
}
