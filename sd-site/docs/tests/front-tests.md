---
id: front-tests
title: Frontend Tests
---

## Testing Table Legend

| Column        | Column Description                                |
| :------------ | :------------------------------------------------ |
| Test Name     | Name of Test                                      |
| UI Components | Page/interface where the changes affect           |
| Steps         | Reproduction steps                                |
| Cases         | List of cases for the test                        |
| Problems      | Problems that future implementation may affect it |

## Master Testing Table

| Test Name      | UI Components                                     | Steps                                                                                                                                                                                                                                                                                                                                                                                                     | Cases                                                                                                                                                             | Problems                                                       |
| :------------- | :------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------- |
| RO Menu Edit   | Restaurant Page, Menu edit page                   | Signup/login as RO (make sure they have a restaurant id), go to restaurant page, edit menu (dishes should be here, should be able to add, edit, and delete), save (restaurant menu should be updated)                                                                                                                                                                                                     | Menu edit page access, add to menu, delete from menu, edit menu, save menu                                                                                        | Refreshing on Menu Edit page resets the role and restaurant id |
| RO Form Guards | Owner Setup Page, Menu Setup Page, Menu Edit Page | Do not login and attempt to access Owner Setup Page, Menu Setup Page and Menu Edit page and repeat while logged in as BU (all should be denied access). Now upgrade/login as a RO and attempt to access Owner Setup Page, Menu Setup Page and Menu Edit page (Make sure to have the needed query params - restaurant ID and role) then access should be granted and the forms can be filled out as normal | Owner setup page access, menu setup page access, menu edit page access, fill out owner story, add dishes using menu setup, add/edit/delete dishes using menu edit | Add and delete dishes are not dynamically displayed on FireFox |
