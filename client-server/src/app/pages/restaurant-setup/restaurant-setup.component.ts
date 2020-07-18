import { Component, OnInit } from '@angular/core';
import { LoginService } from '../../service/login.service';
import { AuthService } from '../../auth/auth.service';
import { RestaurantsService } from '../../service/restaurants.service';

@Component({
  selector: 'app-restaurant-setup',
  templateUrl: './restaurant-setup.component.html',
  styleUrls: ['./restaurant-setup.component.scss'],
})
export class RestaurantSetupComponent implements OnInit {
  restaurantId: any;
  constructor(
    public auth: AuthService,
    private loginService: LoginService,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {}

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
      GEO_location: 'blank',
      external_delivery_link: 'blank',
      cover_photo_url: 'blank',
      logo_url: 'blank',
      rating: '0.00',
    };

    // Attach a restaurant ID to the current user and upgrade them
    this.restaurantsService
      .getRestaurantID(restaurantInfo)
      .subscribe((data) => {
        this.restaurantId = data._id;
        this.auth.userProfile$.source.subscribe((userInfo) => {
          userInfo.role = 'RO';
          userInfo.restaurant_id = data._id;
          this.loginService.addNewUser(userInfo);
        });
      });
  }
}
