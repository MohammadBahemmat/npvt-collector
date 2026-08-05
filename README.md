<!-- README.md (نسخه فارسی) -->
<div align="center" style="margin-bottom: 20px;">
  <a href="https://github.com/MohammadBahemmat/npvt-collector/blob/main/README.EN.md">
    <img src="https://img.shields.io/badge/Read_in-English-009688?style=for-the-badge&logo=readthedocs" alt="Read in English">
  </a>
</div>

<body>
<div class="container">

<div align="center" style="margin-bottom: 15px;">

<img src="https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge&logo=open-source-initiative" alt="License">
<a href="https://github.com/MohammadBahemmat/npvt-collector/blob/main/config/requirements.txt">
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
هر فایل جدید بر اساس <strong>نام + حجم</strong> با فایل‌های قبلاً دیده‌شده مقایسه و در صورت تکراری بودن حذف می‌شود؛ سپس حداکثر ۱۰ فایل یکتای جدیدترین (بر اساس زمان انتشار در کانال مبدأ) در یک پیام، از طریق یک <strong>بات تلگرامی معمولی</strong> به کانال دلخواه شما ارسال می‌شود.
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
    <td><strong>🕐 زمان‌بندی دقیق ساعتی</strong></td>
    <td>با <code>cron</code> استاندارد گیت‌هاب اکشن، راس هر ساعت اجرا می‌شود — ساده، قابل‌اعتماد، و بدون نیاز به هیچ Secret اضافه‌ای.</td>
</tr>
<tr>
    <td><strong>📄 استخراج نام، حجم و زمان انتشار</strong></td>
    <td>برای هر فایل <code>.npvt</code>، نام، حجم (همان‌طور که خودِ تلگرام نمایش می‌دهد) و زمان دقیق انتشار پیام در کانال مبدأ استخراج می‌شود.</td>
</tr>
<tr>
    <td><strong>🧹 حذف هوشمند موارد تکراری</strong></td>
    <td>فقط زمانی که <strong>هم نام و هم حجم</strong> یک فایل با فایلی دیگر (در همین کانال، کانالی دیگر، یا اجرای قبلی) یکسان باشد، تکراری در نظر گرفته و حذف می‌شود.</td>
</tr>
<tr>
    <td><strong>🔟 حداکثر ۱۰ فایل، همیشه جدیدترین‌ها</strong></td>
    <td>اگر بیش از ۱۰ فایل جدید در یک اجرا پیدا شود، فقط ۱۰ تای جدیدترین (بر اساس زمان انتشار) ارسال می‌شود؛ بقیه طبق دستور صریح شما کاملاً کنار گذاشته می‌شوند — نه در صف اجرای بعدی.</td>
</tr>
<tr>
    <td><strong>📤 ارسال با بات معمولی تلگرام</strong></td>
    <td>یک پیام هدر (بولد) و بلافاصله بعد از آن یک پیام حاوی فهرست فایل‌های هایپرلینک‌شده ارسال می‌شود؛ بات فقط باید در کانال مقصد خودتان ادمین باشد.</td>
</tr>
<tr>
    <td><strong>🚫 فیلتر نام فایل</strong></td>
    <td>فایل‌هایی که نامشان حاوی کلیدواژه‌های تعریف‌شده در <code>data/blocked_keywords.txt</code> باشد، اصلاً جمع‌آوری یا منتشر نمی‌شوند؛ فهرست آن‌ها فقط برای شفافیت در <code>data/filtered_files.txt</code> ثبت می‌شود.</td>
</tr>
<tr>
    <td><strong>📈 گزارش وضعیت هر کانال (مثل V2ray-Collector)</strong></td>
    <td><code>data/channel_report.txt</code> نشان می‌دهد در هر اجرا از هر کانال چند فایل <code>.npvt</code> پیدا شده؛ کانال‌های غیرقابل‌دسترسی هم در <code>data/invalid_channels.txt</code> فهرست می‌شوند.</td>
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
فوروارد واقعیِ پیام از کانال‌های دلخواهِ دیگران فقط با یک <strong>اکانت کاربری واقعی</strong> (Userbot، مثل Telethon) ممکن است — یعنی وارد کردن شماره تلفن شخصی و ریسک محدودیت (Flood) یا بن آن اکانت. چون این ریسک قابل قبول نیست، این پروژه به‌طور کامل از آن روش صرف‌نظر کرده و در عوض:
</p>
<ul>
    <li><strong>جمع‌آوری</strong> فقط با درخواست HTTP ساده به صفحهٔ عمومی <code>t.me/s/...</code> انجام می‌شود (بدون لاگین، بدون عضویت، بدون شماره تلفن).</li>
    <li><strong>ارسال</strong> فقط <strong>لینک</strong> پیام اصلی (نه خودِ فایل) از طریق یک <strong>بات تلگرامی معمولی</strong> صورت می‌گیرد — دقیقاً همان روشی که پروژهٔ <code>Telegram</code> شما (<code>version_checker.py</code>) با <code>BOT_TOKEN</code> و <code>CHANNEL_ID</code> استفاده می‌کند.</li>
</ul>
<p>نتیجه: هیچ اکانت شخصی‌ای در معرض ریسک نیست؛ فقط یک بات معمولی (که خودتان از BotFather می‌سازید) به کانال خودتان پیام می‌فرستد.</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- فیلتر کلیدواژه‌ای -->
<h2>🚫 فیلتر کلیدواژه‌ای نام فایل</h2>
<p>
فایلی که نامش حاوی هر یک از کلیدواژه‌های زیر باشد، اصلاً جمع‌آوری یا منتشر نمی‌شود — نه فوروارد و نه حتی لینکش. این کلیدواژه‌ها در <code>data/blocked_keywords.txt</code> نگه‌داری می‌شوند (در اولین اجرا، اگر این فایل وجود نداشته باشد، خودکار با همین فهرست پیش‌فرض ساخته می‌شود):
</p>
<pre class="ltr-block" dir="rtl">
جاوید، جاویدنام، جاوید نام، شاه، آریامهر، آریا مهر، پهلوی،
خمینی، خامنه ای، خامنه‌ای، سیدعلی، سید علی، مجتبی
</pre>
<ul>
    <li><strong>ویرایش فهرست:</strong> کافیست <code>data/blocked_keywords.txt</code> را باز کنید و هر کلیدواژه را در یک خط جدید اضافه یا حذف کنید (خط‌هایی که با <code>#</code> شروع می‌شوند نادیده گرفته می‌شوند). نیازی به تغییر کد پایتون نیست.</li>
    <li><strong>تطبیق مستقل از فاصله‌گذاری:</strong> تفاوت بین «خامنه‌ای» (با نیم‌فاصله)، «خامنه ای» (با فاصله) و «خامنهای» (چسبیده) نادیده گرفته می‌شود؛ هر سه حالت یکسان تشخیص داده می‌شوند.</li>
    <li><strong>تطبیق substring است</strong>، نه فقط کلمه‌ی کامل: یعنی اگر کلیدواژه‌ی «شاه» فعال باشد، فایلی به نام «شاهین.npvt» هم فیلتر می‌شود، چون این کلمه را در خود دارد. این یک محدودیت شناخته‌شده و عمدی است (برای اطمینان بیشتر، حتی به قیمت فیلتر شدن گاه‌به‌گاه یک نام بی‌ربط).</li>
    <li>هر فایلی که فیلتر شود، در <code>data/filtered_files.txt</code> ثبت می‌شود (فقط برای شفافیت و بررسی؛ این فایل‌ها هیچ‌وقت به کانال مقصد ارسال نمی‌شوند).</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- فرمت پیام ارسالی -->
<h2>📨 فرمت پیام‌های ارسالی</h2>
<p>هر اجرا، در صورت داشتن فایل جدید برای ارسال، دقیقاً <strong>دو پیام</strong> به کانال مقصد می‌فرستد:</p>
<ol>
    <li>یک پیام هدر <strong>بولد</strong>:
        <pre class="ltr-block" dir="rtl">فایل های NPVT جدید 😁👇</pre>
    </li>
    <li>بلافاصله بعد از آن، یک پیام حاوی فهرست فایل‌ها که هرکدام به‌صورت <strong>هایپرلینک</strong> به پیام اصلی در کانال مبدأ است:
        <pre class="ltr-block" dir="rtl">
فایل 1   ← لینک به پیام اصلی
فایل 2   ← لینک به پیام اصلی
...
فایل N   ← تا حداکثر ۱۰ مورد
        </pre>
    </li>
</ol>
<p>
فایل‌ها بر اساس <strong>جدیدترین زمان انتشار در کانال مبدأ</strong> مرتب می‌شوند (فایل ۱ = جدیدترین). اگر در یک اجرا بیش از ۱۰ فایل جدید پیدا شود، فقط ۱۰ تای جدیدترین ارسال می‌شود و بقیه — طبق درخواست صریح — <strong>کاملاً کنار گذاشته می‌شوند</strong>؛ نه در صفِ اجرای بعدی می‌مانند و نه دوباره بررسی می‌شوند. اگر هیچ فایل جدیدی پیدا نشود، هیچ پیامی (نه هدر، نه فهرست) ارسال نمی‌شود.
</p>
<div class="highlight">
تنها استثنا: اگر ارسال یکی از این دو پیام به‌خاطر خطای واقعی (نه سرریز سقف ۱۰ تایی) شکست بخورد — مثلاً قطعی موقت شبکه یا محدودیت نرخ تلگرام — کل آن دسته در <code>data/pending_send.json</code> ذخیره و در اجرای بعدی، <strong>پیش از</strong> فایل‌های تازه‌یاب، دوباره تلاش می‌شود.
</div>

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
<tr><td><code>SLEEP_BETWEEN_SENDS</code></td><td><code>2</code></td><td>تاخیر (ثانیه) بین پیام هدر و پیام فهرست فایل‌ها</td></tr>
<tr><td><code>REQUEST_TIMEOUT</code></td><td><code>10</code></td><td>حداکثر زمان انتظار (ثانیه) برای هر درخواست HTTP قبل از شکست خوردن</td></tr>
<tr><td><code>MAX_SEND_RETRIES</code></td><td><code>6</code></td><td>حداکثر تعداد تلاش دوباره برای ارسال یک پیام، وقتی تلگرام خطای 429 (محدودیت نرخ) برمی‌گرداند</td></tr>
<tr><td><code>MAX_RETRY_AFTER_WAIT</code></td><td><code>90</code></td><td>حداکثر زمانی (ثانیه) که برای هر تلاش دوباره صبر می‌شود، حتی اگر تلگرام عدد بزرگ‌تری بخواهد</td></tr>
<tr><td><code>MAX_FILES_PER_MESSAGE</code></td><td><code>10</code></td><td>حداکثر تعداد فایل در هر اجرا؛ مازاد بر این، بدون قید و شرط کنار گذاشته می‌شود (نه در صف)</td></tr>
</tbody>
</table>

<div class="highlight">
<strong>🔐 تنظیم Secrets در گیتهاب:</strong> فقط همین دو مورد لازم است — در <strong>Settings</strong> &gt; <strong>Secrets and variables</strong> &gt; <strong>Actions</strong> تعریف کنید:
<pre class="ltr-block">
BOT_TOKEN         → توکن باتی که از BotFather گرفتید
TARGET_CHANNEL    → یوزرنیم (مثل npvt_backup@) یا آیدی عددی (مثل 100xxxxxxxxxx-) کانال مقصد
</pre>
هیچ Secret دیگری (مثل Personal Access Token) لازم نیست.
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- راه‌اندازی سریع -->
<h2>🧩 راه‌اندازی سریع (Quick Start)</h2>
<p>اگر می‌خواهید همین پروژه را برای خودتان کپی و اجرا کنید:</p>
<ol>
    <li>مخزن را Fork کنید (دکمه Fork در بالای صفحه گیتهاب)</li>
    <li>مخزن Fork شده را Clone کنید:
        <pre class="ltr-block">git clone https://github.com/MohammadBahemmat/npvt-collector.git
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

<h3>۱. فایل Workflow (زمان‌بندی ساعتی با Cron)</h3>
<p>پروژه با یک فایل YAML در مسیر <code>.github/workflows/collector.yml</code> اجرا می‌شود که:</p>
<ul>
    <li>راس هر ساعت (<code>cron: '0 * * * *'</code>) خودکار اجرا می‌شود، و همچنین از تب Actions به‌صورت دستی (<strong>Run workflow</strong>) هم قابل اجراست.</li>
    <li>تمام کانال‌های <code>data/channels.txt</code> را اسکن می‌کند.</li>
    <li>موارد تکراری را حذف، حداکثر ۱۰ فایل جدیدترین را انتخاب و به کانال مقصد ارسال می‌کند.</li>
    <li>فایل‌های وضعیت (چک‌پوینت، آرشیو ضدتکرار، <code>channel_report.txt</code>، <code>invalid_channels.txt</code>) را در مخزن commit می‌کند.</li>
</ul>

<div class="highlight">
<strong>⏱️ دربارهٔ دقت زمان‌بندی:</strong> طبق مستندات خودِ گیت‌هاب، <code>schedule</code> ممکن است در بازه‌های پرترافیک تا چند دقیقه دیرتر از زمان دقیق (<code>0 * * * *</code>) واقعاً اجرا شود — این یک محدودیت پلتفرم گیت‌هاب است و از طریق تنظیمات این پروژه قابل حذف نیست. برای کاربردی مثل این (اسکن ساعتیِ چند کانال)، این مقدار تأخیر معمولاً بی‌اهمیت است. اگر دقت مطلق برایتان حیاتی است، تنها راه‌حل واقعی، اجرای زمان‌بندی‌شده روی یک سرور خودتان (مثل یک VPS با <code>cron</code> واقعی) است، نه GitHub Actions.
</div>

<h3>۲. افزودن کانال‌های مبدأ</h3>
<p>فایل <code>data/channels.txt</code> فهرست کانال‌های عمومی تلگرام را نگهداری می‌کند (هر خط یک یوزرنیم، بدون <code>@</code>). برای افزودن کانال جدید، کافیست یوزرنیم آن را در یک خط جدید اضافه کنید — نیازی به عضویت یا هیچ دسترسی خاصی نیست.</p>

<h3>۳. گزارش وضعیت هر کانال</h3>
<p>پس از هر اجرا، دو فایل زیر در <code>data/</code> به‌روزرسانی می‌شوند:</p>
<ul>
    <li><code>channel_report.txt</code> — به ازای هر کانال، تاریخچه‌ی تعداد فایل <code>.npvt</code> پیدا‌شده در هر اجرا را (به ترتیب، جدا شده با کاما) نشان می‌دهد؛ مثلاً <code>napsternetv_file: 2, 0, 1</code> یعنی در سه اجرای اخیر، به ترتیب ۲، ۰ و ۱ فایل جدید پیدا شده است.</li>
    <li><code>invalid_channels.txt</code> — فهرست به‌روزِ کانال‌هایی که آخرین‌باری که تست شدند قابل خواندن نبودند (کانال وجود ندارد، خصوصی است، یا مسدود شده). در <code>channel_report.txt</code> هم این کانال‌ها با مقدار <code>ERR</code> مشخص می‌شوند.</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- ساختار فایل‌ها -->
<h2>🗂️ ساختار فایل‌های پروژه</h2>
<pre class="ltr-block">
.
├── .github/
│   └── workflows/
│       └── collector.yml          # گردش‌کار اصلی (زمان‌بندی ساعتی + commit خودکار وضعیت)
│
├── src/
│   └── npvt_collector.py          # اسکریپت اصلی (اسکن + حذف تکراری + ارسال)
│
├── config/
│   ├── requirements.txt           # وابستگی‌های پایتون
│   ├── .gitignore                 # فایل‌های نادیده گرفته‌شده
│   └── .env.example               # نمونه فایل متغیرهای محیطی
│
├── data/                          # فایل‌های داده و گزارش‌ها
│   ├── channels.txt               # فهرست کانال‌های تلگرام (ورودی)
│   ├── blocked_keywords.txt       # فهرست کلیدواژه‌های مسدود (ورودی؛ در اولین اجرا خودکار ساخته می‌شود)
│   ├── last_message_id.json       # (تولیدشده) آخرین message_id بررسی‌شده هر کانال
│   ├── seen_files.json            # (تولیدشده) آرشیو فایل‌های قبلاً ارسال‌شده (نام+حجم+زمان)
│   ├── pending_send.json          # (تولیدشده) صف فایل‌هایی که به‌خاطر خطای واقعی ارسال نشده‌اند
│   ├── npvt_report.txt            # (تولیدشده) گزارش خلاصه‌ی هر اجرا
│   ├── channel_report.txt         # (تولیدشده) تاریخچه‌ی تعداد فایل یافت‌شده به ازای هر کانال
│   ├── invalid_channels.txt       # (تولیدشده) کانال‌های نامعتبر/غیرقابل‌دسترسی در آخرین اجرا
│   └── filtered_files.txt         # (تولیدشده) فایل‌هایی که به‌خاطر کلیدواژه‌ی مسدود منتشر نشدند
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
<summary><strong>پیام‌ها به کانال مقصد ارسال نمی‌شوند</strong></summary>
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

<details>
<summary><strong>در لاگ خطای <code>429 Too Many Requests</code> می‌بینم</strong></summary>
<ul>
    <li>چون هر اجرا فقط ۲ پیام (هدر + فهرست) می‌فرستد، این خطا خیلی بعید است؛ اگر دیدید، خودکار مدیریت می‌شود: اسکریپت دقیقاً به‌اندازه‌ی <code>retry_after</code> اعلام‌شده توسط تلگرام صبر و دوباره تلاش می‌کند (تا <code>MAX_SEND_RETRIES</code> بار).</li>
    <li>اگر پس از همه‌ی تلاش‌ها هم ارسال نشود، پیام <strong>گم نمی‌شود</strong> — در <code>data/pending_send.json</code> ذخیره و در اجرای بعدی دوباره امتحان می‌شود.</li>
</ul>
</details>

<details>
<summary><strong>یک فایل که انتظار داشتم ارسال بشه، نیومد</strong></summary>
<ul>
    <li>اول <code>data/filtered_files.txt</code> را چک کنید — اگر نام فایل حاوی یکی از کلیدواژه‌های <code>data/blocked_keywords.txt</code> باشد، عمداً منتشر نشده است.</li>
    <li>بعد <code>data/seen_files.json</code> را بررسی کنید؛ اگر فایلی با همان نام+حجم قبلاً از کانال دیگری ارسال شده باشد، تکراری محسوب و رد می‌شود.</li>
    <li>اگر در یک اجرا بیش از ۱۰ فایل جدید پیدا شده باشد و این فایل جزو ۱۰ تای جدیدترین نبوده، <strong>کاملاً کنار گذاشته شده</strong> و اصلاً ارسال نخواهد شد — این رفتار طبق درخواست صریح است، نه یک باگ.</li>
    <li>در غیر این صورت، <code>data/pending_send.json</code> را چک کنید — ممکن است هنوز در صف ارسال (به‌خاطر یک خطای واقعی) باشد.</li>
</ul>
</details>

<details>
<summary><strong>کانالی همیشه در <code>channel_report.txt</code> مقدار <code>ERR</code> نشان می‌دهد</strong></summary>
<ul>
    <li>یعنی آن کانال در آخرین اجرا اصلاً قابل خواندن نبوده — معمولاً چون یوزرنیم اشتباه است، کانال حذف/خصوصی شده، یا موقتاً توسط تلگرام محدود شده.</li>
    <li>یوزرنیم را در مرورگر با آدرس <code>https://t.me/s/&lt;username&gt;</code> تست کنید؛ اگر صفحه‌ای باز نشد یا خالی بود، همان کانال در <code>data/invalid_channels.txt</code> هم لیست خواهد شد.</li>
</ul>
</details>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- سفارشی‌سازی -->
<h2>🛠️ سفارشی‌سازی</h2>
<ul>
    <li>برای <strong>تغییر فرکانس اجرا</strong>، مقدار <code>cron</code> را در <code>collector.yml</code> ویرایش کنید (مثلاً <code>'0 */2 * * *'</code> برای هر دو ساعت).</li>
    <li>برای <strong>تغییر تعداد فایل در هر اجرا</strong>، <code>MAX_FILES_PER_MESSAGE</code> را در <code>config/.env.example</code> یا Secrets تغییر دهید.</li>
    <li>برای <strong>تغییر متن هدر یا فرمت پیام</strong>، مقدار <code>HEADER_TEXT</code> و تابع <code>build_file_list_message</code> در <code>src/npvt_collector.py</code> را ویرایش کنید.</li>
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
     t.me/s scraper, github actions collector, telegram bot,
     جمع آوری فایل تلگرام, کانفیگ NPV Tunnel, ربات تلگرام لینک -->

</body>
</html>
