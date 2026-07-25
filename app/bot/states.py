# app/bot/states.py
from aiogram.fsm.state import State, StatesGroup

class SMSGenerationStates(StatesGroup):
    choose_niche = State()
    choose_platform = State()
    choose_goal = State()
    choose_format = State()
    custom_brief = State()
    generating = State()
    result_ready = State()

class GameStates(StatesGroup):
    viewing_city = State()
    choosing_business = State()
    business_management = State()
    hiring_staff = State()

class ConsultantStates(StatesGroup):
    asking_question = State()
    waiting_response = State()
    viewing_response = State()

class WhatsAppSetupStates(StatesGroup):
    awaiting_phone = State()
    phone_confirmed = State()
