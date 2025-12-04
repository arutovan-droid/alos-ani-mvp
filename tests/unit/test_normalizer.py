from alos_core.customs.normalizer import ArmNormalizer


def test_normalizer_basic_armenian():
    norm = ArmNormalizer()
    text = "բլուտուզ խոսփաքեր"
    out = norm.normalize(text)
    # Проверяем, что что-то осмысленное получилось
    assert "blutuz" in out
    assert "khospaker" in out


def test_normalizer_mixed_text():
    norm = ArmNormalizer()
    text = "բլուտուզ speaker 123!"
    out = norm.normalize(text)
    # Цифры должны сохраниться, спецсимволы – уйти
    assert "blutuz" in out
    assert "speaker" in out
    assert "123" in out
    assert "!" not in out
