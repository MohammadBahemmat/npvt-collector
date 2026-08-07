<!-- README.EN.md -->
<div align="center" style="margin-bottom: 18px;">
  <a href="https://github.com/MohammadBahemmat/npvt-collector/blob/main/README.md">
    <img src="https://img.shields.io/badge/Read_in-Farsi-FF5722?style=for-the-badge&logo=readthedocs" alt="Read in Farsi">
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

<h1>📦 NPVT Collector — Collect <code>.npvt</code> files from Telegram</h1>

<p>
<strong>A web-based collector for <code>.npvt</code> files (NPVT / NPV Tunnel configs) published in public Telegram channels.</strong><br>
It reads only each channel's public web preview page (<code>t.me/s</code>), finds <code>.npvt</code> files, extracts their name, size, and publish time, removes duplicates using <strong>normalized name + size</strong>, and posts the newest files as links to your destination channel through a <strong>regular Telegram bot</strong>.
</p>

<div class="highlight">
<strong>What this repo is for:</strong> collection, deduplication, and link publishing. No personal account login, no phone number, no Userbot, and no real file forwarding.
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>✨ What it does</h2>

<table>
<thead>
<tr><th>Part</th><th>Description</th></tr>
</thead>
<tbody>
<tr>
  <td><strong>Public channel scanning</strong></td>
  <td>Reads only public Telegram pages (<code>t.me/s/&lt;channel&gt;</code>) — no login, no membership.</td>
</tr>
<tr>
  <td><strong>File extraction</strong></td>
  <td>Finds messages containing <code>.npvt</code> files and stores their name, size, and exact publish time.</td>
</tr>
<tr>
  <td><strong>Filename filter</strong></td>
  <td>Files whose name contains a keyword from <code>data/blocked_keywords.txt</code> are never collected or published.</td>
</tr>
<tr>
  <td><strong>Deduplication</strong></td>
  <td>If two files (even from different channels) share the same <strong>normalized name</strong> and <strong>size</strong>, only one is kept.</td>
</tr>
<tr>
  <td><strong>Newest-first selection</strong></td>
  <td>If more new files are found than the configured limit, only the newest ones (by publish time) are posted; the rest are discarded.</td>
</tr>
<tr>
  <td><strong>Publishing</strong></td>
  <td>Instead of forwarding files, a header message and a message with links to the original posts are sent via a Telegram bot.</td>
</tr>
<tr>
  <td><strong>Scheduling</strong></td>
  <td>Runs automatically through GitHub Actions on a fixed <code>cron</code> schedule — no separate server needed.</td>
</tr>
<tr>
  <td><strong>Reporting</strong></td>
  <td>Keeps per-channel status, invalid channels, filtered files, and a deduplication archive.</td>
</tr>
</tbody>
</table>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>📨 Message Format</h2>
<p>Each run, if there are new files to publish, sends exactly <strong>two messages</strong> to the target channel, one right after the other:</p>
<ol>
  <li>A bold header message:
    <pre class="ltr-block" dir="rtl">فایل های NPVT جدید 😁👇</pre>
  </li>
  <li>A message listing the files, each one linking to the original post on the source channel:
    <pre class="ltr-block" dir="rtl">
فایل 1   (links to the original message)
فایل 2   (links to the original message)
...
    </pre>
  </li>
</ol>
<p>
Files are ordered by <strong>newest publish time first</strong> (File 1 = newest). The number of files per run is capped by <code>MAX_FILES_PER_MESSAGE</code> (default 10). If more new files are found than this cap, only the newest ones are sent and the <strong>rest are discarded permanently</strong> — not queued for the next run, not reconsidered later. If no new files are found, no message is sent at all.
</p>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>⚠️ Scope and limitations</h2>
<ul>
  <li>This project is intended for <strong>public channels only</strong>. A private channel has no public web page and is recorded as invalid.</li>
  <li>It does <strong>not</strong> use the Telegram API or a personal phone number — only plain HTTP requests to the public web page.</li>
  <li>The output is <strong>link-based</strong>: it publishes the original message URL, not the file itself.</li>
  <li>Each run publishes at most a fixed number of files (10 by default); anything beyond that is discarded, not saved for later.</li>
  <li>The filename filter matches on substrings, not whole words only — see the filter section below for details.</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🧠 Why link-only output, not real forwarding?</h2>
<p>
Real forwarding from channels you don't administer generally requires a genuine user account (a Userbot, e.g. via Telethon) — meaning a personal phone number and the ongoing risk of a flood limit or ban on that account. This project intentionally avoids that path so it can run with zero risk to any personal account, using only a regular Telegram bot.
</p>

<table>
<thead>
<tr><th>Criteria</th><th>This project</th><th>Userbot-based approaches</th></tr>
</thead>
<tbody>
<tr><td>Requires a phone number</td><td>❌ No</td><td>✅ Yes</td></tr>
<tr><td>Risk of ban/flood on a personal account</td><td>❌ None</td><td>⚠️ Always present</td></tr>
<tr><td>Needs to join the source channel</td><td>❌ No</td><td>Usually yes</td></tr>
<tr><td>Content retrieval method</td><td>Public web page (<code>t.me/s</code>)</td><td>MTProto API</td></tr>
<tr><td>Delivery to target channel</td><td>Link message (Bot API)</td><td>Real message forward</td></tr>
</tbody>
</table>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🚫 Filename Keyword Filter</h2>
<p>
Any file whose name contains one of the keywords below is never collected or published. This list lives in <code>data/blocked_keywords.txt</code> (auto-created with these defaults on the first run, if the file doesn't already exist):
</p>
<pre class="ltr-block" dir="rtl">
جاوید، جاویدنام، جاوید نام، شاه، آریامهر، آریا مهر، پهلوی،
خمینی، خامنه ای، خامنه‌ای، سیدعلی، سید علی، مجتبی
</pre>
<ul>
  <li><strong>Editing the list:</strong> open <code>data/blocked_keywords.txt</code> and add or remove a keyword on its own line (lines starting with <code>#</code> are ignored) — no code changes needed.</li>
  <li><strong>Spacing-independent matching:</strong> "خامنه‌ای" (ZWNJ half-space), "خامنه ای" (regular space), and "خامنهای" (joined) are all recognized as the same keyword.</li>
  <li><strong>It's a substring match, not a whole-word match:</strong> for example, with "شاه" enabled, a file named "شاهین.npvt" is also filtered, since it contains that string. This is a known, intentional trade-off favoring caution over precision.</li>
  <li>Every filtered file is logged to <code>data/filtered_files.txt</code> purely for transparency — these files are never published.</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🚀 Quick start</h2>
<ol>
  <li>Fork the repository and clone it locally.</li>
  <li>Install dependencies:
    <pre class="ltr-block">pip install -r config/requirements.txt</pre>
  </li>
  <li>Create a Telegram bot via <a href="https://t.me/BotFather" target="_blank">@BotFather</a> (no separate personal phone number required).</li>
  <li>Add the bot to your target channel as an admin with posting rights.</li>
  <li>Create a <code>.env</code> file from <code>config/.env.example</code> and set <code>BOT_TOKEN</code> and <code>TARGET_CHANNEL</code>.</li>
  <li>Put the source channel usernames (without <code>@</code>) in <code>data/channels.txt</code>, one per line.</li>
  <li>Edit <code>data/blocked_keywords.txt</code> if you want to adjust the filter.</li>
  <li>Run the project once manually and review the outputs:
    <pre class="ltr-block">python src/npvt_collector.py</pre>
  </li>
</ol>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>⚙️ Main settings</h2>
<table>
<thead>
<tr><th>Variable</th><th>Default</th><th>Description</th></tr>
</thead>
<tbody>
<tr><td><code>BOT_TOKEN</code></td><td>—</td><td>Telegram bot token (required)</td></tr>
<tr><td><code>TARGET_CHANNEL</code></td><td>—</td><td>Destination channel for publishing (required)</td></tr>
<tr><td><code>MAX_FILES_PER_MESSAGE</code></td><td><code>10</code></td><td>Max files published per run; anything beyond this is discarded, not queued</td></tr>
<tr><td><code>MAX_PAGES_PER_CHANNEL</code></td><td><code>3</code></td><td>Max backward pages (<code>?before=</code>) scanned per channel to reach the previous checkpoint</td></tr>
<tr><td><code>SLEEP_BETWEEN_CHANNELS</code></td><td><code>1.5</code></td><td>Delay (seconds) between checking channels</td></tr>
<tr><td><code>SLEEP_BETWEEN_PAGES</code></td><td><code>1</code></td><td>Delay (seconds) between pages of a single channel</td></tr>
<tr><td><code>SLEEP_BETWEEN_SENDS</code></td><td><code>2</code></td><td>Delay (seconds) between the header message and the file-list message</td></tr>
<tr><td><code>REQUEST_TIMEOUT</code></td><td><code>10</code></td><td>Max time (seconds) to wait for each HTTP request</td></tr>
<tr><td><code>MAX_SEND_RETRIES</code></td><td><code>6</code></td><td>Max retry attempts for a message when Telegram returns a 429 (rate limit) error</td></tr>
<tr><td><code>MAX_RETRY_AFTER_WAIT</code></td><td><code>90</code></td><td>Max wait (seconds) on any single retry, even if Telegram asks for longer</td></tr>
</tbody>
</table>

<div class="highlight">
<strong>GitHub Actions secrets required:</strong>
<pre class="ltr-block">
BOT_TOKEN
TARGET_CHANNEL
</pre>
Only these two are needed — no Personal Access Token or any other secret.
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🤖 GitHub Actions automation</h2>
<ul>
  <li>The main workflow lives at <code>.github/workflows/collector.yml</code> and can also be triggered manually from the Actions tab (<strong>Run workflow</strong>).</li>
  <li>The current schedule is <code>cron: '45 */3 * * *'</code> — every 3 hours, at minute 45. To change the interval, edit this value in <code>collector.yml</code>.</li>
  <li>After each run, the state and report files (per-channel checkpoint, dedup archive, channel report, invalid channels) are committed back to the repository automatically.</li>
  <li>If sending either message (header or list) fails due to a genuine error (not the file-count cap), that batch is saved to <code>data/pending_send.json</code> and retried on the next run, before any newly found files.</li>
</ul>

<div class="highlight">
<strong>About scheduling precision:</strong> per GitHub's own documentation, <code>schedule</code> runs can be delayed by a few minutes during high-load periods — this is a platform limitation, not something this project's settings can remove. For a periodic scan like this, that delay is usually negligible.
</div>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>🗂️ Project structure</h2>
<pre class="ltr-block">
.
├── .github/workflows/collector.yml
├── src/npvt_collector.py
├── config/
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
├── data/
│   ├── channels.txt               # source channel list (input)
│   ├── blocked_keywords.txt       # blocked-keyword list (input)
│   ├── last_message_id.json       # (generated) per-channel checkpoint
│   ├── seen_files.json            # (generated) archive of already-published files
│   ├── pending_send.json          # (generated) queue of files with a genuine send failure
│   ├── channel_report.txt         # (generated) per-channel history of files found
│   ├── invalid_channels.txt       # (generated) unreachable/invalid channels
│   ├── filtered_files.txt         # (generated) files skipped due to a blocked keyword
│   └── npvt_report.txt            # (generated) per-run summary report
├── README.md
└── README.EN.md
</pre>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>📊 Similar projects and inspiration</h2>
<p>
This repository is inspired by public Telegram scraping techniques used in the owner's earlier projects, especially <code>V2ray-Collector</code> and <code>news-monitor</code>. The main difference is that this repo is focused specifically on <code>.npvt</code> files.
</p>

<h2>🏷️ Suggested GitHub topics</h2>
<pre class="ltr-block">npvt, napsternetv, npv-tunnel, telegram-scraper, telegram-channel-scraper, public-web-scraping, v2ray-config, vpn-config, github-actions, telegram-bot</pre>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>❓ FAQ</h2>

<details>
<summary><strong>Why is there no real forwarding — just links?</strong></summary>
<p>Real forwarding from channels you don't own requires a genuine user account, which carries a ban risk. This project intentionally avoids that so it can run with zero risk to any personal account, using only a regular bot.</p>
</details>

<details>
<summary><strong>Does it work on private channels?</strong></summary>
<p>No. It's built for public channels only, since it only reads Telegram's public web preview page.</p>
</details>

<details>
<summary><strong>What happens if a file is a duplicate?</strong></summary>
<p>If the normalized name and size match a file already published — even from a different channel — it's treated as a duplicate and skipped.</p>
</details>

<details>
<summary><strong>Why do some files never get published?</strong></summary>
<p>If a run finds more new files than the <code>MAX_FILES_PER_MESSAGE</code> cap (default 10), only the newest are published and the rest are discarded <strong>permanently</strong>. This is most noticeable on the first run or right after adding several high-volume channels, and it's intentional behavior, not a bug.</p>
</details>

<details>
<summary><strong>What happens if a channel can't be opened?</strong></summary>
<p>That channel is recorded in <code>data/invalid_channels.txt</code> and shows as <code>ERR</code> in <code>data/channel_report.txt</code>.</p>
</details>

<details>
<summary><strong>Can I change how often it runs?</strong></summary>
<p>Yes. Edit the <code>cron</code> value in <code>.github/workflows/collector.yml</code>; the current value, <code>'45 */3 * * *'</code>, means every 3 hours.</p>
</details>

<img src="line.gif" alt="separator" style="display: block; margin: 26px auto;" />

<h2>📝 License</h2>
<p>This project is released under the MIT License.</p>

</div>

<!-- keywords: npvt collector, npv tunnel, telegram file collector, t.me/s scraper, telegram bot, github actions -->
</body>
</html>
