from openai import AsyncOpenAI
from app.config import GROK_API_KEY

client = AsyncOpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
) if GROK_API_KEY else None

async def grok_chat(prompt: str, lang: str = "ky", is_pro: bool = False) -> str:
    if not client:
        return f"(DEMO) {prompt}"

    system = (
        "Сен Tilek AIсың. Ар жооп структуралуу болсун: "
        "📌 Негизги жооп, 📊 Түшүндүрмө (1-3 пункт), 💡 Кеңеш. "
        "Кыска, түшүнүктүү, кыргызча. "
        f"Жооп тили: {lang}."
    )

    model = "grok-beta"  # сен кааласаң grok-2 ж.б кылып алмаштырасың
    resp = await client.chat.completions.create(
        model=model,
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":prompt},
        ],
        temperature=0.7,
        max_tokens=700,
    )
    return resp.choices[0].message.content.strip()
