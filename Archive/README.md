# DasPress

Publish your Obsidian notes as blogs in **one click**.

* 🖱 **Not technical?** [Download the portable app](https://shuvangkardas.com/daspress/) — the fastest and easiest way to use DasPress.
* 💻 **Are you a developer?** [Follow the manual setup guide](#manual-setup-guide) to explore and customize the code.


## Currently Supported Operating System
| Platform   | Status      | Setup Options       | Notes                    |
| ---------- | ----------- | ------------------- | ------------------------ |
| 🪟 Windows | ✅ Supported | Manual + Executable | Beta testers Needed |
| 🍎 macOS   | ⚠️ Limited  | Manual only         | Beta testers needed      |
| 🐧 Linux   | ⚠️ Limited  | Manual only         | Beta testers needed      |


## Blog Technolgy Support
| Blog Platform     | Supported | Notes                                                                               |
| ----------------- | --------- | ----------------------------------------------------------------------------------- |
| Jekyll            | ✅         | Actively tested (used in [my blog](blog.shuvangkardas.com))                                               |
| Hugo              | ✅         | Markdown-compatible, but not extensively tested                                     |
| Hexo              | ✅         | Markdown-compatible, user testing welcome                                           |
| Wordpress         | ❌         | Coming soon                                                                         |
| Others (Markdown) | ✅         | Should work — feel free to test and [send feedback](mailto:shuvangkardas@gmail.com) |

Email [me](mailto:shuvangkarcdas@gmail.com) your requrest. What feature you think will be useful and what technology support are you looking for?

## Coming Soon
- Mac and Linux support  
- Multiple platforms support (WordPress, Ghost, Medium, Substack)  
- Post scheduling  
- SEO optimization (auto-rename Obsidian images)
- Multi-site support

# Manual Setup Guide

### Install
```bash
pip install daspress
```

### Setup
```bash
python -m  daspress setup
```

### Verify Installation
```bash
python -m  daspress --version
```
Returns: `daspress <version>`



## Features

- **Convert**:  Convert your notes into blog format. Sanitize note and images. Handle images and formatting
- **Local Preview**: Start Jekyll server automatically for instant preview
- **Git Publishing**: Auto-commit and push to your repository
- **Smart Paths**: Works with Obsidian's file paths and regular filenames
- **Cross-Platform**: Works on Windows, Mac, and Linux

## 📋 Commands

```bash
python -m daspress setup                 # Interactive configuration wizard
python -m daspress convert "post.md"     # Convert post to Jekyll format
python -m daspress local "post.md"       # Convert + start local Jekyll server
python -m daspress remote "post.md"      # Convert + publish to git repository  
python -m daspress both "post.md"        # Convert + local preview + git publish
```

## Setup Requirements

1. **Obsidian vault** with your blog posts
2. **Jekyll blog** repository 
3. **Git** configured for your Jekyll repository (for remote publishing)
4. **Ruby/Jekyll** installed (for local server)

## Obsidian Integration
1. Configure daspress from command line 
2. Configure Obsidian Shell Command Plugin
**Command:** 
```bash
python -m daspress remote "{{file_path:absolute}}"
```
3. Install git and make sure you can post your blog from local machine
4. 

**Name:** "Publish Blog Post"

Now you can publish directly from Obsidian with one click!

## How It Works

1. **Reads** your Obsidian markdown files
2. **Converts** `![[image.png]]` syntax to Jekyll format
3. **Copies** images from Obsidian to Jekyll assets folder
4. **Saves** processed post to Jekyll `_posts` folder
5. **Optionally** starts local server and/or publishes to git

## Configuration

Run `daspress setup` to configure:
- Obsidian posts folder path
- Obsidian images folder path  
- Jekyll blog root directory

Configuration is saved to `~/.daspress/config.yaml`

## Documentation

- See `docs/GETTING-STARTED.md` for detailed setup
- See `QUICKSTART.md` for developers

## License

See LICENSE.txt for terms and conditions.

## Issues

If you encounter any issues, run with debug mode.
```bash
daspress --debug convert "post.md"
```