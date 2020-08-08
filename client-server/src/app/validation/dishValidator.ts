import { formValidator } from "./formValidator"
import { formValidation } from "./forms"
export class dishValidator extends formValidator{
    
    constructor(){
        super();
        this.errors = {
            'name': '',
            'description': '',
            'price': '',
            'cuisine': '',
            'dishInfo': '',
            'allergy': '',
            'menuCategory': ''
        }
    }

    errors = {}

    errorStrings = {
        'name': 'Invalid Name',
        'description': 'Invalid Description',
        'price':"Invalid Price, make sure it is a positve number",
        'cuisine': 'Invalid Cuisine',
        'dishInfo': 'Invalid Dish',
        'allergy': 'Invalid Allergy',
        'menuCategory': 'Invalid Menu Category'
    }

    validationFuncs = formValidator.replaceDefaults({
        'name': '',
        'description': '',
        'price': (price) => formValidation.isNumberValid(price) && Number(price) > 0,
        'cuisine': '',
        'dishInfo': '',
        'allergy': '',
        'menuCategory': ''
    });

}