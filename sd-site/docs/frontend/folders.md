---
id: folders
title: Frontend Structure
---

List of folders and functionalities in the Angular folder.

## Folder Structure

```
📦client-server
 ┣ 📂src
 ┃ ┣ 📂app
 ┃ ┃ ┣ 📂auth
 ┃ ┃ ┃ ┣ 📜auth.guard.ts
 ┃ ┃ ┃ ┣ 📜auth.service.ts
 ┃ ┃ ┃ ┗ 📜ro-check.guard.ts
 ┃ ┃ ┣ 📂components
 ┃ ┃ ┃ ┣ 📂all-order-card
 ┃ ┃ ┃ ┣ 📂carousel
 ┃ ┃ ┃ ┣ 📂cart-card
 ┃ ┃ ┃ ┣ 📂dish-card
 ┃ ┃ ┃ ┣ 📂dynamic-label
 ┃ ┃ ┃ ┣ 📂filterlist-card
 ┃ ┃ ┃ ┣ 📂footer
 ┃ ┃ ┃ ┣ 📂map
 ┃ ┃ ┃ ┣ 📂navbar
 ┃ ┃ ┃ ┣ 📂order-card
 ┃ ┃ ┃ ┣ 📂owner-card
 ┃ ┃ ┃ ┣ 📂page-error
 ┃ ┃ ┃ ┣ 📂restaurant-card
 ┃ ┃ ┃ ┣ 📂review-card
 ┃ ┃ ┃ ┣ 📂timeline-post
 ┃ ┃ ┃ ┗ 📂view-review-card
 ┃ ┃ ┣ 📂pages
 ┃ ┃ ┃ ┣ 📂all-orders
 ┃ ┃ ┃ ┣ 📂all-owners
 ┃ ┃ ┃ ┣ 📂all-restaurants
 ┃ ┃ ┃ ┣ 📂all-transactions
 ┃ ┃ ┃ ┣ 📂checkout
 ┃ ┃ ┃ ┣ 📂favourites
 ┃ ┃ ┃ ┣ 📂home
 ┃ ┃ ┃ ┣ 📂menu-edit
 ┃ ┃ ┃ ┣ 📂menu-setup
 ┃ ┃ ┃ ┣ 📂owner-edit
 ┃ ┃ ┃ ┣ 📂owner-setup
 ┃ ┃ ┃ ┣ 📂payment
 ┃ ┃ ┃ ┣ 📂profile
 ┃ ┃ ┃ ┣ 📂restaurant-edit
 ┃ ┃ ┃ ┣ 📂restaurant-page
 ┃ ┃ ┃ ┣ 📂restaurant-setup
 ┃ ┃ ┃ ┣ 📂restuarant-dashboard
 ┃ ┃ ┃ ┗ 📂timeline
 ┃ ┃ ┣ 📂service
 ┃ ┃ ┃ ┣ 📜login.service.ts
 ┃ ┃ ┃ ┣ 📜orders.service.ts
 ┃ ┃ ┃ ┣ 📜restaurants.service.ts
 ┃ ┃ ┃ ┣ 📜reviews.service.ts
 ┃ ┃ ┃ ┗ 📜timeline.service.ts
 ┃ ┃ ┣ 📂utils
 ┃ ┃ ┃ ┣ 📜general.ts
 ┃ ┃ ┃ ┣ 📜geolocation.ts
 ┃ ┃ ┃ ┗ 📜orders.ts
 ┃ ┃ ┣ 📂validation
 ┃ ┃ ┃ ┣ 📜dishValidator.ts
 ┃ ┃ ┃ ┣ 📜forms.ts
 ┃ ┃ ┃ ┣ 📜formValidator.ts
 ┃ ┃ ┃ ┣ 📜ownerValidator.ts
 ┃ ┃ ┃ ┣ 📜restaurantValidator.ts
 ┃ ┃ ┃ ┗ 📜userValidator.ts
 ┃ ┃ ┣ 📜app-routing.module.ts
 ┃ ┃ ┣ 📜app.component.html
 ┃ ┃ ┣ 📜app.component.scss
 ┃ ┃ ┣ 📜app.component.spec.ts
 ┃ ┃ ┣ 📜app.component.ts
 ┃ ┃ ┗ 📜app.module.ts
 ┃ ┣ 📂assets
 ┃ ┃ ┣ 📂images
 ┃ ┃ ┃ ┣ 📂cuisines
 ┃ ┃ ┃ ┣ 📂food
 ┃ ┃ ┃ ┣ 📜...
 ┃ ┃ ┗ 📜.gitkeep
 ┃ ┣ 📂environments
 ┃ ┃ ┣ 📜environment.prod.ts
 ┃ ┃ ┗ 📜environment.ts
 ┃ ┣ 📜favicon.ico
 ┃ ┣ 📜index.html
 ┃ ┣ 📜main.ts
 ┃ ┣ 📜polyfills.ts
 ┃ ┣ 📜styles.scss
 ┃ ┗ 📜test.ts
 ┣ 📂ssl
 ┃ ┣ 📜server.crt
 ┃ ┗ 📜server.key
 ┣ 📜.gitignore
 ┣ 📜angular.json
 ┣ 📜package.json
 ┗ 📜README.md
```

## Breakdown

Components and pages folders each contain a `.html`, `.css`, `.ts` file, which function like your regular `.html`, `.css`, and `.js` files.

### Favicon

The site URL image can be changed by changing the `favicon.ico` in `/src`.

### Enviroments

Enviroment variables are set in the folder `/src/environments`. In a sense, these are like constant, global variables which do not change unless someone goes in and manually changes them.

There is a dev and prod file for whichever situation. Contains URLs to the backend for endpoints and access tokens to the used third party services (which makes it easier to change since it is located in one place).

### SSL

`\ssl` contains a certificate for secure browsing of the website. When there is a legit, paid version, this can be easily updated to reflect that.

## Components

Check out the components tab for specifics on how to use each component. They can be called into another component/page to be used.

## Pages

All pages of the application.

### All Orders

For RO usage. Ability to see all current and past orders made for the restuarant from the dashboard.

### All Owners

For customer usage. Ability to see list of all owners of restuarants in the database and click to view their restaurant pages.

### All Restaurants

For customer usage. Ability to see list of all restaurants, sorted my proximity to the current user. Ability to see a map with pinned current locations and locations of restaurants. Ability to search and filter all restaurants and all dishes.

### All Transactions

For customer usage. Ability to see all previous purchases and their status indicator.

### Checkout

For customer usage. Ability to view items in cart, change the amounts, delete items, clear cart, and send cart to make a purchase.

### Favourites

For customer usage. Ability to view list of favourited restaurants and dishes.

### Home

For all users. Home page.

### Menu Edit

For RO usage. Ability to add and edit menu items to restaurant.

### Menu Setup

For RO usage. Ability to add dishes to menu on initial set up of a restaurant.

### Owner Edit

For RO usage. Ability to edit information and picture of the owner.

### Owner Setup

For RO usage. Ability to add information and picture of the owner on initial set up of a restaurant.

### Payment

For customer usage. Ability to fill in payment information to pay for orders.

### Profile

For customer usage. Ability to view and edit personal account information.

### Restaurant Page

For any user. Ability to view a restaurants details.

Customers can use the menu to place orders and write reviews for the restaurant.

ROs can use the page to access edits for restaurant information, header, owner, and menu.

### Restaurant Edit

For RO usage. Ability to edit information and logo of the restaurant.

### Restaurant Setup

For RO usage. Ability to add information and logo of the restaurant on initial set up of a restaurant.

### Restaurant Dashboard

For RO usage. Ability to see all incoming orders, orders in progress, and completed orders. Status of the cards can be manipulated on completion of each step

### Timeline

For any user. Ability to see all conversations from restaurant updates.

Customers can comment on any post.

ROs can add a post, delete a post, and delete comments.

## Services

#### Login Service

Endpoints relating to user information.

#### Orders Service

Endpoints relating to the ordering system and RO dashboard capabilities.

#### Restaurant Service

Endpoints relating to restaurants and dishes.

#### Reviews Service

Endpoints relating to reviews of restaurants.

#### Timeline Service

Endpoints relating to timeline posts and comments.
