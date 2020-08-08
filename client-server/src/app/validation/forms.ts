export class formValidation {

    static RESPONSE_INVALID: string = "Invalid"
    static MS_PER_DAY = 1000 * 60 * 60 * 24;
    static DAYS_PER_YEAR = 365.2422;
    static YOUNGEST_VALID_AGE = 18;

    static VALID_PRICE_POINTS: Set<string> = new Set<string>(['Low', 'Medium', 'High']) 

    static EMAIL_VALIDATION_REGEX = /^(([^<>()\[\]\.,;:\s@\"]+(\.[^<>()\[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
    static YYYYMMDD_REGEX = '^\\d{4}-\\d{2}-\\d{2}$'

    static isBirthdayValid(birthday: string){
        return birthday != null && birthday.match(formValidation.YYYYMMDD_REGEX);
    }
    // gives the difference calculated as abs(Date1-Date2) in years
    static ageDifference(Date1: string, Date2: string) {
        console.log("date1" + Date1.toString());
        console.log("date2" + Date2.toString());
        let First = new Date(Date1.toString().replace('-', '/'));
        let Second = new Date(Date2.toString().replace('-', '/'));
        let diffMs = First.getTime() - Second.getTime();
        return diffMs/(formValidation.MS_PER_DAY*formValidation.DAYS_PER_YEAR);
    }
    // current date in YYYY-MM-DD format
    static currentDate() {
        let today = new Date();
        let currentDate = (today.getFullYear()).toString().padStart(4,'0') + "-" + 
        (today.getMonth() + 1).toString().padStart(2,'0') + "-" + 
        today.getDate().toString().padStart(2,'0');
        console.log(currentDate);
        return currentDate;
    }

    static isOlderThanAge(birthday: string, age: number) {
        // debugging print
        let currentAge = formValidation.ageDifference(formValidation.currentDate(), birthday);
        console.log(currentAge)
        return currentAge > age;
    }

    static isPricepointValid(pricepoint: string){
        return formValidation.VALID_PRICE_POINTS.has(pricepoint);
    }

    static isEmailValid(email: string){
        // credit: found at https://stackoverflow.com/questions/46155/how-to-validate-an-email-address-in-javascript
        return email != null && email != '' && formValidation.EMAIL_VALIDATION_REGEX.test(email.toLowerCase());
    }

    static isPhoneValid(phone: string){
        return phone != null && phone.length == 10;
    }

    static isInvalidResponse(data: JSON){
        return data.hasOwnProperty(formValidation.RESPONSE_INVALID);
    }

    static HandleInvalid(data: JSON, errorFunc: Function){
        data[formValidation.RESPONSE_INVALID].forEach(element => {
            errorFunc(element);
        });
    }

    static isNumberValid(num: string){
        return formValidation.nonEmpty(num) && !isNaN(Number(num));
    }

    static nonEmpty(s: string){
        return s != '';
    }
    static isDefined(obj: any){
        return obj != undefined;
    }
}
