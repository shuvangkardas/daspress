# DasPress

Publish your Obsidian notes as blogs in **one click**.

* **Not technical?** [Download the portable app](https://shuvangkardas.com/daspress/). This is the fastest and easiest way to use DasPress.
* **Are you a developer?** [Follow the manual setup guide](#manual-setup-guide) to explore and customize the code.

---

## Currently Supported Operating Systems

| Platform | Status    | Setup Options         | Notes               |
| -------- | --------- | --------------------- | ------------------- |
| Windows  | Supported | Manual and Executable | Beta testers needed |
| macOS    | Limited   | Manual only           | Beta testers needed |
| Linux    | Limited   | Manual only           | Beta testers needed |

---

## Blog Technology Support

| Blog Platform     | Supported | Notes                                                                              |
| ----------------- | --------- | ---------------------------------------------------------------------------------- |
| Jekyll            | Yes       | Actively tested. Used in [my blog](https://blog.shuvangkardas.com)                 |
| Hugo              | Yes       | Markdown-compatible, but not extensively tested                                    |
| Hexo              | Yes       | Markdown-compatible. User testing is welcome                                       |
| WordPress         | No        | Coming soon                                                                        |
| Others (Markdown) | Yes       | Should work. Feel free to test and [send feedback](mailto:shuvangkardas@gmail.com) |

If you want support for a new platform or feature, feel free to [email me](mailto:shuvangkarcdas@gmail.com) with your request.

---

## Coming Soon

* Full support for macOS and Linux
* Platform integration for WordPress, Ghost, Medium, and Substack
* Post scheduling
* SEO optimization (e.g., auto-renaming Obsidian images)
* Multi-site support

---

# Manual Setup Guide

### Install

```bash
pip install daspress
```

### Setup

```bash
python -m daspress setup
```

### Verify Installation

```bash
python -m daspress --version
```

Expected output: `daspress <version>`

---

## Features

* **Convert**: Convert notes into blog format. Sanitizes text and images and handles formatting
* **Local Preview**: Automatically starts a Jekyll server for preview
* **Git Publishing**: Automatically commits and pushes to your Git repository
* **Smart Paths**: Supports Obsidian file paths and standard filenames
* **Cross-Platform**: Works on Windows, macOS, and Linux

---

## Commands

```bash
python -m daspress setup                 # Interactive configuration wizard  
python -m daspress convert "post.md"     # Convert post to Jekyll format  
python -m daspress local "post.md"       # Convert and start local Jekyll server  
python -m daspress remote "post.md"      # Convert and publish to Git repository  
python -m daspress both "post.md"        # Convert, preview locally, and publish
```

---

## Setup Requirements

1. An Obsidian vault with your blog posts
2. A Jekyll blog repository
3. Git installed and configured for the Jekyll repository
4. Ruby and Jekyll installed for running the local server

---

## Obsidian Integration

1. Run `daspress setup` from the command line
2. Configure the Obsidian Shell Commands plugin

**Shell Command**:

```bash
python -m daspress remote "{{file_path:absolute}}"
```

3. Ensure Git is installed and local publishing works
4. Add the command as a named action

**Suggested name**: `Publish Blog Post`

Now you can publish directly from Obsidian with a single click.

---

## How It Works

1. Reads your Obsidian markdown files
2. Converts image links like `![[image.png]]` to Jekyll-compatible syntax
3. Copies images from the Obsidian vault to the Jekyll assets folder
4. Saves the converted post in the Jekyll `_posts` directory
5. Optionally starts a local server and/or publishes to Git

---

## Configuration

Run:

```bash
daspress setup
```

This configures:

* Obsidian posts folder path
* Obsidian images folder path
* Jekyll blog root directory

Configuration is saved at `~/.daspress/config.yaml`

---

## Documentation

* See `docs/GETTING-STARTED.md` for step-by-step instructions
* See `QUICKSTART.md` for developer usage and API integration

---

## License

See `LICENSE.txt` for terms and conditions.

---

## Troubleshooting

If you face any issues, use debug mode to identify errors:

```bash
daspress --debug convert "post.md"
```

