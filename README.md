<!-- README.md (نسخه فارسی) -->
<div align="center" style="margin-bottom: 18px;">
  <a href="https://github.com/MohammadBahemmat/npvt-collector/blob/main/README.EN.md">
    <img src="https://img.shields.io/badge/Read_in-English-009688?style=for-the-badge&logo=readthedocs" alt="Read in English">
  </a>
</div>

<body>
<div class="container">

<div align="center" style="margin-bottom: 14px;">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative" alt="License">
  <a href="https://github.com/MohammadBahemmat/npvt-collector/blob/main/config/requirements.txt">
    <img src="https://img.shields.io/badge/Requirements-txt-critical?style=for-the-badge&logo=pypi" alt="Requirements">
  </a>
  <img src="https://img.shields.io/badge/Platform-GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions" alt="GitHub Actions">
  <img src="https://img.shields.io/badge/No_Login_Required-Telegram_Account-critical?style=for-the-badge&logo=telegram" alt="No Login Required">
</div>

<p align="center">
  <img src="https://github.com/MohammadBahemmat/npvt-collector/actions/workflows/collector.yml/badge.svg" alt="Collector Status">
</p>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h1>📦 NPVT Collector — جمع‌آوری فایل‌های <code>.npvt</code> از تلگرام</h1>

<p>
<strong>یک جمع‌آورندهٔ مبتنی بر وب برای فایل‌های <code>.npvt</code> (کانفیگ‌های NPVT / NPV Tunnel) در کانال‌های عمومی تلگرام.</strong><br>
این پروژه فقط صفحهٔ پیش‌نمایش عمومی هر کانال (<code>t.me/s</code>) را می‌خواند، فایل‌های <code>.npvt</code> را پیدا می‌کند، نام و حجم و زمان انتشار آن‌ها را استخراج می‌کند، موارد تکراری را بر اساس <strong>نام نرمال‌شده + حجم</strong> حذف می‌کند، و در نهایت جدیدترین فایل‌ها را با یک <strong>بات معمولی تلگرام</strong> به‌صورت لینک به کانال مقصد می‌فرستد.
</p>

<div class="highlight">
<strong>هدف پروژه:</strong> جمع‌آوری، پاک‌سازی، حذف موارد تکراری و انتشار لینک. نه لاگین اکانت شخصی، نه شماره تلفن، نه Userbot، نه فوروارد واقعی فایل.
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>✨ این پروژه دقیقاً چه کار می‌کند؟</h2>

<table>
<thead>
<tr><th>بخش</th><th>توضیح</th></tr>
</thead>
<tbody>
<tr>
  <td><strong>اسکن کانال‌های عمومی</strong></td>
  <td>فقط از صفحات عمومی تلگرام (<code>t.me/s/&lt;channel&gt;</code>) داده می‌گیرد؛ بدون لاگین، بدون عضویت.</td>
</tr>
<tr>
  <td><strong>استخراج فایل</strong></td>
  <td>پیام‌هایی را که فایل با پسوند <code>.npvt</code> دارند پیدا می‌کند و نام، حجم و زمان دقیق انتشار را ذخیره می‌کند.</td>
</tr>
<tr>
  <td><strong>فیلتر نام فایل</strong></td>
  <td>فایل‌هایی که نامشان حاوی کلیدواژه‌های <code>data/blocked_keywords.txt</code> باشد، اصلاً جمع‌آوری یا منتشر نمی‌شوند.</td>
</tr>
<tr>
  <td><strong>حذف تکراری‌ها</strong></td>
  <td>اگر <strong>نام نرمال‌شده</strong> و <strong>حجم</strong> دو فایل یکی باشد (حتی از دو کانال متفاوت)، فقط یکی نگه داشته می‌شود.</td>
</tr>
<tr>
  <td><strong>انتخاب جدیدترین‌ها</strong></td>
  <td>اگر در یک اجرا بیش از حد مجاز فایل جدید پیدا شود، فقط جدیدترین‌ها (بر اساس زمان انتشار در کانال مبدأ) منتشر و بقیه کنار گذاشته می‌شوند.</td>
</tr>
<tr>
  <td><strong>انتشار خروجی</strong></td>
  <td>به‌جای فوروارد فایل، یک پیام هدر و یک پیام حاوی لینک‌های پیام‌های اصلی، با بات تلگرام به کانال مقصد ارسال می‌شود.</td>
</tr>
<tr>
  <td><strong>زمان‌بندی خودکار</strong></td>
  <td>با GitHub Actions و طبق یک زمان‌بندی ثابت (<code>cron</code>) اجرا می‌شود؛ نیاز به سرور جداگانه ندارد.</td>
</tr>
<tr>
  <td><strong>گزارش‌گیری</strong></td>
  <td>خروجی‌های وضعیت هر کانال، کانال‌های نامعتبر، فایل‌های فیلترشده و آرشیو ضدتکرار را نگه می‌دارد.</td>
</tr>
</tbody>
</table>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>📨 فرمت پیام‌های ارسالی</h2>
<p>در هر اجرا، اگر فایل جدیدی برای ارسال وجود داشته باشد، دقیقاً <strong>دو پیام</strong> پشت‌سرهم به کانال مقصد فرستاده می‌شود:</p>
<ol>
  <li>یک پیام هدر (بولد):
    <pre class="ltr-block" dir="rtl">فایل های NPVT جدید 😁👇</pre>
  </li>
  <li>بلافاصله بعد از آن، یک پیام با فهرست فایل‌ها که هرکدام به‌صورت لینک به پیام اصلی در کانال مبدأ است:
    <pre class="ltr-block" dir="rtl">
فایل 1   (لینک به پیام اصلی)
فایل 2   (لینک به پیام اصلی)
...
    </pre>
  </li>
</ol>
<p>
فایل‌ها بر اساس <strong>جدیدترین زمان انتشار</strong> در کانال مبدأ مرتب می‌شوند (فایل ۱ = جدیدترین). تعداد فایل در هر اجرا با <code>MAX_FILES_PER_MESSAGE</code> محدود می‌شود (پیش‌فرض ۱۰ تا). اگر تعداد فایل‌های جدید بیشتر از این سقف باشد، فقط جدیدترین‌ها ارسال و <strong>مابقی برای همیشه کنار گذاشته می‌شوند</strong> — نه در صف اجرای بعدی می‌مانند و نه دوباره بررسی می‌شوند. اگر هیچ فایل جدیدی پیدا نشود، هیچ پیامی ارسال نمی‌شود.
</p>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>⚠️ محدوده و محدودیت‌ها</h2>
<ul>
  <li>این پروژه فقط برای <strong>کانال‌های عمومی</strong> مناسب است. کانال خصوصی صفحهٔ وب عمومی ندارد و در گزارش «نامعتبر» ثبت می‌شود.</li>
  <li>برای خواندن محتوا از <strong>API تلگرام</strong> یا <strong>شماره تلفن شخصی</strong> استفاده نمی‌شود؛ فقط درخواست HTTP معمولی به صفحهٔ عمومی وب.</li>
  <li>خروجی، <strong>لینک‌محور</strong> است؛ یعنی لینک پیام اصلی منتشر می‌شود، نه خودِ فایل.</li>
  <li>در هر اجرا حداکثر تعداد مشخصی فایل (پیش‌فرض ۱۰ تا) منتشر می‌شود؛ مازاد بر آن به‌طور کامل کنار گذاشته می‌شود، نه ذخیره برای بعد.</li>
  <li>فیلتر کلیدواژه‌ای بر اساس تطابق substring است، نه فقط کلمهٔ کامل؛ جزئیات در بخش بعدی.</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🧠 چرا لینک‌محور، نه فوروارد واقعی؟</h2>
<p>
فوروارد واقعی از کانال‌هایی که مال خودتان نیستند، معمولاً به یک اکانت کاربری واقعی (Userbot، مثل Telethon) نیاز دارد — یعنی وارد کردن شماره تلفن شخصی و ریسک محدودیت یا بن آن اکانت. این پروژه عمداً آن مسیر را کنار گذاشته تا بدون هیچ ریسکی برای اکانت شخصی، فقط با یک بات معمولی تلگرام قابل اجرا باشد.
</p>

<table>
<thead>
<tr><th>معیار</th><th>این پروژه</th><th>روش‌های مبتنی بر Userbot</th></tr>
</thead>
<tbody>
<tr><td>نیاز به شماره تلفن</td><td>❌ ندارد</td><td>✅ لازم است</td></tr>
<tr><td>ریسک بن/محدودیت اکانت شخصی</td><td>❌ وجود ندارد</td><td>⚠️ همیشه وجود دارد</td></tr>
<tr><td>نیاز به عضویت در کانال مبدأ</td><td>❌ ندارد</td><td>معمولاً بله</td></tr>
<tr><td>روش دریافت محتوا</td><td>صفحهٔ عمومی وب (<code>t.me/s</code>)</td><td>MTProto API</td></tr>
<tr><td>نوع خروجی در کانال مقصد</td><td>پیام لینک (Bot API)</td><td>فوروارد واقعی پیام</td></tr>
</tbody>
</table>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🚫 فیلتر کلیدواژه‌ای نام فایل</h2>
<p>
فایلی که نامش حاوی هر یک از کلیدواژه‌های زیر باشد، اصلاً جمع‌آوری یا منتشر نمی‌شود. این فهرست در <code>data/blocked_keywords.txt</code> نگه‌داری می‌شود (در اولین اجرا، اگر این فایل وجود نداشته باشد، خودکار با همین مقادیر پیش‌فرض ساخته می‌شود):
</p>
<pre class="ltr-block" dir="rtl">
جاوید، جاویدنام، جاوید نام، شاه، آریامهر، آریا مهر، پهلوی،
خمینی، خامنه ای، خامنه‌ای، سیدعلی، سید علی، مجتبی
</pre>
<ul>
  <li><strong>ویرایش فهرست:</strong> کافیست <code>data/blocked_keywords.txt</code> را باز کنید و هر کلیدواژه را در یک خط جدید اضافه یا حذف کنید (خط‌هایی که با <code>#</code> شروع می‌شوند نادیده گرفته می‌شوند)؛ نیازی به تغییر کد نیست.</li>
  <li><strong>مستقل از فاصله‌گذاری:</strong> «خامنه‌ای» (نیم‌فاصله)، «خامنه ای» (فاصله) و «خامنهای» (چسبیده) یکسان تشخیص داده می‌شوند.</li>
  <li><strong>تطبیق substring است، نه کلمهٔ کامل:</strong> برای مثال اگر کلیدواژهٔ «شاه» فعال باشد، فایلی به نام «شاهین.npvt» هم فیلتر می‌شود، چون این رشته را در خود دارد. این یک محدودیت شناخته‌شده و عمدی است (اولویت با احتیاط بیشتر است، حتی به قیمت فیلتر شدن گاه‌به‌گاه یک نام بی‌ربط).</li>
  <li>هر فایل فیلترشده در <code>data/filtered_files.txt</code> ثبت می‌شود (فقط برای شفافیت؛ این فایل‌ها هیچ‌وقت منتشر نمی‌شوند).</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🚀 مراحل راه‌اندازی</h2>
<ol>
  <li>مخزن را Fork کنید و روی سیستم خود Clone بگیرید.</li>
  <li>وابستگی‌ها را نصب کنید:
    <pre class="ltr-block">pip install -r config/requirements.txt</pre>
  </li>
  <li>یک بات تلگرام از <a href="https://t.me/BotFather" target="_blank">@BotFather</a> بسازید (نیازی به شماره تلفن شخصی جداگانه نیست).</li>
  <li>بات را در کانال مقصد به‌عنوان ادمین با دسترسی «ارسال پیام» اضافه کنید.</li>
  <li>فایل <code>.env</code> را بر اساس <code>config/.env.example</code> بسازید و <code>BOT_TOKEN</code> و <code>TARGET_CHANNEL</code> را تنظیم کنید.</li>
  <li>یوزرنیم کانال‌های مبدأ (بدون <code>@</code>) را در <code>data/channels.txt</code> وارد کنید، هر خط یک کانال.</li>
  <li>در صورت نیاز، <code>data/blocked_keywords.txt</code> را ویرایش کنید.</li>
  <li>یک بار پروژه را دستی اجرا کنید تا خروجی‌ها بررسی شوند:
    <pre class="ltr-block">python src/npvt_collector.py</pre>
  </li>
</ol>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>⚙️ تنظیمات اصلی</h2>
<table>
<thead>
<tr><th>متغیر</th><th>پیش‌فرض</th><th>توضیح</th></tr>
</thead>
<tbody>
<tr><td><code>BOT_TOKEN</code></td><td>—</td><td>توکن بات تلگرام (الزامی)</td></tr>
<tr><td><code>TARGET_CHANNEL</code></td><td>—</td><td>کانال مقصد برای انتشار (الزامی)</td></tr>
<tr><td><code>MAX_FILES_PER_MESSAGE</code></td><td><code>10</code></td><td>حداکثر فایل قابل انتشار در هر اجرا؛ مازاد بر آن کاملاً کنار گذاشته می‌شود</td></tr>
<tr><td><code>MAX_PAGES_PER_CHANNEL</code></td><td><code>3</code></td><td>حداکثر تعداد صفحهٔ عقب‌گرد (<code>?before=</code>) برای رسیدن به چک‌پوینت قبلی هر کانال</td></tr>
<tr><td><code>SLEEP_BETWEEN_CHANNELS</code></td><td><code>1.5</code></td><td>تأخیر (ثانیه) بین بررسی کانال‌ها</td></tr>
<tr><td><code>SLEEP_BETWEEN_PAGES</code></td><td><code>1</code></td><td>تأخیر (ثانیه) بین صفحات یک کانال</td></tr>
<tr><td><code>SLEEP_BETWEEN_SENDS</code></td><td><code>2</code></td><td>تأخیر (ثانیه) بین پیام هدر و پیام فهرست فایل‌ها</td></tr>
<tr><td><code>REQUEST_TIMEOUT</code></td><td><code>10</code></td><td>حداکثر زمان انتظار (ثانیه) برای هر درخواست HTTP</td></tr>
<tr><td><code>MAX_SEND_RETRIES</code></td><td><code>6</code></td><td>حداکثر تعداد تلاش دوباره برای ارسال، هنگام خطای 429 (محدودیت نرخ تلگرام)</td></tr>
<tr><td><code>MAX_RETRY_AFTER_WAIT</code></td><td><code>90</code></td><td>حداکثر زمان انتظار (ثانیه) در هر تلاش دوباره، حتی اگر تلگرام عدد بزرگ‌تری بخواهد</td></tr>
</tbody>
</table>

<div class="highlight">
<strong>Secrets لازم در GitHub Actions:</strong>
<pre class="ltr-block">
BOT_TOKEN
TARGET_CHANNEL
</pre>
فقط همین دو مورد لازم است؛ هیچ Personal Access Token یا Secret دیگری نیاز نیست.
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🤖 اجرای خودکار با GitHub Actions</h2>
<ul>
  <li>Workflow اصلی در <code>.github/workflows/collector.yml</code> قرار دارد و از تب Actions هم به‌صورت دستی (<strong>Run workflow</strong>) قابل اجراست.</li>
  <li>در نسخهٔ فعلی، اجرای خودکار طبق <code>cron: '45 */3 * * *'</code> است؛ یعنی هر ۳ ساعت یک‌بار، در دقیقهٔ ۴۵. برای تغییر فاصلهٔ اجرا، همین مقدار <code>cron</code> را در <code>collector.yml</code> ویرایش کنید.</li>
  <li>پس از هر اجرا، فایل‌های وضعیت و گزارش‌ها (چک‌پوینت هر کانال، آرشیو ضدتکرار، گزارش کانال‌ها، کانال‌های نامعتبر) به‌طور خودکار در مخزن commit می‌شوند.</li>
  <li>اگر ارسال یکی از دو پیام (هدر یا فهرست) به‌خاطر یک خطای واقعی (نه سرریز سقف فایل) شکست بخورد، آن دسته در <code>data/pending_send.json</code> ذخیره و در اجرای بعدی، پیش از فایل‌های تازه‌یاب، دوباره تلاش می‌شود.</li>
</ul>

<div class="highlight">
<strong>دربارهٔ دقت زمان‌بندی:</strong> طبق مستندات خودِ گیت‌هاب، <code>schedule</code> ممکن است در بازه‌های پرترافیک تا چند دقیقه دیرتر از زمان دقیق واقعاً اجرا شود؛ این یک محدودیت پلتفرم گیت‌هاب است، نه چیزی که از تنظیمات این پروژه قابل حذف باشد. برای کاربردی مثل این (اسکن دوره‌ای چند کانال)، این تأخیر معمولاً بی‌اهمیت است.
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🗂️ ساختار پروژه</h2>
<pre class="ltr-block">
.
├── .github/workflows/collector.yml
├── src/npvt_collector.py
├── config/
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── data/
│   ├── channels.txt               # فهرست کانال‌های مبدأ (ورودی)
│   ├── blocked_keywords.txt       # فهرست کلیدواژه‌های مسدود (ورودی)
│   ├── last_message_id.json       # (تولیدشده) چک‌پوینت هر کانال
│   ├── seen_files.json            # (تولیدشده) آرشیو فایل‌های قبلاً منتشرشده
│   ├── pending_send.json          # (تولیدشده) صف فایل‌هایی با خطای واقعی در ارسال
│   ├── channel_report.txt         # (تولیدشده) تاریخچه‌ی تعداد فایل یافت‌شده به ازای هر کانال
│   ├── invalid_channels.txt       # (تولیدشده) کانال‌های نامعتبر/غیرقابل‌دسترسی
│   ├── filtered_files.txt         # (تولیدشده) فایل‌های فیلترشده به‌خاطر کلیدواژه
│   └── npvt_report.txt            # (تولیدشده) گزارش خلاصه‌ی هر اجرا
├── README.md
└── README.EN.md
</pre>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>📊 پروژه‌های مشابه و الهام‌گیری</h2>
<p>
این پروژه از ایده‌های استخراج محتوا از صفحات عمومی تلگرام الهام گرفته است؛ مخصوصاً از پروژه‌های قبلی خودِ مالک این مخزن، <code>V2ray-Collector</code> و <code>news-monitor</code>. تفاوت اصلی این ریپو این است که به‌طور خاص برای فایل‌های <code>.npvt</code> طراحی شده است.
</p>

<h2>🏷️ کلیدواژه‌های پیشنهادی برای GitHub Topics</h2>
<pre class="ltr-block">npvt, napsternetv, npv-tunnel, telegram-scraper, telegram-channel-scraper, public-web-scraping, v2ray-config, vpn-config, github-actions, telegram-bot</pre>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>❓ سوالات رایج</h2>

<details>
<summary><strong>چرا فایل‌ها فوروارد نمی‌شوند و فقط لینک ارسال می‌شود؟</strong></summary>
<p>فوروارد واقعی از کانال‌های دیگران فقط با یک اکانت کاربری واقعی ممکن است که ریسک بن دارد. این پروژه عمداً از آن روش صرف‌نظر کرده تا بدون هیچ ریسکی برای هیچ اکانت شخصی، فقط با یک بات معمولی اجرا شود.</p>
</details>

<details>
<summary><strong>آیا کانال خصوصی هم پشتیبانی می‌شود؟</strong></summary>
<p>خیر. این پروژه فقط برای کانال‌های عمومی است، چون فقط از صفحهٔ پیش‌نمایش عمومی وب تلگرام می‌خواند.</p>
</details>

<details>
<summary><strong>اگر یک فایل تکراری باشد چه می‌شود؟</strong></summary>
<p>اگر نام نرمال‌شده و حجم فایل با فایلی که قبلاً منتشر شده یکی باشد (حتی از کانال دیگری)، آن فایل تکراری تشخیص داده و رد می‌شود.</p>
</details>

<details>
<summary><strong>چرا بعضی فایل‌ها هیچ‌وقت منتشر نمی‌شوند؟</strong></summary>
<p>اگر در یک اجرا تعداد فایل‌های جدید بیشتر از سقف <code>MAX_FILES_PER_MESSAGE</code> (پیش‌فرض ۱۰) باشد، فقط جدیدترین‌ها منتشر می‌شوند و بقیه <strong>برای همیشه</strong> کنار گذاشته می‌شوند. این معمولاً در اولین اجرا یا بعد از افزودن چند کانال پرحجم بیشتر دیده می‌شود و رفتاری عمدی است، نه خطا.</p>
</details>

<details>
<summary><strong>اگر کانالی باز نشود چه اتفاقی می‌افتد؟</strong></summary>
<p>آن کانال در <code>data/invalid_channels.txt</code> و با مقدار <code>ERR</code> در <code>data/channel_report.txt</code> ثبت می‌شود.</p>
</details>

<details>
<summary><strong>آیا امکان تغییر فرکانس اجرا هست؟</strong></summary>
<p>بله. مقدار <code>cron</code> در <code>.github/workflows/collector.yml</code> را ویرایش کنید؛ مقدار فعلی <code>'45 */3 * * *'</code> یعنی هر ۳ ساعت یک‌بار.</p>
</details>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>📝 مجوز</h2>
<p>این پروژه تحت مجوز MIT منتشر شده است.</p>

</div>

<!-- keywords: npvt collector, npv tunnel, telegram file collector, t.me/s scraper, telegram bot, github actions -->
</body>
</html>
