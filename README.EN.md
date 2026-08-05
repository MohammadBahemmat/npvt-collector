<!-- README.EN.md -->
<div align="center" style="margin-bottom: 20px;">
  <a href="https://github.com/MohammadBahemmat/npvt-collector/blob/main/README.md">
    <img src="https://img.shields.io/badge/Read_in-Farsi-FF5722?style=for-the-badge&logo=readthedocs" alt="Read in Farsi">
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

<h1>📦 NPVT Collector — Automated NPVT File Collector for Telegram</h1>

<p>
<strong>A safe, zero-risk collector for <code>.npvt</code> files (NPVT / NPV Tunnel configs) posted in public Telegram channels.</strong><br>
This project reads each channel's public web preview page (<code>t.me/s</code>) — the exact same technique used in your <code>V2ray-Collector</code> and <code>news-monitor</code> projects — with no need for an <strong>API, a user-account login, or a personal phone number</strong>.
</p>
<p>
Every newly found file is compared against previously seen files by <strong>name + size</strong>, and duplicates are dropped; then up to 10 of the newest unique files (by publish time on the source channel) are sent in a single message, via a <strong>plain Telegram bot</strong>, to a channel of your choice.
</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Features -->
<h2>✨ Key Features</h2>
<table>
<thead>
<tr><th>Feature</th><th>Description</th></tr>
</thead>
<tbody>
<tr>
    <td><strong>🔒 Zero risk to any personal account</strong></td>
    <td>No phone number, no user-account (Userbot) login, no need to join source channels. Only each channel's public web page (<code>t.me/s/&lt;channel&gt;</code>) is read.</td>
</tr>
<tr>
    <td><strong>🕐 Precise hourly scheduling</strong></td>
    <td>Runs on the hour via GitHub Actions' standard <code>cron</code> — simple, reliable, and needs no extra secrets.</td>
</tr>
<tr>
    <td><strong>📄 Extracts name, size, and publish time</strong></td>
    <td>For every <code>.npvt</code> file, the name, size (exactly as Telegram displays it), and the exact time the message was posted on the source channel are extracted.</td>
</tr>
<tr>
    <td><strong>🧹 Smart duplicate removal</strong></td>
    <td>A file is treated as a duplicate — and dropped — only when <strong>both name and size</strong> match another file (same channel, a different channel, or a previous run).</td>
</tr>
<tr>
    <td><strong>🔟 Max 10 files, always the newest</strong></td>
    <td>If more than 10 new files are found in one run, only the 10 newest (by publish time) are sent; the rest are — per your explicit request — completely discarded, not queued for the next run.</td>
</tr>
<tr>
    <td><strong>📤 Delivery via a plain Telegram bot</strong></td>
    <td>A bold header message is sent, immediately followed by one message listing the files as hyperlinks; the bot only needs admin rights in your own target channel.</td>
</tr>
<tr>
    <td><strong>🚫 Filename keyword filter</strong></td>
    <td>Files whose name contains a keyword defined in <code>data/blocked_keywords.txt</code> are never collected or published; a record is kept in <code>data/filtered_files.txt</code> purely for transparency.</td>
</tr>
<tr>
    <td><strong>📈 Per-channel report (like V2ray-Collector)</strong></td>
    <td><code>data/channel_report.txt</code> shows how many <code>.npvt</code> files were found per channel on every run; unreachable channels are also listed in <code>data/invalid_channels.txt</code>.</td>
</tr>
<tr>
    <td><strong>🚀 Fully automated & free</strong></td>
    <td>The entire system runs on free GitHub Actions with a single workflow file — no external server needed.</td>
</tr>
</tbody>
</table>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Why no real forwarding -->
<h2>⚠️ Why there's no "real forwarding" in this project</h2>
<p>
Real message forwarding from channels you don't administer is only possible with a genuine <strong>user account</strong> (a Userbot, e.g. via Telethon) — meaning a personal phone number and the ongoing risk of flood limits or a ban on that account. Since that risk isn't acceptable here, this project avoids it entirely:
</p>
<ul>
    <li><strong>Collection</strong> is done with plain HTTP requests to the public <code>t.me/s/...</code> page (no login, no membership, no phone number).</li>
    <li><strong>Delivery</strong> only sends a <strong>link</strong> to the original message (not the file itself), via a <strong>plain Telegram bot</strong> — the exact same approach your <code>Telegram</code> project's <code>version_checker.py</code> already uses with <code>BOT_TOKEN</code> and <code>CHANNEL_ID</code>.</li>
</ul>
<p>Result: no personal account is ever at risk — just an ordinary bot (that you create via BotFather) posting to your own channel.</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Keyword filter -->
<h2>🚫 Filename Keyword Filter</h2>
<p>
Any file whose name contains one of the keywords below is never collected or published — not forwarded, not even linked. These keywords live in <code>data/blocked_keywords.txt</code> (auto-created with this default list on the first run, if the file doesn't already exist):
</p>
<pre class="ltr-block" dir="rtl">
جاوید، جاویدنام، جاوید نام، شاه، آریامهر، آریا مهر، پهلوی،
خمینی، خامنه ای، خامنه‌ای، سیدعلی، سید علی، مجتبی
</pre>
<ul>
    <li><strong>Editing the list:</strong> just open <code>data/blocked_keywords.txt</code> and add or remove a keyword on its own line (lines starting with <code>#</code> are ignored). No Python code changes needed.</li>
    <li><strong>Spacing-independent matching:</strong> the difference between "خامنه‌ای" (with a ZWNJ half-space), "خامنه ای" (with a regular space), and "خامنهای" (joined) is ignored; all three are recognized as the same.</li>
    <li><strong>It's a substring match</strong>, not a whole-word match: e.g. with "شاه" enabled, a file named "شاهین.npvt" would also get filtered, since it contains that string. This is a known, intentional trade-off (favoring caution over precision, even at the cost of occasionally filtering an unrelated name).</li>
    <li>Every filtered file is logged to <code>data/filtered_files.txt</code> purely for transparency/auditing — these files are never sent to the target channel.</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Message format -->
<h2>📨 Message Format</h2>
<p>Each run, if there are new files to send, posts exactly <strong>two messages</strong> to the target channel:</p>
<ol>
    <li>A <strong>bold</strong> header message:
        <pre class="ltr-block" dir="rtl">فایل های NPVT جدید 😁👇</pre>
    </li>
    <li>Immediately after, a message listing the files, each as a <strong>hyperlink</strong> to the original message on the source channel:
        <pre class="ltr-block" dir="rtl">
فایل 1   ← links to the original message
فایل 2   ← links to the original message
...
فایل N   ← up to 10 total
        </pre>
    </li>
</ol>
<p>
Files are ordered by <strong>newest publish time on the source channel first</strong> (File 1 = newest). If more than 10 new files are found in one run, only the 10 newest are sent, and the rest are — per explicit request — <strong>completely discarded</strong>: not queued for the next run, not reconsidered later. If no new files are found, no message (neither header nor list) is sent at all.
</p>
<div class="highlight">
The one exception: if either of the two messages fails to send due to a genuine error (not the 10-file cap) — e.g. a temporary network outage or Telegram's rate limit — the entire batch is saved to <code>data/pending_send.json</code> and retried on the next run, <strong>before</strong> any newly found files.
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Requirements -->
<h2>📦 Requirements</h2>
<ul>
    <li><strong>Git</strong> installed locally (to clone the repository)</li>
    <li>Python 3.10 or higher</li>
    <li>
        The libraries in <code>requirements.txt</code>:
        <pre class="ltr-block">pip install -r config/requirements.txt</pre>
    </li>
    <li>A Telegram bot from <a href="https://t.me/BotFather" target="_blank">@BotFather</a> (no separate personal phone number required)</li>
    <li>A target Telegram channel where the bot has posting (admin) rights</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Configuration -->
<h2>⚙️ Configuration</h2>
<p>All key parameters can be set as environment variables, defined at the top of <code>src/npvt_collector.py</code>:</p>

<table>
<thead>
<tr><th>Parameter</th><th>Default</th><th>Description</th></tr>
</thead>
<tbody>
<tr><td><code>BOT_TOKEN</code></td><td>—</td><td>Telegram bot token (required)</td></tr>
<tr><td><code>TARGET_CHANNEL</code></td><td>—</td><td>Target channel username or numeric ID (required)</td></tr>
<tr><td><code>MAX_PAGES_PER_CHANNEL</code></td><td><code>3</code></td><td>Max number of backward pages (<code>?before=</code>) to reach the previous checkpoint</td></tr>
<tr><td><code>SLEEP_BETWEEN_CHANNELS</code></td><td><code>1.5</code></td><td>Delay (seconds) between checking channels</td></tr>
<tr><td><code>SLEEP_BETWEEN_PAGES</code></td><td><code>1</code></td><td>Delay (seconds) between pages of a single channel</td></tr>
<tr><td><code>SLEEP_BETWEEN_SENDS</code></td><td><code>2</code></td><td>Delay (seconds) between the header message and the file-list message</td></tr>
<tr><td><code>REQUEST_TIMEOUT</code></td><td><code>10</code></td><td>Max time (seconds) to wait for each HTTP request before it's considered failed</td></tr>
<tr><td><code>MAX_SEND_RETRIES</code></td><td><code>6</code></td><td>Max number of retry attempts for a single message when Telegram returns a 429 (rate limit) error</td></tr>
<tr><td><code>MAX_RETRY_AFTER_WAIT</code></td><td><code>90</code></td><td>Max time (seconds) to wait on any single retry, even if Telegram asks for longer</td></tr>
<tr><td><code>MAX_FILES_PER_MESSAGE</code></td><td><code>10</code></td><td>Max number of files per run; anything beyond this is discarded unconditionally (not queued)</td></tr>
</tbody>
</table>

<div class="highlight">
<strong>🔐 Setting GitHub Secrets:</strong> only these two are needed. Add them under <strong>Settings</strong> &gt; <strong>Secrets and variables</strong> &gt; <strong>Actions</strong>:
<pre class="ltr-block">
BOT_TOKEN         → the token you got from BotFather
TARGET_CHANNEL    → username (e.g. @npvt_backup) or numeric ID (e.g. -100xxxxxxxxxx) of the target channel
</pre>
No other secret (like a Personal Access Token) is required.
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Quick start -->
<h2>🧩 Quick Start</h2>
<p>If you want to copy and run this project yourself:</p>
<ol>
    <li>Fork the repository (Fork button at the top of the GitHub page)</li>
    <li>Clone your fork:
        <pre class="ltr-block">git clone https://github.com/MohammadBahemmat/npvt-collector.git
cd npvt-collector</pre>
    </li>
    <li>Install the Python dependencies:
        <pre class="ltr-block">pip install -r config/requirements.txt</pre>
    </li>
    <li>Create a <code>.env</code> file based on <code>config/.env.example</code> with your <code>BOT_TOKEN</code> and <code>TARGET_CHANNEL</code>.</li>
    <li>Fill <code>data/channels.txt</code> with the usernames of the source channels that post <code>.npvt</code> files.</li>
    <li>Run the script once manually to test everything:
        <pre class="ltr-block">python src/npvt_collector.py</pre>
    </li>
</ol>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Automated run -->
<h2>🤖 Setting Up Automated Runs with GitHub Actions</h2>

<h3>1. Workflow file (hourly cron)</h3>
<p>The project runs via a YAML file at <code>.github/workflows/collector.yml</code>, which:</p>
<ul>
    <li>Runs automatically on the hour (<code>cron: '0 * * * *'</code>), and can also be triggered manually from the Actions tab (<strong>Run workflow</strong>).</li>
    <li>Scans every channel listed in <code>data/channels.txt</code>.</li>
    <li>Removes duplicates, picks up to 10 newest files, and sends them to the target channel.</li>
    <li>Commits the updated state files (checkpoint, dedup archive, <code>channel_report.txt</code>, <code>invalid_channels.txt</code>) back to the repository.</li>
</ul>

<div class="highlight">
<strong>⏱️ About scheduling precision:</strong> per GitHub's own documentation, <code>schedule</code> runs can be delayed by a few minutes during high-load periods — this is a platform limitation, not something this project's settings can remove. For a use case like this (hourly scan of a few channels), that delay is usually negligible. If absolute precision is critical, the only real solution is running a scheduled job on your own server (e.g. a VPS with real <code>cron</code>), not GitHub Actions.
</div>

<h3>2. Adding source channels</h3>
<p><code>data/channels.txt</code> holds the list of public Telegram channels (one username per line, no <code>@</code>). To add a new channel, just add its username on a new line — no membership or special access needed.</p>

<h3>3. Per-channel status report</h3>
<p>After every run, two files under <code>data/</code> are updated:</p>
<ul>
    <li><code>channel_report.txt</code> — for each channel, shows the history of how many <code>.npvt</code> files were found on each run, comma-separated in order; e.g. <code>napsternetv_file: 2, 0, 1</code> means the last three runs found 2, 0, and 1 new files respectively.</li>
    <li><code>invalid_channels.txt</code> — an up-to-date list of channels that weren't readable the last time they were tested (doesn't exist, private, or blocked). These channels also show up as <code>ERR</code> in <code>channel_report.txt</code>.</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Project structure -->
<h2>🗂️ Project Structure</h2>
<pre class="ltr-block">
.
├── .github/
│   └── workflows/
│       └── collector.yml          # main workflow (hourly schedule + automatic state commit)
│
├── src/
│   └── npvt_collector.py          # main script (scan + dedup + send)
│
├── config/
│   ├── requirements.txt           # Python dependencies
│   ├── .gitignore                 # ignored files
│   └── .env.example               # example environment variables file
│
├── data/                          # data files and reports
│   ├── channels.txt               # list of Telegram channels (input)
│   ├── blocked_keywords.txt       # blocked-keyword list (input; auto-created on first run)
│   ├── last_message_id.json       # (generated) last checked message_id per channel
│   ├── seen_files.json            # (generated) archive of already-sent files (name+size+time)
│   ├── pending_send.json          # (generated) batch queued after a genuine send failure
│   ├── npvt_report.txt            # (generated) per-run summary report
│   ├── channel_report.txt         # (generated) per-channel history of files found
│   ├── invalid_channels.txt       # (generated) unreachable/invalid channels from the latest run
│   └── filtered_files.txt         # (generated) files skipped due to a blocked keyword
│
├── line.gif                       # animated separator for the README
├── README.md                      # Persian documentation
└── README.EN.md                   # English documentation
</pre>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Comparison -->
<h2>📊 Comparison with Common Userbot-Forwarding Approaches</h2>
<table>
<thead>
<tr><th>Criteria</th><th>This project</th><th>Userbot-based approaches (Telethon/Pyrogram)</th></tr>
</thead>
<tbody>
<tr><td><strong>Requires a phone number</strong></td><td>❌ No</td><td>✅ Yes</td></tr>
<tr><td><strong>Risk of ban/flood on a personal account</strong></td><td>❌ None</td><td>⚠️ Always present</td></tr>
<tr><td><strong>Needs to join the source channel</strong></td><td>❌ No</td><td>Usually yes</td></tr>
<tr><td><strong>Content retrieval method</strong></td><td>Public web page (<code>t.me/s</code>)</td><td>MTProto API</td></tr>
<tr><td><strong>Delivery to target channel</strong></td><td>Link message (Bot API)</td><td>Real message forward</td></tr>
<tr><td><strong>Setup complexity</strong></td><td>A simple bot from BotFather</td><td>Session creation, login with confirmation code</td></tr>
</tbody>
</table>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Common errors -->
<h2>❗ Common Errors & Solutions</h2>

<details>
<summary><strong>Error: "BOT_TOKEN and/or TARGET_CHANNEL not set"</strong></summary>
<p>Make sure both the <code>BOT_TOKEN</code> and <code>TARGET_CHANNEL</code> secrets are correctly set under <strong>Settings → Secrets and variables → Actions</strong>.</p>
</details>

<details>
<summary><strong>Messages aren't being sent to the target channel</strong></summary>
<ul>
    <li>Verify the bot is an <strong>admin</strong> of the target channel with posting rights.</li>
    <li><code>TARGET_CHANNEL</code> must be a valid public username (<code>@channel</code>) or numeric ID (<code>-100...</code>).</li>
</ul>
</details>

<details>
<summary><strong>Files aren't being extracted from a channel</strong></summary>
<ul>
    <li>Make sure the channel is <strong>public</strong> (private channels have no <code>t.me/s</code> page).</li>
    <li>Enter the channel username in <code>data/channels.txt</code> without <code>https://t.me/</code> and without <code>@</code>.</li>
</ul>
</details>

<details>
<summary><strong>State files (checkpoint/seen_files) aren't being updated</strong></summary>
<ul>
    <li>Check that the <code>Commit and push updated state</code> step in the workflow ran without errors.</li>
    <li>Make sure <code>permissions: contents: write</code> hasn't been removed from <code>collector.yml</code>.</li>
</ul>
</details>

<details>
<summary><strong>I'm seeing a <code>429 Too Many Requests</code> error in the log</strong></summary>
<ul>
    <li>Since each run only sends 2 messages (header + list), this is unlikely; if it happens, it's handled automatically: the script waits exactly as long as the <code>retry_after</code> value Telegram returns, then retries (up to <code>MAX_SEND_RETRIES</code> times).</li>
    <li>If it still fails after all retries, the message is <strong>not lost</strong> — it's saved to <code>data/pending_send.json</code> and retried again on the next run.</li>
</ul>
</details>

<details>
<summary><strong>A file I expected never got sent</strong></summary>
<ul>
    <li>First check <code>data/filtered_files.txt</code> — if the file's name matched a keyword in <code>data/blocked_keywords.txt</code>, it was intentionally not published.</li>
    <li>Then check <code>data/seen_files.json</code>; if a file with the same name+size was already sent from a different channel, it's skipped as a duplicate.</li>
    <li>If more than 10 new files were found in one run and this file wasn't among the 10 newest, it was <strong>completely discarded</strong> and never sent — this is intentional behavior, not a bug.</li>
    <li>Otherwise, check <code>data/pending_send.json</code> — it may still be queued due to a genuine send error.</li>
</ul>
</details>

<details>
<summary><strong>A channel always shows <code>ERR</code> in <code>channel_report.txt</code></strong></summary>
<ul>
    <li>It means that channel couldn't be read at all in the last run — usually a wrong username, a deleted/private channel, or a temporary block by Telegram.</li>
    <li>Test the username in your browser at <code>https://t.me/s/&lt;username&gt;</code>; if the page doesn't load or is empty, that same channel will also appear in <code>data/invalid_channels.txt</code>.</li>
</ul>
</details>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Customization -->
<h2>🛠️ Customization</h2>
<ul>
    <li>To <strong>change the run frequency</strong>, edit the <code>cron</code> value in <code>collector.yml</code> (e.g. <code>'0 */2 * * *'</code> for every 2 hours).</li>
    <li>To <strong>change how many files are sent per run</strong>, adjust <code>MAX_FILES_PER_MESSAGE</code> in <code>config/.env.example</code> or your secrets.</li>
    <li>To <strong>change the header text or message format</strong>, edit <code>HEADER_TEXT</code> and the <code>build_file_list_message</code> function in <code>src/npvt_collector.py</code>.</li>
    <li>To <strong>target a different file extension</strong> (e.g. for a similar project), change the <code>FILE_SUFFIX</code> value.</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Contributing -->
<h2>🙏 Contributing</h2>
<p>
Suggestions, bug reports, or new Telegram channels to add to <code>channels.txt</code> are welcome via <strong>Pull Request</strong> or <strong>Issue</strong>.<br>
For developers: please do a test run locally before submitting changes.
</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Acknowledgements -->
<h2>💡 Acknowledgements</h2>
<p>The idea of using <code>t.me/s</code> to access Telegram channels without an API is inspired by your own earlier projects — <code>V2ray-Collector</code> and <code>news-monitor</code>.</p>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- License -->
<h2>📄 License</h2>
<p>This project is released under the <strong>MIT</strong> license. Use, modification, and distribution are free.</p>

</div>

<!-- keywords: npvt collector, npv tunnel config, telegram file collector,
     t.me/s scraper, github actions collector, telegram bot -->

</body>
</html>
