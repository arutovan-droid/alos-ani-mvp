import re


class ArmNormalizer:
    """
    Normalizer for MVP:
    - lowercases text
    - converts Armenian letters to latin
    - keeps latin + cyrillic + digits
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

        result_chars: list[str] = []
        i = 0
        while i < len(text):
            # handle "ու" as a digraph → "u"
            if text[i : i + 2] == "ու":
                result_chars.append("u")
                i += 2
                continue

            ch = text[i]
            # map Armenian letters to latin; keep other chars (latin/cyrillic) as-is
            result_chars.append(self.ARM_TO_LAT.get(ch, ch))
            i += 1

        clean_text = "".join(result_chars)
        # allow latin, cyrillic and digits
        clean_text = re.sub(r"[^a-zа-яё0-9\s]", " ", clean_text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        return clean_text


if __name__ == "__main__":
    n = ArmNormalizer()
    s = "բլուտուզ խոսփաքեր (новый, 2025)"
    print("RAW:", s)
    print("NORM:", n.normalize(s))
