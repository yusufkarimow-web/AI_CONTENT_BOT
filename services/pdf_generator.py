# services/pdf_generator.py — Генератор брендированных PDF-отчетов "TojikAI Marketing Package"
# Использует ReportLab и DejaVuSans для полной поддержки кириллицы (русский, таджикский).

import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# === НАСТРОЙКА ШРИФТОВ ===
# Сначала ищем во внутренней директории проекта assets/fonts (рекомендуется для VPS и деплоя)
LOCAL_FONT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts", "DejaVuSans.ttf")
LOCAL_FONT_BOLD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fonts", "DejaVuSans-Bold.ttf")

SYSTEM_FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SYSTEM_FONT_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

# Выбираем доступные пути
FONT_PATH = LOCAL_FONT_PATH if os.path.exists(LOCAL_FONT_PATH) else SYSTEM_FONT_PATH
FONT_BOLD_PATH = LOCAL_FONT_BOLD_PATH if os.path.exists(LOCAL_FONT_BOLD_PATH) else SYSTEM_FONT_BOLD_PATH

# Безопасно регистрируем DejaVuSans с полной поддержкой кириллицы
if os.path.exists(FONT_PATH) and os.path.exists(FONT_BOLD_PATH):
    pdfmetrics.registerFont(TTFont('DejaVuSans', FONT_PATH))
    pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', FONT_BOLD_PATH))
    DEFAULT_FONT = 'DejaVuSans'
    DEFAULT_FONT_BOLD = 'DejaVuSans-Bold'
else:
    DEFAULT_FONT = 'Helvetica'
    DEFAULT_FONT_BOLD = 'Helvetica-Bold'


def generate_marketing_pdf(
    country: str,
    language: str,
    niche: str,
    platform: str,
    goal: str,
    content_text: str
) -> io.BytesIO:
    """Генерирует брендированный PDF-документ маркетингового пакета TojikAI"""

    buffer = io.BytesIO()

    # 1. Настройка документа
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Кастомные стили
    style_title = ParagraphStyle(
        name='TitleStyle',
        fontName=DEFAULT_FONT_BOLD,
        fontSize=22,
        textColor=colors.HexColor('#2A2D34'),
        spaceAfter=15,
        alignment=1 # Center
    )

    style_subtitle = ParagraphStyle(
        name='SubTitleStyle',
        fontName=DEFAULT_FONT_BOLD,
        fontSize=13,
        textColor=colors.HexColor('#0088CC'),
        spaceAfter=15,
        alignment=1 # Center
    )

    style_section = ParagraphStyle(
        name='SectionStyle',
        fontName=DEFAULT_FONT_BOLD,
        fontSize=14,
        textColor=colors.HexColor('#2A2D34'),
        spaceBefore=15,
        spaceAfter=8,
        borderPadding=4
    )

    style_body = ParagraphStyle(
        name='BodyStyle',
        fontName=DEFAULT_FONT,
        fontSize=10,
        textColor=colors.HexColor('#4A4E5D'),
        leading=14,
        spaceAfter=6
    )

    style_meta_label = ParagraphStyle(
        name='MetaLabel',
        fontName=DEFAULT_FONT_BOLD,
        fontSize=9,
        textColor=colors.HexColor('#4A4E5D')
    )

    style_meta_val = ParagraphStyle(
        name='MetaVal',
        fontName=DEFAULT_FONT,
        fontSize=9,
        textColor=colors.HexColor('#1A1A1A')
    )

    story = []

    # 2. Шапка отчета (TojikAI Branding)
    story.append(Paragraph("🚀 TojikAI Marketing Platform", style_title))
    story.append(Paragraph("📄 PROFESSIONAL SMM & MARKETING PACKAGE", style_subtitle))
    story.append(Spacer(1, 10))

    # 3. Таблица метаданных
    meta_data = [
        [
            Paragraph("<b>Страна / Кишвар:</b>", style_meta_label),
            Paragraph(country.upper(), style_meta_val),
            Paragraph("<b>Дата / Сана:</b>", style_meta_label),
            Paragraph(datetime.now().strftime("%d.%m.%Y"), style_meta_val)
        ],
        [
            Paragraph("<b>Ниша / Соҳа:</b>", style_meta_label),
            Paragraph(niche, style_meta_val),
            Paragraph("<b>Язык / Забон:</b>", style_meta_label),
            Paragraph(language.upper(), style_meta_val)
        ],
        [
            Paragraph("<b>Платформа:</b>", style_meta_label),
            Paragraph(platform, style_meta_val),
            Paragraph("<b>Цель / Ҳадаф:</b>", style_meta_label),
            Paragraph(goal, style_meta_val)
        ]
    ]

    t = Table(meta_data, colWidths=[110, 150, 110, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F4F6F9')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
    ]))

    story.append(t)
    story.append(Spacer(1, 15))

    # 4. Обработка и вставка основного текста контента
    lines = content_text.split('\n')
    for line in lines:
        line_strip = line.strip()
        if not line_strip:
            story.append(Spacer(1, 4))
            continue

        # Если строка является заголовком раздела
        if line_strip.startswith('📌') or line_strip.startswith('✅') or line_strip.startswith('🎬') or line_strip.startswith('📝') or line_strip.startswith('📸') or line_strip.startswith('📋') or line_strip.startswith('🎯') or line_strip.startswith('📢'):
            story.append(Paragraph(line_strip, style_section))
        elif line_strip.startswith('•') or line_strip.startswith('-'):
            story.append(Paragraph(line_strip, style_body))
        else:
            story.append(Paragraph(line_strip, style_body))

    # 5. Подпись / Footer
    story.append(Spacer(1, 20))
    story.append(Paragraph("<i>* Сгенерировано автоматически SMM-платформой TojikAI. Все права защищены.</i>", style_meta_val))

    doc.build(story)

    buffer.seek(0)
    return buffer
