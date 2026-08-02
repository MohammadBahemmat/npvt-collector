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
CURSOR_FILE = DATA_DIR / "channel_cursor.json"
PENDING_FILE = DATA_DIR / "pending_send.json"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))

SLEEP_BETWEEN_CHANNELS = float(os.getenv("SLEEP_BETWEEN_CHANNELS", "1.5"))
SLEEP_BETWEEN_PAGES = float(os.getenv("SLEEP_BETWEEN_PAGES", "1"))
# تلگرام برای پیام‌های یک بات به یک چت، تقریباً حداکثر ۲۰ پیام در دقیقه را
# مجاز می‌داند؛ ۳.۵ ثانیه فاصله ≈ ۱۷ پیام در دقیقه، با کمی حاشیه‌ی امن.
SLEEP_BETWEEN_SENDS = float(os.getenv("SLEEP_BETWEEN_SENDS", "3.5"))
MAX_PAGES_PER_CHANNEL = int(os.getenv("MAX_PAGES_PER_CHANNEL", "3"))

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

# ---- پردازش دسته‌ای و چرخشی کانال‌ها ----
# هر اجرا فقط این تعداد کانال را بررسی می‌کند (نه لزوماً کل لیست)؛ اجرای
# بعدی از همان‌جا که این اجرا متوقف شده ادامه می‌دهد. این تضمین می‌کند که
# مدت‌زمان هر اجرا صرف‌نظر از تعداد کل کانال‌ها یا حجم بک‌لاگ، محدود و
# قابل‌پیش‌بینی بماند (و به Timeout گیت‌هاب اکشن نخورد).
CHANNELS_PER_RUN = int(os.getenv("CHANNELS_PER_RUN", "15"))

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL", "")  # مثال: @my_channel یا -100xxxxxxxxxx

FILE_SUFFIX = ".npvt"


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


def select_batch(channels: list[str]) -> tuple[list[str], int, int]:
    """
    یک دسته‌ی چرخشی از کانال‌ها را برمی‌گرداند تا هر اجرا محدود بماند.
    خروجی: (کانال‌های این اجرا, ایندکس شروع, ایندکس بعدی برای اجرای آینده)
    """
    cursor_data = load_json(CURSOR_FILE, {"index": 0})
    total = len(channels)

    if CHANNELS_PER_RUN <= 0 or CHANNELS_PER_RUN >= total:
        return channels, 0, 0  # همه‌ی کانال‌ها در یک اجرا؛ بدون نیاز به چرخش

    start = cursor_data.get("index", 0) % total
    end = start + CHANNELS_PER_RUN

    if end <= total:
        batch = channels[start:end]
    else:
        # دور زدن به ابتدای لیست
        batch = channels[start:total] + channels[0:end - total]

    next_index = end % total
    return batch, start, next_index


def save_cursor(next_index: int) -> None:
    save_json(CURSOR_FILE, {"index": next_index})


# ----------------------------------------------------------------------------
# ----------------------------------------------------------------------------
def scan_channel(channel: str, last_id: int) -> tuple[list[NpvtFile], int, bool]:
    """
    خروجی: (فایل‌های .npvt پیدا‌شده, جدیدترین message_id دیده‌شده, آیا کانال نامعتبر است)
    کانال «نامعتبر» یعنی: صفحه اصلاً واکشی نشد یا هیچ data-post (پیام) در آن پیدا نشد —
    معمولاً به این معناست که کانال وجود ندارد، خصوصی است، یا دسترسی به آن مسدود شده.
    """
    found: list[NpvtFile] = []
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
            if item:
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

    return found, newest_id, invalid


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


def write_invalid_channels(tested_this_run: list[str], invalid_this_run: list[str]) -> None:
    """
    چون هر اجرا فقط یک دسته از کانال‌ها را تست می‌کند (نه همه)، این فایل به‌جای
    بازنویسی کامل، با نتیجهٔ اجراهای قبلی ادغام می‌شود: کانال‌های همین دسته
    با نتیجهٔ تازه جایگزین می‌شوند و بقیه (که این‌بار تست نشده‌اند) دست‌نخورده
    باقی می‌مانند.
    """
    previous: list[str] = []
    if INVALID_CHANNELS_FILE.exists():
        for line in INVALID_CHANNELS_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("Invalid Telegram Channels"):
                previous.append(line)

    tested_set = set(tested_this_run)
    kept = [ch for ch in previous if ch not in tested_set]
    merged = sorted(set(kept) | set(invalid_this_run))

    INVALID_CHANNELS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INVALID_CHANNELS_FILE, "w", encoding="utf-8") as f:
        f.write(f"Invalid Telegram Channels — {datetime.now(timezone.utc).isoformat()}\n\n")
        for ch in merged:
            f.write(f"{ch}\n")

    if invalid_this_run:
        logger.info("📁 %d کانال نامعتبر در این اجرا؛ مجموع فعلی: %d (در %s)",
                    len(invalid_this_run), len(merged), INVALID_CHANNELS_FILE)


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

    batch, start_idx, next_idx = select_batch(channels)
    if len(batch) < len(channels):
        logger.info(
            "🔁 پردازش دسته‌ای: این اجرا کانال‌های %d تا %d از مجموع %d را بررسی می‌کند "
            "(اجرای بعدی از کانال %d ادامه می‌دهد).",
            start_idx + 1, start_idx + len(batch), len(channels), next_idx + 1,
        )

    checkpoints: dict = load_json(CHECKPOINT_FILE, {})
    seen_files: dict = load_json(SEEN_FILES_FILE, {})

    all_new: list[NpvtFile] = []
    channel_results: list[tuple[str, str]] = []  # برای channel_report.txt
    invalid_channels: list[str] = []              # برای invalid_channels.txt

    for idx, ch in enumerate(batch, 1):
        logger.info("📡 [%d/%d] بررسی کانال: %s", idx, len(batch), ch)
        last_id = checkpoints.get(ch, 0)
        found, newest_id, invalid = scan_channel(ch, last_id)

        if invalid:
            logger.warning("   ↳ ⚠️ کانال نامعتبر یا غیرقابل‌دسترسی (وجود ندارد/خصوصی/مسدود).")
            invalid_channels.append(ch)
            channel_results.append((ch, "ERR"))
        else:
            if found:
                logger.info("   ↳ %d فایل .npvt جدید پیدا شد.", len(found))
            else:
                logger.info("   ↳ فایل .npvt جدیدی پیدا نشد.")
            channel_results.append((ch, str(len(found))))

        if newest_id:
            checkpoints[ch] = max(newest_id, last_id)

        all_new.extend(found)
        if idx < len(batch):
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
    write_invalid_channels(tested_this_run=batch, invalid_this_run=invalid_channels)
    if len(batch) < len(channels):
        save_cursor(next_idx)

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"{time.strftime('%Y-%m-%d %H:%M:%S')} | found={len(all_new)} "
            f"duplicates={duplicate_in_batch} already_sent={already_sent} "
            f"attempted={len(attempt_now)} sent={sent} failed={failed} "
            f"pending_queue={len(leftover)} invalid_channels={len(invalid_channels)}\n"
        )

    logger.info(
        "✅ پایان اجرا. ارسال‌شده: %d | ناموفق (در صف ماند): %d | در انتظار کل: %d | کانال نامعتبر: %d",
        sent, failed, len(leftover), len(invalid_channels),
    )


if __name__ == "__main__":
    main()
