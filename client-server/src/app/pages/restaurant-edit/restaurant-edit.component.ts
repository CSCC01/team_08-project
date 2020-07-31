import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup } from '@angular/forms';
import { DataService } from 'src/app/service/data.service';
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
    private data: DataService,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    this.userId = this.route.snapshot.queryParams.userId;
    this.role = this.route.snapshot.queryParams.role;
    if (!this.restaurantId || this.role !== 'RO' || !this.userId) {
      this.router.navigate([''], {
        queryParams: {
          role: this.role,
          userId: this.userId,
          restaurantId: this.restaurantId,
        },
      });
      alert('No matching restaurant found for this profile!');
    }
    this.data.changeRestaurantId(this.restaurantId);
    this.data.changeUserId(this.userId);
    this.data.changeRole(this.role);

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
      this.router.navigate(['/restaurant'], {
        queryParams: {
          role: this.role,
          userId: this.userId,
          restaurantId: this.restaurantId,
        },
      });
    }
  }

  cancel() {
    this.router.navigate(['/restaurant'], {
      queryParams: {
        role: this.role,
        userId: this.userId,
        restaurantId: this.restaurantId,
      },
    });
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
