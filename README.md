# Oxygen Live Event: Project Design

Nov 20, 2026 · @ABDOUL HAKI

Oxygen Live Event is a booking website where clients reserve event services (sound, video recording, studio, training) and pay online; this is version 1 of the design and it will evolve.

## Core rules

Each service accepts at most 3 bookings per date; when a date is full for that service, the client sees "Not available, choose another date".

- The limit (3) is a setting per service, so the admin can change it later.
- A client chooses service, date, time, and describes what they want.
- Payment is automatic and an invoice (PDF) is issued right after.
- Registration requires email verification.
- All site content (services, news, contact info) comes from the database and is managed by the admin.
- An AI assistant guides the client through the site and the booking.
- Open question: is the limit of 3 per service, or 3 in total for all services? This design assumes per service.

## Features

The site has three parts that share one backend and one database; a role field (client or admin) decides who can see what.

| Part | Who | Pages and features |
| --- | --- | --- |
| Public site | Any visitor | Home (hero, featured services, latest announcements), Services list, Service detail (name, picture, description, price), News, Contact form, Register, Login |
| Client area | Logged-in client | Booking (service, date, time, details), automatic payment, invoice PDF, profile, booking history, content shared by the company, AI assistant chat |
| Admin area | Staff only | Manage services (add, edit, delete, max per day), publish announcements, site settings (contact info, home text), bookings (confirm, cancel, block dates), clients and payments, contact messages, shared content |

## Tech stack

Python and PostgreSQL carry the backend because you already know Python and SQL; Django Admin gives the admin part almost for free.

| Layer | Technology | Library or tool |
| --- | --- | --- |
| Backend | Python, Django | Django REST Framework, django-cors-headers, django-environ |
| Database | PostgreSQL | psycopg |
| Auth and security | JWT, email verification | simplejwt, dj-rest-auth, django-allauth, django-ratelimit |
| Background jobs | Celery, Redis | emails, invoices, reminders |
| Frontend (public and client) | Next.js, TypeScript | Tailwind CSS, shadcn/ui, React Hook Form, Zod, TanStack Query, Axios, react-day-picker |
| Admin (phase 1) | Django Admin | django-jazzmin |
| Admin (phase 2, optional) | React dashboard | Refine or React Admin, Recharts |
| Payment | FedaPay or KKiaPay | official SDK (supports Mobile Money in Benin) |
| Email | Brevo or Resend | verification and invoice emails |
| Invoices | PDF generation | WeasyPrint |
| Images | Cloud storage | Cloudinary or S3 |
| AI assistant | Claude API | anthropic Python SDK |
| Deployment | Docker, Nginx, HTTPS | Render, Railway or a VPS |

## Database

Ten tables cover users, services, bookings, payments and all site content; the 3-per-day rule is checked by counting active bookings for a service and date before saving.

| Table | Key fields |
| --- | --- |
| User | email, password, role (client or admin), email\_verified, full name, phone |
| Service | name, image, description, price, max\_per\_day, is\_active |
| Booking | user, service, date, time, details, status (pending, confirmed, cancelled, done) |
| Payment | booking, amount, provider, reference, status, paid\_at |
| Invoice | payment, number, pdf file, issued\_at |
| Announcement | title, text, image, is\_published, published\_at |
| ContactMessage | name, email, message, is\_read, created\_at |
| SiteSetting | key, value (phone, address, social links, home text) |
| SharedContent | title, file or link, description, visible to clients |
| ChatMessage | user, role (user or assistant), text, created\_at |

## Roadmap

Build the backend first, since it is where your Python and SQL skills help most; learn the frontend once the API works.

1. Setup: Python, virtual environment, Django project, PostgreSQL, Git and GitHub
2. Models: services and announcements, with Django Admin
3. Public pages: home, services, service detail, news, contact
4. Auth: register, email verification, login, roles
5. Booking: form, availability check, the 3-per-day rule
6. Payment and invoice PDF
7. Client profile and booking history
8. AI assistant
9. Security review and deployment

Learning goal: for each step, read the matching official documentation (Django, DRF, Next.js), write the code yourself first, then review it with Claude and note what you learned.

Security checklist: role check on every API route, password hashing, HTTPS, rate limiting, secrets in .env, never store card data.

## Recap for the next chat

Paste this prompt at the start of a new conversation so another Claude can continue as a tutor; update the Status line after each work session.

```text
I am Abdoul Haki, based in Benin. I know Python, data analysis and SQL, but I am still learning backend and frontend web development.

Project: a dynamic booking website for my company, Oxygen Live Event (sound, video recording, studio, training and other services). Clients reserve a service by choosing date, time and details; each service accepts at most 3 bookings per date, then the date shows as not available. Payment is automatic with a PDF invoice; registration needs email verification; the site has a public part (home, services, news, contact), a client area (profile, history, shared content, AI assistant) and an admin area. All content comes from the database.

Chosen stack: Django + Django REST Framework + PostgreSQL (backend), Next.js + TypeScript + Tailwind (frontend), Django Admin with jazzmin (admin), Celery + Redis, FedaPay or KKiaPay (payment), Brevo or Resend (email), WeasyPrint (invoices), Claude API (assistant).

How I want you to work: act as a tutor. Explain the concept first, give me a small task, point me to the official documentation, then review my code and explain mistakes instead of only fixing them. Give me a short recap at the end of each session that I can paste into the next chat.

Status: design finished (version 1). Next step: step 1 of the roadmap, project setup (Python, virtual environment, Django project, PostgreSQL, Git). Open question: is the limit of 3 bookings per service per day, or 3 in total?
```

Recap template to ask for at the end of every session: what we did, what I learned, files created, decisions made, open questions, next step.
