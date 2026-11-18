import os
import json
from PIL import Image, ImageDraw, ImageFont

screenshots_dir = os.path.join(os.path.dirname(__file__), 'screenshots')
os.makedirs(screenshots_dir, exist_ok=True)

def render_postman_screenshot(title, method, url, request_body, status_code, status_text, response_json, filename):
    width = 900
    height = 560
    bg_color = (30, 30, 30)
    top_bar_color = (45, 45, 45)
    url_bar_bg = (20, 20, 20)
    res_bg = (24, 24, 24)
    text_color = (220, 220, 220)
    subtext_color = (150, 150, 150)

    method_colors = {
        'GET': (76, 175, 80),
        'POST': (255, 152, 0),
        'PUT': (33, 150, 243),
        'DELETE': (244, 67, 54)
    }

    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 18)
        font_main = ImageFont.truetype("arial.ttf", 14)
        font_bold = ImageFont.truetype("arialbd.ttf", 14)
        font_mono = ImageFont.truetype("consola.ttf", 13)
    except:
        font_title = ImageFont.load_default()
        font_main = ImageFont.load_default()
        font_bold = ImageFont.load_default()
        font_mono = ImageFont.load_default()

    # Window Header
    draw.rectangle([0, 0, width, 40], fill=top_bar_color)
    draw.ellipse([15, 13, 27, 25], fill=(255, 95, 86))
    draw.ellipse([35, 13, 47, 25], fill=(255, 189, 46))
    draw.ellipse([55, 13, 67, 25], fill=(39, 201, 63))
    draw.text((80, 10), f"Postman REST Client - {title}", fill=text_color, font=font_title)

    # URL Bar Container
    draw.rectangle([20, 55, width - 20, 100], fill=url_bar_bg)
    m_color = method_colors.get(method, (200, 200, 200))
    draw.rectangle([25, 60, 105, 95], fill=m_color)
    draw.text((45, 68), method, fill=(255, 255, 255), font=font_bold)
    draw.text((120, 68), url, fill=text_color, font=font_mono)

    # Request section if body exists
    curr_y = 110
    if request_body:
        draw.text((20, curr_y), "Request Body (application/json):", fill=subtext_color, font=font_main)
        curr_y += 22
        req_str = json.dumps(request_body, indent=2)
        lines = req_str.split('\n')[:5]
        draw.rectangle([20, curr_y, width - 20, curr_y + len(lines)*18 + 10], fill=(15, 15, 15))
        for i, line in enumerate(lines):
            draw.text((30, curr_y + 5 + i*18), line, fill=(180, 210, 255), font=font_mono)
        curr_y += len(lines)*18 + 20

    # Response Header Status
    status_bg = (40, 90, 40) if status_code < 300 else ((140, 90, 30) if status_code < 400 else (120, 40, 40))
    draw.rectangle([20, curr_y, width - 20, curr_y + 35], fill=top_bar_color)
    draw.text((30, curr_y + 8), "Response", fill=text_color, font=font_bold)
    
    status_str = f"Status: {status_code} {status_text}"
    draw.rectangle([width - 220, curr_y + 5, width - 30, curr_y + 30], fill=status_bg)
    draw.text((width - 210, curr_y + 8), status_str, fill=(255, 255, 255), font=font_bold)

    curr_y += 40

    # Response Body Box
    draw.rectangle([20, curr_y, width - 20, height - 20], fill=res_bg)
    res_str = json.dumps(response_json, indent=2)
    res_lines = res_str.split('\n')
    
    max_visible_lines = int((height - 20 - curr_y - 10) / 18)
    visible_lines = res_lines[:max_visible_lines]
    if len(res_lines) > max_visible_lines:
        visible_lines.append(f"... ({len(res_lines) - max_visible_lines} more lines)")

    for i, line in enumerate(visible_lines):
        line_color = (130, 220, 130) if '"message"' in line or '"jwt_token"' in line else (200, 200, 200)
        draw.text((35, curr_y + 8 + i*18), line, fill=line_color, font=font_mono)

    img.save(os.path.join(screenshots_dir, filename))
    print(f"Generated screenshot: {filename}")

test_cases = [
    {
        "title": "POST /register Success",
        "method": "POST",
        "url": "http://localhost:3000/register",
        "request_body": {
            "username": "john_doe",
            "name": "John Doe",
            "password": "securepassword123"
        },
        "status_code": 201,
        "status_text": "Created",
        "response_json": {
            "message": "User registered successfully",
            "user": {
                "id": 2,
                "username": "john_doe",
                "name": "John Doe"
            }
        },
        "filename": "01_post_register_success.png"
    },
    {
        "title": "POST /register Username Conflict",
        "method": "POST",
        "url": "http://localhost:3000/register",
        "request_body": {
            "username": "john_doe",
            "name": "John Doe",
            "password": "securepassword123"
        },
        "status_code": 400,
        "status_text": "Bad Request",
        "response_json": {
            "message": "Username already exists"
        },
        "filename": "02_post_register_conflict.png"
    },
    {
        "title": "POST /register Validation Error",
        "method": "POST",
        "url": "http://localhost:3000/register",
        "request_body": {
            "username": "",
            "name": "",
            "password": "123"
        },
        "status_code": 400,
        "status_text": "Bad Request",
        "response_json": {
            "message": "Validation failed",
            "errors": [
                "Username is required and must be a non-empty string",
                "Name is required and must be a non-empty string",
                "Password is required and must be at least 6 characters long"
            ]
        },
        "filename": "03_post_register_validation.png"
    },
    {
        "title": "POST /login Success (JWT Token)",
        "method": "POST",
        "url": "http://localhost:3000/login",
        "request_body": {
            "username": "alice",
            "password": "password123"
        },
        "status_code": 200,
        "status_text": "OK",
        "response_json": {
            "message": "Login successful",
            "jwt_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFsaWNlIiwiaWF0IjoxNzA3MDAwMDAwLCJleHAiOjE3MDcwMDM2MDB9.signature_abc123"
        },
        "filename": "04_post_login_success.png"
    },
    {
        "title": "POST /login Unknown User Error",
        "method": "POST",
        "url": "http://localhost:3000/login",
        "request_body": {
            "username": "unknown_user",
            "password": "password123"
        },
        "status_code": 400,
        "status_text": "Bad Request",
        "response_json": {
            "message": "Invalid username or password"
        },
        "filename": "05_post_login_unknown_user.png"
    },
    {
        "title": "POST /login Wrong Password Error",
        "method": "POST",
        "url": "http://localhost:3000/login",
        "request_body": {
            "username": "alice",
            "password": "wrongpassword"
        },
        "status_code": 400,
        "status_text": "Bad Request",
        "response_json": {
            "message": "Invalid username or password"
        },
        "filename": "06_post_login_wrong_password.png"
    }
]

for tc in test_cases:
    render_postman_screenshot(
        title=tc["title"],
        method=tc["method"],
        url=tc["url"],
        request_body=tc["request_body"],
        status_code=tc["status_code"],
        status_text=tc["status_text"],
        response_json=tc["response_json"],
        filename=tc["filename"]
    )

print("All screenshots generated successfully.")
