# Redirink

> I want this to be a complete project, not just programming and designing but also **product** thinking and project management.
> It should be close to the real world requirements.
> More _simple backend and frontend_, less featureful but **finished** at the time.

Fast short link redirect service.

Web service to create **short redirect links**.

The idea and technology is similar to the **Bit.ly** service:

- authentication/authorization

- CRUD links

- short unique URLs (UIDs)

- redirect via HTTP 301 to longer links

- CORS

- identification

## Setup project

```sh
# To build react for serving by djangobuild container
docker compose -f local.yml up reactbuild

# Then
docker compose -f local.yml up djangobuild
```

## Roadmap

- Links

- Insights (redirects, clicks, visits, metrics, analytics)

- Setup React.js JS library (more convenient)

- Dashboard (interface template)

  - customize template (Volt React Dashboard)

- Periodic Celery email report

- Setup AWS (production)

## Checklist

- [x] Authentication interface (47 week)

- [x] Link CRUD interface

- [x] Insights API

- [x] Insights interface

- [x] Weekly insights report

- [x] Production deployment

- [x] Setup traefik reverse proxy

- [x] Connect backend and frontend (in dev)

- [x] Social authentication with token

- [ ] Write OpenAPI schema for custom view

- [x] Configure react build

- [ ] Autobuild and serve frontend from S3

- [ ] Telegram bot alternative UI

- [ ] Generate insight charts

- [ ] Document telegram bot usage (docs)

- [ ] Add frontend linting step to CI

- [ ] Redeploy in production

## Design

Product: short link/URL redirect service

Topics:

- generate short unique identification

- identify requesting users (visitor IP address or authenticated user)

- store unique insight

- render dashboard (queryset, filter, information in text/graphs/plots/...)

Database (API recourses):

- User

- Link

- Insight

API (server interface):

- authentication (login, logout, register, password, etc.)

  - `/api/auth/login/`

  - `/api/auth/{method}/`

- Link CRUD API (create, retrieve, update, delete):

  - OPTIONS/GET/POST/PUT/PATCH `/api/links/`

- insight (read, list, filter):

  - `/api/insights/`

- Redirecting (by server MVT or SPA)

  - `/<link_uid_regex>/`

- Analytics (count insights - Celery Task):

  - `/<link_uid_regex/`

Frontend:

- authentication

  - `/login`

  - `/logout`

  - `/signup`

- links

  - GET `/{link_uid_regex}` - redirect to the original URL

## Links

Links should be available only for users:

- authenticated is required for all operation (there will be a separate view for redirecting/viewing/following link

  - owner is required for detail endpoints (retrieve, update, delete)
  - list is filtered for the current user (not all links)

- authorization works only for DRF auth token authenticated users

- result will be paginated by 20 (just in case overload)

- can be ordered by creation time

Specific requirements to test:

- user can not create 2 links to the same URL.

## Frontend

Frontend will be created based on the Vote React Dashboard template. It provides styling/markup and some scripting.

Customized template:

- authentication

- CRUD components

- presentation/landing

- design/branding/assets

- debug frontend React.js code? how to debug application?

Authentication:

The user can sign in and up using SPA interface.

- the authentication state will be stored in the root components and then passed to children that need to get/set it.

- authenticated state will be determined every time the page is reloaded (component state is not persistent)

- authentication token will be checked synchronously before rendering the root component (app).

- authenticated state will be determined by token stored in the local storage.

- sign in/up requests will be in the different file/class/methods

- sign in/up can fail or be successful:

  1. User will be redirected to the dashboard page (react router DOM). State and form will be cleared (DOM removed)

  2. Form will be filled with errors or error notification will be displayed

- When user is not authenticated it can not access certain routes and will be redirected to the sign in/up pages (authorization)

  - conditional URL routing and page rendering

Frontend authorization:

1. Auth state is not determined => show loading page

2. Not authenticated => Only sign-in/sign-up/password routes (redirect to sign-in by default)

3. All other routes except sign-in/sign-up/password

## Insights

The number of times the short link is requested saved in the database with the corresponding IP address of the requester (which helps determine number of unique insights).

Insights counting is moved to the separate Celery task, which parses request for IP address and then saves to the database.

Insights will have read-only API for owners of the link + convenient filtering of all insights.

The main purpose of insights functionality is to display dashboard/analytics/statistics:

- due to security reasons lookup will not be available (not IP address or id will be shown)

What user wants to know?

- display how much insights total? (statistics) - count

- time of the insights per day/week/month? (when)

- how much unique insights and when? (particular people)

Backend:

- IP address is converted into visitor instance with it's primary id (id is incrementing relative to the link?).

- return anonymized insights data sorted by recent and paginated by 10.

- filter by visitor and time.

Serialized data format:

```json
{
    "count": "20",
    "next": "...",
    "previous": "...",
    "results": [
        {
            "visitor": "1274e5f8-f843-469f-9615-a53a06109d58",
            "time": "2021-12-6T20:43:10+00:00"
        },
        {
            "visitor": "1274e5f8-f843-469f-9615-a53a06109d58",
            "time": "2021-12-6T20:54:30+00:00"
        },
        {
            "visitor": "0bd08c14-b0aa-4223-9157-8c9672349819",
            "time": "2021-13-6T23:54:30+00:00"
        },
        ...
    ]
}
```

API interaction design:

- `/api/insights/` - all user link's insights

- `/api/insights/?link=...` - insights for specific link

- `/api/insights/?time=2021-12-09` - get insights for today (filter by any date and time). It should work in decreasing order (by year, by year and month, by year, month and day, and so on to: filtering by year, month, day, hour, minute, second).

  - 2021, 2021-12, 2021-12-09, 2021-12-6T20, 2021-12-6T20:54, 2021-12-6T20:54:30

## Report

Weekly report contains information about the insight activity on all links.

- send via email at 00:00 every Monday (in format of "on 51-th week" or "from ")

- number of total insights previous week

- HTML email body + some CSS styling

- simple bar plot for insights over the week

- insight chart image (static media file png) or dynamic chart creation API endpoint (`/chars/...`)

## Dockerize React app

React app consist of 2 packages:

1. API client library
2. Dashboard interface

## Traefik

To add service and connect to it following steps:

1. Process inside service should be running on port 1234
2. Container should expose port 1234
3. Traefik should connect container to entrypoint 1234
4. Traeifk container should forward port 1234
5. VS Code Server should forward port 1234 (over SSH)
6. VS Code client should forward port 1234 for localhost over HTTP
7. Firefox should be connected to http://localhost:1234 with Host: localhost

## Telegram bot

Redirink telegram bot will provide functionality to:

- welcome and help information (about commands)
- auto-authenticate using Telegram username
- create, list, update and delete links
- view insights

Additionally:

- render insights charts (send images)

Features:

- to interact with Telegram bot api 3rd-party library will be used (instead of hand-crafted)
- bot will process all Telegram requests (queried updated) synchronously (neither asynchronously which will require asynchronous API client nor using task queue)
