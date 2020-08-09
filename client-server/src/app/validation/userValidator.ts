import { formValidator } from "./formValidator"
import { formValidation } from "./forms"
export class userValidator extends formValidator{

    constructor() {
        super();
        //all errors start off empty
        this.errors = {
            'name': '',
            'address': '',
            'phone': '',
            'birthday': '',
            'age': ''
        }
    }

    errors = {}

    errorStrings = {
        'name': 'Invalid Name',
        'address': 'Invalid Address',
        'phone': 'Invalid phone number - ensure exactly 10 digits',
        'birthday': 'Invalid Birthday, ensure YYYY-MM-DD format',
        'age': 'Must be older than 18 years of age'
    }
    // age checks if the date is invalid, then don't throw an error, because birthday will throw an error
    validationFuncs = formValidator.replaceDefaults({
        'name': '',
        'address': '',
        'phone': (phone) => formValidation.isPhoneValid(phone),
        'birthday': (birthday) => formValidation.isBirthdayValid(birthday),
        'age' : (birthday) =>  formValidation.isOlderThanAge(birthday, 18) || !formValidation.isBirthdayValid(birthday)
    })
}