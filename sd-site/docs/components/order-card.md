---
id: order-card
title: Order Card
---

## Usage

Displaying incoming and in-progress restaurant orders from the restaurant perspective. Card automatically detects if it's a new order or in-progress order depending on it's time stamps present.

Files exist under `src\app\components\order-card`

## UI Appearance

Notice the differnce in buttons (New Order vs. In-Progress)

![Order Card New](../../static/img/examples/order-card-new.PNG "Order Card - New Order")
![Order Card Progress](../../static/img/examples/order-card-progress.PNG "Order Card - In-Progress")

## Tag Fields

**Identifier**: `app-order-card`

### Input

Specify the input:

| Parameter | Type  | Desc         | Required |
| --------- | ----- | ------------ | -------- |
| `order`   | `any` | Order Object | Yes      |

Currently, the dish object should contain:

```json
{
  "id": "{{ id from MongoDB }}",
  "user_name": "{{ person name }}",
  "email": "{{ person email }}",
  "phone": "{{ person phone number }}",
  "dishes": "{{ list of objects (each object contains a dish name & count) }}",
  "send_tstmp": "{{ the time stamp for when the order was sent to the restaurant }}",
  "accept_tstmp": "{{ the time stamp for when the order was accepted by the restaurant }}",
  "complete_tstmp": "{{ the time stamp for when the order was completed by the restaurant }}"
}
```

Example:

```json
{{
  "id": "1235",
  "user_name": "Jean Doe",
  "email": "sample1@email.com",
  "phone": "4163214567",
  "dishes": [
    {
      "dish_name": "Fancy Dish #1",
      "count": 1
    },
    {
      "dish_name": "Fancy Dish #2",
      "count": 2
    }
  ],
  "send_tstmp": "12:05:21",
  "accept_tstmp": "",
  "complete_tstmp": ""
}
```

Add this to the `.html` file. Replace the sections `{{ }}` with the input to be generated.

```html
<app-order-card [order]="{{ order object }}"></app-order-card>
```

### Output

There is no output. The card example above will be generated.
