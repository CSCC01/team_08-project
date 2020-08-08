import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { LoginService } from '../../service/login.service';
import { AuthService } from '../../auth/auth.service';
import { RestaurantsService } from '../../service/restaurants.service';
import { Router, ActivatedRoute } from '@angular/router';
import { formValidation } from '../../validation/forms';
import { restaurantValidator } from '../../validation/restaurantValidator';
import { formValidator } from '../../validation/formValidator';

@Component({
  selector: 'app-restaurant-setup',
  templateUrl: './restaurant-setup.component.html',
  styleUrls: ['./restaurant-setup.component.scss'],
})
export class RestaurantSetupComponent implements OnInit {
  userId: string = '';
  restaurantId: string = '';

  uploadForm: FormGroup;
  newImage: boolean = false;
  validator: formValidator = new restaurantValidator();

  constructor(
    public auth: AuthService,
    private loginService: LoginService,
    private restaurantsService: RestaurantsService,
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder
  ) {}

  ngOnInit(): void {
    this.userId = sessionStorage.getItem('userId');
    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
  }

  upgradeUser(): void {
    // Extract form inputs from the user
    var restaurantInfo = {
      name: (<HTMLInputElement>document.getElementById('restaurant-name'))
        .value,
      address: (<HTMLInputElement>document.getElementById('restaurant-address'))
        .value,
      city: (<HTMLInputElement>document.getElementById('restaurant-city'))
        .value,
      phone: (<HTMLInputElement>document.getElementById('phone-number')).value,
      email: (<HTMLInputElement>document.getElementById('restaurant-email'))
        .value,
      pricepoint: (<HTMLInputElement>document.getElementById('pricepoint'))
        .value,
      cuisine: (<HTMLInputElement>document.getElementById('restaurant-cuisine'))
        .value,
      bio: (<HTMLInputElement>document.getElementById('restaurant-bio')).value,
      twitter: (<HTMLInputElement>document.getElementById('twitter')).value,
      instagram: (<HTMLInputElement>document.getElementById('instagram')).value,
      external_delivery_link: (<HTMLInputElement>(
        document.getElementById('external-delivery')
      )).value,
      rating: '0.00',
      GEO_location: 'blank',
    };

    this.validator.clearAllErrors();

    let failFlag = this.validator.validateAll(restaurantInfo, (key) => this.validator.setError(key));

    //if any of the validations failed, do not POST
    if (!failFlag){
      // Attach a restaurant ID to the current user and upgrade them
      this.restaurantsService.getRestaurantID(restaurantInfo).subscribe(
        (data) => {
          if(data && formValidation.isInvalidResponse(data)){
            console.log(data);
            formValidation.HandleInvalid(data, (key) => this.validator.setError(key))
          }else{
            this.restaurantId = data._id;
            if (this.newImage) {
                this.onSubmit();
            }

            sessionStorage.setItem('restaurantId', data._id);
            this.router.navigate(['/owner-setup']);

            this.auth.userProfile$.source.subscribe((userInfo) => {
                userInfo.role = 'RO';
                userInfo.restaurant_id = data._id;
                sessionStorage.setItem('role', 'RO');
                this.loginService.addNewUser(userInfo);
            });
          }
        },
        (error) => {
          alert('Sorry a restaurant with this email has already been found');
          this.router.navigate(['']);
        }
      );
    }
  }

  onFileSelect(event) {
    if (event.target.files.length > 0) {
      this.newImage = true;
      const file = event.target.files[0];
      this.uploadForm.get('file').setValue(file);
    }
  }

  onSubmit() {
    const formData = new FormData();
    formData.append('file', this.uploadForm.get('file').value);
    this.restaurantsService
      .uploadRestaurantMedia(formData, this.restaurantId, 'logo')
      .subscribe((data) => {});
    this.newImage = false;
  }
}
