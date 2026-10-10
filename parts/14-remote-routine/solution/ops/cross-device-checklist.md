# Cross-device continuation checklist

| Check | Status |
|---|---|
| Remote Control is enabled for the org (Team/Enterprise: an Owner turns it on in the admin settings) | ☐ |
| Logged in with a claude.ai account (`/login`), not an API key | ☐ |
| Session started with `claude --remote-control "<name>"` or `/remote-control` in a running session | ☐ |
| Laptop stays awake and online; the `claude` process keeps running (the session runs locally) | ☐ |
| Session visible at claude.ai/code and in the mobile app's Code tab | ☐ |
| Permission mode chosen before leaving the desk (Manual for anything risky) | ☐ |
| I know what stays local: files, credentials, VPN access, `/plugin`, `/resume` | ☐ |
| Stop condition written in the first prompt ("stop after the report; do not edit files") | ☐ |
| Result written to a file in the repo, not only in chat | ☐ |
| Local session vs cloud session: if no local context is needed, consider `claude --cloud` or a routine instead | ☐ |
