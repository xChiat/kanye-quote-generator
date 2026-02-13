from http.server import BaseHTTPRequestHandler
from urllib import request
import json
from PIL import Image, ImageDraw, ImageFont
import io
import textwrap

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Obtener quote de Kanye API
            response = request.urlopen('https://api.kanye.rest/')
            data = json.loads(response.read())
            quote = data['quote']
            
            # Configuración de la imagen
            width = 800
            height = 400
            bg_color = (13, 17, 23)  # Dark background
            text_color = (255, 121, 198)  # Pink color (#ff79c6)
            author_color = (139, 148, 158)  # Gray color
            
            # Crear imagen
            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Intentar cargar fuente personalizada, si no usar default
            try:
                quote_font = ImageFont.truetype("assets/BebasNeue-Regular.ttf", 32)
                author_font = ImageFont.truetype("assets/BebasNeue-Regular.ttf", 24)
            except:
                quote_font = ImageFont.load_default()
                author_font = ImageFont.load_default()
            
            # Wrap text para que no se salga de la imagen
            max_width = 50  # caracteres por línea
            wrapped_quote = textwrap.fill(quote, width=max_width)
            
            # Calcular posición del texto
            # Usar textbbox para calcular dimensiones
            bbox = draw.textbbox((0, 0), wrapped_quote, font=quote_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            x = (width - text_width) // 2
            y = (height - text_height) // 2 - 40
            
            # Dibujar quote
            draw.text((x, y), wrapped_quote, font=quote_font, fill=text_color, align='center')
            
            # Dibujar autor
            author = "- Kanye West"
            author_bbox = draw.textbbox((0, 0), author, font=author_font)
            author_width = author_bbox[2] - author_bbox[0]
            author_x = (width - author_width) // 2
            author_y = y + text_height + 30
            
            draw.text((author_x, author_y), author, font=author_font, fill=author_color)
            
            # Convertir imagen a bytes
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            # Enviar respuesta
            self.send_response(200)
            self.send_header('Content-Type', 'image/png')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            self.wfile.write(img_byte_arr.getvalue())
            
        except Exception as e:
            # En caso de error, devolver imagen con mensaje de error
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())

    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-Type', 'image/png')
        self.end_headers()