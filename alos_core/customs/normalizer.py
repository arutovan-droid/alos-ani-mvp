# alos_core/customs/normalizer.py
import re


class ArmNormalizer:
    """
    Превращает армяно-смешанный инвойс в удобный для ML латинский текст.
    Это MVP: кастомный маппинг + грубая очистка.
    """

    ARM_TO_LAT = {
        "ա": "a", "բ": "b", "գ": "g", "դ": "d", "ե": "e", "զ": "z",
        "է": "e", "ը": "y", "թ": "t", "ժ": "zh", "ի": "i", "լ": "l",
        "խ": "kh", "ծ": "ts", "կ": "k", "հ": "h", "ձ": "dz", "ղ": "gh",
        "ճ": "ch", "մ": "m", "յ": "y", "ն": "n", "շ": "sh", "ո": "o",
        "չ": "ch", "պ": "p", "ջ": "j", "ռ": "r", "ս": "s", "վ": "v",
        "տ": "t", "ր": "r", "ց": "c", "ու": "u", "փ": "p", "ք": "k",
        "և": "ev", "օ": "o", "ֆ": "f",
    }

    def normalize(self, text: str) -> str:
        if not text:
            return ""

        text = text.lower().strip()

        # грубая замена армянских символов
        result_chars: list[str] = []
        skip_next = False
        for i, ch in enumerate(text):
            if skip_next:
                skip_next = False
                continue
            # простой хэндл "ու" как биграммы
            if ch == "ու"[0] and i + 1 < len(text) and text[i : i + 2] == "ու":
                result_chars.append("u")
                skip_next = True
                continue
            result_chars.append(self.ARM_TO_LAT.get(ch, ch))

        clean_text = "".join(result_chars)
        # оставляем только латинские буквы, цифры и пробел
        clean_text = re.sub(r"[^a-z0-9\s]", " ", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        return clean_text


if __name__ == "__main__":
    n = ArmNormalizer()
    s = "բլուտուզ խոսփաքեր (новый, 2025)"
    print("RAW:", s)
    print("NORM:", n.normalize(s))
