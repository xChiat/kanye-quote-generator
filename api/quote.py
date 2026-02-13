#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from http.server import BaseHTTPRequestHandler
from urllib import request, parse
import json
import io
import textwrap
import traceback
import sys

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
        'text_color': (254, 254, 254),
        'quote_color': (255, 121, 198),
        'author_color': (139, 148, 158),
        'accent_color': (255, 121, 198)
    },
    'react': {
        'bg_color': (32, 42, 53),
        'text_color': (97, 218, 251),
        'quote_color': (97, 218, 251),
        'author_color': (139, 148, 158),
        'accent_color': (0, 216, 255)
    },
    'omni': {
        'bg_color': (25, 22, 34),
        'text_color': (255, 122, 199),
        'quote_color': (232, 223, 122),
        'author_color': (216, 216, 221),
        'accent_color': (255, 122, 199)
    },
    'dark': {
        'bg_color': (13, 17, 23),
        'text_color': (201, 209, 217),
        'quote_color': (88, 166, 255),
        'author_color': (139, 148, 158),
        'accent_color': (88, 166, 255)
    },
    'github_dark': {
        'bg_color': (13, 17, 23),
        'text_color': (201, 209, 217),
        'quote_color': (79, 192, 141),
        'author_color': (139, 148, 158),
        'accent_color': (79, 192, 141)
    },
    'tokyonight': {
        'bg_color': (26, 27, 38),
        'text_color': (169, 177, 214),
        'quote_color': (122, 162, 247),
        'author_color': (86, 95, 137),
        'accent_color': (187, 154, 247)
    },
    'dracula': {
        'bg_color': (40, 42, 54),
        'text_color': (248, 248, 242),
        'quote_color': (255, 121, 198),
        'author_color': (98, 114, 164),
        'accent_color': (189, 147, 249)
    },
    'monokai': {
        'bg_color': (39, 40, 34),
        'text_color': (248, 248, 240),
        'quote_color': (249, 38, 114),
        'author_color': (117, 113, 94),
        'accent_color': (166, 226, 46)
    },
    'gruvbox': {
        'bg_color': (40, 40, 40),
        'text_color': (235, 219, 178),
        'quote_color': (254, 128, 25),
        'author_color': (168, 153, 132),
        'accent_color': (184, 187, 38)
    },
    'nord': {
        'bg_color': (46, 52, 64),
        'text_color': (216, 222, 233),
        'quote_color': (136, 192, 208),
        'author_color': (129, 161, 193),
        'accent_color': (143, 188, 187)
    },
    'kanye': {
        'bg_color': (0, 0, 0),
        'text_color': (255, 255, 255),
        'quote_color': (255, 215, 0),
        'author_color': (192, 192, 192),
        'accent_color': (255, 215, 0)
    },
    'default': {
        'bg_color': (13, 17, 23),
        'text_color': (201, 209, 217),
        'quote_color': (255, 121, 198),
        'author_color': (139, 148, 158),
        'accent_color': (255, 121, 198)
    }
}

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
            
            # Obtener quote de Kanye API
            try:
                response = request.urlopen('https://api.kanye.rest/', timeout=5)
                data = json.loads(response.read())
                quote = data['quote']
            except Exception as api_error:
                print(f"Error fetching Kanye quote: {api_error}", file=sys.stderr)
                quote = "I'm doing pretty good as far as geniuses go"
            
            # Configuración de la imagen
            width = 800
            height = 400
            
            # Crear imagen
            img = Image.new('RGB', (width, height), theme_colors['bg_color'])
            draw = ImageDraw.Draw(img)
            
            # Cargar fuente
            try:
                quote_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
                author_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            except Exception as font_error:
                print(f"Font error: {font_error}, using default", file=sys.stderr)
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
            
            # Dibujar autor
            author = "— Kanye West"
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