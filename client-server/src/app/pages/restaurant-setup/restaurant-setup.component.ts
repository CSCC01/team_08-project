import { Component, OnInit } from '@angular/core';
import { LoginService } from '../../service/login.service';
import { AuthService } from '../../auth/auth.service';
import { RestaurantsService } from '../../service/restaurants.service';
import { faThumbsDown } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-restaurant-setup',
  templateUrl: './restaurant-setup.component.html',
  styleUrls: ['./restaurant-setup.component.scss'],
})
export class RestaurantSetupComponent implements OnInit {
  constructor(
    public auth: AuthService,
    private loginService: LoginService,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {}

  upgradeUser(): void {
    var restaurantInfo = {
      'restaurant-name': (<HTMLInputElement>(
        document.getElementById('restaurant-name')
      )).value,
      'restaurant-address': (<HTMLInputElement>(
        document.getElementById('restaurant-address')
      )).value,
      'restaurant-city': (<HTMLInputElement>(
        document.getElementById('restaurant-city')
      )).value,
      'phone-number': (<HTMLInputElement>(
        document.getElementById('phone-number')
      )).value,
      'restaurant-email': (<HTMLInputElement>(
        document.getElementById('restaurant-email')
      )).value,
      pricepoint: (<HTMLInputElement>document.getElementById('pricepoint'))
        .value,
      'restaurant-cuisine': (<HTMLInputElement>(
        document.getElementById('restaurant-cuisine')
      )).value,
      'restaurant-bio': (<HTMLInputElement>(
        document.getElementById('restaurant-bio')
      )).value,
      twitter: (<HTMLInputElement>document.getElementById('twitter')).value,
      instagram: (<HTMLInputElement>document.getElementById('instagram')).value,
    };
    var restaurantID = this.restaurantsService.getRestaurantID(restaurantInfo);
    console.log(restaurantID);
    this.auth.userProfile$.source.subscribe((data) => {
      var userInfo = data;
      userInfo.role = 'RO';
      userInfo.restaurant_id = restaurantID;
      this.loginService.addNewUser(userInfo);
    });
    // this.loginService.addNewUser(this.auth.userProfile$.source)
    // this.loginService.updateUser(this.auth.userProfile$.source, null);
    // this.auth.role = 'RO';
  }
}
