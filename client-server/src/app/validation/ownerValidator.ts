import { formValidator } from "./formValidator"

export class ownerValidator extends formValidator{
    
    constructor(){
        super();
        this.errors = {
            'owner_name': '',
            'owner_story': ''
        }
    }

    errors = {}

    errorStrings = {
        'owner_name': 'Invalid Owner Name',
        'owner_story': 'Invalid Owner Story'
    }

    validationFuncs = formValidator.replaceDefaults({
        'owner_name': '',
        'owner_story': '',
    })

}