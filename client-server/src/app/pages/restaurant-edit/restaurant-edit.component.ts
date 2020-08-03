import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { RestaurantsService } from '../../service/restaurants.service';

@Component({
  selector: 'app-restaurant-edit',
  templateUrl: './restaurant-edit.component.html',
  styleUrls: ['./restaurant-edit.component.scss'],
})
export class RestaurantEditComponent implements OnInit {
  restaurantId: string = '';
  restaurantDetails: any;
  userId: string = '';
  role: string = '';

  uploadForm: FormGroup;
  newImage: boolean = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private formBuilder: FormBuilder,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {
    this.role = sessionStorage.getItem('role');
    this.userId = sessionStorage.getItem('userId');
    this.restaurantId = sessionStorage.getItem('restaurantId');

    if (!this.restaurantId || this.role !== 'RO' || !this.userId) {
      this.router.navigate(['']);
      alert('No matching restaurant found for this profile!');
    }

    this.restaurantsService
      .getRestaurant(this.restaurantId)
      .subscribe((data) => {
        this.restaurantDetails = data;
      });

    this.uploadForm = this.formBuilder.group({
      file: [''],
    });
  }

  updateRestaurantInfo() {
    // Extract form inputs from the user
    var restaurantInfo = {
      restaurant_id: this.restaurantId,
      name: (<HTMLInputElement>document.getElementById('restaurant-name'))
        .value,
      address: (<HTMLInputElement>document.getElementById('restaurant-address'))
        .value,
      city: (<HTMLInputElement>document.getElementById('restaurant-city'))
        .value,
      phone: (<HTMLInputElement>document.getElementById('phone-number')).value,
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
    };

    if (
      restaurantInfo.name == '' ||
      restaurantInfo.address == '' ||
      restaurantInfo.city == '' ||
      restaurantInfo.phone == '' ||
      restaurantInfo.pricepoint == 'Choose...' ||
      restaurantInfo.cuisine == '' ||
      restaurantInfo.bio == ''
    ) {
      alert('Please enter all requried information about the restaurant!');
    } else {
      this.restaurantsService.editRestaurant(restaurantInfo);
      if (this.newImage) {
        this.onSubmit();
      }

      this.router.navigate(['/restaurant']);
    }
  }

  cancel() {
    this.router.navigate(['/restaurant']);
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
