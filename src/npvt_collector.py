#!/usr/bin/env python3
"""
src/npvt_collector.py

اسکن صفحات وب عمومی تلگرام (t.me/s/<channel>) برای پیام‌هایی که فایل با
پسوند .npvt دارند — بدون نیاز به لاگین، شماره تلفن، یا عضویت در هیچ کانالی؛
دقیقاً همان روش HTTP/HTML که در پروژه‌های V2ray-Collector و news-monitor
خودتان استفاده شده (t.me/s/... به‌صورت عمومی و بدون احراز هویت در دسترس
است).

سپس موارد تکراری (بر اساس ترکیب «نام فایل + حجم فایل») حذف می‌شوند و برای
هر مورد یکتا، فقط یک پیام متنی حاوی نام، حجم و لینک مستقیم پیام اصلی —
از طریق یک بات تلگرامی معمولی (Bot API) — به کانال مقصد ارسال می‌شود.
این بات فقط باید در کانال *مقصد* خودتان دسترسی ارسال پیام داشته باشد؛ هیچ
نیازی به عضویت در کانال‌های مبدأ یا هیچ اکانت کاربری نیست.

همچنین، مثل پروژه‌ی V2ray-Collector، دو فایل گزارش تولید می‌شود:
  - data/channel_report.txt   → تاریخچه‌ی تعداد فایل .npvt یافت‌شده در هر اجرا، به ازای هر کانال
  - data/invalid_channels.txt → کانال‌هایی که در این اجرا هیچ پیامی از آن‌ها خوانده نشد
                                 (وجود ندارند، خصوصی‌اند، یا مسدود شده‌اند)

برای مقابله با محدودیت نرخ ارسال تلگرام (خطای 429 Too Many Requests)، دو
مکانیزم اضافه شده:
  - در صورت 429، دقیقاً به‌اندازه‌ی retry_after اعلام‌شده توسط تلگرام صبر و
    دوباره تلاش می‌شود (تا MAX_SEND_RETRIES بار).
  - هر موردی که پس از این تلاش‌ها هم ارسال نشود، در data/pending_send.json
    ذخیره می‌شود و در اجرای بعدی دوباره تلاش می‌شود — یعنی هیچ فایلی، حتی
    زیر فشار محدودیت نرخ، برای همیشه گم نمی‌شود.
"""
from __future__ import annotations

import json
import logging
import os
import re
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("npvt_collector")

# ----------------------------------------------------------------------------
# تنظیمات
# ----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CHANNELS_FILE = DATA_DIR / "channels.txt"
CHECKPOINT_FILE = DATA_DIR / "last_message_id.json"
SEEN_FILES_FILE = DATA_DIR / "seen_files.json"
REPORT_FILE = DATA_DIR / "npvt_report.txt"
CHANNEL_REPORT_FILE = DATA_DIR / "channel_report.txt"
INVALID_CHANNELS_FILE = DATA_DIR / "invalid_channels.txt"
PENDING_FILE = DATA_DIR / "pending_send.json"
BLOCKED_KEYWORDS_FILE = DATA_DIR / "blocked_keywords.txt"
FILTERED_FILES_FILE = DATA_DIR / "filtered_files.txt"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

SLEEP_BETWEEN_CHANNELS = float(os.getenv("SLEEP_BETWEEN_CHANNELS", "1.5"))
SLEEP_BETWEEN_PAGES = float(os.getenv("SLEEP_BETWEEN_PAGES", "1"))
# تلگرام برای پیام‌های یک بات به یک چت، تقریباً حداکثر ۲۰ پیام در دقیقه را
# مجاز می‌داند؛ ۳.۵ ثانیه فاصله ≈ ۱۷ پیام در دقیقه، با کمی حاشیه‌ی امن.
SLEEP_BETWEEN_SENDS = float(os.getenv("SLEEP_BETWEEN_SENDS", "3.5"))
MAX_PAGES_PER_CHANNEL = int(os.getenv("MAX_PAGES_PER_CHANNEL", "1"))

# ---- تلاش مجدد هنگام محدودیت نرخ ارسال (429 Too Many Requests) ----
# اگر تلگرام یک پیام را رد کند و بگوید «بعد از N ثانیه دوباره امتحان کن»،
# دقیقاً همان مدت صبر می‌کنیم و دوباره تلاش می‌کنیم (نه اینکه پیام را از
# دست بدهیم). حداکثر تعداد تلاش و حداکثر زمان انتظار قابل تنظیم است.
MAX_SEND_RETRIES = int(os.getenv("MAX_SEND_RETRIES", "6"))
MAX_RETRY_AFTER_WAIT = int(os.getenv("MAX_RETRY_AFTER_WAIT", "90"))

# ---- سقف تعداد پیام ارسالی در هر اجرا ----
# اگر یک‌باره تعداد زیادی فایل جدید پیدا شود (مثلاً اولین اجرا)، برای اینکه
# فاز ارسال، کل اجرا را بیش‌ازحد طولانی نکند، فقط این تعداد در هر اجرا
# ارسال می‌شود؛ باقی در data/pending_send.json برای اجرای بعدی می‌مانند —
# یعنی هیچ فایلی گم نمی‌شود، فقط با تأخیر ارسال می‌شود.
MAX_SENDS_PER_RUN = int(os.getenv("MAX_SENDS_PER_RUN", "40"))

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL", "")  # مثال: @my_channel یا -100xxxxxxxxxx

FILE_SUFFIX = ".npvt"

# ---- فیلتر نام فایل ----
# فایل‌هایی که نامشان حاوی هر یک از این کلیدواژه‌ها باشد، اصلاً جمع‌آوری یا
# منتشر نمی‌شوند. این لیست پیش‌فرض است؛ می‌توانید آن را در
# data/blocked_keywords.txt (بدون نیاز به تغییر این فایل) ویرایش کنید.
DEFAULT_BLOCKED_KEYWORDS = [
    "جاوید", "جاویدنام", "جاوید نام",
    "شاه", "آریامهر", "آریا مهر", "پهلوی",
    "خمینی", "خامنه ای", "خامنه‌ای",
    "سیدعلی", "سید علی", "مجتبی",
]


# ----------------------------------------------------------------------------
# مدل داده
# ----------------------------------------------------------------------------
@dataclass
class NpvtFile:
    channel: str
    message_id: int
    file_name: str
    size_text: str
    link: str

    @property
    def dedup_key(self) -> str:
        # طبق درخواست: فقط وقتی تکراری است که «هم نام و هم حجم» یکسان باشند
        name = re.sub(r"\s+", " ", self.file_name.strip().lower())
        size = re.sub(r"\s+", "", self.size_text.strip().lower())
        return f"{name}::{size}"

    def to_dict(self) -> dict:
        return {
            "channel": self.channel,
            "message_id": self.message_id,
            "file_name": self.file_name,
            "size_text": self.size_text,
            "link": self.link,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "NpvtFile":
        return cls(
            channel=data.get("channel", ""),
            message_id=int(data.get("message_id", 0)),
            file_name=data.get("file_name", ""),
            size_text=data.get("size_text", ""),
            link=data.get("link", ""),
        )


# ----------------------------------------------------------------------------
# توابع کمکی
# ----------------------------------------------------------------------------
def normalize_fa(text: str) -> str:
    """
    برای مقایسه‌ی قابل‌اعتماد بین حالت‌های مختلف نگارشی یک عبارت فارسی
    (با فاصله، با نیم‌فاصله ZWNJ، یا چسبیده)، همه‌ی این‌ها را حذف کرده و
    به حروف کوچک تبدیل می‌کند؛ مثلاً «خامنه‌ای»، «خامنه ای» و «خامنهای»
    همه به یک رشته‌ی یکسان تبدیل می‌شوند.
    """
    text = text.replace("\u200c", "")  # نیم‌فاصله (ZWNJ)
    text = re.sub(r"\s+", "", text)
    return text.strip().lower()


def load_blocked_keywords() -> list[str]:
    if not BLOCKED_KEYWORDS_FILE.exists():
        # فایل هنوز ساخته نشده؛ لیست پیش‌فرض را روی دیسک هم می‌نویسیم تا
        # کاربر بتواند بعداً آن را مستقیماً ویرایش کند.
        BLOCKED_KEYWORDS_FILE.parent.mkdir(parents=True, exist_ok=True)
        BLOCKED_KEYWORDS_FILE.write_text(
            "# هر خط یک کلیدواژه؛ نام فایل‌هایی که حاوی هر یک از این‌ها باشند منتشر نمی‌شوند.\n"
            "# خط‌هایی که با # شروع می‌شوند نادیده گرفته می‌شوند.\n"
            + "\n".join(DEFAULT_BLOCKED_KEYWORDS) + "\n",
            encoding="utf-8",
        )
        return list(DEFAULT_BLOCKED_KEYWORDS)

    lines = BLOCKED_KEYWORDS_FILE.read_text(encoding="utf-8").splitlines()
    keywords = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
    return keywords


BLOCKED_KEYWORDS = load_blocked_keywords()


def load_channels() -> list[str]:
    if not CHANNELS_FILE.exists():
        logger.error("فایل %s پیدا نشد.", CHANNELS_FILE)
        return []
    lines = CHANNELS_FILE.read_text(encoding="utf-8").splitlines()
    channels = [
        line.strip().lstrip("@")
        for line in lines
        if line.strip() and not line.strip().startswith("#")
    ]
    logger.info("📋 %d کانال از %s بارگذاری شد.", len(channels), CHANNELS_FILE)
    return channels


def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            logger.warning("خطا در خواندن %s؛ از مقدار پیش‌فرض استفاده می‌شود.", path)
    return default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def fetch_url(url: str) -> str:
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logger.warning("   ↳ خطا در واکشی %s: %s", url, e)
        return ""


def extract_npvt_from_node(node, channel: str, msg_id: int) -> NpvtFile | None:
    """استخراج اطلاعات فایل .npvt از یک بلوک پیام، در صورت وجود ضمیمه."""
    doc_anchor = node.select_one('a[class*="document"]')
    if not doc_anchor:
        return None

    title_el = doc_anchor.select_one('[class*="document_title"]')
    extra_el = doc_anchor.select_one('[class*="document_extra"]')
    file_name = title_el.get_text(strip=True) if title_el else ""
    size_text = extra_el.get_text(strip=True) if extra_el else ""

    if not file_name or not file_name.lower().endswith(FILE_SUFFIX):
        return None

    return NpvtFile(
        channel=channel,
        message_id=msg_id,
        file_name=file_name,
        size_text=size_text or "نامشخص",
        link=f"https://t.me/{channel}/{msg_id}",
    )


def find_blocked_keyword(file_name: str) -> str | None:
    """اگر نام فایل حاوی یکی از کلیدواژه‌های مسدود باشد، همان کلیدواژه را برمی‌گرداند، وگرنه None."""
    normalized_name = normalize_fa(file_name)
    for keyword in BLOCKED_KEYWORDS:
        if normalize_fa(keyword) in normalized_name:
            return keyword
    return None


# ----------------------------------------------------------------------------
# اسکن یک کانال (با صفحه‌بندی محدود برای رسیدن به چک‌پوینت قبلی)
# ----------------------------------------------------------------------------
def scan_channel(channel: str, last_id: int) -> tuple[list[NpvtFile], int, bool, list[tuple[str, str, str]]]:
    """
    خروجی: (فایل‌های .npvt پیدا‌شده, جدیدترین message_id دیده‌شده, آیا کانال نامعتبر است, فایل‌های فیلترشده)
    کانال «نامعتبر» یعنی: صفحه اصلاً واکشی نشد یا هیچ data-post (پیام) در آن پیدا نشد —
    معمولاً به این معناست که کانال وجود ندارد، خصوصی است، یا دسترسی به آن مسدود شده.
    فایل‌های فیلترشده: (نام فایل, کلیدواژه‌ی مسدودکننده, لینک) — اصلاً به لیست found اضافه نمی‌شوند.
    """
    found: list[NpvtFile] = []
    filtered: list[tuple[str, str, str]] = []
    newest_id = last_id
    before: int | None = None
    first_page = True
    invalid = False

    for page in range(MAX_PAGES_PER_CHANNEL):
        url = f"https://t.me/s/{channel}" + (f"?before={before}" if before else "")
        html = fetch_url(url)
        if not html:
            if first_page:
                invalid = True
            break

        soup = BeautifulSoup(html, "lxml")
        nodes = soup.select("[data-post]")
        if not nodes:
            if first_page:
                invalid = True
            break

        ids_on_page: list[int] = []
        for node in nodes:
            data_post = node.get("data-post", "")
            m = re.search(r"/(\d+)$", data_post)
            if not m:
                continue
            msg_id = int(m.group(1))
            ids_on_page.append(msg_id)
            newest_id = max(newest_id, msg_id)

            if msg_id <= last_id:
                continue

            item = extract_npvt_from_node(node, channel, msg_id)
            if not item:
                continue

            matched_keyword = find_blocked_keyword(item.file_name)
            if matched_keyword:
                filtered.append((item.file_name, matched_keyword, item.link))
                continue

            found.append(item)

        first_page = False
        if not ids_on_page:
            break

        oldest_on_page = min(ids_on_page)
        if oldest_on_page <= last_id:
            break  # به آخرین چک‌پوینت رسیدیم؛ نیازی به صفحهٔ قبل‌تر نیست

        before = oldest_on_page
        if page < MAX_PAGES_PER_CHANNEL - 1:
            time.sleep(SLEEP_BETWEEN_PAGES)

    return found, newest_id, invalid, filtered


# ----------------------------------------------------------------------------
# ارسال پیام لینک از طریق بات تلگرام (Bot API)
# ----------------------------------------------------------------------------
def send_link_message(item: NpvtFile) -> bool:
    """
    ارسال پیام لینک با احترام کامل به محدودیت نرخ تلگرام: اگر ۴۲۹ برگردد،
    دقیقاً به‌اندازه‌ی retry_after اعلام‌شده صبر می‌کنیم و دوباره تلاش
    می‌کنیم (نه اینکه پیام را از دست بدهیم). حداکثر MAX_SEND_RETRIES بار.
    """
    text = (
        "📦 فایل جدید NPVT\n"
        f"نام: {item.file_name}\n"
        f"حجم: {item.size_text}\n"
        f"لینک: {item.link}"
    )
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TARGET_CHANNEL,
        "text": text,
        "disable_web_page_preview": True,
    }

    for attempt in range(1, MAX_SEND_RETRIES + 1):
        try:
            resp = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        except Exception as e:
            logger.error("   ↳ خطای شبکه هنگام ارسال «%s» (تلاش %d/%d): %s",
                         item.file_name, attempt, MAX_SEND_RETRIES, e)
            time.sleep(min(5 * attempt, MAX_RETRY_AFTER_WAIT))
            continue

        if resp.status_code == 200:
            return True

        if resp.status_code == 429:
            try:
                retry_after = int(resp.json().get("parameters", {}).get("retry_after", 5))
            except Exception:
                retry_after = 5
            wait_time = min(retry_after + 1, MAX_RETRY_AFTER_WAIT)
            logger.warning(
                "   ↳ ⏳ محدودیت نرخ تلگرام (429) برای «%s»؛ %ss صبر می‌کنیم "
                "(تلاش %d/%d)...",
                item.file_name, wait_time, attempt, MAX_SEND_RETRIES,
            )
            time.sleep(wait_time)
            continue

        # سایر خطاها (مثلاً بات ادمین کانال نیست) با تلاش دوباره حل نمی‌شوند
        logger.error("   ↳ ارسال پیام «%s» شکست خورد: %s", item.file_name, resp.text)
        return False

    logger.error(
        "   ↳ ارسال «%s» پس از %d تلاش، همچنان با محدودیت نرخ مواجه شد؛ "
        "برای اجرای بعدی در صف نگه داشته می‌شود.",
        item.file_name, MAX_SEND_RETRIES,
    )
    return False


# ----------------------------------------------------------------------------
# گزارش‌ها: channel_report.txt (تاریخچه) و invalid_channels.txt (این اجرا)
# ----------------------------------------------------------------------------
def update_channel_report(channel_results: list[tuple[str, str]]) -> None:
    """
    channel_results: لیستی از (channel, value) که value یا تعداد فایل .npvt
    پیدا‌شده (به‌صورت رشته) و یا "ERR" برای کانال نامعتبر است.
    مثل V2ray-Collector، تاریخچه‌ی همه‌ی اجراهای قبلی هم نگه داشته می‌شود.
    """
    history: dict[str, list[str]] = {}
    if CHANNEL_REPORT_FILE.exists():
        with open(CHANNEL_REPORT_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                ch, counts = line.split(":", 1)
                ch = ch.strip()
                values = [c.strip() for c in counts.split(",") if c.strip()]
                history[ch] = values

    for ch, value in channel_results:
        history.setdefault(ch, []).append(value)

    CHANNEL_REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CHANNEL_REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(f"NPVT Channel Report — last update: {datetime.now(timezone.utc).isoformat()}\n\n")
        for ch in sorted(history.keys()):
            f.write(f"{ch}: {', '.join(history[ch])}\n")

    logger.info("📊 تاریخچه‌ی کانال‌ها در %s به‌روزرسانی شد.", CHANNEL_REPORT_FILE)


def write_invalid_channels(invalid_channels: list[str]) -> None:
    INVALID_CHANNELS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INVALID_CHANNELS_FILE, "w", encoding="utf-8") as f:
        f.write(f"Invalid Telegram Channels — {datetime.now(timezone.utc).isoformat()}\n\n")
        for ch in sorted(invalid_channels):
            f.write(f"{ch}\n")

    if invalid_channels:
        logger.info("📁 %d کانال نامعتبر در %s ذخیره شد.", len(invalid_channels), INVALID_CHANNELS_FILE)


def append_filtered_files(filtered: list[tuple[str, str, str]]) -> None:
    """هر فایلی که به‌خاطر تطابق با data/blocked_keywords.txt منتشر نشد، اینجا ثبت می‌شود (فقط برای شفافیت)."""
    if not filtered:
        return
    FILTERED_FILES_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(FILTERED_FILES_FILE, "a", encoding="utf-8") as f:
        ts = time.strftime("%Y-%m-%d %H:%M:%S")
        for file_name, keyword, link in filtered:
            f.write(f"{ts} | keyword=«{keyword}» | {file_name} | {link}\n")
    logger.info("🚫 %d فایل به‌خاطر کلیدواژه‌ی مسدود، منتشر نشد (جزئیات در %s).", len(filtered), FILTERED_FILES_FILE)


# ----------------------------------------------------------------------------
# اجرای اصلی
# ----------------------------------------------------------------------------
def main() -> None:
    if not BOT_TOKEN or not TARGET_CHANNEL:
        logger.error("❌ BOT_TOKEN و/یا TARGET_CHANNEL تنظیم نشده است؛ اجرا متوقف شد.")
        return

    channels = load_channels()
    if not channels:
        return

    checkpoints: dict = load_json(CHECKPOINT_FILE, {})
    seen_files: dict = load_json(SEEN_FILES_FILE, {})

    all_new: list[NpvtFile] = []
    all_filtered: list[tuple[str, str, str]] = []  # برای filtered_files.txt
    channel_results: list[tuple[str, str]] = []  # برای channel_report.txt
    invalid_channels: list[str] = []              # برای invalid_channels.txt

    for idx, ch in enumerate(channels, 1):
        logger.info("📡 [%d/%d] بررسی کانال: %s", idx, len(channels), ch)
        last_id = checkpoints.get(ch, 0)
        found, newest_id, invalid, filtered = scan_channel(ch, last_id)

        if invalid:
            logger.warning("   ↳ ⚠️ کانال نامعتبر یا غیرقابل‌دسترسی (وجود ندارد/خصوصی/مسدود).")
            invalid_channels.append(ch)
            channel_results.append((ch, "ERR"))
        else:
            if found:
                logger.info("   ↳ %d فایل .npvt جدید پیدا شد.", len(found))
            else:
                logger.info("   ↳ فایل .npvt جدیدی پیدا نشد.")
            if filtered:
                logger.info("   ↳ 🚫 %d فایل به‌خاطر کلیدواژه‌ی مسدود نادیده گرفته شد.", len(filtered))
            channel_results.append((ch, str(len(found))))

        if newest_id:
            checkpoints[ch] = max(newest_id, last_id)

        all_new.extend(found)
        all_filtered.extend(filtered)
        if idx < len(channels):
            time.sleep(SLEEP_BETWEEN_CHANNELS)

    # ---- گام ۱: حذف تکراری‌های داخل همین اجرا (اولین موردِ هر نام+حجم می‌ماند) ----
    unique_batch: dict[str, NpvtFile] = {}
    duplicate_in_batch = 0
    for item in all_new:
        if item.dedup_key in unique_batch:
            duplicate_in_batch += 1
            continue
        unique_batch[item.dedup_key] = item

    # ---- گام ۲: حذف مواردی که در اجراهای قبلی قبلاً ارسال شده‌اند ----
    already_sent = 0
    to_send: list[NpvtFile] = []
    for key, item in unique_batch.items():
        if key in seen_files:
            already_sent += 1
            continue
        to_send.append(item)

    logger.info(
        "🔍 جمع‌بندی اسکن: %d پیام یافت شد | %d تکراری در همین اجرا حذف شد | "
        "%d مورد قبلاً ارسال شده بود | %d مورد تازه‌یاب برای ارسال.",
        len(all_new), duplicate_in_batch, already_sent, len(to_send),
    )

    # ---- گام ۳: ادغام با صف باقی‌مانده از اجراهای قبلی (که به هر دلیلی ----
    # ---- ارسال نشده بودند، مثلاً به‌خاطر محدودیت نرخ تلگرام) ----
    pending: dict = load_json(PENDING_FILE, {})
    work_items: dict[str, NpvtFile] = {
        key: NpvtFile.from_dict(data) for key, data in pending.items()
    }
    for item in to_send:
        work_items.setdefault(item.dedup_key, item)

    if pending:
        logger.info("📥 %d مورد از صف اجراهای قبلی نیز برای ارسال اضافه شد.", len(pending))

    all_work = list(work_items.items())
    if MAX_SENDS_PER_RUN > 0:
        attempt_now = all_work[:MAX_SENDS_PER_RUN]
        deferred = all_work[MAX_SENDS_PER_RUN:]
    else:
        attempt_now, deferred = all_work, []

    if deferred:
        logger.info(
            "⏭️ %d مورد به‌خاطر سقف %d ارسال در هر اجرا، برای اجرای بعدی در صف می‌مانند.",
            len(deferred), MAX_SENDS_PER_RUN,
        )

    sent = failed = 0
    leftover: dict[str, NpvtFile] = dict(deferred)

    for i, (key, item) in enumerate(attempt_now, 1):
        ok = send_link_message(item)
        if ok:
            sent += 1
            seen_files[key] = {
                "file_name": item.file_name,
                "size": item.size_text,
                "source_channel": item.channel,
                "link": item.link,
                "date": time.strftime("%Y-%m-%d %H:%M:%S"),
            }
        else:
            failed += 1
            leftover[key] = item  # برای اجرای بعدی نگه داشته می‌شود، گم نمی‌شود
        if i < len(attempt_now):
            time.sleep(SLEEP_BETWEEN_SENDS)

    save_json(CHECKPOINT_FILE, checkpoints)
    save_json(SEEN_FILES_FILE, seen_files)
    save_json(PENDING_FILE, {key: item.to_dict() for key, item in leftover.items()})
    update_channel_report(channel_results)
    write_invalid_channels(invalid_channels)
    append_filtered_files(all_filtered)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} | found={len(all_new)} "
            f"duplicates={duplicate_in_batch} already_sent={already_sent} "
            f"attempted={len(attempt_now)} sent={sent} failed={failed} "
            f"pending_queue={len(leftover)} filtered={len(all_filtered)} "
            f"invalid_channels={len(invalid_channels)}\n"
        )

    logger.info(
        "✅ پایان اجرا. ارسال‌شده: %d | ناموفق (در صف ماند): %d | در انتظار کل: %d | "
        "فیلترشده: %d | کانال نامعتبر: %d",
        sent, failed, len(leftover), len(all_filtered), len(invalid_channels),
    )


if __name__ == "__main__":
    main()
