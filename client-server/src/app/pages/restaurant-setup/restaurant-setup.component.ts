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
      cover_photo_url: 'link',
      logo_url: 'link',
      rating: '3.00',
    };
    this.restaurantsService
      .getRestaurantID(restaurantInfo)
      .subscribe((data) => {
        this.restaurantId = data._id;
      });
    console.log(this.restaurantId);
    this.auth.userProfile$.source.subscribe((data) => {
      var userInfo = data;
      userInfo.role = 'RO';
      userInfo.restaurant_id = this.restaurantsService.restaurantId;
      this.loginService.addNewUser(userInfo);
    });
    // this.loginService.addNewUser(this.auth.userProfile$.source)
    // this.loginService.updateUser(this.auth.userProfile$.source, null);
    // this.auth.role = 'RO';
  }
}
