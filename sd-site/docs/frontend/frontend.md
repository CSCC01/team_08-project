---
id: frontend
title: Frontend
---

Compliation of how to use **packages** that are used in Angular, and rules set for the project.

## Keeping Data on Local

To resolve (most) problems with the local saved version of the role and ids being wiped on refresh.

### DataService

`src/app/service/data.service.ts` acts as a file for global variables, which can be accessed by:

1. Adding `private data: DataService` to the constructor of it `.ts` file

```typescript
constructor(private data: DataService) {}
```

2. Calling and subscribing to get the value of the variables (in this case, it's `varName`)

```typescript
ngOnInit(): void {
  this.data.varName.subscribe((data) => (this.localVarName = data));
}
```

3. Use that variable you set it at to access it within the `.html` and `.ts` file

### Query Parameters

In order for `DataService` to first get its variables set, we'll be using query parameters right when the user logs in and pass it to every page they go to. Navigation bar has been configured to pass `role` and `restaurantId` at the moment to the pages that are clicked on from the navigation.

## New Pages

To adher to passing query parameters as a mock local storage, new pages should:

1. Have `role` and `restaurantId` passed as query parameters from wherever they clicked in from

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

  this.data.changeRestaurantId(this.restaurantId);
  this.data.changeRole(this.role);
}
```

`this.route.snapshot.queryParams.var` returns the query parameters set.

`this.data.changeFunc(this.var);` sets the value to `DataService`, which is used to access roles and permissions on all pages.

The combination of both is needed to:

1. Allow refreshing the page to not reset our knowledge of what role the user is
2. Allow for guards to do their permissions since they have a variable to access

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
