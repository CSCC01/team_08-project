---
id: auth-guard
title: Auth Guards
---

Compliation of auth guards created and how to use them.

Guard services are under `src/app/auth`.

## How to use Guards

The guards in out case prevent some pages from being accessed if they do not have the correct permissions.

To generate a guard, head to `src/app/auth` folder and call `ng generate guard {{guard name}}`. Select `canActivate`.

In the `app-routing.module.ts`, import the guard.

```javascript
import { AuthGuard } from "./auth/auth.guard";
```

In the `Routes` constant, add the guard where applicable. Add the `canActivate` parameter and the guard in the list.

```javascript
const routes: Routes = [
  ...
  {
    path: 'profile',
    component: ProfileComponent,
    canActivate: [AuthGuard],
  },
  ...
];
```

If the condition of the guard is true, the page will be accessible to the user.

## Types

### Auth

File: `src/app/auth/auth.guard.ts`

The auth guard checks if the user is logged in to the site. Returns `true` if user is logged in.

### ROCheck

File: `src/app/auth/ro-check.guard.ts`

The RO Check guard checks if the user is a restuarant owner. Returns `true` if role of user is 'RO'.
