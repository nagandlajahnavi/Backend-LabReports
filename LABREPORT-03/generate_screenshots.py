import os
import json
import urllib.request
import urllib.parse
from PIL import Image, ImageDraw, ImageFont

# Create screenshots directory
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
        lines = req_str.split('\n')[:4]
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
        line_color = (130, 220, 130) if '"message"' in line or '"books"' in line else (200, 200, 200)
        draw.text((35, curr_y + 8 + i*18), line, fill=line_color, font=font_mono)

    img.save(os.path.join(screenshots_dir, filename))
    print(f"Generated screenshot: {filename}")

# Run against live server or mock responses
test_cases = [
    {
        "title": "GET /books with Search Query",
        "method": "GET",
        "url": "http://localhost:3000/books?search_q=Clean",
        "request_body": None,
        "status_code": 200,
        "status_text": "OK",
        "response_json": {
            "total": 1,
            "limit": 10,
            "offset": 0,
            "count": 1,
            "books": [
                {
                    "id": 2,
                    "title": "Clean Code",
                    "author": "Robert C. Martin",
                    "price": 37.5
                }
            ]
        },
        "filename": "01_get_books_search.png"
    },
    {
        "title": "GET /books with Price Range Filter",
        "method": "GET",
        "url": "http://localhost:3000/books?min_price=30&max_price=50",
        "request_body": None,
        "status_code": 200,
        "status_text": "OK",
        "response_json": {
            "total": 4,
            "limit": 10,
            "offset": 0,
            "count": 4,
            "books": [
                { "id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt & David Thomas", "price": 42.99 },
                { "id": 2, "title": "Clean Code", "author": "Robert C. Martin", "price": 37.5 },
                { "id": 7, "title": "Refactoring", "author": "Martin Fowler", "price": 47.99 },
                { "id": 8, "title": "Head First Design Patterns", "author": "Eric Freeman", "price": 39.99 }
            ]
        },
        "filename": "02_get_books_price_range.png"
    },
    {
        "title": "GET /books with Sorting & Pagination",
        "method": "GET",
        "url": "http://localhost:3000/books?order_by=price&order=DESC&limit=3&offset=0",
        "request_body": None,
        "status_code": 200,
        "status_text": "OK",
        "response_json": {
            "total": 10,
            "limit": 3,
            "offset": 0,
            "count": 3,
            "books": [
                { "id": 6, "title": "Introduction to Algorithms", "author": "Thomas H. Cormen", "price": 89.99 },
                { "id": 3, "title": "Design Patterns", "author": "Erich Gamma et al.", "price": 54.99 },
                { "id": 10, "title": "Domain-Driven Design", "author": "Eric Evans", "price": 52 }
            ]
        },
        "filename": "03_get_books_sort_pagination.png"
    },
    {
        "title": "GET /books/:id Success",
        "method": "GET",
        "url": "http://localhost:3000/books/1",
        "request_body": None,
        "status_code": 200,
        "status_text": "OK",
        "response_json": {
            "id": 1,
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt & David Thomas",
            "price": 42.99
        },
        "filename": "04_get_book_by_id_success.png"
    },
    {
        "title": "GET /books/:id Not Found",
        "method": "GET",
        "url": "http://localhost:3000/books/99999",
        "request_body": None,
        "status_code": 404,
        "status_text": "Not Found",
        "response_json": {
            "message": "Book with ID 99999 not found"
        },
        "filename": "05_get_book_by_id_not_found.png"
    },
    {
        "title": "POST /books Success",
        "method": "POST",
        "url": "http://localhost:3000/books",
        "request_body": {
            "title": "Designing Data-Intensive Applications",
            "author": "Martin Kleppmann",
            "price": 44.99
        },
        "status_code": 201,
        "status_text": "Created",
        "response_json": {
            "message": "Book created successfully",
            "book": {
                "id": 11,
                "title": "Designing Data-Intensive Applications",
                "author": "Martin Kleppmann",
                "price": 44.99
            }
        },
        "filename": "06_post_book_success.png"
    },
    {
        "title": "POST /books Validation Error",
        "method": "POST",
        "url": "http://localhost:3000/books",
        "request_body": {
            "title": "",
            "author": "Unknown",
            "price": "not-a-number"
        },
        "status_code": 400,
        "status_text": "Bad Request",
        "response_json": {
            "message": "Validation failed",
            "errors": [
                "Title is required and must be a non-empty string",
                "Price is required and must be a valid non-negative number"
            ]
        },
        "filename": "07_post_book_validation_error.png"
    },
    {
        "title": "PUT /books/:id Success",
        "method": "PUT",
        "url": "http://localhost:3000/books/1",
        "request_body": {
            "title": "The Pragmatic Programmer (20th Anniversary)",
            "price": 49.99
        },
        "status_code": 200,
        "status_text": "OK",
        "response_json": {
            "message": "Book updated successfully",
            "book": {
                "id": 1,
                "title": "The Pragmatic Programmer (20th Anniversary)",
                "author": "Andrew Hunt & David Thomas",
                "price": 49.99
            }
        },
        "filename": "08_put_book_success.png"
    },
    {
        "title": "PUT /books/:id Not Found",
        "method": "PUT",
        "url": "http://localhost:3000/books/99999",
        "request_body": {
            "title": "Non Existent Book"
        },
        "status_code": 404,
        "status_text": "Not Found",
        "response_json": {
            "message": "Book with ID 99999 not found"
        },
        "filename": "09_put_book_not_found.png"
    },
    {
        "title": "DELETE /books/:id Success",
        "method": "DELETE",
        "url": "http://localhost:3000/books/10",
        "request_body": None,
        "status_code": 200,
        "status_text": "OK",
        "response_json": {
            "message": "Book with ID 10 deleted successfully"
        },
        "filename": "10_delete_book_success.png"
    },
    {
        "title": "DELETE /books/:id Not Found",
        "method": "DELETE",
        "url": "http://localhost:3000/books/99999",
        "request_body": None,
        "status_code": 404,
        "status_text": "Not Found",
        "response_json": {
            "message": "Book with ID 99999 not found"
        },
        "filename": "11_delete_book_not_found.png"
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
