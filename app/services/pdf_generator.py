# app/services/pdf_generator.py
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import structlog

logger = structlog.get_logger(__name__)

class PDFGenerator:
    def __init__(self):
        self._register_fonts()

    def _register_fonts(self):
        """Регистрация TrueType шрифтов для поддержки кириллицы"""
        font_paths = [
            "assets/fonts/DejaVuSans.ttf",
            "app/static/fonts/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/System/Library/Fonts/Arial.ttf",  # macOS
            "C:\\Windows\\Fonts\\arial.ttf",  # Windows
        ]

        font_registered = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    pdfmetrics.registerFont(TTFont('DejaVuSans', font_path))
                    pdfmetrics.registerFont(TTFont('DejaVuSansBold', font_path))
                    logger.info("font_registered", path=font_path)
                    font_registered = True
                    break
                except Exception as e:
                    logger.warning("font_registration_failed", path=font_path, error=str(e))
                    continue

        if not font_registered:
            logger.warning("no_custom_fonts_found_using_default")

    async def generate_branded_pdf(
        self,
        output_path: str,
        user_name: str,
        content_type: str,
        content_text: str,
        branding_data: dict = None
    ) -> str:
        """Генерация брендированного PDF с SMM-пакетом"""

        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            doc = SimpleDocTemplate(
                output_path,
                pagesize=A4,
                rightMargin=40,
                leftMargin=40,
                topMargin=50,
                bottomMargin=40,
                title="TojikAI SMM Package",
                author="TojikAI Platform"
            )

            styles = self._create_styles()
            story = []

            # Логотип и заголовок
            logo_path = "app/static/images/tojikai_logo_light.png"
            if os.path.exists(logo_path):
                try:
                    story.append(Image(logo_path, width=100, height=35))
                    story.append(Spacer(1, 10))
                except Exception as e:
                    logger.warning("logo_load_failed", error=str(e))

            # Заголовок
            story.append(Paragraph(
                "<b>🎯 TOJIKAI SMM MARKETING PACKAGE</b>",
                styles['TitleStyle']
            ))
            story.append(Spacer(1, 5))

            # Метаинформация
            meta_text = f"""
            <b>Пакет:</b> {content_type.upper()}<br/>
            <b>Создано для:</b> {user_name}<br/>
            <b>Дата:</b> {datetime.now().strftime('%d.%m.%Y %H:%M')}<br/>
            <b>Платформа:</b> TojikAI v4.0
            """
            story.append(Paragraph(meta_text, styles['MetaStyle']))
            story.append(Spacer(1, 15))

            # Разделитель
            story.append(self._create_divider())
            story.append(Spacer(1, 10))

            # Основной контент
            # Парсинг и форматирование
            sections = content_text.split("\n\n")

            for i, section in enumerate(sections):
                if section.strip():
                    # Проверка на заголовок (жирный текст)
                    if section.startswith("**") and section.endswith("**"):
                        section_title = section.replace("**", "").strip()
                        story.append(Paragraph(f"<b>{section_title}</b>", styles['HeadingStyle']))
                    else:
                        # Обычный текст
                        formatted_section = section.replace("\n", "<br/>").strip()
                        story.append(Paragraph(formatted_section, styles['BodyStyle']))

                    story.append(Spacer(1, 8))

                    # Разделитель между секциями
                    if i < len(sections) - 1:
                        story.append(Spacer(1, 5))

            # Футер с советом
            story.append(Spacer(1, 15))
            story.append(self._create_divider())
            story.append(Spacer(1, 10))

            footer_text = """
            <i><b>💡 PRO TIP:</b> Используй этот контент как основу и адаптируй под свою аудиторию.
            Тестируй разные варианты CTA и отслеживай метрики! Успеха в продажах! 🚀</i>
            """
            story.append(Paragraph(footer_text, styles['FooterStyle']))

            # Финальная информация
            story.append(Spacer(1, 15))
            final_text = """
            <font size="8" color="#999999">
            Этот контент создан автоматически AI-генератором TojikAI Platform.<br/>
            Для более глубокого анализа и консультации свяжитесь с нашей командой через @tojikai_bot
            </font>
            """
            story.append(Paragraph(final_text, styles['SmallStyle']))

            # Построение PDF
            doc.build(story)

            logger.info("pdf_generated_success", path=output_path, size_mb=os.path.getsize(output_path) / 1024 / 1024)
            return output_path

        except Exception as e:
            logger.exception("pdf_generation_error", error=str(e))
            raise

    def _create_styles(self) -> dict:
        """Создание стилей для PDF"""
        styles = getSampleStyleSheet()

        # Use registered DejaVuSans font if possible, or fallback to Helvetica
        has_dejavu = False
        try:
            pdfmetrics.getFont('DejaVuSans')
            has_dejavu = True
        except KeyError:
            pass

        font_name = 'DejaVuSans' if has_dejavu else 'Helvetica'

        custom_styles = {
            'TitleStyle': ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontName=font_name,
                fontSize=24,
                leading=28,
                textColor=colors.HexColor('#1E1B4B'),
                spaceAfter=10,
                alignment=1  # Центрирование
            ),
            'HeadingStyle': ParagraphStyle(
                'CustomHeading',
                parent=styles['Heading2'],
                fontName=font_name,
                fontSize=14,
                leading=16,
                textColor=colors.HexColor('#2563EB'),
                spaceAfter=8,
                spaceBefore=8
            ),
            'BodyStyle': ParagraphStyle(
                'CustomBody',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=11,
                leading=15,
                textColor=colors.HexColor('#374151'),
                spaceAfter=10,
                alignment=4  # Justify
            ),
            'MetaStyle': ParagraphStyle(
                'CustomMeta',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=10,
                leading=13,
                textColor=colors.HexColor('#2563EB'),
                spaceAfter=10,
                leftIndent=20
            ),
            'FooterStyle': ParagraphStyle(
                'CustomFooter',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=10,
                leading=13,
                textColor=colors.HexColor('#059669'),
                spaceAfter=10,
                alignment=0
            ),
            'SmallStyle': ParagraphStyle(
                'CustomSmall',
                parent=styles['Normal'],
                fontName=font_name,
                fontSize=8,
                leading=10,
                textColor=colors.HexColor('#999999'),
                alignment=0
            )
        }

        return custom_styles

    def _create_divider(self):
        """Создание линии-разделителя"""
        from reportlab.platypus import HRFlowable
        return HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E5E7EB'))
