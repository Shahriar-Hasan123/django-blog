# Django Blog Platform

A production-deployed Django blog application with public content pages, authenticated commenting, and an administrative dashboard for managing categories, posts, and users.

Live Demo: [https://shahriar19735.pythonanywhere.com/](https://shahriar19735.pythonanywhere.com/)

## Table of Contents

- [Project Overview](#project-overview)
- [Tech Stack](#tech-stack)
- [Core Features](#core-features)
- [Feature Implementation Status](#feature-implementation-status)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [Local Setup](#local-setup)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Permissions and Roles](#permissions-and-roles)
- [Deployment](#deployment)
- [Known Limitations](#known-limitations)
- [Future Improvements](#future-improvements)

## Project Overview

This project is a full-stack Django blogging system that supports:

- Public browsing of published posts
- Category-based filtering
- Full-text style search across title and content fields
- Auth system (register/login/logout)
- Dashboard-based CRUD for categories, posts, and users
- Image upload for blog posts
- Post comments for authenticated users

The application is split into focused Django apps (`blogs`, `dashboards`, `about_us`) to keep responsibilities clear and maintainable.

## Tech Stack

- Python 3
- Django 6
- SQLite (default development database)
- Bootstrap 4
- django-crispy-forms + crispy-bootstrap4
- Pillow (image handling)

Dependencies are listed in `requirements.txt`.

## Core Features

- Home page with featured and latest published posts
- Public blog detail page with comments
- Search page with persisted search term in the navbar input
- Category listing and category-specific post views
- Dashboard cards with aggregate counts
- Table views for posts, categories, and users
- CRUD operations for posts and categories
- User management from dashboard (add/edit/delete)
- Slug generation for posts in dashboard create/update flows
- Admin prepopulated slug support for blog posts
- Media upload support for featured images
- Social links and about section integration

## Feature Implementation Status

Below is the status of the features you targeted:

1. Multi-role system (Admin / Manager / Editor / Author): **Partially implemented**
   - Role primitives exist through Django Groups/Permissions fields in user forms.
   - User management UI supports assigning groups and explicit permissions.
   - Dedicated role-restricted view logic per role (manager/editor/author) is not fully enforced in all dashboard endpoints yet.

2. CRUD for posts and categories: **Implemented**
   - Full create, list, edit, delete flows are available in dashboard views.

3. Unique slug generation and prepopulation: **Implemented**
   - Dashboard post create/edit views generate slugs using `slugify(title) + id`.
   - Django admin uses `prepopulated_fields` for slug from title.

4. Media upload and configuration: **Implemented**
   - `ImageField` with date-based upload path.
   - `MEDIA_URL`/`MEDIA_ROOT` configured and served in development URL patterns.

5. Comment system (authenticated users only): **Implemented**
   - Comment form is shown only to authenticated users in template.

6. Manager and Editor dashboards with counts and tables: **Partially implemented**
   - Dashboard count cards and table views exist.
   - Separate manager/editor route segmentation and strict role-based endpoint restrictions are not fully separated yet.

7. Granular permission checks (Groups/Permissions + custom checks): **Partially implemented**
   - Template-level permission checks are present (for example, user listing visibility).
   - Most view functions currently use login checks but do not yet enforce object/action-level permission decorators.

8. Search with retained search term in textbox: **Implemented**
   - Search keyword is returned in context and persisted in the navbar input.

9. Deployment on PythonAnywhere: **Implemented**
   - App is publicly deployed at [https://shahriar19735.pythonanywhere.com/](https://shahriar19735.pythonanywhere.com/).

## Project Structure

```text
blog/
├── about_us/                 # About and social links content
├── blog_main/                # Project settings, root urls, auth/home views
├── blogs/                    # Blog, category, comment domain logic
├── dashboards/               # Dashboard CRUD and management views/forms
├── templates/                # Frontend templates (public + dashboard)
├── media/                    # Uploaded files
├── manage.py
└── requirements.txt
```

## Data Models

### blogs app

- `Category`
  - `category_name` (unique)
  - timestamps

- `Blog`
  - `title`, `slug` (unique)
  - `category` (FK)
  - `author` (FK to `User`)
  - `featured_image`
  - `short_description`, `blog_body`
  - `status` (`Draft` / `Published`)
  - `is_featured`
  - timestamps

- `Comment`
  - `user` (FK)
  - `blog` (FK)
  - `comment`
  - timestamps

### about_us app

- `About`
- `SocialLink`

## Local Setup

### 1) Clone the repository

```bash
git clone <your-repository-url>
cd blog
```

### 2) Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Apply migrations

```bash
python manage.py migrate
```

### 5) Create a superuser (optional, recommended)

```bash
python manage.py createsuperuser
```

### 6) Run development server

```bash
python manage.py runserver
```

Open: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

## Configuration

Current key settings include:

- Installed apps: `blogs`, `about_us`, `dashboards`, crispy form packages
- Static files:
  - `STATIC_URL = "static/"`
  - `STATIC_ROOT = BASE_DIR / "static"`
  - `STATICFILES_DIRS = ["blog_main/static"]`
- Media files:
  - `MEDIA_URL = "/media/"`
  - `MEDIA_ROOT = BASE_DIR / "media"`

For production use, move sensitive values (for example `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`) to environment variables.

## Usage Guide

### Public Side

- Visit home page to browse featured and recent posts.
- Use category navigation to filter posts.
- Use search from top navigation.
- Open a post detail page to read content and comments.

### Authenticated Side

- Register or log in.
- Open dashboard.
- Manage categories and posts.
- If authorized, manage users and assign groups/permissions.

## Permissions and Roles

The project uses Django's built-in auth model with:

- Group assignment support in dashboard user forms
- Direct user permission assignment support
- Template-level checks (example: `perms.auth.view_user`) for certain UI sections

Recommended production hardening:

- Add `@permission_required` or `@user_passes_test` decorators to create/update/delete views
- Enforce role-based route access for manager/editor/author-specific areas
- Add object-level checks where needed (for example, authors editing only their own posts)

## Deployment

Application is deployed on PythonAnywhere:

- URL: [https://shahriar19735.pythonanywhere.com/](https://shahriar19735.pythonanywhere.com/)

Typical PythonAnywhere steps:

1. Create virtual environment and install requirements.
2. Configure web app with correct WSGI path.
3. Set static and media mappings.
4. Run migrations.
5. Reload web app.

## Known Limitations

- Role-specific dashboard separation is not fully strict at the view layer.
- Most dashboard endpoints require login but not fine-grained permission decorators yet.
- No automated test coverage currently included for critical CRUD and permission flows.
- Development settings currently include values that should be externalized for production.

## Future Improvements

- Add comprehensive test suite (unit + integration) for auth, CRUD, and permissions.
- Implement strict role-based dashboards for Admin/Manager/Editor/Author.
- Add permission decorators across all sensitive dashboard endpoints.
- Improve auditing (created_by/updated_by logs) for management actions.
- Add pagination and richer filtering on dashboard tables.
- Add API layer (DRF) for future frontend/mobile integration.

---