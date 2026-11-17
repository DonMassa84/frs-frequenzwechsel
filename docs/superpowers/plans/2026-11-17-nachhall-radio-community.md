# Nachhall Radio Community Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a Colorado-style community contact flow to Nachhall: live-chat handoff, guest-DJ submission, and official FRS support CTA.

**Architecture:** Keep the existing buildless HTML/CSS/JS site. Add accessible sections and client-side mailto handoffs; do not add a backend, third-party chat script, or payment processing.

**Tech Stack:** HTML, CSS, vanilla JavaScript, GitHub Pages.

**Spec:** `docs/superpowers/specs/2026-11-17-nachhall-live-chat-gast-dj-design.md`

## Global Constraints

- No automatic message or application submission.
- No local or server-side storage of personal form data.
- Use the official FRS Förderverein URL for donations.
- State clearly that the live-chat panel is a handoff/demo until a real chat backend exists.

## Review Focus

- Empty chat input must not create an email.
- Special characters in form values must be safely URL-encoded.
- The donation CTA must point to `https://www.freies-radio.de/foerderverein`.
- Mobile navigation and two-column sections must remain readable.
- Form labels and status updates must remain accessible.

### Task 1: Add community sections and navigation

**Files:** Modify `website/index.html`.

- Add navigation links for `#community`, `#gast-djs`, and `#support`.
- Add live-chat/handoff, guest-DJ form, and support sections before the status section.
- Keep all contact actions explicit and visible.

### Task 2: Style the new sections

**Files:** Modify `website/style.css`.

- Add responsive card, chat, form, status, and support styles using existing color tokens.
- Preserve the existing visual language and mobile breakpoints.

### Task 3: Wire interactions

**Files:** Modify `website/app.js`.

- Add local chat-demo messages and an explicit `mailto:` handoff.
- Build a URL-encoded guest-DJ application email without sending it automatically.
- Keep the recipient and support URL in named constants.

### Task 4: Verify and publish

- Run syntax/HTML checks and `git diff --check`.
- Preview the site locally and verify the new sections and links with browser UI.
- Commit and push the reviewed changes to the existing GitHub Pages branch.
