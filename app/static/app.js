// app/static/app.js
class TojikaiApp {
    constructor() {
        this.tg = window.Telegram.WebApp;
        this.tg.ready();
        this.tg.expand();

        this.state = {
            currentStep: 1,
            niche: null,
            platform: null,
            goal: null,
            format: null,
            brief: null,
            generationId: null,
            plan: 'free',
            remaining: 5,
            userId: "00000000-0000-0000-0000-000000000000" // Simulated or set from initData
        };

        this.initializeEventListeners();
        this.loadUserData();
    }

    initializeEventListeners() {
        // Main buttons
        document.getElementById('btnStartGeneration').addEventListener('click', () => this.startWizard());
        document.getElementById('btnEmpireGame').addEventListener('click', () => this.openGame());
        document.getElementById('btnAIConsultant').addEventListener('click', () => this.openConsultant());
        document.getElementById('btnSettings').addEventListener('click', () => this.openSettings());
        document.getElementById('btnUpgrade').addEventListener('click', () => this.openPayment());

        // Wizard navigation
        document.getElementById('btnNext').addEventListener('click', () => this.nextStep());
        document.getElementById('btnBack').addEventListener('click', () => this.prevStep());

        // Result actions
        document.getElementById('btnDownloadPDF').addEventListener('click', () => this.downloadPDF());
        document.getElementById('btnSendWhatsApp').addEventListener('click', () => this.sendToWhatsApp());
        document.getElementById('btnCreateNew').addEventListener('click', () => this.startWizard());

        // Niche selection
        document.addEventListener('click', (e) => {
            const nicheBtn = e.target.closest('.niche-btn');
            if (nicheBtn) {
                this.selectNiche(nicheBtn.dataset.value);
            }
            if (e.target.classList.contains('platform-btn')) {
                this.selectPlatform(e.target.dataset.value);
            }
            if (e.target.classList.contains('goal-btn')) {
                this.selectGoal(e.target.dataset.value);
            }
            if (e.target.classList.contains('format-btn')) {
                this.selectFormat(e.target.dataset.value);
            }
        });
    }

    async loadUserData() {
        try {
            // Simulated or fetch from real endpoint
            const response = await fetch(`/api/user/profile?user_id=${this.state.userId}`, {
                headers: {
                    'X-Telegram-Init-Data': this.tg.initData
                }
            });
            const data = await response.json();

            this.state.plan = data.plan;
            this.state.remaining = data.remaining_generations;

            this.updateSubscriptionStatus();
        } catch (error) {
            console.error('Failed to load user data:', error);
        }
    }

    updateSubscriptionStatus() {
        document.getElementById('planName').textContent = this.state.plan.toUpperCase();
        document.getElementById('remaining').textContent = this.state.remaining;
    }

    startWizard() {
        document.getElementById('welcomeScreen').classList.add('hidden');
        document.getElementById('generationWizard').classList.remove('hidden');
        this.populateNiches();
        this.showStep(1);
    }

    populateNiches() {
        const niches = {
            uz: {
                cafe: { label: '☕ Кафе / Чайхана', emoji: '☕' },
                textile: { label: '👕 Текстиль / Одежда', emoji: '👕' },
                real_estate: { label: '🏢 Недвижимость', emoji: '🏢' },
                auto: { label: '🚗 Авто / Сервис', emoji: '🚗' }
            },
            tj: {
                wholesale: { label: '📊 Саводои Яклухт', emoji: '📊' },
                cargo: { label: '📮 Карго', emoji: '📮' },
                construction: { label: '🏗 Сохтмон', emoji: '🏗' },
                cafe: { label: '☕ Курутобхона', emoji: '☕' }
            }
        };

        const country = this.tg.initDataUnsafe.user?.language_code === 'tj' ? 'tj' : 'uz';
        const nicheContainer = document.getElementById('nicheOptions');
        nicheContainer.innerHTML = '';

        for (const [key, value] of Object.entries(niches[country])) {
            const btn = document.createElement('button');
            btn.className = 'niche-btn p-3 border-2 border-gray-300 rounded-lg hover:border-blue-600 text-center transition';
            btn.dataset.value = key;
            btn.innerHTML = `<div class="text-2xl">${value.emoji}</div><div class="text-sm">${value.label}</div>`;
            nicheContainer.appendChild(btn);
        }
    }

    selectNiche(niche) {
        this.state.niche = niche;
        document.querySelectorAll('.niche-btn').forEach(btn => {
            btn.classList.toggle('border-blue-600', btn.dataset.value === niche);
        });
    }

    selectPlatform(platform) {
        this.state.platform = platform;
        document.querySelectorAll('.platform-btn').forEach(btn => {
            btn.classList.toggle('border-blue-600', btn.dataset.value === platform);
        });
    }

    selectGoal(goal) {
        this.state.goal = goal;
        document.querySelectorAll('.goal-btn').forEach(btn => {
            btn.classList.toggle('border-blue-600', btn.dataset.value === goal);
        });
    }

    selectFormat(format) {
        this.state.format = format;
        document.querySelectorAll('.format-btn').forEach(btn => {
            btn.classList.toggle('border-blue-600', btn.dataset.value === format);
        });
    }

    nextStep() {
        // Validation
        if (this.state.currentStep === 1 && !this.state.niche) {
            alert('Пожалуйста, выберите нишу');
            return;
        }
        if (this.state.currentStep === 2 && !this.state.platform) {
            alert('Пожалуйста, выберите платформу');
            return;
        }
        if (this.state.currentStep === 3 && !this.state.goal) {
            alert('Пожалуйста, выберите цель');
            return;
        }
        if (this.state.currentStep === 4 && !this.state.format) {
            alert('Пожалуйста, выберите формат');
            return;
        }

        if (this.state.currentStep < 4) {
            this.showStep(this.state.currentStep + 1);
        } else {
            this.askForBrief();
        }
    }

    prevStep() {
        if (this.state.currentStep > 1) {
            this.showStep(this.state.currentStep - 1);
        } else {
            document.getElementById('generationWizard').classList.add('hidden');
            document.getElementById('welcomeScreen').classList.remove('hidden');
        }
    }

    showStep(step) {
        // Hide all steps
        for (let i = 1; i <= 4; i++) {
            document.getElementById(`step${i}`).classList.add('hidden');
        }

        // Show current step
        document.getElementById(`step${step}`).classList.remove('hidden');

        // Update indicator
        document.querySelectorAll('#stepIndicator .step').forEach((el, i) => {
            el.classList.toggle('bg-blue-600', i < step);
            el.classList.toggle('bg-gray-300', i >= step);
        });

        this.state.currentStep = step;
    }

    askForBrief() {
        const brief = prompt('Расскажите о вашем бизнесе (или оставьте пусто для использования стандартного текста)');

        if (brief !== null) {
            this.state.brief = brief || 'Профессиональный бизнес с современным подходом к продажам';
            this.generateContent();
        }
    }

    async generateContent() {
        // Show loading
        document.getElementById('generationWizard').classList.add('hidden');
        document.getElementById('loadingState').classList.remove('hidden');

        try {
            const response = await fetch(`/api/generations/create?user_id=${this.state.userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Telegram-Init-Data': this.tg.initData
                },
                body: JSON.stringify({
                    niche: this.state.niche,
                    platform: this.state.platform,
                    goal: this.state.goal,
                    format_type: this.state.format,
                    brief: this.state.brief
                })
            });

            const data = await response.json();

            if (response.ok && data.success) {
                this.state.generationId = data.generation_id;
                this.displayResult(data.output_text, data.pdf_url);
            } else {
                alert('Ошибка при генерации: ' + (data.detail || data.error || 'Unknown error'));
                this.backToWelcome();
            }
        } catch (error) {
            console.error('Generation error:', error);
            alert('Ошибка при генерации контента');
            this.backToWelcome();
        }
    }

    displayResult(content, pdfUrl) {
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('resultScreen').classList.remove('hidden');

        // Format content for display
        const formatted = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>');

        document.getElementById('resultContent').innerHTML = `<p>${formatted}</p>`;

        // Store PDF URL for download
        this.pdfUrl = `${pdfUrl}?user_id=${this.state.userId}`;
    }

    downloadPDF() {
        if (this.pdfUrl) {
            window.open(this.pdfUrl, '_blank');
        }
    }

    async sendToWhatsApp() {
        const phone = prompt('Введите номер WhatsApp (+992... или +998...)');

        if (phone) {
            try {
                const response = await fetch(`/api/whatsapp/send?user_id=${this.state.userId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Telegram-Init-Data': this.tg.initData
                    },
                    body: JSON.stringify({
                        generation_id: this.state.generationId,
                        phone: phone
                    })
                });

                const data = await response.json();

                if (response.ok && data.success) {
                    alert('✅ Контент отправлен в WhatsApp!');
                } else {
                    alert('❌ Ошибка при отправке: ' + (data.detail || data.error));
                }
            } catch (error) {
                console.error('WhatsApp send error:', error);
                alert('Ошибка при отправке в WhatsApp');
            }
        }
    }

    openGame() {
        alert('🎮 Раздел TojikAI Empire скоро будет доступен');
    }

    openConsultant() {
        alert('🤖 AI Консультант скоро будет доступен');
    }

    openSettings() {
        alert('⚙️ Настройки скоро будут доступны');
    }

    openPayment() {
        // Open payment link
        window.open(`/api/payments/create-link?plan=pro&user_id=${this.state.userId}`, '_blank');
    }

    backToWelcome() {
        document.getElementById('loadingState').classList.add('hidden');
        document.getElementById('generationWizard').classList.add('hidden');
        document.getElementById('resultScreen').classList.add('hidden');
        document.getElementById('welcomeScreen').classList.remove('hidden');
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new TojikaiApp();
});
