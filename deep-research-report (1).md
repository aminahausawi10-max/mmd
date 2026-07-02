# Nigerian VTU/Data Subscription Platform – PRD and Architecture (2026)

## 1. Product Strategy 

The Nigerian VTU (Virtual Top-Up) market is large and growing. In 2025, Nigerian consumers spent ₦9 trillion (~$5.67B) on airtime and data. Internet subscriptions exceed 161 million and data usage hit 721,522 TB in Jan 2024, demonstrating massive demand. Leading fintech apps (e.g. AidaPay, Cardtonic, Motobills) emphasize **speed, reliability and cashback rewards**. A competitive audit shows top apps market themselves on low rates and generous incentives; for example, Motobills promises “very fast and reliable” service with “good cashback”. Reviews note high satisfaction (e.g. 96%+ satisfaction rates for well-designed fintech UIs) but cite issues like *delays* or *unexpected fees*. Common complaints include transaction delays or failed top-ups, high prices, and poor support. 

**Competitive analysis & SWOT:** Our competitors (Opay, Kuda, AidaPay, Cardtonic, iRecharge, etc) offer similar core services (airtime, data, bills) and incentives (cashback, referral bonuses). Strengths of existing players are wide service coverage and rewards; weaknesses include intermittent reliability, hidden charges, and lack of advanced automation (users still complain of top-up failures). Market opportunities include the regulatory push for instant refunds (ensuring trust), and unmet demand for automated/AI-driven features. Revenue streams exist not only in commissions on airtime/data sales but also from **utility payments** (electricity, cable TV), exam pins, and reseller networks. A **SWOT** might highlight: 

- *Strengths:* Large market, growing smartphone penetration (66% MTN subscribers use smartphones), and existing fintech adoption (98 M bank users).  
- *Weaknesses:* Heavy competition, need for trust (network outages remain top complaint), regulatory compliance.  
- *Opportunities:* Leveraging new regulations for quick refunds, introducing AI assistants and scheduling to differentiate, tapping the reseller segment (many run small airtime shops).  
- *Threats:* Service disruptions (telco downtime), margin pressure from regulators’ tariff hikes, security/fraud risks.

**Positioning:** We position our platform as a **premium, reliable, and feature-rich VTU app**. Unlike basic recharge apps, we will offer **smart automation** (auto-renew, scheduling, AI assistance) and **family/business features** (shared wallets, resellers) to drive engagement and loyalty. We will compete on *reliability and user experience* while maintaining competitive pricing (leveraging direct VTU APIs for low cost). 

## 2. Unique Selling Proposition 

To stand out, we will implement the following key features:

- **Smart Automation:**  
  - *Auto-Renew & Scheduling:* Users can schedule recurring purchases (e.g. daily 100MB plan) or auto-renew subscriptions. This is highly convenient and reduces churn. Complexity: requires background tasks (Celery beat) and user controls. Business impact: increases usage and retention.  
  - *AI Purchase Assistant:* Chatbot or voice assistant can suggest plans based on usage patterns. Adds a modern touch; complexity moderate (could use an LLM/GPT API or heuristic). Impact: better user guidance, possible upsells.  
  - *Smart Reminders:* Notify users when balances or data are low, or bills are due. Improves retention; complexity low (Celery tasks + notifications). 

- **Family & Beneficiary Features:**  
  - *Family Wallet & Shared Balances:* Allows families to pool funds or assign allowances. Implementation: associate multiple beneficiaries to one “family” account. Impact: stickiness through social use.  
  - *Beneficiary Management:* Save frequently topped-up contacts (family, friends). Standard in banks, easy to implement, encourages repeat use.  

- **Business & Reseller System:**  
  - *Reseller/Agent Accounts:* Allow users to register as resellers, with lower API rates and the ability to top up customers. Implement user roles, sub-accounts, commission tracking. Very important in Nigeria where many are small airtime merchants. Complexity: high (new roles, commission accounting) but critical for growth.  
  - *Commission Structures:* Multi-level referral and reseller commissions. For example, a reseller might earn 2–5% on all sales they process. Define tiered rates (higher volume→higher commission).  
   
- **Gamification & Rewards:**  
  - *XP/Levels & Badges:* Award badges for milestones (e.g. 10th purchase, 1-year user). Gamification can boost engagement (studies show ~45% engagement increase). Simple to implement via badge definitions in code.  
  - *Cashback & Rewards Points:* Offer cashback on transactions and accumulate points to redeem. Already a popular feature, drives loyalty.  
  - *Referral Tree & Sharing:* Visualize the referral network and reward users for referred signups (e.g. 50% of first purchase commission). Trees encourage users to recruit others.

- **Trust & Transparency Features:**  
  - *Real-Time Success Rates:* Show each telco provider’s historical transaction success rate. Builds confidence. Needs analytics and dashboard (Prometheus/Grafana for infra; custom queries for business).  
  - *Transparency Dashboard:* Display live feed of transactions (anon) or system status. Eases trust (akin to banking “latest transactions”). Medium complexity.  
  - *Instant Refunds:* Leveraging the new NCC/CBN rule requiring 30-second refunds, automate full rollback on failures. This compliance itself is a USP (few apps will guarantee instant refunds).  

Each feature enhances user value: automation and AI make the service smarter, family/reseller features extend its market, gamification drives engagement, and trust features address core user concerns.

## 3. UI/UX Design System 

**Design Philosophy:** We aim for a **clean, modern fintech aesthetic**. White space and minimal layouts to reduce cognitive load. Use friendly, clear language (avoid jargon) for inclusivity. The interface should feel premium and trustworthy (inspired by apps like Wise and Chime). For example, display all costs upfront (no hidden fees) and use **human-centered copy** to reassure the user. Real-time feedback (push alerts, in-app updates) will keep users aware.

**Color & Typography:** A distinct brand palette (e.g. modern teal or blue for trust, with accent colors for action buttons). We’ll meet **WCAG contrast guidelines** (minimum 4.5:1 for text) for accessibility. Sans-serif typography (e.g. Open Sans, Inter) with ample sizing. 

**Grid & Spacing:** Use a responsive 8-point grid system. All layouts (mobile/tablet/desktop) adapt fluidly: e.g. on mobile, a bottom tab bar with icons; on desktop, a sidebar navigation.

**Components:** Button styles (primary accent color, ghost/outline variants), card components for plan listings, form elements (inputs, dropdowns) styled consistently. Use a toggle for dark mode. 

**Dark Mode Strategy:** Provide a fully dark theme with inverted colors. Ensure accent colors remain distinct and contrast is adequate (follow WCAG in dark context). E.g. light gray text on dark background still at 7:1 contrast (WCAG AAA). Toggle should be automatic (based on system preference) but user-overridable. 

**Accessibility:** Follow WCAG 2.1 AA. All text ≥4.5:1 contrast, large clickable areas for mobile, support screen readers (ARIA labels). Keyboard navigation (tab order) for web. No pure color to convey info (add icons/text labels). Ensure focus states on buttons. Mobile usability: thumb-friendly buttons, single-handed reach for key actions.

## 4. Information Architecture 

**Public Pages:** 
- **Landing (Home):** Hero banner (key USP), feature highlights, download/signup CTA. 
- **Pricing:** Clear summary of any fees or premium tiers (if any). 
- **Features:** List platform features (auto renew, cashback, reseller, etc). 
- **Contact/Support:** Contact form, FAQ. 
- **About:** Company info.

**Auth Pages:** 
- **Login/Register:** Simple, mobile-optimised forms. 
- **Password Reset:** Email reset flow. 
- **Verification:** OTP or email verification page.
  
**Dashboard (after login):** Top nav or sidebar with: 
- **Overview:** Wallet balance, recent transactions, quick actions (buy data/airtime), pending alerts.  
- **Wallet:** View funds, add funds, transaction history.  
- **Transactions:** Detailed history and filters (date, type).  
- **Referrals:** Show referral stats, referral link, commission earned.  
- **Rewards:** Points/Badges page, loyalty progress.  
- **Settings:** Profile, security (password, 2FA), notification prefs.  

**Services Pages:** (main content area) 
- **Buy Data:** Choose network (MTN, Airtel…), select data plan (with UI card for each plan).  
- **Buy Airtime:** Similar flow, choose network and amount (preset buttons and custom).  
- **Electricity:** Choose DISCO, input meter number, amount.  
- **TV Subscription:** Choose provider (DSTV, GOtv, Startimes), smartcard number, package.  
- **Exam Pins:** Choose exam (WAEC, NECO, etc), number of pins.  

Each service page includes input validation (e.g. meter number format) and a summary of cost before confirming.

*Hierarchy Diagram:* (Description) Home → Services (Data/Airtime/Bills/TV/Pin) and Dashboard sections. Authentication gates Dashboard. Each main section may have subpages (e.g. in Settings: Profile, Security). 

## 5. User Flows 

We detail critical flows as step sequences (or flowcharts if drawn):

- **Registration:** User opens app → taps Register → enters phone/email + password → optional referral code → system sends OTP/verification email → user enters code → account created (with initial wallet) → user lands on Dashboard.  

- **Wallet Funding:** (Using Paystack/Flutterwave) User taps “Fund Wallet” → enters amount → choose payment gateway (Paystack or Flutterwave) → system creates a payment reference and redirects to checkout → user completes card or USSD payment → our webhook listens and verifies payment → on success, credit user’s wallet balance and notify user. For failures, automatically rollback and notify.  

- **Data Purchase:** User selects “Buy Data” → picks network, selects a plan, enters phone (auto-detect network), taps “Buy” → shows confirmation (cost, balance check) → on confirm, system debits wallet and sends top-up API request to provider (e.g. Interswitch) → wait for success webhook/response → if success, credit phone; if fail, rollback and refund. Notify user of result.  

- **Airtime Purchase:** Similar to Data purchase (except no plan selection, just amount).  

- **Bill Payment (Electricity/TV):** User selects bill type, enters account number, system optionally verifies customer (e.g. meter validity via provider API), user confirms bill amount displayed (if possible), then proceed as data purchase. 

- **Referral System:** A logged-in user goes to Referrals → sees unique referral link/code → shares with friends. When a new user registers with that code and completes first purchase, the referring user earns a bonus commission (automatically tracked). Users can see their referral hierarchy and earnings.  

- **Reseller Registration:** In Profile or separate “Become an Agent” section: user applies by providing business info, accept T&Cs → admin review/auto-approval (if criteria met) → user gets “reseller” status. Then they have access to discounted rates and can manage downline.  

- **Cashback Redemption:** System tracks cashback (e.g. as wallet credit). User sees cashback balance in Rewards or Wallet. They can “redeem” by converting points to credit (immediately applied to wallet).  

- **Failed Transaction Recovery:** If a transaction fails (e.g. telco API error), the system automatically refunds in <30s. The user sees an error message and refunded balance. A retry option may be offered.  

(Flow diagrams: For each, we would draw decision nodes: e.g. “Payment success?” branches to success/refund.)

## 6. Wireframes 

For each page, we define key layout:

- **Landing Page:** Top navigation (Logo, About, Contact, Login/Sign Up). Hero section with product tagline and CTA buttons (e.g. “Sign Up” or app store icons). Below, sections highlighting features (cards with icon+title+blurb). Footer with links (Privacy, T&C). Mobile: collapse nav to hamburger.

- **Login / Register:** A centered form card (on wide screens, split screen with graphics). Fields stacked vertically. "Submit" button full-width. Link to switch between Login/Register. Mobile: full-width input.

- **Dashboard Overview:** Sidebar (or top bar on mobile) for navigation. Main area: wallet balance card at top with "Add Funds" button. Below: buttons or cards for quick actions (Buy Data, Airtime, Bills). Recent transactions listed as a scrollable list or table. On wider screens, a two-column grid: left for balance/quick actions, right for news/alerts.

- **Wallet Page:** Show balance prominently. A list of transactions (scrollable). “Fund Wallet” button. Each transaction card: date, type, amount, status.

- **Buy Data Page:** 
  - **Desktop:** Two columns. Left: list of networks (icons). Right: data plans table or cards (each: name, volume, price, validity, “Buy” button). Top bar: back or breadcrumb, and wallet balance indicator.
  - **Mobile:** Step 1: Select network (list or icons). Step 2: Display plans; user scrolls vertically.

- **Electricity Page:** Form: dropdown for Disco, input meter #, display account name (after validation), input amount, “Pay”. Responsive to mobile screen.

- **Profile/Settings:** Form sections for personal info (email, phone), security (change password, enable 2FA), and app settings (dark mode toggle, notification preferences).

Every page will have a consistent header with logo and a user menu (Profile/Logout) on desktop; mobile uses a bottom tab bar or slide-out menu. Use cards and clean lists (no clutter). Buttons in accent color.

## 7. Database Design 

We propose a **PostgreSQL schema** with tables:

- **users**: *id (PK)*, name, email (unique), phone (unique), password_hash, role (user/reseller/admin), referral_code (unique), created_at, is_active, etc. Index on email/phone.  

- **wallets**: *id*, user_id (FK→users), balance (decimal), currency, updated_at. Unique index on user_id. (Optionally split balances per currency).  

- **transactions**: *id*, user_id (FK), wallet_id (FK), type (enum: “fund”, “purchase”, “refund”, “commission”, etc), service (nullable: e.g. “data”, “airtime”, “electricity”), amount (decimal), status (enum: “pending”, “success”, “failed”), provider_id (FK to providers table, if used), provider_txn_ref (string), created_at, updated_at. Index on user_id and status.  

- **data_plans**: *id*, network (e.g. “MTN”), plan_code (provider’s code), name (e.g. “Daily 200MB”), volume (e.g. 200MB), validity (days), price (decimal), active (bool). FK network_id if separate networks table.  

- **networks**: *id*, name (Airtel/MTN/Glo/9Mobile/Cable/Electric), type (enum: “telco”, “tv”, “electricity”), etc.  

- **referrals**: *id*, referrer_id (FK users), referee_id (FK users), commission_amount (decimal), created_at. (Alternate: store commission per transaction in an affiliate table).  

- **rewards**: *id*, user_id, points (int), description, earned_at. (For cashback or loyalty points.)  

- **notifications**: *id*, user_id, type (“email”, “sms”, “in-app”), content (text/json), status (“sent”, “queued”, “failed”), created_at, delivered_at. Index on user_id.  

- **beneficiaries**: *id*, user_id, name, phone, service_type (“airtime”, “electricity”), created_at.  

- **subscriptions**: *id*, user_id, service_type (e.g. “data”, “tv”), details (JSON for plan info), schedule (cron expression or interval), next_run (timestamp), active (bool). Used for auto-renew.  

- **audit_logs**: *id*, action (string), model (string), model_id, performed_by (FK users or system), changes (JSON), timestamp. Tracks admin actions or important events.  

- **support_tickets**: *id*, user_id, subject, message, status (“open”, “resolved”), created_at, updated_at.  

**Relationships:** Each wallet belongs to a user. Each transaction links to user and wallet. Referrals link two users. Subscriptions and beneficiaries belong to users. 

**Indexing:** 
- Primary keys on all id columns. 
- Unique indexes on users.email, users.phone, users.referral_code. 
- Foreign keys with ON DELETE CASCADE where appropriate (e.g. deleting user removes their wallet, transactions). 
- Transactions: index on (user_id, created_at) for fast history queries; index on type or status for reports. 
- DataPlans: index on network type + volume. 
- Beneficiaries: index on user_id. 
- Use UUIDs for PKs if desired for security (or bigserial). 
- Audit logs: consider partitioning or TTL purge if very large.

*(ER Diagram:* Entities as above with the stated FKs. For brevity, diagram not shown.*)

## 8. Django Project Architecture 

We will use a modular Django setup (example from best practice). For instance:

```
project_root/
├── config/          # project-level configuration (settings, URLs, wsgi, celery)
├── apps/
│   ├── accounts/    # user models, authentication, profiles, referrals
│   ├── wallet/      # wallet balance logic, funding
│   ├── transactions/ # payment & purchase transactions
│   ├── services/    # logic for data, airtime, bills, tv subscriptions
│   ├── referrals/   # referral program logic
│   ├── rewards/     # cashback, loyalty points
│   ├── notifications/ # sending emails/SMS/in-app
│   ├── analytics/   # usage stats, providers performance
│   ├── support/     # support tickets
│   └── common/      # shared utilities (custom exceptions, mixins, permissions)
└── infrastructure/  # third-party integrations (e.g. payment, VTU clients)
```

**config/** contains `settings.py` split by env (development, production), `urls.py`, `asgi.py`, `wsgi.py`. We keep sensitive settings out via environment variables. 

**apps/** are Django apps focused on a single domain. For example: 
- *accounts*: user registration, login, 2FA, and referral tracking.  
- *wallet*: model and APIs to fund wallets (integration with Paystack/Flutterwave).  
- *transactions*: handles processing of purchases and recording outcomes.  
- *services*: calls VTU biller APIs for data, airtime, electricity, TV, exam pins.  
- *referrals*: tracks referral relationships and bonuses.  
- *rewards*: awards cashback or points after transactions.  
- *notifications*: queuing and sending emails/SMS/push (using Celery tasks).  
- *analytics*: collects metrics (e.g. provider uptime, conversion rates).  
- *support*: CRM for user tickets.

**infrastructure/** can hold low-level code for integrations: e.g. Paystack client, VTU API clients (eBills, Interswitch), Celery config, etc.

This clear separation ensures maintainability.

## 9. API Architecture 

We will expose a RESTful JSON API (versioned, e.g. `/api/v1/...`), built with Django REST Framework. Endpoints include:

- **Authentication:** 
  - `POST /api/v1/auth/register` (body: email, phone, password) → registers user (sends OTP)  
  - `POST /api/v1/auth/verify` (body: user_id, otp) → verifies account  
  - `POST /api/v1/auth/login` (body: email/phone, password) → returns JWT token  
  - `POST /api/v1/auth/password-reset` and `/password-confirm` for resetting.

- **Wallet:**  
  - `GET /api/v1/wallet/balance` → `{balance: 1000.00}`  
  - `POST /api/v1/wallet/fund` (body: amount, gateway) initiates a funding transaction (response with `payment_url` or `reference`).  
  - `POST /api/v1/wallet/fund/callback` – webhook endpoint for gateways (internal, not exposed to clients).  

- **Transactions:**  
  - `GET /api/v1/transactions/` → list user transactions (with filters, pagination).  
  - `GET /api/v1/transactions/{id}` → detail of a specific transaction.  

- **Data Purchase:**  
  - `GET /api/v1/data/plans` → list available plans (can filter by network).  
  - `POST /api/v1/data/purchase` (body: plan_id, phone, request_id) → processes purchase.  
    - *Request Example:* `{"plan_id": 5, "phone": "08012345678", "request_id": "req_abc123"}`  
    - *Response Example (success):* `{"status":"processing","order_id":"12345","message":"ORDER PROCESSING"}` or final `status: "completed"`.  
  - Error handling: returns 4xx with error message if e.g. insufficient funds or invalid input.  

- **Airtime Purchase:** (similar to data)  
  - `GET /api/v1/airtime/` (optional list of networks).  
  - `POST /api/v1/airtime/purchase` (body: network, amount, phone, request_id).  

- **Bills (Electricity/TV/Exam Pins):**  
  - Each has endpoints, e.g. `POST /api/v1/bills/electricity` (body: disco_code, meter, amount, request_id).  
  - For TV: `POST /api/v1/bills/tv` (body: provider, smartcard_no, package_id, request_id).  
  - Exam Pins: `POST /api/v1/exams/pins` (body: exam_type, quantity, request_id).  

  *These verify input (e.g. validate meter number) and call provider APIs. Example success: `{"status":"completed","data":{...}}`.*

- **Referrals:**  
  - `GET /api/v1/referrals/` → referral stats (total referrals, earnings).  
  - `GET /api/v1/referrals/tree` → nested referral tree.  
  - `POST /api/v1/referrals/redeem` → convert referral bonus to wallet funds.

- **Notifications:**  
  - `GET /api/v1/notifications/` → list of in-app notifications.  
  - `PUT /api/v1/notifications/{id}/read` → mark as read.

- **Rewards:**  
  - `GET /api/v1/rewards/balance` → points/cashback balance.  
  - `POST /api/v1/rewards/redeem` (body: points) → redeem for wallet credit.

- **Subscriptions:**  
  - `GET /api/v1/subscriptions/` → list active subscriptions.  
  - `POST /api/v1/subscriptions/` (body: service_type, details, schedule) → create auto-renew.  
  - `DELETE /api/v1/subscriptions/{id}` → cancel.

- **Admin APIs:** (protected, or via Django admin UI)  
  - For analytics: `GET /api/v1/admin/transactions` (all users), user management (`GET /api/v1/admin/users`), etc.  

All endpoints require JWT auth (Authorization: Bearer). Errors use standard DRF format, e.g. `{"detail":"Invalid token"}` (401) or `{"error":"Insufficient balance"}` (400). We ensure CSRF is disabled for API or use token auth.

_Citation:_ REST APIs should use nouns and consistent URIs; we follow that convention. 

## 10. Payment System 

We integrate **Paystack** and **Flutterwave** for wallet funding. Both support NGN and local payment methods.

- **Paystack:**  
  - We redirect users to Paystack’s checkout (or inline via their JS). Create a payment via Paystack API; store the `reference`.  
  - **Webhook:** Implement a `/webhook/paystack/` endpoint. Verify events by checking the `X-Paystack-Signature` (HMAC SHA512) header before processing. On `charge.success`, verify the transaction via Paystack’s verify API for extra safety, then credit the user’s wallet. If webhook fails (no 200 OK), Paystack retries (up to 72h).  
  - **Reconciliation:** On app startup (or periodically), call Paystack’s transaction verification API to reconcile any missed updates.  
  - **Security:** Use Paystack’s webhooks with signature verification and ensure our endpoint is HTTPS.  

- **Flutterwave:**  
  - Similar process: create a payment session via Flutterwave API, redirect user to their payment page.  
  - **Webhook:** Use Flutterwave’s webhook. They recommend signature verification (set a `secret_hash` in dashboard) by checking `verif-hash` header, matching our known secret.  
  - On receiving `charge.completed`, validate and update wallet.  
  - **Reconciliation:** Also available via their API if needed.  
  - **Security:** Whitelist IPs optionally, and always verify signature.  

- **Flow:**  
  1. User initiates `POST /wallet/fund` → server calls Paystack/Flutterwave to initialize transaction.  
  2. User completes payment on gateway.  
  3. Gateway sends webhook event to our server.  
  4. We verify webhook signature and mark the transaction as successful (credit wallet) or failed (no credit, possibly retry).  
  5. All status changes (success/failure) are logged in `transactions` table.

- **Automatic refunds:** If a VTU order fails later, we refund by creating a "refund" transaction tied to the original, returning funds to wallet.

## 11. VTU Integration 

We will integrate multiple Nigerian VTU providers for redundancy. Key considerations are reliability, API quality, and cost.

- **Interswitch (Quickteller VTU):** Covers all major networks (MTN, Airtel, Glo, 9mobile) with instant delivery. Uses OAuth2 (client ID/secret) and requires a virtual card. We can fetch plans and recharge via their API. Reliability is high (direct bank-backed service).  
- **eBills.africa:** Offers broad services (airtime, data, cable TV, electricity, exam pins) with direct connections to operators. Notably, it *automatically refunds all failed orders*, easing compliance. Authentication is via JWT token (update every 7 days). We will use eBills for most services due to its comprehensiveness and low prices (direct operator integration).  
- **MobileVTU.com:** Provides RESTful API for airtime/data. Uses API token and request IDs in headers. Good as a backup for airtime/data.  
- **Aggregator fallback:** We can also use global aggregators like **Reloadly** (covers Nigerian networks) or **VTUGate** for multi-country support if needed.  
- **Failover strategy:** Implement a *multi-provider* pattern: primary calls to eBills/Interswitch; if a transaction fails or times out, automatically retry the same request through a secondary provider (if supported). For example, if eBills is down for an MTN recharge, switch to Interswitch or MobileVTU. Track provider health metrics (via Grafana) to pick best route.  

We recommend **eBills** as the primary provider (for its price and refunds guarantee) and **Interswitch Quickteller** as backup (for airtime/data) or vice versa. Another backup is **Flutterwave’s VTU API** if one becomes available.  

*(Provider comparison: eBills – broad services, auto-refunds; Interswitch – high trust; Reloadly – broad network, but as an international service.)* 

## 12. Automation System 

We will use **Celery** with **Redis** as broker to handle background jobs. Key tasks include:

- **Periodic Jobs (celery beat):**  
  - **Auto-renew Purchases:** Cron job that checks `subscriptions` table for due renewals and triggers purchases.  
  - **Reminders:** Daily or weekly tasks to send “low balance” or “due bill” notifications via email/SMS.  
  - **Referral Payouts:** On a schedule (e.g. daily), calculate referral commissions earned and credit them to wallets.  
  - **Data/Revenue Reports:** Generate daily summaries (e.g. total sales, pending transactions) and send to admins.  
  - **Cache Refresh:** Preload frequently used data (e.g. plan lists) daily.

- **Task Queues:**  
  - **Processing Transactions:** When a user makes a purchase, the view enqueues a Celery task to call the VTU API. The HTTP request runs asynchronously; the user sees “processing” and later gets success/fail.  
  - **Sending Notifications:** Email/SMS is done asynchronously (so web requests are fast).  
  - **Retry Logic:** Celery retries (exponential backoff) for transient failures (e.g. provider API timeout).  

- **Example:** Celery Beat runs the task `process_due_subscriptions()` every hour. This function queries all active auto-renew subscriptions whose `next_run <= now`, and for each, enqueues a data purchase task, then updates `next_run`.  

This design ensures no human admin action is required: everything from refunds (triggered by provider callbacks) to payouts is automated. Celery’s scheduling is well-suited for such periodic tasks.

## 13. Security Architecture 

We adopt enterprise-grade security measures:

- **Authentication:** Use JWT (JSON Web Tokens) for stateless API auth. Refresh tokens can be implemented for long sessions. All sensitive endpoints require HTTPS.  
- **Session Security:** On web (if any), set `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` (HTTPS only). Use Django’s CSRF middleware for any form.  
- **Rate Limiting:** Implement throttling on APIs (e.g. max 5 login attempts per minute, max 100 requests/min per IP) using Django REST Framework’s throttling classes. This mitigates brute force and abuse.  
- **CSRF Protection:** Disabled for API endpoints (using tokens instead), but enabled on any web forms. Ensure `X-Frame-Options: DENY`.  
- **XSS Protection:** All templates auto-escape output. Content Security Policy (CSP) headers will be configured to only allow known script sources (minimize inline JS).  
- **SQL Injection:** Using Django ORM avoids manual SQL. All user inputs must be validated/escaped.  
- **API Security:** All endpoints require authentication except public info. Use scopes/roles to restrict admin APIs.  
- **Webhook Security:** As noted, verify Paystack HMAC signature and Flutterwave `verif-hash` to ensure authenticity. Whitelist their IP ranges if desired.  
- **Data Encryption:** Store sensitive data (passwords) hashed with bcrypt/Argon2. Do not store any card details. Wallet balance is a simple number.  
- **Fraud Prevention:** Monitor for unusual patterns (e.g. bulk refills, high-value transactions) and flag accounts. Implement 2FA (via SMS or Authy) for high-risk actions. Possibly integrate AML checks (customer KYC) for large amounts.  
- **Logging & Monitoring:** All security events (failed logins, transaction failures) are logged. Use Sentry for exception alerts, and Prometheus alerts on suspicious spikes. Regular security audits and penetration testing are scheduled.

## 14. Admin Dashboard 

The admin interface (using Django Admin or a custom dashboard) will include:

- **Analytics Widgets:** Total revenue (daily/week/month), number of transactions, top-selling services (charts). Possibly using Grafana dashboards integrated (Prometheus/Grafana for system metrics).  
- **User Management:** Search/modify users, block suspicious accounts, manage KYC tiers (for resellers).  
- **Transaction Monitoring:** View all transactions, filter by type/status, flag anomalies.  
- **Revenue Tracking:** View commission payouts, total fees collected.  
- **Support:** List of support tickets, ability to update status and reply to users (possibly with canned responses).  
- **Audit Logs:** View of recent critical actions (user created, payments failed, password resets) from `audit_logs`.  
- **System Health:** Dashboard of Celery tasks status, Redis/DB usage, etc. (Potentially integrated via Prometheus/Grafana charts for uptime and errors).

For ease, we could enhance Django’s admin with custom reports or build a simple React/Vue admin panel pulling from secured internal APIs.

## 15. Notification System 

We will support multiple channels:

- **Email:** Use a service like **SendGrid** or **Amazon SES** for transactional emails (OTP, receipts). Emails are sent asynchronously by Celery. Emails templates (Django template or Markdown) will be responsive and include system branding.  
- **SMS:** Use a bulk SMS provider. Options: **Twilio** (Nigeria coverage via partners), or local SMS API (e.g. BulkSMSNigeria.com, Celcom Africa). We’ll use SMS for OTP and critical alerts (failed transaction). For bulk promotions, use a compatible gateway that supports high volumes. The system will queue SMS via Celery and parse delivery reports.  
- **Push Notifications:** For mobile app (if any), use **Firebase Cloud Messaging (FCM)**. For web push, also FCM or another service. We should design in-app notifications (stored in `notifications` table) that users see in the UI, and optionally badge on mobile.  
- **In-app (UI) Notifications:** Show alert banners or a notification center with messages (e.g. “Top-up successful”, “Your bill is due tomorrow”). These are generated by backend and fetched via API.  
- **Preference Handling:** In Settings, users can opt in/out of email/SMS alerts for promotions vs essential alerts.  

All outbound channels must have templates and be localised (English UK). For email/SMS providers, ensure data privacy (GDPR-like compliance) by not storing more data than needed.  

## 16. Analytics 

We will track and display key metrics:

- **Revenue Analytics:** Daily/weekly/monthly top-line sales, broken down by service (data vs airtime vs bills). Charts of growth trends.  
- **User Analytics:** New registrations per day, active users (DAU/MAU), retention rates. Segment by channel (referrals, organic).  
- **Referral Analytics:** Number of referrals made, conversion rate of invites, commission earned per tier.  
- **Conversion Tracking:** E.g. what percentage of wallet funds lead to purchases. If integrated with web/landing, track conversion funnel (register→fund→buy). Possibly integrate with Google Analytics or a tool like PostHog.  
- **Provider Performance:** Success rate per VTU provider (e.g. Interswitch vs eBills) shown over time, to choose failover paths.  
- **Retention Metrics:** How many recurring customers (savings by subscribers vs one-offs), average transactions per user.

We will use Grafana dashboards (connected to Prometheus and/or our database) to plot these. For business metrics, custom SQL queries on PostgreSQL can feed a BI tool or Grafana via PostgreSQL plugin. Alternatively, integrate with a SaaS BI or use Jupyter for offline analysis.

## 17. Deployment 

We compare cloud options:

- **AWS:** Extremely scalable, many services. We can use EC2/Docker on ECS or EKS, RDS for Postgres, ElastiCache (Redis), S3, etc. Pro: industry-standard, global. Con: complex and can be costly at scale.
- **DigitalOcean:** Simpler. DO App Platform or Droplets: starting $5/mo per droplet. Managed Postgres/Redis available. Good for mid-scale.  
- **Hetzner:** Very cost-effective (e.g. €4.50 VM with 4GB RAM), but requires more DIY (set up DB, load balancing ourselves). Very cheap for pure compute/DB.
- **Render:** PaaS (like Heroku). Render’s Hobby tier is free (no hours) plus usage charges. Good for straightforward Docker deployments and has managed Postgres. Tiered pricing (Pro ~$25+) for more resources. 
- **Railway:** PaaS with usage-based billing. Easier for quick deploys, but as of mid-2026 had reliability concerns (frequent outages noted). Likely not ideal for production-critical service.
- **AWS vs Others:** AWS is most robust for scale (99.99% SLAs), but requires ops expertise. DO/Hetzner are cheaper but require manual scaling. PaaS like Render offers managed cron and DB, good for MVP/Growth, though usually more expensive per resource than raw VMs.

**Recommendation:** Use **Render** (or similar PaaS) for initial launch (ease of CI/CD, autoscaling features) and **AWS** for long-term scaling. Render has free and low-cost tiers to start, and supports Docker, cron jobs, and managed Postgres/Redis out-of-box. If budget allows, a Dockerized app on DigitalOcean with managed PostgreSQL and Terraform for infra is another path. 

**Cost Estimate:** 
- Render: ~$25-50/month for web + worker + DB in modest use. 
- AWS: e.g. t3.small (~$20/mo) + RDS ~ $25 + bandwidth. 
- DO: ~$5-10 droplet + managed Postgres $15-30. 
- Hetzner: VM €4 + maybe cloud database €15 = ~€25/month.

**Scalability:** All platforms can auto-scale. Use Docker containers (Gunicorn + Nginx). Keep stateless (use Redis for sessions/queues). For high load, add more web dynos/instances behind load balancer. 

**Backups:** Use managed DB snapshots (Daily on AWS/Render/DO). Store media (user uploads, receipts) on **Cloudinary** (as per tech stack) with backups. 

## 18. DevOps 

- **Docker:** Containerize each service (web, Celery worker, Redis, Postgres). Use Docker Compose for local dev; Kubernetes or Docker Compose on target.  
- **CI/CD:** Use **GitHub Actions** (leading tool with ~33% usage) to run tests and deploy on push to `main`. For example, on push:
  1. Lint/format (flake8, black).
  2. Run unit tests (pytest) with coverage. 
  3. Build Docker images and push to container registry.
  4. Deploy to chosen platform (Render CLI or DO kubectl).
- **Secrets Management:** Use GitHub Secrets for CI. Use environment variables for production (e.g. on Render or AWS Parameter Store) to store keys (Paystack, DB credentials). Do not embed secrets in code.  
- **Monitoring & Logging:**  
  - *Application logs:* Structured logs (JSON) collected by a service (e.g. Sentry or Loggly). Set levels (INFO, WARN, ERROR).  
  - *System metrics:* Prometheus collects CPU, memory, queue lengths. Grafana dashboards for health.  
  - *Alerts:* Sentry for exceptions; cloudWatch/Datadog for infra alerts.  
- **Infrastructure as Code:** Use Terraform to provision AWS/DO resources.  
- **Environment Management:** Multiple envs (dev, staging, production). Use Django settings module switch (DJANGO_SETTINGS_MODULE) or django-environ.  
- **Testing Pipelines:** GitHub Actions flows separate branches; PRs must pass tests before merge. Deploy on tag push or manual trigger to prod. 

*Diagram (conceptual):* Developer → GitHub → CI (GitHub Actions) → Build/Test → Registry → PaaS (Render/AWS) → Auto-deploy + run → Monitors (Sentry/Prometheus)*.

## 19. Testing Strategy 

We will aim for high coverage (≥90%):

- **Unit Tests:** For every Django app, test models, serializers, and utilities. Use `pytest-django` or Django TestCase. E.g. test user registration flow, edge cases (invalid phone).  
- **Integration Tests:** Using Django’s test client or tools like Postman. Tests for API endpoints: simulate complete flows (login→buy data), including error cases.  
- **API Tests:** Use DRF test suite or Postman collection to test REST endpoints. Validate authentication, permissions, rate limiting.  
- **Security Tests:** Run tools like [sqlmap](https://sqlmap.org/) to test SQL injection (should find none). Use Django’s built-in tests for CSRF. Possibly OWASP ZAP to scan the running app for XSS, etc.  
- **Load/Stress Tests:** Use a tool like **Locust** or **k6** to simulate heavy usage (e.g. 1000 concurrent users doing top-ups). Focus on peak capacity of Celery queue and DB.  
- **End-to-End Tests:** For critical paths (e.g. payment checkout), we can write automated Selenium or Cypress tests (especially for web interface).  
- **Continuous Testing:** CI pipeline runs tests on every commit. Coveralls or Codecov for coverage reports.  
- **Performance Tests:** Profile Django endpoints; use `pytest-benchmark` or Django’s `assertNumQueries` to minimize N+1 queries.

All tests should run in CI. Security tests (like dependency vulnerability scanning) should also run (e.g. `bandit` or GitHub Dependabot alerts). Regularly schedule regressions on staging.

## 20. Business Model 

**Revenue Streams:**  
- **Airtime/Data Sales:** Margins on bundles (e.g. 5–10% profit per sale). We might add a small convenience fee.  
- **Utility Bills & Pins:** Typically smaller volumes, but commissions per transaction (e.g. ₦5–₦20).  
- **Reseller/Agent Fees:** We may charge agents a membership/sub-account fee or let them keep margin (we profit on wholesale difference).  
- **Premium Subscriptions:** Offer a paid “Plus” tier (e.g. ₦5000/yr) giving higher referral rates or priority support.  
- **Advertisement/Partner Offers:** (Optional) display targeted promotions (though we must balance UX).

**Financial Projections (example):**  
- *Startup Costs:* Minimal as a software platform. Expect costs for development (if outsourced, otherwise mainly salaries), infrastructure (~$100–$300/month initially), marketing (~variable).  
- *Monthly Costs:* Servers/DB ($50–$100), SMS/Email API ($50), support staff (if any).  
- *Revenue:* If 10,000 active users each transacting ₦5,000/month (data+airtime) at 5% margin, that’s ₦25M revenue (before VAT) per month. Break-even can be reached quickly if user acquisition is strong.  
- *Breakeven:* If fixed costs ~₦1M/month and net margin 5%, need ₦20M/month sales. With marketing, maybe 6–12 months to reach thousands of users.

**Pricing Example:** We earn on volume rather than user fees. For instance, resellers buying ₦1M airtime would yield ₦50k profit (at 5% margin). 

*(All figures rough; detailed finance model would require actual cost and user forecasts.)*

## 21. MVP Roadmap 

- **Phase 1 (MVP) – Core Platform (Months 1–3):**  
  - Basic wallet, user registration, login (including OTP).  
  - Integrate a primary payment gateway (Paystack) for wallet funding.  
  - Implement Data and Airtime purchase flows (select plan, confirm, send to VTU).  
  - Ensure automatic refund on failures (comply with NCC 30s rule).  
  - Launch on web/mobile-web (responsive).  
  - Basic UI (light mode only), minimal design system, essential analytics (volume).  

- **Phase 2 – Growth Features (Months 4–6):**  
  - Add other services: Electricity bills, TV subscriptions, Exam Pins.  
  - Implement referral program and reseller signup.  
  - Introduce cashback rewards and gamification badges.  
  - Build admin dashboards (analytics, user management).  
  - Implement dark mode, accessibility improvements.  
  - Expand to multi-channel notifications (SMS + email) and add Flutterwave as second payment provider.  

- **Phase 3 – Scale and Differentiation (Months 7–12):**  
  - Launch AI assistant (simple chatbot or smart plan suggestions).  
  - Enhance family features (shared wallet, beneficiary management UI).  
  - Optimize performance and scaling (migrate to Kubernetes or additional instances).  
  - Expand marketing, add premium subscriptions or loyalty tiers.  
  - Expand into other African markets (if desired) using provider-agnostic design.  
  - Continuous improvements: more languages, deep analytics, specialized campaigns (e.g. seasonal data promos).  

Each phase ends with a private beta release to test features before wide launch. Ongoing: gather user feedback to iterate UI and add requested features.

**Development Timeline:**

1. **Month 1:** Setup project repo, CI/CD, basic Django skeleton. Implement user auth (including phone OTP).  
2. **Month 2:** Develop wallet funding (Paystack) and data purchase flow. Integrate one VTU provider. Basic UI layouts. Testing core flows.  
3. **Month 3:** Test, fix bugs, prepare initial launch (friends/family testing). Deploy to production.  
4. **Month 4–5:** Add remaining services (bills, TV, pins). Build referral and admin modules.  
5. **Month 6:** Analytics dashboards and marketing launch.  
6. **Months 7+:** Implement advanced features (AI, gamification), scale platform.

Each sprint (2–4 weeks) will deliver increments. We will follow Agile methodology, with user stories for each feature.

 

**Sources:** Market statistics, competitor analyses, design guidelines, technical best practices. These informed our strategy and architecture.