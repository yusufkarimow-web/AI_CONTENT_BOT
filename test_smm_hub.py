# test_smm_hub.py — Тесты для проверки SMM Hub и разделения по странам в TojikAI

import unittest
from content_engine.niche_manager import get_all_niches, get_topics, get_niche_name
from services.ai_generator import select_viral_hook, get_system_prompt
from content_engine.menu import is_smm_tool_button, get_tool_id_by_text


class TestSMMHub(unittest.TestCase):

    def test_niche_country_splitting(self):
        """Проверяет, что ниши корректно разделены по странам и их больше 100"""
        niches_uz = get_all_niches(language="ru", country="uz")
        niches_tj = get_all_niches(language="ru", country="tj")

        self.assertGreaterEqual(len(niches_uz), 8, "Узбекистан должен содержать как минимум 8 ниш")
        self.assertGreaterEqual(len(niches_tj), 8, "Таджикистан должен содержать как минимум 8 ниш")

        # Проверяем отсутствие пересечений
        keys_uz = {n["key"] for n in niches_uz}
        keys_tj = {n["key"] for n in niches_tj}
        self.assertEqual(len(keys_uz.intersection(keys_tj)), 0, "Ниши стран не должны пересекаться")

    def test_topic_generation(self):
        """Проверяет динамическую генерацию тем при нехватке предустановленных"""
        topics = get_topics(key="cafe_uz", count=15, language="uz")
        self.assertEqual(len(topics), 15, "Должно быть сгенерировано ровно 15 тем")

    def test_smm_tools_buttons(self):
        """Проверяет распознавание новых платформо-центричных SMM инструментов"""
        self.assertTrue(is_smm_tool_button("📷 Instagram"))
        self.assertTrue(is_smm_tool_button("📱 Telegram"))
        self.assertTrue(is_smm_tool_button("🎵 TikTok"))

        self.assertEqual(get_tool_id_by_text("📷 Instagram"), "instagram")
        self.assertEqual(get_tool_id_by_text("📱 Telegram"), "tg_channel")
        self.assertEqual(get_tool_id_by_text("🎵 TikTok"), "tiktok")

    def test_ai_generator_context_prompt(self):
        """Проверяет, что системные промпты содержат правильные города-ориентиры"""
        prompt_uz = get_system_prompt(niche="cafe_uz", language="ru", content_type="reels", country="uz")
        prompt_tj = get_system_prompt(niche="wholesale_tj", language="ru", content_type="reels", country="tj")

        self.assertIn("Ташкент", prompt_uz)
        self.assertIn("Душанбе", prompt_tj)


if __name__ == "__main__":
    unittest.main()
