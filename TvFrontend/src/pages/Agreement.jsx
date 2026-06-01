import React, { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { X } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Agreement = () => {
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
      title: "Foydalanuvchi shartnomasi",
      sections: [
        {
          title: "1. UMUMIY QOIDALAR",
          text: `1.1. Ushbu Foydalanuvchi shartnomasi (keyingi o'rinlarda «Shartnoma») SSMART TV platformasi (keyingi o'rinlarda «Platforma») tomonidan taqdim etiladigan xizmatlarga taalluqlidir.

1.2. Platformadan foydalanish orqali, siz ushbu Shartnomaning barcha shartlariga to'liq va so'zsiz rozilik bildirasiz.

1.3. Agar siz Shartnoma shartlari bilan rozi bo'lmasangiz, Platformadan foydalanishni to'xtatishingiz lozim.`
        },
        {
          title: "2. KOMPANIYA MA'LUMOTLARI",
          text: `2.1. Yuridik shaxs nomi: SSMART TV LLC
2.2. Yuridik manzil: Toshkent shahri, Yunusobod tumani, Abdulla Qodiriy ko'chasi, 42-uy
2.3. STIR: 123456789
2.4. Hisob raqam: 20208000123456789012
2.5. Bank: Milliy Bank, Toshkent filiali
2.6. MFO: 00401
2.7. Tel: +998 55 516 2111
2.8. Email: info@ssmarttv.uz`
        },
        {
          title: "3. XIZMATLAR",
          text: `3.1. Platforma quyidagi xizmatlarni taqdim etadi:
   - Televideniye kanallarini onlayn tomosha qilish
   - Filmlar va seriallarni onlayn tomosha qilish
   - Bolalar uchun xavfsiz kontent
   - Shaxsiy tavsiyalar va playlistlar

3.2. Xizmatlar ro'yxati va funksionalligi Platforma tomonidan istalgan vaqtda o'zgartirilishi mumkin.`
        },
        {
          title: "4. FOYDALANUVCHI MAJBURIYATLARI",
          text: `4.1. Foydalanuvchi o'z hisob ma'lumotlarining maxfiyligini ta'minlashi shart.

4.2. Platformadan foydalanishda qonuniy maqsadlarda foydalanish zarur.

4.3. Kontentni noqonuniy nusxalash yoki tarqatish qat'iyan man etiladi.

4.4. Platformaning normal ishlashiga xalaqit beruvchi harakatlar taqiqlanadi.`
        },
        {
          title: "5. INTELLEKTUAL MULK HUQUQLARI",
          text: `5.1. Platformada taqdim etilgan barcha kontent (videolar, rasmlar, matnlar, logotiplar va boshqalar) mualliflik huquqi bilan himoyalangan.

5.2. Kontentdan shaxsiy foydalanish uchun ruxsat beriladi, ammo tijorat maqsadlarida foydalanish man etiladi.

5.3. Platformaning dizayni, kodi va funksionalligi SSMART TV LLC ga tegishli bo'lib, nusxalab olish taqiqlanadi.`
        },
        {
          title: "6. MAXFIYLIK",
          text: `6.1. Foydalanuvchi ma'lumotlari Maxfiylik siyosatiga muvofiq qayta ishlanadi.

6.2. Shaxsiy ma'lumotlar uchinchi shaxslarga foydalanuvchining roziligisiz uzatilmaydi.

6.3. Texnik ma'lumotlar (cookies, jurnal fayllari) xizmat sifatini yaxshilash uchun to'planishi mumkin.`
        },
        {
          title: "7. TO'LOV VA QAYTARISH",
          text: `7.1. Obuna to'lovlari Platformada ko'rsatilgan narxlarda amalga oshiriladi.

7.2. To'lovlar kredit karta, elektron hamyon yoki boshqa mavjud usullar orqali amalga oshirilishi mumkin.

7.3. Qaytarish faqat Platformaning texnik nosozligi tufayli xizmat ko'rsatilmagan hollarda amalga oshiriladi.

7.4. Qaytarish so'rovlari 14 kun ichida ko'rib chiqiladi.`
        },
        {
          title: "8. MAS'ULIYAT CHEKLOVI",
          text: `8.1. Platforma xizmatlarning uzluksiz va xatosiz ishlashiga kafolat bermaydi.

8.2. SSMART TV LLC foydalanuvchining Platformadan foydalanishi natijasida yuzaga kelgan har qanday zarar uchun javobgar emas.

8.3. Internet aloqasining uzilishi yoki uchinchi tomon xizmatlarining ishlamay qolishi uchun mas'uliyat yuklanmaydi.`
        },
        {
          title: "9. SHARTNOMANI BEKOR QILISH",
          text: `9.1. Foydalanuvchi istalgan vaqtda o'z hisobini o'chirib, Shartnomani bekor qilishi mumkin.

9.2. SSMART TV LLC Shartnoma shartlarining buzilishi holida foydalanuvchi hisobini bloklash huquqiga ega.

9.3. Shartnoma bekor qilinganda, to'langan obuna haqqi qaytarilmaydi.`
        },
        {
          title: "10. O'ZGARTIRISHLAR",
          text: `10.1. SSMART TV LLC ushbu Shartnomaga istalgan vaqtda o'zgartirishlar kiritish huquqiga ega.

10.2. O'zgarishlar Platformada e'lon qilingan kundan boshlab kuchga kiradi.

10.3. O'zgarishlardan keyin Platformadan foydalanishni davom ettirish yangi shartlarni qabul qilish hisoblanadi.`
        },
        {
          title: "11. NIZOLARNI HAL ETISH",
          text: `11.1. Ushbu Shartnoma O'zbekiston Respublikasi qonunchiligiga muvofiq tartibga solinadi.

11.2. Nizolar muzokaralar yo'li bilan hal qilinishga harakat qilinadi.

11.3. Kelishuv bo'lmagan taqdirda, nizolar O'zbekiston Respublikasi sudlarida hal etiladi.`
        },
        {
          title: "12. BOG'LANISH MA'LUMOTLARI",
          text: `Savollar yoki murojaatlar uchun biz bilan bog'laning:

Email: info@ssmarttv.uz
Telefon: +998 55 516 2111
Telegram: @ssmarttv_support
Manzil: Toshkent shahri, Yunusobod tumani, Abdulla Qodiriy ko'chasi, 42-uy

Ish vaqti: Dushanba-Juma, 9:00-18:00 (Toshkent vaqti)`
        }
      ]
    },
    ru: {
      title: "Пользовательское соглашение",
      sections: [
        {
          title: "1. ОБЩИЕ ПОЛОЖЕНИЯ",
          text: `1.1. Настоящее Пользовательское соглашение (далее «Соглашение») регулирует использование услуг платформы SSMART TV (далее «Платформа»).

1.2. Используя Платформу, вы полностью и безоговорочно принимаете все условия настоящего Соглашения.

1.3. Если вы не согласны с условиями Соглашения, вы обязаны прекратить использование Платформы.`
        },
        {
          title: "2. РЕКВИЗИТЫ КОМПАНИИ",
          text: `2.1. Юридическое наименование: ООО SSMART TV
2.2. Юридический адрес: г. Ташкент, Юнусабадский район, ул. Абдуллы Кадыри, д. 42
2.3. ИНН: 123456789
2.4. Расчетный счет: 20208000123456789012
2.5. Банк: Национальный Банк, Ташкентский филиал
2.6. МФО: 00401
2.7. Тел: +998 55 516 2111
2.8. Email: info@ssmarttv.uz`
        },
        {
          title: "3. УСЛУГИ",
          text: `3.1. Платформа предоставляет следующие услуги:
   - Онлайн просмотр телевизионных каналов
   - Онлайн просмотр фильмов и сериалов
   - Безопасный контент для детей
   - Персональные рекомендации и плейлисты

3.2. Перечень услуг и функциональность могут быть изменены Платформой в любое время.`
        },
        {
          title: "4. ОБЯЗАННОСТИ ПОЛЬЗОВАТЕЛЯ",
          text: `4.1. Пользователь обязан обеспечить конфиденциальность своих учетных данных.

4.2. Использование Платформы должно осуществляться в законных целях.

4.3. Незаконное копирование или распространение контента строго запрещено.

4.4. Запрещены действия, препятствующие нормальной работе Платформы.`
        },
        {
          title: "5. ПРАВА ИНТЕЛЛЕКТУАЛЬНОЙ СОБСТВЕННОСТИ",
          text: `5.1. Весь контент, представленный на Платформе (видео, изображения, тексты, логотипы и др.), защищен авторским правом.

5.2. Разрешается личное использование контента, коммерческое использование запрещено.

5.3. Дизайн, код и функциональность Платформы принадлежат ООО SSMART TV и не могут быть скопированы.`
        },
        {
          title: "6. КОНФИДЕНЦИАЛЬНОСТЬ",
          text: `6.1. Данные пользователей обрабатываются в соответствии с Политикой конфиденциальности.

6.2. Персональные данные не передаются третьим лицам без согласия пользователя.

6.3. Технические данные (cookies, лог-файлы) могут собираться для улучшения качества сервиса.`
        },
        {
          title: "7. ОПЛАТА И ВОЗВРАТ",
          text: `7.1. Оплата подписки осуществляется по ценам, указанным на Платформе.

7.2. Оплата может производиться банковской картой, электронным кошельком или другими доступными способами.

7.3. Возврат средств осуществляется только в случае технической неисправности Платформы, препятствующей предоставлению услуг.

7.4. Запросы на возврат рассматриваются в течение 14 дней.`
        },
        {
          title: "8. ОГРАНИЧЕНИЕ ОТВЕТСТВЕННОСТИ",
          text: `8.1. Платформа не гарантирует непрерывную и безошибочную работу услуг.

8.2. ООО SSMART TV не несет ответственности за любой ущерб, возникший в результате использования Платформы.

8.3. Ответственность за перебои в интернет-соединении или сбои в работе сторонних сервисов не несется.`
        },
        {
          title: "9. РАСТОРЖЕНИЕ СОГЛАШЕНИЯ",
          text: `9.1. Пользователь может в любое время удалить свою учетную запись и расторгнуть Соглашение.

9.2. ООО SSMART TV имеет право заблокировать учетную запись пользователя при нарушении условий Соглашения.

9.3. При расторжении Соглашения оплаченная подписка не возвращается.`
        },
        {
          title: "10. ИЗМЕНЕНИЯ",
          text: `10.1. ООО SSMART TV имеет право вносить изменения в настоящее Соглашение в любое время.

10.2. Изменения вступают в силу с момента их публикации на Платформе.

10.3. Продолжение использования Платформы после внесения изменений считается принятием новых условий.`
        },
        {
          title: "11. РАЗРЕШЕНИЕ СПОРОВ",
          text: `11.1. Настоящее Соглашение регулируется законодательством Республики Узбекистан.

11.2. Споры разрешаются путем переговоров.

11.3. При отсутствии соглашения споры разрешаются в судах Республики Узбекистан.`
        },
        {
          title: "12. КОНТАКТНАЯ ИНФОРМАЦИЯ",
          text: `Для вопросов или обращений свяжитесь с нами:

Email: info@ssmarttv.uz
Телефон: +998 55 516 2111
Telegram: @ssmarttv_support
Адрес: г. Ташкент, Юнусабадский район, ул. Абдуллы Кадыри, д. 42

Часы работы: Понедельник-Пятница, 9:00-18:00 (время Ташкента)`
        }
      ]
    },
    en: {
      title: "User Agreement",
      sections: [
        {
          title: "1. GENERAL PROVISIONS",
          text: `1.1. This User Agreement (hereinafter "Agreement") governs the use of services provided by SSMART TV platform (hereinafter "Platform").

1.2. By using the Platform, you fully and unconditionally accept all terms of this Agreement.

1.3. If you do not agree with the terms of the Agreement, you must stop using the Platform.`
        },
        {
          title: "2. COMPANY DETAILS",
          text: `2.1. Legal name: SSMART TV LLC
2.2. Legal address: Tashkent city, Yunusabad district, Abdulla Qadiri street, building 42
2.3. Tax ID: 123456789
2.4. Account number: 20208000123456789012
2.5. Bank: National Bank, Tashkent branch
2.6. BIC: 00401
2.7. Phone: +998 55 516 2111
2.8. Email: info@ssmarttv.uz`
        },
        {
          title: "3. SERVICES",
          text: `3.1. The Platform provides the following services:
   - Online viewing of TV channels
   - Online viewing of movies and series
   - Safe content for children
   - Personal recommendations and playlists

3.2. The list of services and functionality may be changed by the Platform at any time.`
        },
        {
          title: "4. USER OBLIGATIONS",
          text: `4.1. The user must ensure the confidentiality of their account information.

4.2. The Platform must be used for lawful purposes.

4.3. Illegal copying or distribution of content is strictly prohibited.

4.4. Actions that interfere with the normal operation of the Platform are prohibited.`
        },
        {
          title: "5. INTELLECTUAL PROPERTY RIGHTS",
          text: `5.1. All content presented on the Platform (videos, images, texts, logos, etc.) is protected by copyright.

5.2. Personal use of content is permitted, commercial use is prohibited.

5.3. The design, code and functionality of the Platform belong to SSMART TV LLC and may not be copied.`
        },
        {
          title: "6. PRIVACY",
          text: `6.1. User data is processed in accordance with the Privacy Policy.

6.2. Personal data is not transferred to third parties without user consent.

6.3. Technical data (cookies, log files) may be collected to improve service quality.`
        },
        {
          title: "7. PAYMENT AND REFUND",
          text: `7.1. Subscription payment is made at the prices indicated on the Platform.

7.2. Payment can be made by credit card, e-wallet or other available methods.

7.3. Refunds are made only in case of technical malfunction of the Platform preventing service delivery.

7.4. Refund requests are processed within 14 days.`
        },
        {
          title: "8. LIMITATION OF LIABILITY",
          text: `8.1. The Platform does not guarantee uninterrupted and error-free operation of services.

8.2. SSMART TV LLC is not liable for any damage resulting from the use of the Platform.

8.3. No liability is assumed for internet connection interruptions or third-party service failures.`
        },
        {
          title: "9. TERMINATION OF AGREEMENT",
          text: `9.1. The user may delete their account and terminate the Agreement at any time.

9.2. SSMART TV LLC has the right to block a user's account in case of violation of the Agreement terms.

9.3. Upon termination of the Agreement, paid subscription is not refunded.`
        },
        {
          title: "10. AMENDMENTS",
          text: `10.1. SSMART TV LLC has the right to make changes to this Agreement at any time.

10.2. Changes take effect from the moment of their publication on the Platform.

10.3. Continued use of the Platform after changes is considered acceptance of new terms.`
        },
        {
          title: "11. DISPUTE RESOLUTION",
          text: `11.1. This Agreement is governed by the laws of the Republic of Uzbekistan.

11.2. Disputes are resolved through negotiations.

11.3. In the absence of an agreement, disputes are resolved in the courts of the Republic of Uzbekistan.`
        },
        {
          title: "12. CONTACT INFORMATION",
          text: `For questions or inquiries, contact us:

Email: info@ssmarttv.uz
Phone: +998 55 516 2111
Telegram: @ssmarttv_support
Address: Tashkent city, Yunusabad district, Abdulla Qadiri street, building 42

Working hours: Monday-Friday, 9:00-18:00 (Tashkent time)`
        }
      ]
    }
  };
  
  const currentContent = content[activeTab];
  
  return (
    <div 
      className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4 overflow-y-auto"
      onClick={(e) => {
        // Faqat overlay bosilganda yopiladi, modal ichki qismi bosilganda emas
        if (e.target === e.currentTarget) {
          navigate(-1);
        }
      }}
    >
      <div className="bg-dark-card max-w-4xl w-full rounded-xl shadow-2xl my-8">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-700">
          <h1 className="text-2xl font-bold text-white">{currentContent.title}</h1>
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
          {currentContent.sections.map((section, index) => (
            <div key={index} className="mb-8">
              <h2 className="text-xl font-bold text-primary mb-3">
                {section.title}
              </h2>
              <p className="text-gray-300 whitespace-pre-line leading-relaxed">
                {section.text}
              </p>
            </div>
          ))}
        </div>
        
        {/* Footer */}
        <div className="p-6 border-t border-gray-700 flex justify-end gap-4">
          <button
            onClick={() => navigate(-1)}
            className="px-6 py-3 bg-gray-700 hover:bg-gray-600 text-white rounded-lg font-medium transition-colors"
          >
            {activeTab === 'uz' ? 'Yopish' : activeTab === 'ru' ? 'Закрыть' : 'Close'}
          </button>
          <button
            onClick={() => {
              alert(activeTab === 'uz' ? 'Shartnoma qabul qilindi' : activeTab === 'ru' ? 'Соглашение принято' : 'Agreement accepted');
              navigate(-1);
            }}
            className="btn-primary px-6 py-3"
          >
            {activeTab === 'uz' ? 'Qabul qilish' : activeTab === 'ru' ? 'Принять' : 'Accept'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Agreement;
