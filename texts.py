"""Bot matnlari: o'zbek, rus, ingliz tillarida.

Kontent landing page'dan olingan. Yangi til qo'shish uchun T va CASES ga
yangi kalit (masalan "es") qo'shing va LANGS ro'yxatiga yozing.
Caption'lar HTML formatda (Telegram parse_mode=HTML).
"""

LANGS = ["uz", "ru", "en"]
LANG_NAMES = {"uz": "🇺🇿 O'zbekcha", "ru": "🇷🇺 Русский", "en": "🇬🇧 English"}

# Odamlar: [lotin (uz), kirill (ru), ingliz (en)]
PEOPLE = {
    "AB": ["Abror Baxtiyarovich", "Аброр Бахтиярович", "Abror Bakhtiyarovich"],
    "RS": ["Rixsitilla Shermuxammedov", "Рихситилла Шермухаммедов", "Rikhsitilla Shermukhammedov"],
    "AI": ["Alisher Isayev", "Алишер Исаев", "Alisher Isaev"],
    "JB": ["Jasur Buriyev", "Жасур Буриев", "Jasur Buriev"],
    "KZ": ["Kamoliddin Ziyovutdinov", "Камолиддин Зиёвутдинов", "Kamoliddin Ziyovutdinov"],
    "SK": ["Sarvar va Komil", "Сарвар и Комил", "Sarvar & Komil"],
    "HA": ["Husan Aliyev", "Хусан Алиев", "Husan Aliev"],
    "HN": ["Habibullo Nabiyev", "Хабибулло Набиев", "Habibullo Nabiev"],
    "BG": ["Bogdan", "Богдан", "Bogdan"],
    "BK": ["Baxtiyor", "Бахтиёр", "Bakhtiyor"],
    "SS": ["Sarvar Sobirov", "Сарвар Собиров", "Sarvar Sobirov"],
    "IL": ["Ilya", "Илья", "Ilya"],
}
PEOPLE_IDX = {"uz": 0, "ru": 1, "en": 2}

CASES = [
    {
        "client": "Sales Doctor Academy", "exec": "Meet Up",
        "scope": ["c", "s", "pre", "prod", "post"],
        "credits": [("r_dir", ["AB"]), ("r_prod", ["AB"]), ("r_dop", ["RS"]), ("r_amb", ["AI"])],
        "t": {
            "uz": ("Sales Doctor Academy nima bilan shug'ullanishini tushuntirish.",
                   "Biznes qanchalik og'ir ahvolda bo'lmasin, uni qutqarish mumkin — Sales Doctor Academy shunda yordamga keladi."),
            "ru": ("Объяснить, чем занимается Sales Doctor Academy.",
                   "Как бы тяжело ни было бизнесу, его можно спасти, и Sales Doctor Academy приходит на помощь."),
            "en": ("Explain what Sales Doctor Academy does.",
                   "No matter how bad things get for a business, it can be saved, and Sales Doctor Academy is there to help."),
        },
    },
    {
        "client": "Grand Capital", "exec": "Bek Shox",
        "scope": ["c", "s", "preS", "prodS", "postS"],
        "credits": [("r_dir", ["JB"]), ("r_prod", ["AB"]), ("r_dop", ["KZ"]), ("r_ambs", ["SK"])],
        "t": {
            "uz": ("Sarvar va Komil ishtirokida Grand Capital uylarining afzalliklarini ko'rsatuvchi axborot rolik.",
                   "Sarvar va Komil didiga mos uy topa olmaydi. Taqdimotdan so'ng ularga Grand Capital qurgan uylar yoqib qoladi."),
            "ru": ("Информационный ролик с Сарваром и Комилом о преимуществах домов Grand Capital.",
                   "Сарвар и Комил не могут найти дом по вкусу. После презентации им нравятся дома, построенные Grand Capital."),
            "en": ("An information film, starring Sarvar and Komil, showing the advantages of Grand Capital homes.",
                   "Sarvar and Komil can't find a home to their taste. After a presentation, they fall for the homes built by Grand Capital."),
        },
    },
    {
        "client": "Yuksalish Choy", "exec": "AB Media",
        "scope": ["c", "s", "pre", "prod", "post"],
        "credits": [("r_dir", ["AB"]), ("r_prod", ["AB"]), ("r_dop", ["HA"])],
        "t": {
            "uz": ("Bozorga yangi kirayotgan brend. Uni nima ajratib turishini topib, rolikni shu atrofida qurish.",
                   "Yuksalish choyidan tushgan daromadning bir qismi o'qiyotgan muhtoj yoshlarga yo'naltiriladi. Har bir piyola ichgan odam kimningdir o'qishiga homiy bo'ladi."),
            "ru": ("Новый бренд на рынке. Найти, чем он выделяется, и снять ролик с акцентом на этом.",
                   "Часть дохода от чая Yuksalish идёт нуждающейся учащейся молодёжи. Покупая этот чай, люди становятся спонсорами их учёбы."),
            "en": ("A new brand entering the market. Find what sets it apart and build a film around it.",
                   "Part of the revenue from Yuksalish tea goes to young people in need who are studying. Every cup makes the drinker a sponsor of someone's education."),
        },
    },
    {
        "client": "IMZO", "exec": "Khabi Media",
        "scope": ["pre", "prodS", "postS"],
        "credits": [("r_dir", ["HN"]), ("r_prod", ["AB"]), ("r_dop", ["SS"])],
        "t": {
            "uz": ("Imzo romlari ishlab chiqarilishi endi Samarqand, Farg'ona va boshqa shaharlarda yo'lga qo'yilganini yetkazish.",
                   "Avval eshik romi uchun Toshkentga borib, kunlab kutish kerak edi, buzilsa — yana o'sha yo'l. Endi Imzo sizning shahringizda, kutish shart emas."),
            "ru": ("Сообщить, что производство рам Imzo налажено в Самарканде, Фергане и других городах.",
                   "Раньше за дверными рамами ехали в Ташкент и ждали несколько дней, а при поломке всё повторялось. Теперь Imzo в вашем городе, и ждать не нужно."),
            "en": ("Tell people that Imzo frame production is now running in Samarkand, Fergana and other cities.",
                   "Ordering door frames used to mean going to Tashkent and waiting days, then doing it again for any repair. Now Imzo is in your city, and there is no need to wait."),
        },
    },
    {
        "client": "Uztelecom", "exec": "Khabi Media",
        "scope": ["preS", "prodS", "postS"],
        "credits": [("r_dir", ["HN", "BG"]), ("r_prod", ["AB", "BK"]), ("r_dop", ["SS", "IL"])],
        "t": {
            "uz": ("Uztelecom 5 yilda nimalarga erishganini kreativ ko'rsatish.",
                   "Avval va hozir — Uztelecom mijozlarining o'z tilidan: internet foydalanuvchilarining hayoti qanday o'zgardi."),
            "ru": ("Креативно показать, что Uztelecom сделал за 5 лет.",
                   "Пять лет назад и сейчас глазами клиентов Uztelecom: как изменилась жизнь интернет-пользователей."),
            "en": ("Show, creatively, what Uztelecom has achieved over five years.",
                   "Then and now, told through Uztelecom's own customers: how life changed for internet users."),
        },
    },
]

# Mijoz yo'lining qaysi bosqichlari Abrorning fokusi (0 = Tanilish, 2 = Ishonch)
FOCUS = [0, 2]

# Test: (bosqich, savol). "a" = Tanilish, "t" = Ishonch. Javob: 2 / 1 / 0 ball.
QUIZ_AXES = ["a", "t", "a", "t", "a", "t"]

T = {
    # ═════════════════════════════ O'ZBEKCHA ═════════════════════════════
    "uz": {
        "name": "Abror Baxtiyarovich",
        "name_lines": ("Abror", "Baxtiyarovich"),
        "role": "Prodyuser va rejissyor · AB Media",
        "slate": ("Prodakshn", "Rulon", "Sahna", "Dubl"),

        "choose_lang": "🎬 <b>Tilni tanlang</b>\nВыберите язык · Choose a language",

        "home": (
            "🎬 <b>Abror Baxtiyarovich</b>\n"
            "<i>Prodyuser va rejissyor · AB Media</i>\n\n"
            "Odamlar o'zlari <b>taniydigan</b> va <b>ishonadigan</b> brendlardan sotib oladi. "
            "Abror ikkalasini ham ekranda quradi.\n\n"
            "Bo'limni tanlang 👇"
        ),
        "b_about": "👤 Abror haqida",
        "b_works": "🎞 Ishlar",
        "b_services": "🛠 Xizmatlar",
        "b_journey": "🧭 Mijoz yo'li",
        "b_process": "🎬 Ish jarayoni",
        "b_quiz": "🧪 Brend diagnostikasi",
        "b_lead": "📝 Ariza qoldirish",
        "b_lang": "🌐 Til",
        "b_site": "🌍 Sayt",
        "b_home": "🏠 Menyu",
        "b_back": "↩️ Orqaga",
        "b_want": "📝 Shunday film xohlayman",

        "about_kicker": "Sahnada",
        "about_head": "Tanilish va ishonch — ekranda",
        "chip_a": "TANILISH",
        "chip_t": "ISHONCH",
        "about": (
            "👤 <b>Abror Baxtiyarovich</b>\n"
            "Prodyuser va rejissyor, <b>AB Media</b> asoschisi.\n\n"
            "Abror yirik kompaniyalarga mijoz yo'lining reklamani o'zi bilan sotib olib bo'lmaydigan "
            "ikki bosqichida g'olib chiqishga yordam beradi: <b>tanilish</b> va <b>ishonch qozonish</b>.\n\n"
            "🎯 <b>Fokus:</b> Tanilish va Ishonch bosqichlari\n"
            "🎬 <b>Format:</b> g'oya va ssenariydan tayyor filmgacha — yoki boshqa jamoa suratga olayotganda prodyuserlik nazorati\n"
            "🏢 <b>Mijozlar:</b> Sales Doctor Academy, Grand Capital, Yuksalish Choy, IMZO, Uztelecom\n\n"
            "<i>«Har bir loyiha mijozning vazifasidan boshlanadi va unga javob beradigan film bilan tugaydi.»</i>"
        ),
        "b_links": "🔗 Ijtimoiy tarmoqlar",

        "works_intro": "🎞 <b>Tanlangan ishlar</b>",
        "l_exec": "Ijrochi",
        "l_task": "Vazifa",
        "l_concept": "Konsepsiya",
        "l_scope": "Abror qismi",
        "l_team": "Titrlar",
        "r_dir": "Rejissyor",
        "r_prod": "Prodyuser",
        "r_dop": "Bosh operator",
        "r_amb": "Ambassador",
        "r_ambs": "Ambassadorlar",
        "sc": {"c": "Konsepsiya", "s": "Ssenariy", "pre": "Pre-prodakshn", "prod": "Prodakshn",
               "post": "Post-prodakshn", "preS": "Pre-prodakshn nazorati",
               "prodS": "Prodakshn nazorati", "postS": "Post-prodakshn nazorati"},

        "svc_kicker": "Ish formatlari",
        "svc": (
            "🛠 <b>Nima qiladi</b>\n\n"
            "🅰️ <b>AB Media bilan to'liq sikl</b>\n"
            "Loyihani birinchi g'oyadan yakuniy faylgacha olib boradi.\n"
            "<i>Konsepsiya · Ssenariy · Pre-prodakshn · Prodakshn · Post-prodakshn</i>\n\n"
            "🅱️ <b>Prodyuserlik nazorati</b>\n"
            "Sizning agentligingiz yoki studiyangiz suratga olayotganda Abror prodakshnni boshqaradi: "
            "tayyorgarlik, maydonchadagi nazorat va post-prodakshn nazorati.\n"
            "<i>Pre-prodakshn · Prodakshn · Post-prodakshn nazorati</i>"
        ),
        "svc_a": "To'liq sikl",
        "svc_a_items": "Konsepsiya · Ssenariy · Pre · Prodakshn · Post",
        "svc_b": "Prodyuserlik nazorati",
        "svc_b_items": "Tayyorgarlik · Maydonchada nazorat · Post nazorati",
        "b_svc_a": "🅰️ To'liq sikl kerak",
        "b_svc_b": "🅱️ Nazorat kerak",

        "j_title": "Mijoz yo'li",
        "j_focus": "Fokus",
        "st": [("Tanilish", "Siz borligingizni bilishadi"),
               ("Qiziqish", "Ko'proq bilishni xohlashadi"),
               ("Ishonch", "Sizga ishonishadi"),
               ("Tanlov", "Sizni tanlashadi"),
               ("Sodiqlik", "Qaytib kelishadi")],
        "j_intro": (
            "🧭 <b>Mijoz yo'lining qayerida ishlaydi</b>\n\n"
            "Har bir xarid shu bosqichlardan o'tadi. Abror brendlar odamlarni eng ko'p "
            "yo'qotadigan ikkitasini quradi: <b>Tanilish</b> va <b>Ishonch</b>.\n\n"
            "Obyektivni bosqichdan bosqichga burang 👇"
        ),
        "j_mine": "🎯 <b>Abrorning fokusi.</b>",
        "j_stage_notes": [
            "Brendni bitta yorqin g'oya atrofida ko'rsatadigan film odamlar xotirasida qoladi.",
            "Tanilgan brendga qiziqish o'z-o'zidan keladi — agar g'oya aniq bo'lsa.",
            "Haqiqiy odamlar va natijalar gapiradigan film reklama so'zlaridan kuchliroq ishontiradi.",
            "Taniydigan va ishonadigan brendni tanlash — oson qaror.",
            "Ishonch saqlansa, mijoz qaytib keladi va boshqalarni olib keladi.",
        ],

        "p_title": "Ish qanday boradi",
        "steps": [("Konsepsiya", "Brendni ajratib turadigan yagona g'oyani topamiz."),
                  ("Ssenariy", "Uni haqiqiy odamlar ishtirokidagi hikoyaga aylantiramiz."),
                  ("Pre-prodakshn", "Kasting, lokatsiyalar, jadval, jamoa."),
                  ("Prodakshn", "Suratga olish."),
                  ("Post-prodakshn", "Montaj, rang, ovoz, topshirish.")],
        "p_cap": "🎬 <b>Ish jarayoni</b> · {i}/{n}\n\n<b>{h}</b>\n{p}\n\n<code>{bar}</code>",

        "q_label": "Brend diagnostikasi",
        "q_intro": (
            "🧪 <b>Brend diagnostikasi</b>\n\n"
            "6 ta savol — 1 daqiqa. Brendingiz mijoz yo'lining ikki muhim bosqichida qanday "
            "holatda ekanini ko'rsatamiz: <b>Tanilish</b> va <b>Ishonch</b>.\n\n"
            "Halol javob bering — natija faqat sizga ko'rinadi."
        ),
        "b_q_start": "🎬 Boshladik!",
        "q": [
            "Ideal mijozingiz sohangizdagi brendlarni sanab bersa, sizni birinchi uchtalikda tilga oladimi?",
            "Mijozlar narxni so'rashdan oldin sizning natijalaringizni — keyslar, sharhlar, raqamlarni ko'ra oladimi?",
            "Brendingizni bitta jumlada, raqobatchilardan farqi bilan tushuntirib bera olasizmi?",
            "Kontentingizda haqiqiy mijozlar va xodimlar o'z ovozi bilan gapiradimi?",
            "So'nggi 3 oyda brendingiz haqidagi video yangi auditoriyaga yetib bordimi?",
            "Yangi mijozlar ko'pincha tavsiya orqali, uzoq ikkilanmasdan keladimi?",
        ],
        "q_ans": ("✅ Ha", "🤏 Qisman", "❌ Yo'q"),
        "q_cap": "🧪 <b>Dubl {i}/{n}</b>\n\n{q}",
        "r_a": "Tanilish",
        "r_t": "Ishonch",
        "r_kicker": "Diagnostika natijasi",
        "r": {
            "strong": ("Kadr tayyor",
                       "Brendingizni bilishadi va ishonishadi — bu kuchli asos. Endi uni kattaroq ekranga olib chiqish vaqti: "
                       "yangi auditoriya va yangi bozorlar uchun film."),
            "both": ("Ikkala bosqich ham bo'sh",
                     "Hozircha brendingizni yetarlicha bilishmaydi va ishonch ham shakllanmagan. "
                     "Yaxshi xabar: bitta to'g'ri g'oya atrofida qurilgan film ikkala bosqichni birga yopadi."),
            "aw": ("Sizni bilishmaydi",
                   "Sizga ishonishadi, lekin sizni yetarlicha bilishmaydi. Kerakli narsa — brendni bitta yorqin, "
                   "esda qoladigan g'oya atrofida ko'rsatadigan film."),
            "tr": ("Bilishadi, lekin ishonishmaydi",
                   "Sizni bilishadi, lekin hali ishonishmaydi. Kerakli narsa — haqiqiy odamlar va natijalar "
                   "o'zi gapiradigan film."),
        },
        "r_cap": "🧪 <b>{title}</b>\n\n🔦 Tanilish: <b>{a}%</b>\n🤝 Ishonch: <b>{t}%</b>\n\n{text}\n\n"
                 "Natijani Abror bilan muhokama qilishni xohlaysizmi?",
        "b_q_lead": "📝 Natijani Abror bilan muhokama qilish",
        "b_q_again": "🔁 Qayta o'tish",

        "lead_kicker": "Sahna 06 · Dubl 01",
        "lead_big": "Brendingiz haqida gaplashamiz",
        "lead_sub": "Ism, telefon va email — Abror o'zi bog'lanadi.",
        "lead_intro": "📝 <b>Ariza</b>\n\nIsm, telefon va email qoldiring — Abror vazifangizni muhokama qilish uchun o'zi bog'lanadi.\n\n"
                      "<b>1/3.</b> Ismingiz nima?",
        "ask_phone": "<b>2/3.</b> Telefon raqamingiz?\nPastdagi tugmani bosing yoki raqamni yozing.",
        "b_share_phone": "📱 Raqamni yuborish",
        "ask_email": "<b>3/3.</b> Email manzilingiz?",
        "b_skip": "⏭ O'tkazib yuborish",
        "b_cancel": "✖️ Bekor qilish",
        "e_name": "Ismingizni yozing (kamida 2 harf).",
        "e_phone": "Raqamni tekshiring — kamida 7 ta raqam bo'lsin.",
        "e_email": "Email manzilini tekshiring, masalan: name@company.com",
        "lead_cancel": "Ariza bekor qilindi.",
        "done_big": "Snyat! Ariza qabul qilindi",
        "done_sub": "Abror telefon yoki email orqali bog'lanadi.",
        "done": "🎬 <b>Snyat!</b>\n\nRahmat, {n}. Arizangiz qabul qilindi — Abror siz bilan telefon yoki email orqali bog'lanadi.",
        "lead_exists": "Sizning arizangiz allaqachon bor ✅ Abror tez orada bog'lanadi. Yangi ariza yuborishni xohlaysizmi?",
        "b_new_lead": "📝 Yangi ariza",

        "unknown": "Menyudan bo'limni tanlang 👇",
        "cmd": {"start": "Bosh menyu", "about": "Abror haqida", "works": "Ishlar",
                "quiz": "Brend diagnostikasi", "contact": "Ariza qoldirish", "lang": "Tilni o'zgartirish"},
        "bot_short": "Abror Baxtiyarovich — prodyuser va rejissyor, AB Media. Brendlar uchun tanilish va ishonch quradigan filmlar.",
        "bot_desc": "🎬 Abror Baxtiyarovich — prodyuser va rejissyor (AB Media).\n\nBu yerda: Abror haqida, ishlar, xizmatlar, "
                    "ish jarayoni, 1 daqiqalik brend diagnostikasi va ariza qoldirish.\n\nBoshlash uchun «Start»ni bosing.",
    },

    # ═════════════════════════════ РУССКИЙ ═════════════════════════════
    "ru": {
        "name": "Аброр Бахтиярович",
        "name_lines": ("Аброр", "Бахтиярович"),
        "role": "Продюсер и режиссёр · AB Media",
        "slate": ("Продакшн", "Ролл", "Сцена", "Дубль"),

        "choose_lang": "🎬 <b>Выберите язык</b>\nTilni tanlang · Choose a language",

        "home": (
            "🎬 <b>Аброр Бахтиярович</b>\n"
            "<i>Продюсер и режиссёр · AB Media</i>\n\n"
            "Люди покупают у брендов, которые они <b>узнают</b> и которым <b>доверяют</b>. "
            "Аброр строит и то и другое на экране.\n\n"
            "Выберите раздел 👇"
        ),
        "b_about": "👤 Об Аброре",
        "b_works": "🎞 Работы",
        "b_services": "🛠 Услуги",
        "b_journey": "🧭 Путь клиента",
        "b_process": "🎬 Как идёт работа",
        "b_quiz": "🧪 Диагностика бренда",
        "b_lead": "📝 Оставить заявку",
        "b_lang": "🌐 Язык",
        "b_site": "🌍 Сайт",
        "b_home": "🏠 Меню",
        "b_back": "↩️ Назад",
        "b_want": "📝 Хочу такой фильм",

        "about_kicker": "На сцене",
        "about_head": "Узнаваемость и доверие — на экране",
        "chip_a": "УЗНАВАЕМОСТЬ",
        "chip_t": "ДОВЕРИЕ",
        "about": (
            "👤 <b>Аброр Бахтиярович</b>\n"
            "Продюсер и режиссёр, основатель <b>AB Media</b>.\n\n"
            "Аброр помогает крупным компаниям выиграть два этапа пути клиента, которые нельзя купить одной рекламой: "
            "<b>узнаваемость</b> и <b>доверие</b>.\n\n"
            "🎯 <b>Фокус:</b> этапы «Узнаваемость» и «Доверие»\n"
            "🎬 <b>Формат:</b> от идеи и сценария до готового фильма — или продюсерский контроль, когда снимает ваша команда\n"
            "🏢 <b>Клиенты:</b> Sales Doctor Academy, Grand Capital, Yuksalish Choy, IMZO, Uztelecom\n\n"
            "<i>«Каждый проект начинается с задачи клиента и заканчивается фильмом, который на неё отвечает.»</i>"
        ),
        "b_links": "🔗 Соцсети",

        "works_intro": "🎞 <b>Избранные работы</b>",
        "l_exec": "Исполнитель",
        "l_task": "Задача",
        "l_concept": "Концепция",
        "l_scope": "Роль Аброра",
        "l_team": "Титры",
        "r_dir": "Режиссёр",
        "r_prod": "Продюсер",
        "r_dop": "Оператор-постановщик",
        "r_amb": "Амбассадор",
        "r_ambs": "Амбассадоры",
        "sc": {"c": "Концепция", "s": "Сценарий", "pre": "Препродакшн", "prod": "Продакшн",
               "post": "Постпродакшн", "preS": "Контроль препродакшна",
               "prodS": "Контроль продакшна", "postS": "Контроль постпродакшна"},

        "svc_kicker": "Форматы работы",
        "svc": (
            "🛠 <b>Что делает Аброр</b>\n\n"
            "🅰️ <b>Полный цикл с AB Media</b>\n"
            "Ведёт проект от первой идеи до финального файла.\n"
            "<i>Концепция · Сценарий · Препродакшн · Продакшн · Постпродакшн</i>\n\n"
            "🅱️ <b>Продюсерский контроль</b>\n"
            "Когда снимает ваше агентство или студия, Аброр управляет продакшном: "
            "подготовка, контроль на площадке и контроль постпродакшна.\n"
            "<i>Контроль препродакшна · продакшна · постпродакшна</i>"
        ),
        "svc_a": "Полный цикл",
        "svc_a_items": "Концепция · Сценарий · Пре · Продакшн · Пост",
        "svc_b": "Продюсерский контроль",
        "svc_b_items": "Подготовка · Контроль на площадке · Пост",
        "b_svc_a": "🅰️ Нужен полный цикл",
        "b_svc_b": "🅱️ Нужен контроль",

        "j_title": "Путь клиента",
        "j_focus": "Фокус",
        "st": [("Узнаваемость", "Знают, что вы есть"),
               ("Интерес", "Хотят узнать больше"),
               ("Доверие", "Верят вам"),
               ("Выбор", "Выбирают вас"),
               ("Лояльность", "Возвращаются")],
        "j_intro": (
            "🧭 <b>Где Аброр работает на пути клиента</b>\n\n"
            "Каждая покупка проходит эти этапы. Аброр строит два, на которых бренды чаще всего теряют людей: "
            "<b>Узнаваемость</b> и <b>Доверие</b>.\n\n"
            "Поверните объектив от этапа к этапу 👇"
        ),
        "j_mine": "🎯 <b>Фокус Аброра.</b>",
        "j_stage_notes": [
            "Фильм, построенный вокруг одной яркой идеи, остаётся в памяти людей.",
            "Интерес к узнаваемому бренду приходит сам — если идея ясна.",
            "Фильм, где говорят реальные люди и результаты, убеждает сильнее рекламных слов.",
            "Выбрать бренд, который знаешь и которому веришь, — лёгкое решение.",
            "Если доверие сохраняется, клиент возвращается и приводит других.",
        ],

        "p_title": "Как идёт работа",
        "steps": [("Концепция", "Находим одну идею, которая выделяет бренд."),
                  ("Сценарий", "Превращаем её в историю с реальными людьми."),
                  ("Препродакшн", "Кастинг, локации, график, команда."),
                  ("Продакшн", "Съёмка."),
                  ("Постпродакшн", "Монтаж, цвет, звук, сдача.")],
        "p_cap": "🎬 <b>Как идёт работа</b> · {i}/{n}\n\n<b>{h}</b>\n{p}\n\n<code>{bar}</code>",

        "q_label": "Диагностика бренда",
        "q_intro": (
            "🧪 <b>Диагностика бренда</b>\n\n"
            "6 вопросов — 1 минута. Покажем, в каком состоянии ваш бренд на двух ключевых этапах пути клиента: "
            "<b>Узнаваемость</b> и <b>Доверие</b>.\n\n"
            "Отвечайте честно — результат видите только вы."
        ),
        "b_q_start": "🎬 Мотор!",
        "q": [
            "Если ваш идеальный клиент перечислит бренды в вашей нише, назовёт ли он вас в первой тройке?",
            "Видят ли клиенты ваши результаты — кейсы, отзывы, цифры — ещё до того, как спросят цену?",
            "Можете ли вы объяснить свой бренд одной фразой, с отличием от конкурентов?",
            "Говорят ли в вашем контенте реальные клиенты и сотрудники своими словами?",
            "Доходило ли видео о вашем бренде до новой аудитории за последние 3 месяца?",
            "Приходят ли новые клиенты чаще по рекомендации, без долгих сомнений?",
        ],
        "q_ans": ("✅ Да", "🤏 Частично", "❌ Нет"),
        "q_cap": "🧪 <b>Дубль {i}/{n}</b>\n\n{q}",
        "r_a": "Узнаваемость",
        "r_t": "Доверие",
        "r_kicker": "Результат диагностики",
        "r": {
            "strong": ("Кадр готов",
                       "Ваш бренд знают и ему доверяют — это сильная база. Пора выводить его на экран побольше: "
                       "фильм для новой аудитории и новых рынков."),
            "both": ("Оба этапа пусты",
                     "Пока ваш бренд знают мало, и доверие ещё не сложилось. Хорошая новость: фильм, построенный "
                     "вокруг одной верной идеи, закрывает оба этапа сразу."),
            "aw": ("Вас мало знают",
                   "Вам доверяют, но вас недостаточно знают. Нужен фильм, который покажет бренд вокруг одной яркой, "
                   "запоминающейся идеи."),
            "tr": ("Знают, но не доверяют",
                   "Вас знают, но пока не доверяют. Нужен фильм, где за вас говорят реальные люди и результаты."),
        },
        "r_cap": "🧪 <b>{title}</b>\n\n🔦 Узнаваемость: <b>{a}%</b>\n🤝 Доверие: <b>{t}%</b>\n\n{text}\n\n"
                 "Хотите обсудить результат с Аброром?",
        "b_q_lead": "📝 Обсудить результат с Аброром",
        "b_q_again": "🔁 Пройти заново",

        "lead_kicker": "Сцена 06 · Дубль 01",
        "lead_big": "Поговорим о вашем бренде",
        "lead_sub": "Имя, телефон и email — Аброр свяжется сам.",
        "lead_intro": "📝 <b>Заявка</b>\n\nОставьте имя, телефон и email — Аброр свяжется с вами, чтобы обсудить задачу.\n\n"
                      "<b>1/3.</b> Как вас зовут?",
        "ask_phone": "<b>2/3.</b> Ваш номер телефона?\nНажмите кнопку ниже или напишите номер.",
        "b_share_phone": "📱 Отправить номер",
        "ask_email": "<b>3/3.</b> Ваш email?",
        "b_skip": "⏭ Пропустить",
        "b_cancel": "✖️ Отмена",
        "e_name": "Напишите имя (минимум 2 буквы).",
        "e_phone": "Проверьте номер — нужно минимум 7 цифр.",
        "e_email": "Проверьте email, например: name@company.com",
        "lead_cancel": "Заявка отменена.",
        "done_big": "Снято! Заявка получена",
        "done_sub": "Аброр свяжется по телефону или email.",
        "done": "🎬 <b>Снято!</b>\n\nСпасибо, {n}. Заявка получена — Аброр свяжется с вами по телефону или email.",
        "lead_exists": "Ваша заявка уже у нас ✅ Аброр скоро свяжется. Отправить новую заявку?",
        "b_new_lead": "📝 Новая заявка",

        "unknown": "Выберите раздел в меню 👇",
        "cmd": {"start": "Главное меню", "about": "Об Аброре", "works": "Работы",
                "quiz": "Диагностика бренда", "contact": "Оставить заявку", "lang": "Сменить язык"},
        "bot_short": "Аброр Бахтиярович — продюсер и режиссёр, AB Media. Фильмы, которые строят узнаваемость и доверие к бренду.",
        "bot_desc": "🎬 Аброр Бахтиярович — продюсер и режиссёр (AB Media).\n\nЗдесь: об Аброре, работы, услуги, "
                    "процесс, диагностика бренда за 1 минуту и заявка.\n\nНажмите «Старт», чтобы начать.",
    },

    # ═════════════════════════════ ENGLISH ═════════════════════════════
    "en": {
        "name": "Abror Bakhtiyarovich",
        "name_lines": ("Abror", "Bakhtiyarovich"),
        "role": "Producer & director · AB Media",
        "slate": ("Production", "Roll", "Scene", "Take"),

        "choose_lang": "🎬 <b>Choose a language</b>\nTilni tanlang · Выберите язык",

        "home": (
            "🎬 <b>Abror Bakhtiyarovich</b>\n"
            "<i>Producer & director · AB Media</i>\n\n"
            "People buy from brands they <b>recognise</b> and <b>trust</b>. "
            "Abror builds both on screen.\n\n"
            "Pick a section 👇"
        ),
        "b_about": "👤 About Abror",
        "b_works": "🎞 Work",
        "b_services": "🛠 Services",
        "b_journey": "🧭 Customer journey",
        "b_process": "🎬 How it works",
        "b_quiz": "🧪 Brand check",
        "b_lead": "📝 Request a call",
        "b_lang": "🌐 Language",
        "b_site": "🌍 Website",
        "b_home": "🏠 Menu",
        "b_back": "↩️ Back",
        "b_want": "📝 I want a film like this",

        "about_kicker": "On stage",
        "about_head": "Awareness and trust, built on screen",
        "chip_a": "AWARENESS",
        "chip_t": "TRUST",
        "about": (
            "👤 <b>Abror Bakhtiyarovich</b>\n"
            "Producer and director, founder of <b>AB Media</b>.\n\n"
            "Abror helps large companies win the two stages of the customer journey that ads alone can't buy: "
            "<b>being known</b> and <b>being believed</b>.\n\n"
            "🎯 <b>Focus:</b> the Awareness and Trust stages\n"
            "🎬 <b>Format:</b> from concept and script to the finished film, or producer oversight when your own team is shooting\n"
            "🏢 <b>Clients:</b> Sales Doctor Academy, Grand Capital, Yuksalish Choy, IMZO, Uztelecom\n\n"
            "<i>“Each project starts with a task from the client and ends with a film that answers it.”</i>"
        ),
        "b_links": "🔗 Social",

        "works_intro": "🎞 <b>Selected work</b>",
        "l_exec": "Executor",
        "l_task": "Task",
        "l_concept": "Concept",
        "l_scope": "Abror's part",
        "l_team": "Credits",
        "r_dir": "Director",
        "r_prod": "Producer",
        "r_dop": "Director of photography",
        "r_amb": "Ambassador",
        "r_ambs": "Ambassadors",
        "sc": {"c": "Concept", "s": "Script", "pre": "Pre-production", "prod": "Production",
               "post": "Post-production", "preS": "Pre-production supervision",
               "prodS": "Production supervision", "postS": "Post-production supervision"},

        "svc_kicker": "Ways to work",
        "svc": (
            "🛠 <b>What Abror does</b>\n\n"
            "🅰️ <b>Full cycle with AB Media</b>\n"
            "Takes the project from the first idea to the final file.\n"
            "<i>Concept · Script · Pre-production · Production · Post-production</i>\n\n"
            "🅱️ <b>Producer oversight</b>\n"
            "When your agency or studio is shooting, Abror runs the production: "
            "preparation, on-set supervision and post-production control.\n"
            "<i>Pre-production · Production · Post-production supervision</i>"
        ),
        "svc_a": "Full cycle",
        "svc_a_items": "Concept · Script · Pre · Production · Post",
        "svc_b": "Producer oversight",
        "svc_b_items": "Preparation · On-set supervision · Post control",
        "b_svc_a": "🅰️ I need full cycle",
        "b_svc_b": "🅱️ I need oversight",

        "j_title": "Customer journey",
        "j_focus": "Focus",
        "st": [("Awareness", "They know you exist"),
               ("Interest", "They want to know more"),
               ("Trust", "They believe you"),
               ("Choice", "They pick you"),
               ("Loyalty", "They come back")],
        "j_intro": (
            "🧭 <b>Where Abror works in the customer journey</b>\n\n"
            "Every purchase passes through these stages. Abror builds the two where brands most often lose people: "
            "<b>Awareness</b> and <b>Trust</b>.\n\n"
            "Turn the lens from stage to stage 👇"
        ),
        "j_mine": "🎯 <b>Abror's focus.</b>",
        "j_stage_notes": [
            "A film built around one clear idea is the one people remember.",
            "Interest follows a known brand on its own, as long as the idea is clear.",
            "A film where real people and real results do the talking convinces better than ad copy.",
            "Choosing a brand you know and believe is an easy decision.",
            "Keep the trust, and customers come back and bring others.",
        ],

        "p_title": "How the work goes",
        "steps": [("Concept", "We find the one idea that sets the brand apart."),
                  ("Script", "We turn it into a story with real people."),
                  ("Pre-production", "Casting, locations, schedule, crew."),
                  ("Production", "The shoot."),
                  ("Post-production", "Edit, colour, sound, delivery.")],
        "p_cap": "🎬 <b>How the work goes</b> · {i}/{n}\n\n<b>{h}</b>\n{p}\n\n<code>{bar}</code>",

        "q_label": "Brand check",
        "q_intro": (
            "🧪 <b>Brand check</b>\n\n"
            "6 questions, 1 minute. See where your brand stands on the two stages that matter most: "
            "<b>Awareness</b> and <b>Trust</b>.\n\n"
            "Answer honestly — only you see the result."
        ),
        "b_q_start": "🎬 Action!",
        "q": [
            "If your ideal customer listed the brands in your field, would you make their top three?",
            "Can customers see your results — cases, reviews, numbers — before they ask for a price?",
            "Can you explain your brand in one sentence, including how it differs from competitors?",
            "Do real customers and employees speak in their own words in your content?",
            "Has a video about your brand reached a new audience in the last 3 months?",
            "Do new customers mostly come through referrals, without long hesitation?",
        ],
        "q_ans": ("✅ Yes", "🤏 Partly", "❌ No"),
        "q_cap": "🧪 <b>Take {i}/{n}</b>\n\n{q}",
        "r_a": "Awareness",
        "r_t": "Trust",
        "r_kicker": "Brand check result",
        "r": {
            "strong": ("That's a take",
                       "People know your brand and believe it — a strong base. Time to take it to a bigger screen: "
                       "a film for new audiences and new markets."),
            "both": ("Both stages are empty",
                     "Right now few people know your brand and trust hasn't formed yet. The good news: a film built "
                     "around one right idea closes both stages at once."),
            "aw": ("They don't know you yet",
                   "People trust you, but not enough of them know you. What's missing is a film that shows the brand "
                   "around one bright, memorable idea."),
            "tr": ("Known, not yet trusted",
                   "People know you, but don't believe you yet. What's missing is a film where real people and "
                   "real results do the talking."),
        },
        "r_cap": "🧪 <b>{title}</b>\n\n🔦 Awareness: <b>{a}%</b>\n🤝 Trust: <b>{t}%</b>\n\n{text}\n\n"
                 "Want to go through the result with Abror?",
        "b_q_lead": "📝 Discuss the result with Abror",
        "b_q_again": "🔁 Take it again",

        "lead_kicker": "Scene 06 · Take 01",
        "lead_big": "Let's talk about your brand",
        "lead_sub": "Name, phone and email — Abror will reach out himself.",
        "lead_intro": "📝 <b>Request</b>\n\nLeave your name, phone and email. Abror will get in touch to discuss your task.\n\n"
                      "<b>1/3.</b> What's your name?",
        "ask_phone": "<b>2/3.</b> Your phone number?\nTap the button below or type the number.",
        "b_share_phone": "📱 Share my number",
        "ask_email": "<b>3/3.</b> Your email?",
        "b_skip": "⏭ Skip",
        "b_cancel": "✖️ Cancel",
        "e_name": "Enter your name (at least 2 letters).",
        "e_phone": "Check the number — at least 7 digits.",
        "e_email": "Check the email address, e.g. name@company.com",
        "lead_cancel": "Request cancelled.",
        "done_big": "Cut! Request received",
        "done_sub": "Abror will contact you by phone or email.",
        "done": "🎬 <b>Cut!</b>\n\nThank you, {n}. Your request is in — Abror will contact you by phone or email.",
        "lead_exists": "We already have your request ✅ Abror will be in touch soon. Send a new one?",
        "b_new_lead": "📝 New request",

        "unknown": "Pick a section from the menu 👇",
        "cmd": {"start": "Main menu", "about": "About Abror", "works": "Work",
                "quiz": "Brand check", "contact": "Request a call", "lang": "Change language"},
        "bot_short": "Abror Bakhtiyarovich — producer & director, AB Media. Brand films that build awareness and trust.",
        "bot_desc": "🎬 Abror Bakhtiyarovich — producer & director (AB Media).\n\nInside: about Abror, selected work, services, "
                    "process, a 1-minute brand check and a request form.\n\nTap “Start” to begin.",
    },
}


def t(lang: str, key: str):
    return T.get(lang, T["uz"]).get(key, T["uz"][key])


def people(ids: list[str], lang: str) -> str:
    i = PEOPLE_IDX.get(lang, 0)
    return ", ".join(PEOPLE[x][i] for x in ids)
