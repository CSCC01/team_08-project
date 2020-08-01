import { Component, OnInit } from '@angular/core';
import { LoginService } from '../../service/login.service';
import { AuthService } from '../../auth/auth.service';
import { RestaurantsService } from '../../service/restaurants.service';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-restaurant-setup',
  templateUrl: './restaurant-setup.component.html',
  styleUrls: ['./restaurant-setup.component.scss'],
})
export class RestaurantSetupComponent implements OnInit {
  userId: string = '';

  constructor(
    public auth: AuthService,
    private loginService: LoginService,
    private restaurantsService: RestaurantsService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.userId = sessionStorage.getItem('userId');
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
      GEO_location: 'blank',
      external_delivery_link: 'blank',
      rating: '0.00',
    };

    if (
      restaurantInfo.name == '' ||
      restaurantInfo.address == '' ||
      restaurantInfo.city == '' ||
      restaurantInfo.phone == '' ||
      restaurantInfo.email == '' ||
      restaurantInfo.pricepoint == 'Choose...' ||
      restaurantInfo.cuisine == '' ||
      restaurantInfo.bio == ''
    ) {
      alert('Please enter all requried information about the restaurant!');
    } else {
      // Attach a restaurant ID to the current user and upgrade them
      this.restaurantsService.getRestaurantID(restaurantInfo).subscribe(
        (data) => {
          sessionStorage.setItem('restaurantId', data._id);
          this.router.navigate(['/owner-setup']);
          this.auth.userProfile$.source.subscribe((userInfo) => {
            userInfo.role = 'RO';
            userInfo.restaurant_id = data._id;
            sessionStorage.setItem('role', 'RO');
            this.loginService.addNewUser(userInfo);
          });
        },
        (error) => {
          alert('Sorry a restaurant with this email has already been found');
          this.router.navigate(['']);
        }
      );
    }
  }
}
