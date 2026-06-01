import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { X, Shield, Lock, Eye, Database, UserCheck, RefreshCw, Trash2 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Privacy = () => {
  const { i18n } = useTranslation();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState(i18n.language);
  
  // ESC tugmasi va overlay click uchun
  React.useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        navigate(-1);
      }
    };
    
    window.addEventListener('keydown', handleEscape);
    return () => window.removeEventListener('keydown', handleEscape);
  }, [navigate]);
  
  const handleOverlayClick = (e) => {
    if (e.target === e.currentTarget) {
      navigate(-1);
    }
  };
  
  const content = {
    uz: {
      title: "Maxfiylik siyosati",
      sections: [
        {
          icon: Database,
          title: "Qaysi ma'lumotlar yig'iladi",
          text: `Faqat foydalanuvchi avtorizatsiyasini va foydalanuvchi bilan aloqani qo'llab-quvvatlash imkoniyatini ta'minlovchi ma'lumotlar yig'iladi.

Foydalanuvchining roziligi bilan platforma foydalanuvchidan quyidagi ma'lumotlarni oladi:
• Telefon raqami

Foydalanuvchilarning ba'zi harakatlari server jurnallarida avtomatik ravishda saqlanadi:
• IP-manzil
• Brauzer turi haqidagi ma'lumotlar
• Qo'shimcha dasturlar
• So'rov vaqti va boshqalar`
        },
        {
          icon: Eye,
          title: "Olingan ma'lumotlardan qanday foydalaniladi",
          text: `Foydalanuvchi tomonidan taqdim etilgan ma'lumotlar foydalanuvchini avtorizatsiya qilish va u bilan aloqa o'rnatish, shu jumladan turli xizmatlarning holatidagi o'zgarishlar haqida xabarnomalar yuborish uchun ishlatiladi.

Shaxsiy ma'lumotlar faqat SSMART TV platformasining sifatli xizmatlarini ta'minlash maqsadida ishlatiladi.`
        },
        {
          icon: UserCheck,
          title: "Shaxsiy ma'lumotlarni boshqarish",
          text: `Foydalanuvchi o'zining shaxsiy ma'lumotlarini istalgan vaqtda ko'rib chiqishi va o'zgartirishi mumkin.

Ma'lumotlarni boshqarish uchun:
• Shaxsiy kabinetga kiring
• Sozlamalar bo'limini oching
• Kerakli o'zgarishlarni kiriting

Yoki bizning qo'llab-quvvatlash xizmatimizga murojaat qiling.`
        },
        {
          icon: Shield,
          title: "Ma'lumotlarni uchinchi shaxslarga taqdim etish",
          text: `Foydalanuvchilarning shaxsiy ma'lumotlari ushbu sayt bilan bog'liq bo'lmagan shaxslarga faqat quyidagi hollarda uzatilishi mumkin:

• Qonun, normativ-huquqiy hujjatlarga rioya qilish, sud qarorini ijro etish uchun zarur bo'lsa
• Firibgarlikni aniqlash yoki oldini olish uchun
• Saytning texnik nosozliklarini bartaraf etish uchun
• Vakolatli davlat organlarining so'roviga asosan ma'lumot taqdim etish uchun

Boshqa hollarda shaxsiy ma'lumotlar uchinchi shaxslarga uzatilmaydi.`
        },
        {
          icon: Lock,
          title: "Ma'lumotlar xavfsizligi",
          text: `SSMART TV platformasi foydalanuvchilar ma'lumotlarini ruxsatsiz kirishdan himoya qilish uchun barcha choralarni ko'radi:

• Saytni boshqarish xizmatlari va tizimlarini muntazam yangilash
• Arxiv nusxalarini shifrlash
• Zararli kodlarning mavjudligini muntazam tekshirish
• Saytni joylashtirish uchun virtual ajratilgan serverdan foydalanish
• Zamonaviy shifrlash usullari (SSL/TLS)
• Kirish huquqlarini nazorat qilish tizimi`
        },
        {
          icon: RefreshCw,
          title: "O'zgarishlar",
          text: `Maxfiylik siyosatiga yangilanishlar ushbu sahifada e'lon qilinadi.

Foydalanuvchilarning qulayligi uchun maxfiylik siyosatining barcha versiyalari arxiv fayllarida saqlanadi.

Muhim o'zgarishlar kiritilganda, ro'yxatdan o'tgan foydalanuvchilarga elektron pochta yoki SMS orqali xabar yuboriladi.`
        },
        {
          icon: Trash2,
          title: "Ma'lumotlarni o'chirish",
          text: `Agar biron-bir sababga ko'ra shaxsiy ma'lumotlaringizni saytimizdan o'chirish kerak bo'lsa, quyidagi yo'llar bilan qo'llab-quvvatlash xizmatiga murojaat qilishingiz mumkin:

📧 Email: info@ssmarttv.uz
📱 Telefon: +998 55 516 2111
💬 Telegram: @ssmarttv_support

Ma'lumotlaringiz 30 kun ichida to'liq o'chiriladi va qayta tiklanmaydi.`
        }
      ],
      footer: `© 2024 SSMART TV LLC. Barcha huquqlar himoyalangan.
Oxirgi yangilanish: ${new Date().toLocaleDateString('uz-UZ')}`
    },
    ru: {
      title: "Политика конфиденциальности",
      sections: [
        {
          icon: Database,
          title: "Какая информация подлежит сбору",
          text: `Сбору подлежат только сведения, обеспечивающие возможность авторизации и поддержки обратной связи с пользователем.

С согласия пользователя платформа получает следующие данные от пользователя:
• Номер телефона

Некоторые действия пользователей автоматически сохраняются в журналах сервера:
• IP-адрес
• Данные о типе браузера
• Надстройки
• Время запроса и т.д.`
        },
        {
          icon: Eye,
          title: "Как используется полученная информация",
          text: `Сведения, предоставленные пользователем, используются для авторизации пользователя и осуществления связи с ним, в том числе для направления уведомлений об изменении статуса тех или иных услуг.

Личные данные используются исключительно для обеспечения качественных услуг платформы SSMART TV.`
        },
        {
          icon: UserCheck,
          title: "Управление личными данными",
          text: `Пользователь может просматривать и изменять свои личные данные в любое время.

Для управления данными:
• Войдите в личный кабинет
• Откройте раздел настроек
• Внесите необходимые изменения

Или свяжитесь с нашей службой поддержки.`
        },
        {
          icon: Shield,
          title: "Предоставление данных третьим лицам",
          text: `Личные данные пользователей могут быть переданы лицам, не связанным с настоящим сайтом, только в следующих случаях:

• Для соблюдения закона, нормативно-правового акта, исполнения решения суда
• Для выявления или воспрепятствования мошенничеству
• Для устранения технических неисправностей в работе сайта
• Для предоставления информации на основании запроса уполномоченных государственных органов

В других случаях личные данные третьим лицам не передаются.`
        },
        {
          icon: Lock,
          title: "Безопасность данных",
          text: `Платформа SSMART TV принимает все меры для защиты данных пользователей от несанкционированного доступа:

• Регулярное обновление служб и систем управления сайтом
• Шифровка архивных копий ресурса
• Регулярные проверки на предмет наличия вредоносных кодов
• Использование для размещения сайта виртуального выделенного сервера
• Современные методы шифрования (SSL/TLS)
• Система контроля прав доступа`
        },
        {
          icon: RefreshCw,
          title: "Изменения",
          text: `Обновления политики конфиденциальности публикуются на данной странице.

Для удобства пользователей все версии политики конфиденциальности подлежат сохранению в архивных файлах.

При внесении существенных изменений зарегистрированным пользователям будет отправлено уведомление по электронной почте или SMS.`
        },
        {
          icon: Trash2,
          title: "Удаление данных",
          text: `Если по какой-либо причине Вам понадобится удалить личные данные с нашего сайта, Вы можете обратиться в нашу службу поддержки:

📧 Email: info@ssmarttv.uz
📱 Телефон: +998 55 516 2111
💬 Telegram: @ssmarttv_support

Ваши данные будут полностью удалены в течение 30 дней и не подлежат восстановлению.`
        }
      ],
      footer: `© 2024 ООО SSMART TV. Все права защищены.
Последнее обновление: ${new Date().toLocaleDateString('ru-RU')}`
    },
    en: {
      title: "Privacy Policy",
      sections: [
        {
          icon: Database,
          title: "What information is collected",
          text: `Only information that enables user authorization and support of user feedback is collected.

With user consent, the platform receives the following data from the user:
• Phone number

Some user actions are automatically saved in server logs:
• IP address
• Browser type data
• Extensions
• Request time, etc.`
        },
        {
          icon: Eye,
          title: "How the received information is used",
          text: `Information provided by the user is used to authorize the user and communicate with them, including sending notifications about changes in the status of various services.

Personal data is used solely to provide quality services of the SSMART TV platform.`
        },
        {
          icon: UserCheck,
          title: "Personal data management",
          text: `Users can view and modify their personal data at any time.

To manage data:
• Log in to your personal account
• Open the settings section
• Make necessary changes

Or contact our support service.`
        },
        {
          icon: Shield,
          title: "Providing data to third parties",
          text: `Users' personal data may be transferred to persons not associated with this site only in the following cases:

• To comply with the law, regulatory act, execution of a court decision
• To detect or prevent fraud
• To eliminate technical malfunctions in the site operation
• To provide information based on a request from authorized government agencies

In other cases, personal data is not transferred to third parties.`
        },
        {
          icon: Lock,
          title: "Data security",
          text: `SSMART TV platform takes all measures to protect user data from unauthorized access:

• Regular updates of site management services and systems
• Encryption of archive copies of the resource
• Regular checks for malicious code
• Use of a virtual dedicated server for hosting the site
• Modern encryption methods (SSL/TLS)
• Access control system`
        },
        {
          icon: RefreshCw,
          title: "Changes",
          text: `Privacy policy updates are published on this page.

For user convenience, all versions of the privacy policy are saved in archive files.

When significant changes are made, registered users will be notified via email or SMS.`
        },
        {
          icon: Trash2,
          title: "Data deletion",
          text: `If for any reason you need to delete your personal data from our site, you can contact our support service:

📧 Email: info@ssmarttv.uz
📱 Phone: +998 55 516 2111
💬 Telegram: @ssmarttv_support

Your data will be completely deleted within 30 days and cannot be restored.`
        }
      ],
      footer: `© 2024 SSMART TV LLC. All rights reserved.
Last updated: ${new Date().toLocaleDateString('en-US')}`
    }
  };
  
  const currentContent = content[activeTab];
  
  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4 overflow-y-auto"
      onClick={handleOverlayClick}
    >
      <div className="bg-dark-card max-w-5xl w-full rounded-xl shadow-2xl my-8">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <div className="flex items-center gap-3">
            <Shield className="text-primary" size={32} />
            <h1 className="text-2xl font-bold text-white">{currentContent.title}</h1>
          </div>
          <button
            onClick={() => navigate(-1)}
            className="text-gray-400 hover:text-white transition-colors p-2 hover:bg-gray-700 rounded-lg"
          >
            <X size={24} />
          </button>
        </div>
        
        {/* Language Tabs */}
        <div className="flex border-b border-gray-700">
          <button
            onClick={() => setActiveTab('uz')}
            className={`flex-1 px-6 py-3 font-medium transition-colors ${
              activeTab === 'uz'
                ? 'bg-primary text-black border-b-2 border-primary'
                : 'text-gray-400 hover:text-white hover:bg-gray-700'
            }`}
          >
            O'zbek
          </button>
          <button
            onClick={() => setActiveTab('ru')}
            className={`flex-1 px-6 py-3 font-medium transition-colors ${
              activeTab === 'ru'
                ? 'bg-primary text-black border-b-2 border-primary'
                : 'text-gray-400 hover:text-white hover:bg-gray-700'
            }`}
          >
            Русский
          </button>
          <button
            onClick={() => setActiveTab('en')}
            className={`flex-1 px-6 py-3 font-medium transition-colors ${
              activeTab === 'en'
                ? 'bg-primary text-black border-b-2 border-primary'
                : 'text-gray-400 hover:text-white hover:bg-gray-700'
            }`}
          >
            English
          </button>
        </div>
        
        {/* Content */}
        <div className="p-6 max-h-[600px] overflow-y-auto">
          <div className="space-y-8">
            {currentContent.sections.map((section, index) => {
              const IconComponent = section.icon;
              return (
                <div key={index} className="bg-dark-lighter rounded-lg p-6 hover:bg-opacity-80 transition-all">
                  <div className="flex items-start gap-4">
                    <div className="bg-primary bg-opacity-20 p-3 rounded-lg flex-shrink-0">
                      <IconComponent className="text-primary" size={24} />
                    </div>
                    <div className="flex-1">
                      <h2 className="text-xl font-bold text-white mb-3">
                        {section.title}
                      </h2>
                      <p className="text-gray-300 whitespace-pre-line leading-relaxed">
                        {section.text}
                      </p>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
          
          {/* Footer Text */}
          <div className="mt-8 p-4 bg-dark-lighter rounded-lg border border-gray-700">
            <p className="text-gray-400 text-sm text-center whitespace-pre-line">
              {currentContent.footer}
            </p>
          </div>
        </div>
        
        {/* Footer Buttons */}
        <div className="p-6 border-t border-gray-700 flex justify-end gap-4">
          <button
            onClick={() => navigate(-1)}
            className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
          >
            {activeTab === 'uz' ? 'Yopish' : activeTab === 'ru' ? 'Закрыть' : 'Close'}
          </button>
          <button
            onClick={() => {
              alert(activeTab === 'uz' ? 'Maxfiylik siyosati o\'qildi' : activeTab === 'ru' ? 'Политика конфиденциальности прочитана' : 'Privacy policy read');
              navigate(-1);
            }}
            className="btn-primary px-6 py-3"
          >
            {activeTab === 'uz' ? 'Tushundim' : activeTab === 'ru' ? 'Понятно' : 'Understood'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Privacy;
