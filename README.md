# Muse ↔ Ruflo Bridge

اتصال **Ruflo** به **Muse Code** با نصب یک‌خطی، بدون تنظیم یا ذخیره‌ی کلید APIِ مدل‌های دیگر.

> این پروژه «مدل رایگان» یا راه دورزدن احراز هویت نیست. Muse Code باید با روش رسمی Meta وارد شده باشد؛ همان نشستِ احراز‌شده مدل را اجرا می‌کند. Ruflo به‌صورت یک MCP محلی برای حافظه، هماهنگی وظایف، workflow و ابزارهای محلی اضافه می‌شود. هیچ `ANTHROPIC_API_KEY`، `OPENAI_API_KEY` یا `GOOGLE_API_KEY` در این پروژه خوانده، تولید یا ذخیره نمی‌شود.

## چرا Bridge و نه reverse engineering؟

Ruflo و replica-skill هر دو با مجوز MIT منتشر شده‌اند. بنابراین به‌جای مهندسی معکوسِ کد Ruflo، این پروژه یک **یکپارچه‌سازی مستقیم و قابل‌ممیزی** با Ruflo فراهم می‌کند و attribution را حفظ می‌کند. روش feature-parity / clean-room در skill موجود است، اما فقط برای بازسازیِ قانونیِ رفتارهای عمومی و مجاز کاربرد دارد؛ نه کپی کد، API خصوصی، دارایی، داده یا برند دیگران.

## آنچه نصب می‌شود

1. یک native plugin سبک برای Muse Code با skill و سه فرمان:
   - `/muse-ruflo-bridge:ruflo-health`
   - `/muse-ruflo-bridge:ruflo-swarm-plan <goal>`
   - `/muse-ruflo-bridge:ruflo-replica-plan <public-url-or-product>`
2. یک فایل project-local به نام `.mcp.json` که فقط این MCP محلی را ثبت می‌کند:

```json
{
  "mcpServers": {
    "ruflo": {
      "type": "stdio",
      "command": "npx",
      "args": ["--yes", "ruflo@3.56.10", "--no-update", "mcp", "start"],
      "required": false,
      "startup_timeout_sec": 90,
      "tool_timeout_sec": 300
    }
  }
}
```

نسخه‌ی Ruflo عمداً pin شده است؛ نصب‌کننده هرگز یک ورودی `ruflo` موجود اما متفاوت را overwrite نمی‌کند. Muse Code برای اجرای فایل project-local از شما trust می‌خواهد و MCP را فقط در session جدید بالا می‌آورد.

## پیش‌نیازها

- [Muse Code](https://dev.meta.ai/docs/muse-code) نصب و با روش رسمی Meta وارد شده باشد.
- Node.js 20 یا جدیدتر، npm، npx، Python 3 و Git.
- یک workspace محلی که مجاز هستید به آن trust بدهید.
- دسترسی شبکه در اولین session برای دریافت نسخه‌ی pin‌شده‌ی `ruflo` از npm، مگر آن‌که npm cache قبلاً آن را داشته باشد.

Muse Code از MCP با transport `stdio` و فایل `.mcp.json` پشتیبانی می‌کند. این bridge از همان مسیر رسمی استفاده می‌کند.

## نصب با یک دستور

بعد از انتشار ریپو، این یک خط را در **ریشه‌ی پروژه‌ای که می‌خواهید Muse Code روی آن کار کند** اجرا کنید:

```bash
git clone https://github.com/YOUR_GITHUB_ORG/muse-ruflo-bridge.git .muse-ruflo-bridge && bash .muse-ruflo-bridge/install.sh
```

برای نصب از checkout محلی:

```bash
bash /path/to/muse-ruflo-bridge/install.sh --project /path/to/your-project
```

نصب‌کننده فقط package را validate/install می‌کند و `.mcp.json` را با یک merge محافظه‌کارانه می‌نویسد؛ Ruflo را در زمان نصب اجرا نمی‌کند و هیچ secretی نمی‌خواهد.

سپس:

1. محتوای `.mcp.json` را بازبینی کنید.
2. در همان workspace یک **session جدید** از `muse` شروع کنید.
3. فقط اگر repository را بازبینی کرده‌اید، درخواست Trust را تأیید کنید.
4. با `/mcp` وضعیت server را ببینید.
5. در chat اجرا کنید: `/muse-ruflo-bridge:ruflo-health`

## بررسی و حذف

```bash
# فقط بررسی ورودی MCP
python3 .muse-ruflo-bridge/scripts/merge_mcp.py --project . --check

# حذف محافظه‌کارانه: فقط دقیقاً همان ورودیِ نصب‌شده را پاک می‌کند
bash .muse-ruflo-bridge/uninstall.sh --project .
```

## دامنه‌ی قابلیت‌ها و محدودیت صادقانه

| قابلیت | وضعیت در این Bridge | توضیح |
|---|---|---|
| Muse Code model/session | پشتیبانی‌شده | با login/plan رسمی Muse Code، نه API key در repo |
| Ruflo MCP محلی، حافظه، task/workflow و ابزارهای expose شده | پشتیبانی‌شده، وابسته به نسخه‌ی Ruflo | ابزارهای واقعاً موجود را در `/mcp` کشف کنید |
| Skill برای plan، swarm و clean-room | پشتیبانی‌شده | هیچ ابزار یا نام tool ساختگی ادعا نمی‌کند |
| تمام افزونه‌های Ruflo که local هستند | best-effort | به OS، dependency و tool inventory نسخه‌ی pin‌شده وابسته‌اند |
| Providerهای ابری دیگر، Cloud agents، OAuth connectorها، داده‌ی تجاری | نیازمند auth رسمی خودشان | این Bridge کلید یا auth را دور نمی‌زند |
| «۱۰۰٪ کارایی» | قابل ادعا نیست | فقط پس از feature matrix و تست end-to-end برای scope مشخص قابل اندازه‌گیری است |

Ruflo یک orchestrator است، نه خود مدل. Muse Code نیز orchestration چندعاملی خود را دارد. ترکیب درست این دو این است که **Muse Code مدل/agent host** باشد و Ruflo **ابزارهای local orchestration/memory** را از طریق MCP ارائه دهد. اجرای هر provider cloud خارج از Muse Code، ذاتاً نیازمند credential رسمی همان provider است.

## امنیت

- `install.sh` هیچ API key یا متغیر provider را export نمی‌کند.
- Muse Code برای MCP stdio محیط child را محدود می‌کند؛ این config هیچ `env` secretی پاس نمی‌دهد.
- plugin فقط content capability دارد (skill/command) و هیچ hook یا MCP runtime را auto-approve نمی‌کند.
- `.mcp.json` یک executable configuration است. قبل از Trust کردن workspace، آن را بخوانید.
- نسخه‌ی Ruflo pin شده است. برای upgrade، diff و release notes را بررسی کرده و سپس با `--version` نسخه‌ی دقیق جدید را نصب کنید.
- برای جزئیات، [docs/SECURITY.md](docs/SECURITY.md) را ببینید.

## توسعه و تست

```bash
python3 -m unittest discover -s tests -v
python3 scripts/merge_mcp.py --project . --check
# روی ماشینی که Muse Code نصب است:
muse plugins validate .
```

برای بررسی integration واقعی، Muse Code و Node 20 لازم است. testهای repository عمداً Ruflo را اجرا یا هیچ model/provider APIای را call نمی‌کنند.

## مجوز و attribution

این bridge با مجوز [MIT](LICENSE) ارائه می‌شود. Ruflo و replica-skill نیز MIT هستند. [ATTRIBUTIONS.md](ATTRIBUTIONS.md) نسخه‌ها، لینک‌ها و مرزهای attribution را ثبت می‌کند.
