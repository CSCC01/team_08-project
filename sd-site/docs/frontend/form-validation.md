---
id: form-validation
title: Form Validation
---

Compilation of form validators created and how to use them.

Validation services are under `src/app/validation`.

## How to use Form Validation

The validators in prevent some fomrs from being submitted if they do not have the correct data format or are missing required fields.

To create a validator concretion, head to `src/app/validation` folder and create a new Typescript class which extends the formValidator class.

initialize the errors Object with the field names that you wish to validate, errorStrings with the error messages, and validationFuncs with the functions that will validate these fields.

#### An example using the userValidator concretion
```Typescript
import { formValidator } from "./formValidator"
import { formValidation } from "./forms"
export class userValidator extends formValidator{

    constructor() {
        super();
        //all errors start off empty, stores the state of the error messages
        this.errors = {
            'name': '',
            'address': '',
            'phone': '',
            'birthday': '',
            'age': ''
        }
    }

    errors = {}
    // object with strings used for error messages
    errorStrings = {
        'name': 'Invalid Name',
        'address': 'Invalid Address, if this address exists in multiple cities, specify the city',
        'phone': 'Invalid phone number - ensure exactly 10 digits',
        'birthday': 'Invalid Birthday, ensure YYYY-MM-DD format',
        'age': 'Must be older than 18 years of age'
    }
    // object with functions that will be used for validation
    validationFuncs = formValidator.replaceDefaults({
        'name': '',
        'address': '',
        'phone': (phone) => formValidation.isPhoneValid(phone),
        'birthday': (birthday) => formValidation.isBirthdayValid(birthday),
        'age' : (birthday) =>  formValidation.isOlderThanAge(birthday, 18) || !formValidation.isBirthdayValid(birthday)
    })
}
```

In the typescript file for the form, import the validator you made, as well as formValidator, and formValidation from forms.


```javascript
import { formValidator } from "src/app/validation/formValidator";
import { formValidation } from "src/app/validation/forms";
import { userValidator } from "src/app/validation/formValidator";
```

In the class add an instance of the formValidator abstraction and initialize it using the concretion.

```Typescript
validator: formValidator = new userValidator(); 
```

to validate a form and store the errors in validator.errors, call validateAll(), in the callback add a function which will be called each time a validation fails with the formfield's name as a parameter, and it will return a boolean indicating whether or not there was a validation failure 

```javascript
const routes: Routes = [
  ...
    failFlag = validator.validateAll(formFieldData, (key) => failureCallbackFunction(key));
  ...
];
```

If the condition of the validateALL returns true, a validation error occurred, this can be used when submitting forms to determine whether the form should be POSTed or not.

## Types

### formValidator

File: `src/app/validation/formValidator.ts`

The formValidator provides an abstraction for validation of forms.

### formValidation

File: `src/app/auth/formValidation.ts`

The formValidation contains a function to check if the response fomr the endpoint indicated any invalid fields, a function to use this response to raise error messages, and many helper functions for validation.

This is a static helper class
