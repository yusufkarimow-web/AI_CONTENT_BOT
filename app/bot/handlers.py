# app/bot/handlers.py
import structlog
import uuid
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select
from datetime import datetime

from app.bot.states import SMSGenerationStates
from app.bot.keyboards import (
    build_niche_keyboard, build_platform_keyboard, build_goal_keyboard,
    build_format_keyboard, build_main_menu_keyboard, build_smm_result_keyboard
)
from app.services.generation_service import GenerationService
from app.services.whatsapp_service import WhatsAppService
from app.db.session import get_db_session
from app.db.models import User, Workspace, Membership, Subscription, Generation
from app.core.config import get_settings

logger = structlog.get_logger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Команда старт - приветствие и регистрация пользователя"""
    user_id = message.from_user.id

    # Получение сессии БД
    async for db in get_db_session():
        try:
            # Проверка наличия пользователя
            user_stmt = select(User).where(User.telegram_id == user_id)
            result = await db.execute(user_stmt)
            existing_user = result.scalar_one_or_none()

            if not existing_user:
                # Создание нового пользователя
                new_user = User(
                    id=uuid.uuid4(),
                    telegram_id=user_id,
                    username=message.from_user.username or "unknown",
                    first_name=message.from_user.first_name or "User",
                    language="ru",
                    country="uz",  # Default country
                )
                db.add(new_user)

                default_workspace = Workspace(
                    id=uuid.uuid4(),
                    name=f"{new_user.first_name}'s Workspace",
                    slug=f"ws_{user_id}",
                    country="uz",
                )
                db.add(default_workspace)

                await db.flush()  # Flush to get IDs
                new_user.workspace_id = default_workspace.id

                membership = Membership(
                    id=uuid.uuid4(),
                    user_id=new_user.id,
                    workspace_id=default_workspace.id,
                    role="owner",
                )
                db.add(membership)

                # Создание free subscription
                subscription = Subscription(
                    id=uuid.uuid4(),
                    workspace_id=default_workspace.id,
                    plan_code="free",
                    status="active",
                    current_period_start=datetime.utcnow(),
                    provider=None,
                )
                db.add(subscription)

                await db.commit()
                logger.info("new_user_registered", user_id=user_id)

            await message.answer(
                "🎉 <b>Добро пожаловать в TojikAI SMM Platform!</b>\n\n"
                "Платформа для создания профессионального SMM-контента за секунды.\n\n"
                "Выберите действие:",
                reply_markup=build_main_menu_keyboard(),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.exception("start_handler_error", error=str(e))
            await message.answer("❌ Ошибка при инициализации. Попробуйте позже.")


@router.message(F.text == "🚀 Создать Контент")
async def start_smm_generation(message: Message, state: FSMContext):
    """Начало процесса генерации SMM-пакета"""
    user_id = message.from_user.id

    # Получение страны пользователя
    async for db in get_db_session():
        user_stmt = select(User).where(User.telegram_id == user_id)
        result = await db.execute(user_stmt)
        user = result.scalar_one_or_none()

        if not user:
            await message.answer("❌ Пользователь не найден. Введите /start")
            return

        await state.update_data(user_id=str(user.id), workspace_id=str(user.workspace_id), country=user.country)

        # Отправка клавиатуры выбора ниши
        await message.answer(
            "📋 <b>Умные Шаги #1: Выберите вашу нишу</b>\n\n"
            "Это поможет нам создать релевантный контент для вашей аудитории.",
            reply_markup=build_niche_keyboard(user.country),
            parse_mode="HTML"
        )

        await state.set_state(SMSGenerationStates.choose_niche)


@router.callback_query(SMSGenerationStates.choose_niche, F.data.startswith("niche_"))
async def handle_niche_select(query: CallbackQuery, state: FSMContext):
    """Обработка выбора ниши"""
    niche_code = query.data.replace("niche_", "")
    await state.update_data(niche=niche_code)

    await query.message.edit_text(
        "🎯 <b>Умные Шаги #2: Выберите платформу</b>\n\n"
        "На какой площадке будет размещен контент?",
        reply_markup=build_platform_keyboard(),
        parse_mode="HTML"
    )

    await state.set_state(SMSGenerationStates.choose_platform)
    await query.answer()


@router.callback_query(SMSGenerationStates.choose_platform, F.data.startswith("platform_"))
async def handle_platform_select(query: CallbackQuery, state: FSMContext):
    """Обработка выбора платформы"""
    platform = query.data.replace("platform_", "")
    await state.update_data(platform=platform)

    await query.message.edit_text(
        "💡 <b>Умные Шаги #3: Выберите цель продвижения</b>\n\n"
        "Какой результат вы хотите получить?",
        reply_markup=build_goal_keyboard(),
        parse_mode="HTML"
    )

    await state.set_state(SMSGenerationStates.choose_goal)
    await query.answer()


@router.callback_query(SMSGenerationStates.choose_goal, F.data.startswith("goal_"))
async def handle_goal_select(query: CallbackQuery, state: FSMContext):
    """Обработка выбора цели"""
    goal = query.data.replace("goal_", "")
    await state.update_data(goal=goal)

    await query.message.edit_text(
        "📐 <b>Умные Шаги #4: Выберите формат контента</b>\n\n"
        "Какой формат вам подойдет?",
        reply_markup=build_format_keyboard(),
        parse_mode="HTML"
    )

    await state.set_state(SMSGenerationStates.choose_format)
    await query.answer()


@router.callback_query(SMSGenerationStates.choose_format, F.data.startswith("format_"))
async def handle_format_select(query: CallbackQuery, state: FSMContext):
    """Обработка выбора формата и переход к кастомному брифу"""
    format_type = query.data.replace("format_", "")
    await state.update_data(format_type=format_type)

    await query.message.edit_text(
        "✍️ <b>Финальный шаг: Расскажите о себе</b>\n\n"
        "Напишите краткий бриф о вашем бизнесе:\n"
        "- Что вы продаете?\n"
        "- Кто ваша аудитория?\n"
        "- Какие преимущества?\n\n"
        "Примеры помощи:\n"
        "💬 '/example' - посмотреть пример\n"
        "⏭️ '/skip' - пропустить и использовать стандартный",
        parse_mode="HTML"
    )

    await state.set_state(SMSGenerationStates.custom_brief)
    await query.answer()


@router.message(SMSGenerationStates.custom_brief)
async def handle_custom_brief(message: Message, state: FSMContext):
    """Обработка кастомного описания бизнеса"""
    brief = message.text

    if brief.lower() == "/skip":
        brief = "Профессиональный бизнес с современным подходом к продажам и маркетингу"

    await state.update_data(brief=brief)

    # Начало генерации
    await message.answer(
        "⏳ <b>Генерируется ваш SMM-пакет...</b>\n\n"
        "Это может занять 15-30 секунд. Пожалуйста, подождите.",
        parse_mode="HTML"
    )

    await state.set_state(SMSGenerationStates.generating)

    # Получение данных для генерации
    data = await state.get_data()

    try:
        async for db in get_db_session():
            generation_service = GenerationService(db)

            generation_result = await generation_service.generate_smm_package(
                user_id=data['user_id'],
                workspace_id=data['workspace_id'],
                niche=data.get('niche'),
                platform=data.get('platform'),
                goal=data.get('goal'),
                format_type=data.get('format_type'),
                brief=brief,
                language="ru",
                country=data.get('country', 'uz')
            )

            if generation_result.success:
                output_text = generation_result.output_text

                # Форматирование для отправки в Telegram (макс 4096 символов)
                chunks = [output_text[i:i+4000] for i in range(0, len(output_text), 4000)]

                for i, chunk in enumerate(chunks):
                    if i == len(chunks) - 1:
                        await message.answer(
                            chunk,
                            reply_markup=build_smm_result_keyboard(str(generation_result.generation_id)),
                            parse_mode="HTML"
                        )
                    else:
                        await message.answer(chunk, parse_mode="HTML")

                logger.info("smm_package_generated", user_id=data['user_id'])
            else:
                await message.answer(f"❌ Ошибка при генерации: {generation_result.error_message}")
                logger.error("smm_generation_failed", error=generation_result.error_message)

            await state.clear()

    except Exception as e:
        logger.exception("generation_handler_error", error=str(e))
        await message.answer("❌ Ошибка при генерации контента. Попробуйте позже.")
        await state.clear()


@router.callback_query(F.data.startswith("send_whatsapp_"))
async def handle_send_whatsapp(query: CallbackQuery):
    """Отправка контента в WhatsApp"""
    generation_id = query.data.replace("send_whatsapp_", "")
    user_id = query.from_user.id

    async for db in get_db_session():
        user_stmt = select(User).where(User.telegram_id == user_id)
        result = await db.execute(user_stmt)
        user = result.scalar_one_or_none()

        if not user or not user.whatsapp_number:
            await query.answer(
                "⚠️ Сначала укажите номер WhatsApp в настройках",
                show_alert=True
            )
            return

        settings = get_settings()
        whatsapp_service = WhatsAppService(
            api_url=settings.whatsapp_api_url,
            instance_id=settings.whatsapp_instance_id,
            api_token=settings.whatsapp_api_token
        )

        # Получение текста генерации
        gen_stmt = select(Generation).where(Generation.id == uuid.UUID(generation_id))
        result = await db.execute(gen_stmt)
        generation = result.scalar_one_or_none()

        if not generation:
            await query.answer("❌ Генерация не найдена", show_alert=True)
            return

        success = await whatsapp_service.send_message_with_pdf(
            phone=user.whatsapp_number,
            text=generation.output_text,
            pdf_url=generation.pdf_url
        )

        if success:
            generation.whatsapp_sent_status = "sent"
            generation.whatsapp_sent_at = datetime.utcnow()
            await db.commit()

            await query.answer("✅ Контент отправлен в WhatsApp!")
            logger.info("whatsapp_sent_success", user_id=user_id, generation_id=generation_id)
        else:
            await query.answer("❌ Ошибка при отправке в WhatsApp", show_alert=True)
            logger.error("whatsapp_send_failed", user_id=user_id)
