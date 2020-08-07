export class formError {

    static RESPONSE_INVALID: string = "Invalid"

    static userErrorConst = {
        'name': 'Invalid Name',
        'address': 'Invalid Address',
        'phone': 'Invalid phone number - ensure exactly 10 digits',
        'birthday': 'Invalid Birthday, ensure YYYY-MM-DD format'
    }

    static restaurantErrorConst = {

    }
    
    static clearErrors(errors: Object){
        Object.keys(errors).forEach(
            key => errors[key] = ''
        );
    }

    static isBirthdayValid(birthday: string){
        return birthday != null && birthday.match('^\\d{4}-\\d{2}-\\d{2}$');
    }

    static isPhoneValid(phone: string){
        return phone != null && phone.length == 10;
    }

    static isInvalidResponse(data: JSON){
        return data.hasOwnProperty(this.RESPONSE_INVALID);
    }

    static HandleInvalid(data: JSON, errorFunc: Function){
        data[this.RESPONSE_INVALID].array.forEach(element => {
            errorFunc(element);
        });
    }

}
