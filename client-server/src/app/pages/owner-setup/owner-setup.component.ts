import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { RestaurantsService } from '../../service/restaurants.service';
import { formValidation } from "../../validation/forms";
import { ownerValidator } from '../../validation/ownerValidator';
import { formValidator } from '../../validation/formValidator';

@Component({
  selector: 'app-owner-setup',
  templateUrl: './owner-setup.component.html',
  styleUrls: ['./owner-setup.component.scss'],
})
export class OwnerSetupComponent implements OnInit {
  restaurantId: string = '';
  userId: string = '';
  role: string = '';

  uploadForm: FormGroup;
  validator: formValidator = new ownerValidator();
  newImage: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {
    this.restaurantId = sessionStorage.getItem('restaurantId');
    this.userId = sessionStorage.getItem('userId');
    this.role = sessionStorage.getItem('role');

    if (!this.restaurantId || !this.userId) {
      this.router.navigate(['']);
      alert('No matching restaurant found for this profile!');
    }

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
  }

  updateOwner() {
    var restaurantInfo = {
      restaurant_id: this.restaurantId,
      owner_name: (<HTMLInputElement>document.getElementById('owner-name'))
        .value,
      owner_story: (<HTMLInputElement>document.getElementById('owner-story'))
        .value,
    };

    this.validator.clearAllErrors();
    let failFlag = this.validator.validateAll(restaurantInfo, (key) => this.validator.setError(key));

    if (!failFlag){
      this.restaurantsService.editRestaurant(restaurantInfo).subscribe((data) => {
        if(data && formValidation.isInvalidResponse(data)){
            console.log(data);
            formValidation.HandleInvalid(data, (key) => this.validator.setError(key))
          }else{
            if (this.newImage) {
                this.onSubmit();
              }
        
              this.router.navigate(['/menu-setup']);
          }
      });

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
      .uploadRestaurantMedia(formData, this.restaurantId, 'owner')
      .subscribe((data) => {});
    this.newImage = false;
  }
}
