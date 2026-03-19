import re


def extract_action_items(text: str) -> list[str]:
    """
    Ekstraksi action item yang lebih canggih menggunakan regex.
    Mendukung:
    - TODO:, ACTION:, FIXME:, CHECK: (case-insensitive)
    - Pola markdown checkbox: [ ] atau [x]
    - Kalimat yang diawali kata kerja perintah (e.g., "Fix", "Update", "Send")
    """
    if not text:
        return []

    # 1. Pola untuk prefix kata kunci (contoh: TODO: beli susu)
    keyword_pattern = r"(?i)^(?:todo|action|fixme|check|task):\s*(.*)"

    # 2. Pola untuk checkbox markdown (contoh: [ ] bayar tagihan)
    checkbox_pattern = r"^\[[ xX]?\]\s*(.*)"

    results = []
    lines = [line.strip("- *") for line in text.splitlines() if line.strip()]

    for line in lines:
        # Coba cocokkan dengan kata kunci
        kw_match = re.match(keyword_pattern, line)
        if kw_match:
            results.append(kw_match.group(1).strip())
            continue

        # Coba cocokkan dengan checkbox
        cb_match = re.match(checkbox_pattern, line)
        if cb_match:
            results.append(cb_match.group(1).strip())
            continue

        # Tetap dukung logika lama: kalimat yang diakhiri tanda seru (!)
        if line.endswith("!") and len(line) > 2:
            results.append(line.strip())

    return [r for r in results if r]
