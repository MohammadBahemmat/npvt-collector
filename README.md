<!-- README.md (نسخه فارسی) -->
<div align="center" style="margin-bottom: 20px;">
  <a href="https://github.com/YOUR_USERNAME/npvt-collector/blob/main/README.EN.md">
    <img src="https://img.shields.io/badge/Read_in-English-009688?style=for-the-badge&logo=readthedocs" alt="Read in English">
  </a>
</div>

<body>
<div class="container">

<!-- ====== ردیف نشان‌های اطلاعاتی پروژه ====== -->
<div align="center" style="margin-bottom: 15px;">

<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative" alt="License">
<a href="https://github.com/YOUR_USERNAME/npvt-collector/blob/main/config/requirements.txt">
    <img src="https://img.shields.io/badge/Requirements-txt-critical?style=for-the-badge&logo=pypi" alt="Requirements">
</a>
<img src="https://img.shields.io/badge/Platform-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions" alt="GitHub Actions">
<img src="https://img.shields.io/badge/No_Login_Required-Telegram_Account-critical?style=for-the-badge&logo=telegram" alt="No Login Required">

</div>

<img src="https://github.com/MohammadBahemmat/npvt-collector/actions/workflows/collector.yml/badge.svg" alt="Collector Status">

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<h1>📦 NPVT Collector — جمع‌آوری خودکار فایل‌های NPVT از تلگرام</h1>

<p>
<strong>یک جمع‌آورندهٔ خودکار و بدون‌ریسک برای فایل‌های <code>.npvt</code> (کانفیگ‌های NPVT / NPV Tunnel) که در کانال‌های عمومی تلگرام منتشر می‌شوند.</strong><br>
این پروژه صفحهٔ پیش‌نمایش وبِ عمومیِ کانال‌ها (<code>t.me/s</code>) را می‌خواند — دقیقاً همان روشی که در پروژه‌های <code>V2ray-Collector</code> و <code>news-monitor</code> استفاده شده — بدون نیاز به <strong>API، لاگین اکانت کاربری یا شماره تلفن شخصی</strong>.
</p>
<p>
هر فایل جدید بر اساس <strong>نام + حجم</strong> با فایل‌های قبلاً دیده‌شده مقایسه و در صورت تکراری بودن حذف می‌شود؛ سپس لینک فایل‌های یکتا از طریق یک <strong>بات تلگرامی معمولی</strong> (بدون نیاز به فوروارد یا عضویت در کانال‌های مبدأ) به کانال دلخواه شما ارسال می‌شود.
</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- ویژگی‌های متمایز -->
<h2>✨ ویژگی‌های متمایز</h2>
<table>
<thead>
<tr><th>ویژگی</th><th>توضیح</th></tr>
</thead>
<tbody>
<tr>
    <td><strong>🔒 بدون هیچ ریسکی برای اکانت شخصی</strong></td>
    <td>هیچ شماره تلفن، لاگین اکانت کاربری (Userbot) یا عضویت در کانال‌های مبدأ لازم نیست. فقط صفحهٔ عمومی وب هر کانال (<code>t.me/s/&lt;channel&gt;</code>) خوانده می‌شود.</td>
</tr>
<tr>
    <td><strong>📄 استخراج دقیق نام و حجم فایل</strong></td>
    <td>نام و حجم هر فایل <code>.npvt</code> (همان‌طور که خودِ تلگرام نمایش می‌دهد، مثل <code>3.5 KB</code>) به‌همراه لینک مستقیم پیام استخراج می‌شود.</td>
</tr>
<tr>
    <td><strong>🧹 حذف هوشمند موارد تکراری</strong></td>
    <td>فقط زمانی که <strong>هم نام و هم حجم</strong> یک فایل با فایلی دیگر (در همین کانال، کانالی دیگر، یا اجرای قبلی) یکسان باشد، تکراری در نظر گرفته و حذف می‌شود.</td>
</tr>
<tr>
    <td><strong>📤 ارسال با بات معمولی تلگرام</strong></td>
    <td>لینک هر فایل یکتا با یک بات ساده (Bot API) به کانال مقصد شما ارسال می‌شود؛ بات فقط باید در کانال مقصد خودتان ادمین باشد.</td>
</tr>
<tr>
    <td><strong>🧩 Checkpoint (ادامه از همان نقطه)</strong></td>
    <td>آخرین <code>message_id</code> بررسی‌شدهٔ هر کانال ذخیره می‌شود؛ در اجرای بعدی فقط پیام‌های جدید بررسی می‌شوند.</td>
</tr>
<tr>
    <td><strong>💾 آرشیو ضدتکرار دائمی</strong></td>
    <td>فایل‌هایی که یک‌بار لینک‌شان ارسال شده در <code>data/seen_files.json</code> ثبت می‌شوند تا هیچ‌وقت دوباره ارسال نشوند.</td>
</tr>
<tr>
    <td><strong>📊 گزارش هر اجرا</strong></td>
    <td>خلاصهٔ هر اجرا (تعداد یافت‌شده، تکراری، جدید، ارسال‌شده) در <code>data/npvt_report.txt</code> ثبت می‌شود.</td>
</tr>
<tr>
    <td><strong>🚀 اجرای کاملاً خودکار و رایگان</strong></td>
    <td>کل سیستم با یک فایل Workflow روی GitHub Actions رایگان اجرا می‌شود و نیازی به هیچ سرور خارجی ندارد.</td>
</tr>
</tbody>
</table>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- چرا بدون فوروارد -->
<h2>⚠️ چرا «فوروارد واقعی» در این پروژه وجود ندارد؟</h2>
<p>
فوروارد واقعیِ یک پیام از کانال‌های دلخواهِ دیگران فقط با یک <strong>اکانت کاربری واقعی</strong> (Userbot، مثل Telethon) ممکن است — یعنی وارد کردن شماره تلفن شخصی و ریسک محدودیت (Flood) یا بن آن اکانت. چون این ریسک قابل قبول نیست، این پروژه به‌طور کامل از آن روش صرف‌نظر کرده و در عوض:
</p>
<ul>
    <li><strong>جمع‌آوری</strong> فقط با درخواست HTTP ساده به صفحهٔ عمومی <code>t.me/s/...</code> انجام می‌شود (بدون لاگین، بدون عضویت، بدون شماره تلفن).</li>
    <li><strong>ارسال</strong> فقط <strong>لینک</strong> پیام اصلی (نه خودِ فایل) از طریق یک <strong>بات تلگرامی معمولی</strong> صورت می‌گیرد — دقیقاً همان روشی که پروژهٔ <code>Telegram</code> شما (<code>version_checker.py</code>) با <code>BOT_TOKEN</code> و <code>CHANNEL_ID</code> استفاده می‌کند.</li>
</ul>
<p>نتیجه: هیچ اکانت شخصی‌ای در معرض ریسک نیست؛ فقط یک بات معمولی (که خودتان از BotFather می‌سازید) به کانال خودتان پیام می‌فرستد.</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- نیازمندی‌ها -->
<h2>📦 پیش‌نیازها (Requirements)</h2>
<ul>
    <li><strong>Git</strong> نصب شده روی سیستم (برای clone کردن مخزن)</li>
    <li>Python 3.10 یا بالاتر</li>
    <li>
        کتابخانه‌های موجود در <code>requirements.txt</code>:
        <pre class="ltr-block">pip install -r config/requirements.txt</pre>
    </li>
    <li>یک بات تلگرام از <a href="https://t.me/BotFather" target="_blank">@BotFather</a> (بدون نیاز به شماره تلفن شخصی جداگانه)</li>
    <li>یک کانال تلگرامی مقصد که بات در آن دسترسی «ارسال پیام» (ادمین) داشته باشد</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- تنظیمات -->
<h2>⚙️ تنظیمات (Configuration)</h2>
<p>تمام پارامترهای کلیدی به‌صورت متغیر محیطی در ابتدای فایل <code>src/npvt_collector.py</code> قابل تنظیم هستند:</p>

<table>
<thead>
<tr><th>پارامتر</th><th>مقدار پیش‌فرض</th><th>توضیح</th></tr>
</thead>
<tbody>
<tr><td><code>BOT_TOKEN</code></td><td>—</td><td>توکن بات تلگرام (الزامی)</td></tr>
<tr><td><code>TARGET_CHANNEL</code></td><td>—</td><td>یوزرنیم یا آیدی عددی کانال مقصد (الزامی)</td></tr>
<tr><td><code>MAX_PAGES_PER_CHANNEL</code></td><td><code>3</code></td><td>حداکثر تعداد صفحه‌ی عقب‌گرد (<code>?before=</code>) برای رسیدن به چک‌پوینت قبلی</td></tr>
<tr><td><code>SLEEP_BETWEEN_CHANNELS</code></td><td><code>1.5</code></td><td>تاخیر (ثانیه) بین بررسی کانال‌ها</td></tr>
<tr><td><code>SLEEP_BETWEEN_PAGES</code></td><td><code>1</code></td><td>تاخیر (ثانیه) بین صفحات یک کانال</td></tr>
<tr><td><code>SLEEP_BETWEEN_SENDS</code></td><td><code>1.5</code></td><td>تاخیر (ثانیه) بین ارسال پیام‌ها به بات</td></tr>
</tbody>
</table>

<div class="highlight">
<strong>🔐 تنظیم Secrets در گیتهاب:</strong> این مقادیر را در <strong>Settings</strong> &gt; <strong>Secrets and variables</strong> &gt; <strong>Actions</strong> تعریف کنید:
<pre class="ltr-block">
BOT_TOKEN         → توکن باتی که از BotFather گرفتید
TARGET_CHANNEL    → یوزرنیم (مثل npvt_backup@) یا آیدی عددی (مثل 100xxxxxxxxxx-) کانال مقصد
</pre>
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- راه‌اندازی سریع -->
<h2>🧩 راه‌اندازی سریع (Quick Start)</h2>
<p>اگر می‌خواهید همین پروژه را برای خودتان کپی و اجرا کنید:</p>
<ol>
    <li>مخزن را Fork کنید (دکمه Fork در بالای صفحه گیتهاب)</li>
    <li>مخزن Fork شده را Clone کنید:
        <pre class="ltr-block">git clone https://github.com/YOUR_USERNAME/npvt-collector.git
cd npvt-collector</pre>
    </li>
    <li>نیازمندی‌های پایتون را نصب کنید:
        <pre class="ltr-block">pip install -r config/requirements.txt</pre>
    </li>
    <li>فایل <code>.env</code> را مطابق <code>config/.env.example</code> با <code>BOT_TOKEN</code> و <code>TARGET_CHANNEL</code> خودتان ایجاد کنید.</li>
    <li>فایل <code>data/channels.txt</code> را با یوزرنیم کانال‌های تلگرامی مبدأ (که فایل <code>.npvt</code> منتشر می‌کنند) پر کنید.</li>
    <li>یک بار اسکریپت را به‌صورت دستی اجرا کنید تا همه‌چیز تست شود:
        <pre class="ltr-block">python src/npvt_collector.py</pre>
    </li>
</ol>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- اجرای خودکار -->
<h2>🤖 راه‌اندازی اجرای خودکار با GitHub Actions</h2>

<h3>۱. فایل Workflow</h3>
<p>پروژه به‌صورت پیش‌فرض با یک فایل YAML در مسیر <code>.github/workflows/collector.yml</code> اجرا می‌شود که:</p>
<ul>
    <li>به‌صورت <strong>ساعتی</strong> (<code>cron</code>) و همچنین با <strong>workflow_dispatch</strong> (اجرای دستی) قابل اجراست.</li>
    <li>تمام کانال‌های <code>data/channels.txt</code> را اسکن می‌کند.</li>
    <li>موارد تکراری را حذف و لینک فایل‌های جدید را به کانال مقصد ارسال می‌کند.</li>
    <li>در پایان، فایل‌های وضعیت (چک‌پوینت، آرشیو ضدتکرار، گزارش) را در مخزن commit می‌کند.</li>
</ul>

<h3>۲. افزودن کانال‌های مبدأ</h3>
<p>فایل <code>data/channels.txt</code> فهرست کانال‌های عمومی تلگرام را نگهداری می‌کند (هر خط یک یوزرنیم، بدون <code>@</code>). برای افزودن کانال جدید، کافیست یوزرنیم آن را در یک خط جدید اضافه کنید — نیازی به عضویت یا هیچ دسترسی خاصی نیست.</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- ساختار فایل‌ها -->
<h2>🗂️ ساختار فایل‌های پروژه</h2>
<pre class="ltr-block">
.
├── .github/
│   └── workflows/
│       └── collector.yml          # گردش‌کار اصلی (اجرای ساعتی + commit خودکار وضعیت)
│
├── src/
│   └── npvt_collector.py          # اسکریپت اصلی (اسکن + حذف تکراری + ارسال لینک)
│
├── config/
│   ├── requirements.txt           # وابستگی‌های پایتون
│   ├── .gitignore                 # فایل‌های نادیده گرفته‌شده
│   └── .env.example               # نمونه فایل متغیرهای محیطی
│
├── data/                          # فایل‌های داده و گزارش‌ها
│   ├── channels.txt               # فهرست کانال‌های تلگرام (ورودی)
│   ├── last_message_id.json       # (تولیدشده) آخرین message_id بررسی‌شده هر کانال
│   ├── seen_files.json            # (تولیدشده) آرشیو فایل‌های قبلاً ارسال‌شده (نام+حجم)
│   └── npvt_report.txt            # (تولیدشده) گزارش خلاصه‌ی هر اجرا
│
├── line.gif                       # جداکننده متحرک برای README
├── README.md                      # مستندات فارسی
└── README.EN.md                   # مستندات انگلیسی
</pre>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- مقایسه -->
<h2>📊 مقایسه با روش‌های رایج (فوروارد با Userbot)</h2>
<table>
<thead>
<tr><th>معیار</th><th>این پروژه</th><th>روش‌های مبتنی بر Userbot (Telethon/Pyrogram)</th></tr>
</thead>
<tbody>
<tr><td><strong>نیاز به شماره تلفن</strong></td><td>❌ ندارد</td><td>✅ لازم است</td></tr>
<tr><td><strong>ریسک بن/Flood اکانت شخصی</strong></td><td>❌ وجود ندارد</td><td>⚠️ همیشه وجود دارد</td></tr>
<tr><td><strong>نیاز به عضویت در کانال مبدأ</strong></td><td>❌ ندارد</td><td>معمولاً بله</td></tr>
<tr><td><strong>روش دریافت محتوا</strong></td><td>صفحهٔ عمومی وب (<code>t.me/s</code>)</td><td>MTProto API</td></tr>
<tr><td><strong>نوع تحویل به کانال مقصد</strong></td><td>پیام لینک (Bot API)</td><td>فوروارد واقعی پیام</td></tr>
<tr><td><strong>پیچیدگی راه‌اندازی</strong></td><td>یک بات ساده از BotFather</td><td>ساخت Session، لاگین با کد تایید</td></tr>
</tbody>
</table>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- خطاهای رایج -->
<h2>❗ خطاهای رایج و راه‌حل</h2>

<details>
<summary><strong>خطای «BOT_TOKEN و/یا TARGET_CHANNEL تنظیم نشده است»</strong></summary>
<p>مطمئن شوید هر دو Secret با نام‌های <code>BOT_TOKEN</code> و <code>TARGET_CHANNEL</code> در <strong>Settings → Secrets and variables → Actions</strong> به‌درستی تنظیم شده‌اند.</p>
</details>

<details>
<summary><strong>پیام لینک به کانال مقصد ارسال نمی‌شود</strong></summary>
<ul>
    <li>بررسی کنید که بات <strong>ادمین</strong> کانال مقصد باشد و دسترسی «ارسال پیام» داشته باشد.</li>
    <li><code>TARGET_CHANNEL</code> باید یوزرنیم عمومی (<code>@channel</code>) یا آیدی عددی صحیح (<code>-100...</code>) باشد.</li>
</ul>
</details>

<details>
<summary><strong>فایلی از یک کانال استخراج نمی‌شود</strong></summary>
<ul>
    <li>مطمئن شوید کانال <strong>عمومی</strong> است (کانال‌های خصوصی صفحهٔ <code>t.me/s</code> ندارند).</li>
    <li>یوزرنیم کانال در <code>data/channels.txt</code> را بدون <code>https://t.me/</code> و بدون <code>@</code> وارد کنید.</li>
</ul>
</details>

<details>
<summary><strong>فایل‌های وضعیت (checkpoint/seen_files) به‌روزرسانی نمی‌شوند</strong></summary>
<ul>
    <li>بررسی کنید که مرحلهٔ <code>Commit and push updated state</code> در Workflow بدون خطا اجرا شده باشد.</li>
    <li>مطمئن شوید <code>permissions: contents: write</code> در فایل <code>collector.yml</code> حذف نشده باشد.</li>
</ul>
</details>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- سفارشی‌سازی -->
<h2>🛠️ سفارشی‌سازی</h2>
<ul>
    <li>برای <strong>تغییر فرکانس اجرا</strong>، مقدار <code>cron</code> را در <code>collector.yml</code> ویرایش کنید.</li>
    <li>برای <strong>تغییر متن پیام ارسالی</strong>، تابع <code>send_link_message</code> در <code>src/npvt_collector.py</code> را ویرایش کنید.</li>
    <li>برای <strong>تغییر پسوند فایل هدف</strong> (مثلاً برای پروژه‌ای مشابه با پسوند دیگر)، مقدار <code>FILE_SUFFIX</code> را تغییر دهید.</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- مشارکت -->
<h2>🙏 مشارکت و توسعه</h2>
<p>
پیشنهادات، گزارش باگ‌ها، یا کانال‌های تلگرام جدید برای افزودن به فایل <code>channels.txt</code> را می‌توانید از طریق <strong>Pull Request</strong> یا <strong>Issue</strong> به اشتراک بگذارید.<br>
برای توسعه‌دهندگان: لطفاً پیش از ارسال تغییرات، یک اجرای آزمایشی روی سیستم خود انجام دهید.
</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- قدردانی -->
<h2>💡 قدردانی</h2>
<p>ایده‌ی استفاده از <code>t.me/s</code> برای دسترسی به کانال‌های تلگرام بدون نیاز به API، از پروژه‌های قبلی خودِ شما — <code>V2ray-Collector</code> و <code>news-monitor</code> — الهام گرفته شده است.</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- مجوز -->
<h2>📄 مجوز</h2>
<p>این پروژه تحت مجوز <strong>MIT</strong> منتشر شده است. استفاده، ویرایش و توزیع آزاد است.</p>

</div>

<!-- keywords: npvt collector, npv tunnel config, telegram file collector,
     t.me/s scraper, github actions collector, telegram bot forwarder,
     جمع آوری فایل تلگرام, کانفیگ NPV Tunnel, ربات تلگرام لینک -->

</body>
</html>
