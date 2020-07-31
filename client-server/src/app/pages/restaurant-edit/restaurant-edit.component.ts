import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
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

  constructor(
    private route: ActivatedRoute,
    private router: Router,
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
      this.router.navigate(['/restaurant']);
    }
  }

  cancel() {
    this.router.navigate(['/restaurant']);
  }
}
