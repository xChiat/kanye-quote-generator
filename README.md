# 🎤 Kanye Quote Generator

A serverless API that generates random Kanye West quotes as images, perfect for GitHub READMEs.

## 🚀 Demo

![Kanye Quote](https://kanye-quote-generator-silk.vercel.app/?theme=yeezus)

## 📦 Features

- Fetches random Kanye quotes from [kanye.rest API](https://api.kanye.rest)
- Generates beautiful PNG images
- **12+ built-in themes** matching popular GitHub README themes
- Serverless deployment with Vercel
- No caching - new quote on every reload
- Responsive text wrapping
- Decorative themed borders

## 🎨 Available Themes

| Theme | Preview |
|-------|---------|
| `radical` (default) | ![](https://kanye-quote-generator-silk.vercel.app/?theme=radical) |
| `yeezus` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=yeezus) |
| `react` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=react) |
| `omni` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=omni) |
| `dark` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=dark) |
| `github_dark` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=github_dark) |
| `tokyonight` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=tokyonight) |
| `dracula` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=dracula) |
| `monokai` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=monokai) |
| `gruvbox` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=gruvbox) |
| `nord` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=nord) |
| `kanye` | ![](https://kanye-quote-generator-silk.vercel.app/?theme=kanye) |

## 🛠️ Tech Stack

- Python 3.9
- Pillow (PIL) for image generation
- Vercel for serverless deployment

## 📖 Usage

Simply add this to your GitHub README with your preferred theme:

```markdown
![Kanye Quote](https://kanye-quote-generator-silk.vercel.app/?theme=yeezus)
```

Or as HTML:

```html
<img src="https://kanye-quote-generator-silk.vercel.app/?theme=dracula" alt="Kanye Quote"/>
```

### Parameters

| Parameter | Description | Default | Options |
|-----------|-------------|---------|---------|
| `theme` | Color theme for the quote | `radical` | `radical`, `yeezus`, `react`, `omni`, `dark`, `github_dark`, `tokyonight`, `dracula`, `monokai`, `gruvbox`, `nord`, `kanye` |

## 🏃‍♂️ Local Development

1. Clone the repository:
```bash
git clone https://github.com/xChiat/kanye-quote-generator.git
cd kanye-quote-generator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run locally with Vercel CLI:
```bash
npm i -g vercel
vercel dev
```

4. Open `http://localhost:3000/?theme=yeezus` in your browser

## 🚢 Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Login to Vercel:
```bash
vercel login
```

3. Deploy:
```bash
vercel --prod
```

4. Your API will be available at: `https://your-project.vercel.app/?theme=yeezus`

## 🎨 Adding Custom Themes

Want to add your own theme? Edit `api/quote.py` and add to the `THEMES` dictionary:

```python
THEMES = {
    'your_theme': {
        'bg_color': (R, G, B),        # Background color
        'text_color': (R, G, B),      # Main text color (unused currently)
        'quote_color': (R, G, B),     # Quote text color
        'author_color': (R, G, B),    # Author name color
        'accent_color': (R, G, B)     # Border color
    },
    # ... other themes
}
```

Example - Creating a "The Life of Pablo" theme:
```python
'pablo': {
    'bg_color': (255, 140, 0),      # Orange background
    'text_color': (255, 255, 255),
    'quote_color': (255, 255, 255), # White text
    'author_color': (245, 245, 245),
    'accent_color': (255, 69, 0)    # Red-orange border
}
```

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new themes (Graduation? 808s & Heartbreak? MBDTF?)
- Improve text rendering
- Add customization options (font size, dimensions, etc.)
- Report bugs or suggest features

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-theme`)
3. Commit your changes (`git commit -m 'Add amazing theme'`)
4. Push to the branch (`git push origin feature/amazing-theme`)
5. Open a Pull Request

## 📝 License

MIT License - feel free to use this in your own projects!

## 🙏 Credits & Inspiration

- **Quotes API**: [kanye.rest](https://github.com/ajzbc/kanye.rest) by [@ajzbc](https://github.com/ajzbc) - A free REST API for random Kanye West quotes
- **Design Inspiration**: [github-readme-quotes](https://github.com/PiyushSuthar/github-readme-quotes) by [@PiyushSuthar](https://github.com/PiyushSuthar)
- **Themes**: Inspired by [github-readme-stats](https://github.com/anuraghazra/github-readme-stats)
- **Made with** 🔥 by [@xChiat](https://github.com/xChiat)

## 🌊 Fun Facts

- The `yeezus` theme is inspired by the iconic minimalist red tape design of the Yeezus album
- Each image is generated on-demand, so you get a fresh quote every time
- No data is stored or tracked - pure serverless magic
- Built during a late-night coding session because why not? 🤷‍♂️

---

<div align="center">

**If you like this project, give it a ⭐️!**

[![GitHub stars](https://img.shields.io/github/stars/xChiat/kanye-quote-generator?style=social)](https://github.com/xChiat/kanye-quote-generator)
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/xChiat/kanye-quote-generator)

</div>
