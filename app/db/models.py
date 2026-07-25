# app/db/models.py
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, ForeignKey,
    LargeBinary, JSON, BigInteger, Numeric, Index, UniqueConstraint,
    ForeignKeyConstraint, CheckConstraint, ARRAY
)
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid

Base = declarative_base()

# ============================================================================
# CORE USER & WORKSPACE MODELS
# ============================================================================

class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_telegram_id", "telegram_id"),
        Index("idx_users_country", "country"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(64), nullable=True)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    whatsapp_number = Column(String(32), nullable=True)  # +992 / +998 format
    language = Column(String(8), default="ru")  # ru, tg, uz
    country = Column(String(8), default="uz")  # uz, tj, ru
    timezone = Column(String(64), default="Asia/Tashkent")
    workspace_id = Column(UUID(as_uuid=True), nullable=True)

    # Referral system
    referrer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    referral_code = Column(String(16), unique=True, nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    is_blocked = Column(Boolean, default=False)
    last_seen_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    memberships = relationship("Membership", back_populates="user", cascade="all, delete-orphan")
    generations = relationship("Generation", back_populates="user", cascade="all, delete-orphan")
    usage_events = relationship("UsageEvent", foreign_keys="UsageEvent.user_id", cascade="all, delete-orphan")
    empire_stats = relationship("EmpireUserStats", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Workspace(Base):
    __tablename__ = "workspaces"
    __table_args__ = (
        Index("idx_workspaces_country", "country"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(120), nullable=False)
    slug = Column(String(120), unique=True, nullable=False)
    country = Column(String(8), default="uz")
    timezone = Column(String(64), default="Asia/Tashkent")
    is_active = Column(Boolean, default=True)
    logo_url = Column(String(256), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    memberships = relationship("Membership", back_populates="workspace", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="workspace", cascade="all, delete-orphan")
    generations = relationship("Generation", back_populates="workspace", cascade="all, delete-orphan")
    usage_events = relationship("UsageEvent", back_populates="workspace", cascade="all, delete-orphan")


class Membership(Base):
    __tablename__ = "memberships"
    __table_args__ = (
        UniqueConstraint("user_id", "workspace_id", name="uq_membership_user_workspace"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    role = Column(String(16), default="member")  # owner, admin, member

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="memberships")
    workspace = relationship("Workspace", back_populates="memberships")


# ============================================================================
# BILLING & SUBSCRIPTION MODELS
# ============================================================================

class Subscription(Base):
    __tablename__ = "subscriptions"
    __table_args__ = (
        Index("idx_subscriptions_workspace_id", "workspace_id"),
        Index("idx_subscriptions_plan_code", "plan_code"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    plan_code = Column(String(32), default="free")  # free, starter, pro, team, enterprise
    status = Column(String(16), default="active")  # active, past_due, cancelled, expired

    current_period_start = Column(DateTime, nullable=False)
    current_period_end = Column(DateTime, nullable=True)  # NULL для free/lifetime

    provider = Column(String(32), nullable=True)  # click, payme, alif, manual
    auto_renew = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workspace = relationship("Workspace", back_populates="subscriptions")
    payments = relationship("Payment", back_populates="subscription", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"
    __table_args__ = (
        UniqueConstraint("provider", "provider_event_id", name="uq_payments_provider_event"),
        Index("idx_payments_subscription_id", "subscription_id"),
        Index("idx_payments_status", "status"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String(32), nullable=False)  # click, payme, alif
    provider_event_id = Column(String(128), nullable=True)
    reference = Column(String(64), unique=True, nullable=False)
    plan_code = Column(String(32), nullable=False)

    status = Column(String(16), default="pending")  # pending, paid, failed, refunded
    amount_minor = Column(Integer, nullable=False)  # в копейках/тиынах/дирамах
    currency = Column(String(3), nullable=False)  # UZS, TJS, RUB

    paid_at = Column(DateTime, nullable=True)
    provider_payload = Column(JSONB, default={})

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    subscription = relationship("Subscription", back_populates="payments")


# ============================================================================
# CONTENT GENERATION MODELS
# ============================================================================

class Generation(Base):
    __tablename__ = "generations"
    __table_args__ = (
        Index("idx_generations_workspace_id", "workspace_id"),
        Index("idx_generations_user_id", "user_id"),
        Index("idx_generations_status", "status"),
        Index("idx_generations_created_at", "created_at"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Request metadata
    content_type = Column(String(32), nullable=False)  # reels, posts, stories, content_plan, smm_package
    language = Column(String(8), nullable=False)  # ru, tg, uz
    country = Column(String(8), nullable=False)

    # Input parameters
    brief = Column(Text, nullable=False)
    niche = Column(String(64), nullable=True)
    platform = Column(String(32), nullable=True)  # instagram, telegram, tiktok, youtube
    goal = Column(String(64), nullable=True)  # sales, reach, engagement, personal_brand
    format_type = Column(String(32), nullable=True)  # reel, post, story, plan
    tone = Column(String(32), default="professional")  # professional, casual, funny, formal

    # Output
    status = Column(String(16), default="pending")  # pending, processing, completed, failed
    output_text = Column(Text, nullable=True)
    output_json = Column(JSONB, default={})
    pdf_url = Column(String(256), nullable=True)
    error_message = Column(Text, nullable=True)

    # Custom fields requested by main APIs
    estimated_reach = Column(Integer, default=0)
    tags = Column(JSON, default=[])
    cta_suggestions = Column(JSON, default=[])
    completed_at = Column(DateTime, nullable=True)

    # WhatsApp
    whatsapp_sent_status = Column(String(16), default="not_sent")  # not_sent, pending, sent, failed
    whatsapp_sent_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    workspace = relationship("Workspace", back_populates="generations")
    user = relationship("User", back_populates="generations")
    usage_events = relationship("UsageEvent", foreign_keys="UsageEvent.generation_id")


class UsageEvent(Base):
    __tablename__ = "usage_events"
    __table_args__ = (
        UniqueConstraint("idempotency_key", name="uq_usage_events_idempotency"),
        Index("idx_usage_events_workspace_id", "workspace_id"),
        Index("idx_usage_events_status", "status"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    workspace_id = Column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    generation_id = Column(UUID(as_uuid=True), ForeignKey("generations.id", ondelete="SET NULL"), nullable=True)

    metric = Column(String(32), default="generation")  # generation, export, api_call
    units = Column(Integer, default=1)
    value = Column(Integer, default=1)
    status = Column(String(16), default="reserved")  # reserved, committed, reversed

    idempotency_key = Column(String(128), unique=True, nullable=False)
    description = Column(String(256), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    workspace = relationship("Workspace", back_populates="usage_events")


# ============================================================================
# GAMIFICATION MODELS (TOJIKAI EMPIRE)
# ============================================================================

class EmpireUserStats(Base):
    __tablename__ = "empire_user_stats"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    balance = Column(Numeric(15, 2), default=1000.00)
    xp = Column(Integer, default=0)
    level = Column(Integer, default=1)

    passive_income_per_hour = Column(Numeric(15, 2), default=0.00)
    last_passive_income_at = Column(DateTime, nullable=True)

    referral_count = Column(Integer, default=0)
    referral_tier = Column(String(16), default="Bronze")  # Bronze, Silver, Gold, Platinum

    unlocked_cities = Column(ARRAY(String), default=["Dushanbe"])
    current_city = Column(String(64), default="Dushanbe")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="empire_stats")
    businesses = relationship("EmpireBusiness", back_populates="user_stats", cascade="all, delete-orphan")


class EmpireBusiness(Base):
    __tablename__ = "empire_businesses"
    __table_args__ = (
        Index("idx_empire_businesses_user_id", "user_id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    city = Column(String(64), nullable=False)  # Dushanbe, Khujand, Tashkent, etc.
    business_type = Column(String(64), nullable=False)  # cafe, salon, textile, cargo, etc.
    name = Column(String(120), nullable=False)

    level = Column(Integer, default=1)
    base_income_per_hour = Column(Numeric(15, 2), nullable=False)
    current_income_per_hour = Column(Numeric(15, 2), nullable=False)

    manager_hired = Column(Boolean, default=False)
    marketer_hired = Column(Boolean, default=False)
    team_size = Column(Integer, default=0)

    total_earnings = Column(Numeric(15, 2), default=0.00)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user_stats = relationship("EmpireUserStats", back_populates="businesses")


class EmpireEvent(Base):
    __tablename__ = "empire_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(120), nullable=False)
    description = Column(Text, nullable=False)
    city = Column(String(64), nullable=False)

    impact_type = Column(String(32))  # positive, negative, neutral
    impact_value = Column(Numeric(15, 2))

    options = Column(JSON, default={})  # {"option_1": {"label": "...", "impact": ...}}
    user_choice = Column(String(32), nullable=True)

    is_resolved = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# MARKETPLACE MODELS
# ============================================================================

class MarketplaceProduct(Base):
    __tablename__ = "marketplace_products"
    __table_args__ = (
        Index("idx_marketplace_products_owner_id", "owner_id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    owner_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    product_type = Column(String(32))  # template, consulting, service, ebook

    price = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), default="UZS")

    is_published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    sales_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MarketplaceOrder(Base):
    __tablename__ = "marketplace_orders"
    __table_args__ = (
        Index("idx_marketplace_orders_buyer_id", "buyer_id"),
        Index("idx_marketplace_orders_status", "status"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), ForeignKey("marketplace_products.id"), nullable=False)
    buyer_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    amount = Column(Numeric(15, 2), nullable=False)
    currency = Column(String(3), default="UZS")

    status = Column(String(16), default="completed")  # pending, completed, failed, refunded

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# ADMIN & SYSTEM MODELS
# ============================================================================

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    role = Column(String(32), default="admin")  # admin, super_admin, moderator
    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class PromoCode(Base):
    __tablename__ = "promo_codes"
    __table_args__ = (
        Index("idx_promo_codes_code", "code"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(64), unique=True, nullable=False)

    discount_percent = Column(Integer, nullable=False)
    max_uses = Column(Integer, nullable=True)  # NULL = unlimited
    current_uses = Column(Integer, default=0)

    valid_from = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)

    created_by = Column(UUID(as_uuid=True), ForeignKey("admin_users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("idx_audit_logs_user_id", "user_id"),
        Index("idx_audit_logs_created_at", "created_at"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    admin_id = Column(UUID(as_uuid=True), ForeignKey("admin_users.id", ondelete="SET NULL"), nullable=True)

    action = Column(String(255), nullable=False)
    entity_type = Column(String(64), nullable=False)  # user, payment, generation, etc.
    entity_id = Column(UUID(as_uuid=True), nullable=True)

    details = Column(JSON, default={})
    ip_address = Column(String(45), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"
    __table_args__ = (
        Index("idx_analytics_events_user_id", "user_id"),
        Index("idx_analytics_events_event_name", "event_name"),
        Index("idx_analytics_events_created_at", "created_at"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    event_name = Column(String(128), nullable=False)
    event_data = Column(JSON, default={})

    session_id = Column(String(64), nullable=True)
    device_type = Column(String(32), nullable=True)  # mobile, desktop, web

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
