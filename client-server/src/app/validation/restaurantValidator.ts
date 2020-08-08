import { formValidator } from "./formValidator"
import { formValidation } from "./forms"

export class restaurantValidator extends formValidator{

    constructor(){
        super();
        this.errors = {
            'name': '',
            'address': '',
            'city': '',
            'phone': '',
            'email': '',
            'pricepoint':'',
            'cuisine':'',
            'bio': '',
            'twitter': '',
            'instagram': '',
            'external_delivery_link': ''
        }
    }

    errors = {}

    linkerror: string = "link does not exist"

    errorStrings = {
        'name': 'Invalid Name',
        'address': 'Invalid Address',
        'city': 'Invalid City',
        'phone': 'Invalid Phone Number, ensure it contains exactly 10 digits',
        'email': 'Invalid Email, ensure it follows the name@domain.name format',
        'pricepoint':'Invalid Price Point, ensure it is one of Low, Medium, or High',
        'cuisine':'Invalid Cuisine',
        'bio': 'Invalid Restaurant Biography',
        'twitter': 'This twitter ' + this.linkerror,
        'instagram': 'This instagram ' + this.linkerror,
        'external_delivery_link': 'This ' + this.linkerror
    }

    validationFuncs = formValidator.replaceDefaults({
        'name': '',
        'address': '',
        'city': '',
        'phone': (phone) => formValidation.isPhoneValid(phone),
        'email': (email) => formValidation.isEmailValid(email),
        'pricepoint':(pricepoint) => formValidation.isPricepointValid(pricepoint) ,
        'cuisine': '',
        'bio': ''
    })

}