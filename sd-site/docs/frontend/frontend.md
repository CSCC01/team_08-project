---
id: frontend
title: Frontend
---

Compliation of how to use **packages** that are used in Angular, and rules set for the project.

## Session Storage

To save current logged in user information in the browser. Closing the tab clears the storage.

We'll be keeping track of 3 pieces of information:

1. role
2. restaurantId (if applicable)
3. userId (email)

To set the values:

```typescript
sessionStorage.setItem('role', {{ the role}});
sessionStorage.setItem('restaurantId', {{ the restaurant id}});
sessionStorage.setItem('userId', {{ the user id / email}});
```

To get the values (can store into a variable):

```typescript
sessionStorage.getItem("role");
sessionStorage.getItem("restaurantId");
sessionStorage.getItem("userId");
```

We will be using this process to track a users role, their user id/email, and which restaurant they are associated with (if applicable).

### Query Parameters

To pass values through the URL as query. Have your variable passed as query parameters from wherever they clicked in from.

From the page they clicked in from (assuming the query params has been set to variables):

```html
<button (click)="function()"></button>
```

```typescript
function() {
  this.router.navigate(['/route_url'], {
    queryParams: { role: this.role, restaurantId: this.restaurantId },
  });
}
```

In the `.ts` file to recieve and set the variables:

```typescript
ngOnInit(): void {
  this.role = this.route.snapshot.queryParams.role;
  this.restaurantId = this.route.snapshot.queryParams.restaurantId;
}
```

`this.route.snapshot.queryParams.var` returns the query parameters set. You can now use those variables in your file.

## Style Guide

### Default Colours

Some of the default site colours are defined in the global `.scss` file.

To use the colours in your page/component, add this to the top of you `.scss` file

```css
@import "src/styles";
```

Then call on the colour using `$`:

```css
.navbar {
  background-color: $primary-color;
}
```

### Bottom Corner Image

Most pages will have an image at the bottom left corner to spice up the appearance of the page. Simply add the image to the page `.html` file and add the `bottom-left` class to it to format properly.

```html
<img class="bottom-left" src="assets/images/undraw_chef.png" />
```

The `bottom-left` class has been defined in `styles.scss`.
