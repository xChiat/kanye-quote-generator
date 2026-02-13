#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
from urllib import request, parse
import io
import textwrap
import traceback
import sys
import random

# Importar PIL con manejo de errores
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError as e:
    PIL_AVAILABLE = False
    PIL_ERROR = str(e)

# Definición de temas
THEMES = {
    'radical': {
        'bg_color': (20, 23, 31),
        'quote_color': (255, 121, 198),
        'author_color': (139, 148, 158),
        'accent_color': (255, 121, 198)
    },
    'react': {
        'bg_color': (32, 42, 53),
        'quote_color': (97, 218, 251),
        'author_color': (139, 148, 158),
        'accent_color': (0, 216, 255)
    },
    'omni': {
        'bg_color': (25, 22, 34),
        'quote_color': (232, 223, 122),
        'author_color': (216, 216, 221),
        'accent_color': (255, 122, 199)
    },
    'dark': {
        'bg_color': (13, 17, 23),
        'quote_color': (88, 166, 255),
        'author_color': (139, 148, 158),
        'accent_color': (88, 166, 255)
    },
    'github_dark': {
        'bg_color': (13, 17, 23),
        'quote_color': (79, 192, 141),
        'author_color': (139, 148, 158),
        'accent_color': (79, 192, 141)
    },
    'tokyonight': {
        'bg_color': (26, 27, 38),
        'quote_color': (122, 162, 247),
        'author_color': (86, 95, 137),
        'accent_color': (187, 154, 247)
    },
    'dracula': {
        'bg_color': (40, 42, 54),
        'quote_color': (255, 121, 198),
        'author_color': (98, 114, 164),
        'accent_color': (189, 147, 249)
    },
    'monokai': {
        'bg_color': (39, 40, 34),
        'quote_color': (249, 38, 114),
        'author_color': (117, 113, 94),
        'accent_color': (166, 226, 46)
    },
    'gruvbox': {
        'bg_color': (40, 40, 40),
        'quote_color': (254, 128, 25),
        'author_color': (168, 153, 132),
        'accent_color': (184, 187, 38)
    },
    'nord': {
        'bg_color': (46, 52, 64),
        'quote_color': (136, 192, 208),
        'author_color': (129, 161, 193),
        'accent_color': (143, 188, 187)
    },
    'yeezus': {
        'bg_color': (254, 254, 254),
        'quote_color': (251, 0, 0), 
        'author_color': (186, 194, 146),  
        'accent_color': (185, 200, 207) 
    },
    'kanye': {
        'bg_color': (94, 121, 167),
        'quote_color': (106,228,100),
        'author_color': (142, 170, 207),
        'accent_color': (42, 56, 76)
    },
    'default': {
        'bg_color': (13, 17, 23),
        'quote_color': (255, 121, 198),
        'author_color': (139, 148, 158),
        'accent_color': (255, 121, 198)
    }
}

# Quotes de respaldo si la API falla
FALLBACK_QUOTES = [
    "I'm doing pretty good as far as geniuses go",
    "I feel like I'm too busy writing history to read it",
    "My greatest pain in life is that I will never be able to see myself perform live",
    "I am Warhol. I am the number one most impactful artist of our generation",
    "I am not a fan of books. I would never want a book's autograph",
    "I make awesome decisions in bike stores",
    "Sometimes you have to get rid of everything",
    "I hate when I'm on a flight and I wake up with a water bottle next to me like oh great now I gotta be responsible for this water bottle",
    "I leave my emojis bart Simpson color",
    "I wish I had a friend like me"
]

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Verificar si PIL está disponible
            if not PIL_AVAILABLE:
                raise ImportError(f"PIL/Pillow not available: {PIL_ERROR}")
            
            # Parse query parameters
            query_components = parse.parse_qs(parse.urlparse(self.path).query)
            theme = query_components.get('theme', ['default'])[0].lower()
            
            # Obtener tema o usar default
            theme_colors = THEMES.get(theme, THEMES['default'])
            
            # Obtener quote de Kanye API usando el endpoint /text
            try:
                # Usar el endpoint /text que devuelve texto plano
                req = request.Request(
                    'https://api.kanye.rest/text',
                    headers={'User-Agent': 'Mozilla/5.0 (Kanye Quote Generator)'}
                )
                response = request.urlopen(req, timeout=5)
                quote = response.read().decode('utf-8').strip()
                print(f"✅ Quote fetched from API: {quote[:50]}...", file=sys.stderr)
            except Exception as api_error:
                print(f"⚠️  API error, using fallback quote: {api_error}", file=sys.stderr)
                quote = random.choice(FALLBACK_QUOTES)
            
            # Configuración de la imagen
            width = 800
            height = 400
            
            # Crear imagen
            img = Image.new('RGB', (width, height), theme_colors['bg_color'])
            draw = ImageDraw.Draw(img)
            
            # Cargar fuente
            try:
                quote_font = ImageFont.truetype("assets/BebasNeue-Regular.ttf", 32)
                author_font = ImageFont.truetype("assets/BebasNeue-Regular.ttf", 24)
            except Exception as font_error:
                print(f"⚠️  Font error, using default: {font_error}", file=sys.stderr)
                quote_font = ImageFont.load_default()
                author_font = ImageFont.load_default()
            
            # Wrap text
            max_width = 45
            wrapped_quote = textwrap.fill(f'"{quote}"', width=max_width)
            
            # Calcular posición del texto centrado
            lines = wrapped_quote.split('\n')
            line_heights = []
            total_height = 0
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=quote_font)
                line_height = bbox[3] - bbox[1]
                line_heights.append(line_height)
                total_height += line_height + 10
            
            # Posición inicial Y
            y = (height - total_height) // 2 - 20
            
            # Dibujar cada línea centrada
            for i, line in enumerate(lines):
                bbox = draw.textbbox((0, 0), line, font=quote_font)
                line_width = bbox[2] - bbox[0]
                x = (width - line_width) // 2
                draw.text((x, y), line, font=quote_font, fill=theme_colors['quote_color'])
                y += line_heights[i] + 10
            
            # Dibujar autor (usando guion simple)
            author = "- Kanye West"
            author_bbox = draw.textbbox((0, 0), author, font=author_font)
            author_width = author_bbox[2] - author_bbox[0]
            author_x = (width - author_width) // 2
            author_y = y + 20
            
            draw.text((author_x, author_y), author, font=author_font, fill=theme_colors['author_color'])
            
            # Agregar borde
            border_width = 3
            draw.rectangle(
                [(border_width, border_width), (width - border_width, height - border_width)],
                outline=theme_colors['accent_color'],
                width=border_width
            )
            
            # Convertir imagen a bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG', optimize=True)
            img_byte_arr.seek(0)
            
            # Enviar respuesta
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(img_byte_arr.getvalue())
            
            print(f"✅ Successfully generated image with theme: {theme}", file=sys.stderr)
            
        except Exception as e:
            # Log del error completo
            error_trace = traceback.format_exc()
            print(f"❌ ERROR: {str(e)}", file=sys.stderr)
            print(error_trace, file=sys.stderr)
            
            # Enviar respuesta de error como imagen
            self.send_response(500)
            self.send_header('Content-Type', 'image/png')
            self.end_headers()
            
            try:
                error_img = Image.new('RGB', (800, 400), (40, 40, 40))
                error_draw = ImageDraw.Draw(error_img)
                
                error_lines = [
                    "Error generating Kanye quote:",
                    "",
                    str(e)[:80],
                    "",
                    "Check server logs for details"
                ]
                
                y_pos = 100
                for line in error_lines:
                    error_draw.text((50, y_pos), line, fill=(255, 100, 100))
                    y_pos += 30
                
                error_byte_arr = io.BytesIO()
                error_img.save(error_byte_arr, format='PNG')
                error_byte_arr.seek(0)
                self.wfile.write(error_byte_arr.getvalue())
            except:
                # Si ni siquiera podemos crear la imagen de error
                self.wfile.write(b'Error: Unable to generate image')

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-Type', 'image/png')
        self.end_headers()