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
Every newly found file is compared against previously seen files by <strong>name + size</strong>, and duplicates are dropped; the link to each unique file is then sent, via a <strong>plain Telegram bot</strong> (no forwarding, no membership in source channels required), to a channel of your choice.
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
    <td><strong>📄 Accurate file name & size extraction</strong></td>
    <td>The name and size of every <code>.npvt</code> file (exactly as Telegram displays it, e.g. <code>3.5 KB</code>), plus a direct link to the message, are extracted.</td>
</tr>
<tr>
    <td><strong>🧹 Smart duplicate removal</strong></td>
    <td>A file is treated as a duplicate — and dropped — only when <strong>both name and size</strong> match another file (same channel, a different channel, or a previous run).</td>
</tr>
<tr>
    <td><strong>📤 Delivery via a plain Telegram bot</strong></td>
    <td>The link to each unique file is sent with a simple Bot API call to your target channel; the bot only needs admin rights in your own target channel.</td>
</tr>
<tr>
    <td><strong>🧩 Checkpointing</strong></td>
    <td>The last checked <code>message_id</code> for every channel is saved; the next run only inspects new messages.</td>
</tr>
<tr>
    <td><strong>💾 Persistent dedup archive</strong></td>
    <td>Files whose link has already been sent are recorded in <code>data/seen_files.json</code> so they're never sent again.</td>
</tr>
<tr>
    <td><strong>📊 Per-run report</strong></td>
    <td>A summary of every run (found, duplicate, new, sent counts) is logged to <code>data/npvt_report.txt</code>.</td>
</tr>
<tr>
    <td><strong>📈 Per-channel report (like V2ray-Collector)</strong></td>
    <td><code>data/channel_report.txt</code> shows how many <code>.npvt</code> files were found per channel on every run; unreachable channels are also listed in <code>data/invalid_channels.txt</code>.</td>
</tr>
<tr>
    <td><strong>🔁 Continuous self-chaining runs</strong></td>
    <td>Just like <code>V2ray-Collector</code>, each run immediately triggers the next one when it finishes, and the cycle continues until you stop it.</td>
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
<tr><td><code>SLEEP_BETWEEN_SENDS</code></td><td><code>1.5</code></td><td>Delay (seconds) between messages sent via the bot</td></tr>
</tbody>
</table>

<div class="highlight">
<strong>🔐 Setting GitHub Secrets:</strong> Add these under <strong>Settings</strong> &gt; <strong>Secrets and variables</strong> &gt; <strong>Actions</strong>:
<pre class="ltr-block">
BOT_TOKEN         → the token you got from BotFather
TARGET_CHANNEL    → username (e.g. @npvt_backup) or numeric ID (e.g. -100xxxxxxxxxx) of the target channel
GH_TOKEN          → a Personal Access Token with repo + workflow scope (needed for the self-chaining run)
</pre>
</div>

<div class="highlight">
<strong>🔗 About <code>GH_TOKEN</code> and self-chaining runs:</strong> Just like <code>V2ray-Collector</code>, instead of a fixed cron schedule, this project triggers the next run itself at the end of every run, and the cycle continues forever. The default token GitHub Actions creates (<code>GITHUB_TOKEN</code>) is not allowed, for security reasons, to trigger another workflow run — so a personal <strong>Personal Access Token</strong> is required. It's free to create:
<ol>
<li>Go to <a href="https://github.com/settings/tokens?type=beta" target="_blank">github.com/settings/tokens</a> (or Settings → Developer settings → Personal access tokens → Tokens (classic))</li>
<li>Click <strong>Generate new token (classic)</strong></li>
<li>Check the <code>repo</code> and <code>workflow</code> scopes</li>
<li>Copy the generated token and save it as a secret named <code>GH_TOKEN</code></li>
</ol>
⚠️ Since this token is equivalent to scoped access to your GitHub account, set an expiration date on it and never store it anywhere other than GitHub Secrets.
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

<h3>1. Workflow file (self-chaining, just like V2ray-Collector)</h3>
<p>The project runs via a YAML file at <code>.github/workflows/collector.yml</code>, which:</p>
<ul>
    <li>Only starts via <strong>workflow_dispatch</strong> (one initial manual run) — there's no fixed <code>cron</code>.</li>
    <li>Scans every channel listed in <code>data/channels.txt</code>.</li>
    <li>Removes duplicates and sends links for new files to the target channel.</li>
    <li>Commits the updated state files (checkpoint, dedup archive, <code>channel_report.txt</code>, <code>invalid_channels.txt</code>) back to the repository.</li>
    <li><strong>Immediately after a successful run, it triggers a new run itself</strong> (the "Trigger next run" step), and this cycle continues until you stop it.</li>
</ul>

<div class="highlight">
<strong>⚠️ Important note about the continuous self-chaining run:</strong>
<ul>
<li>If a run fails (e.g. a network hiccup or rate limit), the "Trigger next run" step won't execute and the chain stops completely; you'll need to trigger it again manually from the Actions tab (<strong>Run workflow</strong>).</li>
<li>Since each run immediately triggers the next one with no delay, on <strong>Private</strong> repositories the free GitHub Actions minutes quota (typically 2,000 minutes/month) can be consumed faster than with an hourly schedule. To manage this, you can increase <code>SLEEP_BETWEEN_CHANNELS</code>, <code>SLEEP_BETWEEN_PAGES</code>, and <code>SLEEP_BETWEEN_SENDS</code> in <code>config/.env.example</code> so each run takes a bit longer between cycles, or switch <code>on: workflow_dispatch</code> to a simple <code>schedule: cron</code> (e.g. every 10 minutes) for a fixed-interval run instead of a continuous chain.</li>
</ul>
</div>

<h3>2. Adding source channels</h3>
<p><code>data/channels.txt</code> holds the list of public Telegram channels (one username per line, no <code>@</code>). To add a new channel, just add its username on a new line — no membership or special access needed.</p>

<h3>3. Per-channel status report</h3>
<p>After every run, two files under <code>data/</code> are updated:</p>
<ul>
    <li><code>channel_report.txt</code> — for each channel, shows the history of how many <code>.npvt</code> files were found on each run, comma-separated in order; e.g. <code>napsternetv_file: 2, 0, 1</code> means the last three runs found 2, 0, and 1 new files respectively.</li>
    <li><code>invalid_channels.txt</code> — lists channels that couldn't be read at all in the most recent run (doesn't exist, private, or blocked). These channels also show up as <code>ERR</code> in <code>channel_report.txt</code>.</li>
</ul>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Project structure -->
<h2>🗂️ Project Structure</h2>
<pre class="ltr-block">
.
├── .github/
│   └── workflows/
│       └── collector.yml          # main workflow (hourly run + automatic state commit)
│
├── src/
│   └── npvt_collector.py          # main script (scan + dedup + send link)
│
├── config/
│   ├── requirements.txt           # Python dependencies
│   ├── .gitignore                 # ignored files
│   └── .env.example               # example environment variables file
│
├── data/                          # data files and reports
│   ├── channels.txt               # list of Telegram channels (input)
│   ├── last_message_id.json       # (generated) last checked message_id per channel
│   ├── seen_files.json            # (generated) archive of already-sent files (name+size)
│   ├── npvt_report.txt            # (generated) per-run summary report
│   ├── channel_report.txt         # (generated) per-channel history of files found
│   └── invalid_channels.txt       # (generated) unreachable/invalid channels from the latest run
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
<summary><strong>Link messages aren't being sent to the target channel</strong></summary>
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
<summary><strong>A channel always shows <code>ERR</code> in <code>channel_report.txt</code></strong></summary>
<ul>
    <li>It means that channel couldn't be read at all in the last run — usually a wrong username, a deleted/private channel, or a temporary block by Telegram.</li>
    <li>Test the username in your browser at <code>https://t.me/s/&lt;username&gt;</code>; if the page doesn't load or is empty, that same channel will also appear in <code>data/invalid_channels.txt</code>.</li>
</ul>
</details>

<details>
<summary><strong>The self-chaining run has stopped and isn't triggering itself anymore</strong></summary>
<ul>
    <li>If a run finishes with a failure, the <code>Trigger next run</code> step won't execute and the cycle stays stopped — this is intentional, so errors don't repeat silently.</li>
    <li>Open the <strong>Actions</strong> tab, check the last failed run, and fix the cause (e.g. a wrong secret, or an expired <code>GH_TOKEN</code>).</li>
    <li>Then trigger <strong>Run workflow</strong> manually once more to restart the chain.</li>
</ul>
</details>

<img src="line.gif" alt="separator" style="display: block; margin: 30px auto;" />

<!-- Customization -->
<h2>🛠️ Customization</h2>
<ul>
    <li>To <strong>change the run frequency</strong>, edit the <code>cron</code> value in <code>collector.yml</code>.</li>
    <li>To <strong>change the message text</strong>, edit the <code>send_link_message</code> function in <code>src/npvt_collector.py</code>.</li>
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
     t.me/s scraper, github actions collector, telegram bot forwarder -->

</body>
</html>
