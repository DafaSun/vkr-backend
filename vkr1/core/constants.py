FLOORS_LIST = [
    ("1floor", "1 этаж"),
    ("2floor", "2 этаж"),
]

BUILDINGS_LIST = [
    ("4building", "4 корпус"),
    ("5building", "5 корпус"),
    ("6building", "6 корпус"),
]

CATEGORIES_LIST = [
    ("1cat", "1 - Двухкомнатный номер на 1 этаже в 4 корпусе с удобствами в номере"),
    ("2cat", "2 - Двухместный номер на 1 этаже в 4 корпусе с удобствами в блоке"),
    ("3cat", "3 - Двухместный номер на 1 этаже в 4 корпусе с удобствами в номере"),
    ("4cat", "4 - Одноместный номер на 1 этаже в 4 корпусе с удобствами в номере"),
    ("5cat", "5 - Двухместный номер на 2 этаже в 4 корпусе с удобствами в блоке"),
    ("6cat", "6 - Двухместный номер на 1 этаже в 6 корпусе с удобствами в номере"),
    ("7cat", "7 - Двухместный номер на 2 этаже в 6 корпусе с удобствами в номере"),
]

ROOM_TYPES_LIST = [
    ("in_room", "Удобства в номере"),
    ("in_block", "Удобства в блоке"),
]

TOUR_TYPES_LIST = [
    ("social", "Социальная путевка по контракту (льгота)"),
    ("usual", "Обычная путевка за свои деньги"),
    ("therapy", "Только лечение"),
    ("hotel", "Только проживание"),
]

BOOKING_STATUSES_LIST = [
    ("free", "Свободно"),
    ("book", "Забронировано"),
    ("prepay", "Внесена предоплата"),
    ("fullpay", "Полностью оплачен"),
    ("occupied", "Заселен"),
]

GENDER_PERSON_LIST = [
    ("male", "Мужской"),
    ("female", "Женский"),
]

GENDER_ROOM_LIST = [
    ("male", "Мужской"),
    ("female", "Женский"),
    ("undefined", "Не указан"),
]

SPECIALITY_LIST = [
    ("nurse", "nurse"),
    ("doctor", "doctor"),
]

HEPATITIS_LIST = [
    ("not", "Не болел"),
    ("a_hep", "Гепатит A"),
    ("b_hep", "Гепатит B"),
    ("c_hep", "Гепатит C"),
    ("d_hep", "Гепатит D"),
    ("e_hep", "Гепатит E"),
    ("g_hep", "Гепатит G"),
]

STATES_LIST = [
    ("good", "Удовлетворительное"),
    ("middle", "Средней степени тяжести"),
    ("serve", "Тяжелое"),
    ("extreme", "Крайней степени тяжести"),
]

DEFORM_LIST = [
    ("has", "С видимыми деформациями"),
    ("not", "Без видимых деформаций"),
]

PAIN_LIST = [
    ("painful", "Болезненный"),
    ("painless", "Безболезнненый"),
]

BODIES_LIST = [
    ("asthenic", "Астеническое"),
    ("normal", "Нормостеническое"),
    ("hypersthenic", "Гиперстеническое"),
]

SKIN_LIST = [
    ("clear", "Чистые"),
    ("rash", "С высыпаниями"),
]

SKIN_WETNESS_LIST = [
    ("normal", "Нормальная"),
    ("dry", "Пониженная"),
    ("wet", "Повышенная"),
]

BREATH_TYPE_LIST = [
    ("vesicular", "Визикулярное"),
    ("rigid", "Жёсткое"),
    ("weak", "Ослабленное"),
]

RALES_LIST = [
    ("not", "Нет"),
    ("dry", "Сухие"),
    ("wet", "Влажные"),
]

HEART_RHYTHM_LIST = [
    ("rhythmic", "Ритмичные"),
    ("arrhythmic", "Аритмичные"),
]

HEART_CLARITY_LIST = [
    ("clear", "Ясные"),
    ("muted", "Приглушенные"),
]

HEART_MURMURS_LIST = [
    ("not", "Нет"),
    ("systolic", "Систолические"),
    ("diastolic", "Диастолические"),
]

ACCENTS_LIST = [
    ("not", "Нет"),
    ("has", "Есть"),
]

TONGUE_WETNESS_LIST = [
    ("wet", "Влажный"),
    ("dry", "Сухой"),
]

TONGUE_RAID_LIST = [
    ("clear", "Чистый"),
    ("raid", "Обложен налетом"),
]

BELLY_SOFTNESS_LIST = [
    ("soft", "Мягкий"),
    ("tense", "Напряженный"),
]

LIVER_SIZE_LIST = [
    ("normal", "Неувеличенная"),
    ("increase", "Увеличенная"),
]

KIDNEYS_SHAKING_LIST = [
    ("neg", "Негативное"),
    ("left", "Позитивное слева"),
    ("right", "Позитивное справа"),
    ("pos", "Позитивное слева и справа"),
]

URINATION_FREENESS_LIST = [
    ("free", "Свободное"),
    ("difficult", "Затрудненное"),
]

EDEMA_LIST = [
    ("has", "Есть"),
    ("not", "Нет"),
]

CHAIR_DEC_LIST = [
    ("dec", "Оформленный"),
    ("not_dec", "Неоформленный"),
]

CHAIR_REG_LIST = [
    ("regular", "Регулярный"),
    ("not_regular", "Нерегулярный"),
]

CONSCIENCE_LIST = [
    ("clear", "Ясное"),
    ("not", "Нет"),
]

ORIENTATION_LIST = [
    ("true", "Правильно"),
    ("false", "Неправильно"),
]

SENSITIVITY_LIST = [
    ("normal", "Не нарушена"),
    ("hypo", "Гипостезия"),
    ("hyper", "Гиперстезия"),
]

ROMBERG_POSE_LIST = [
    ("stable", "Устойчивый"),
    ("unstable", "Неустойчивый"),
]

FINGER_TEST_LIST = [
    ("good", "Удовлетворительная"),
    ("bad", "Неудовлетворительная"),
]

SPINE_MOTION_LIMIT_LIST = [
    ("unlimit", "Неограничены"),
    ("neck_limit", "Ограничены в шейном отделе"),
    ("chest_limit", "Ограничены в грудном отделе"),
    ("back_limit", "Ограничены в поясничном отделе"),
]

JOINTS_MOTION_VOLUME_LIST = [
    ("full", "В полном объеме"),
    ("limit", "Ограничены"),
]

THERAPY_RESULT_LIST = [
    ("best", "Значительное улучшение"),
    ("good", "Улучшение"),
    ("normal", "Без перемен"),
    ("bad", "Ухудшение"),
]

PROCEDURE_CATEGORIES_LIST = [
    ("", ""),
    ("", ""),
]

MEDICAL_ROOMS_LIST = [
    ("", ""),
    ("", ""),
]

PERIODICITY_LIST = [
    ("", ""),
    ("", ""),
]

EMPTY_LIST = [
    ("", ""),
    ("", ""),
]
