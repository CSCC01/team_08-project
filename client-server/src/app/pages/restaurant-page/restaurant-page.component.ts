import { Component, OnInit, Input, HostListener } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import {
  faMapMarkerAlt,
  faPhone,
  faEdit,
} from '@fortawesome/free-solid-svg-icons';
import { faHeart, faEnvelope } from '@fortawesome/free-regular-svg-icons';
import { faTwitter, faInstagram } from '@fortawesome/free-brands-svg-icons';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import dishes from '../../../assets/data/dishes.json';
import reviews from '../../../assets/data/reviews.json';
import { DataService } from 'src/app/service/data.service';

@Component({
  selector: 'app-restaurant-page',
  templateUrl: './restaurant-page.component.html',
  styleUrls: ['./restaurant-page.component.scss'],
})
export class RestaurantPageComponent implements OnInit {
  @Input() userId: any; // pass the user id everywhere

  restaurantId: string;
  role: string;
  dishes: any[] = [];
  reviews: any[] = [];
  restaurantDetails: any;
  restaurantMenu: any[] = [];

  menu = {
    category: [
      {
        name: 'Appetizer',
        menu: dishes,
      },
      {
        name: 'Dessert',
        menu: dishes,
      },
    ],
  };

  totalStars = 5;
  faMapMarker = faMapMarkerAlt;
  faPhone = faPhone;
  faMail = faEnvelope;
  faHeartLine = faHeart;
  faTwitter = faTwitter;
  faInstagram = faInstagram;
  faEdit = faEdit;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private restaurantsService: RestaurantsService,
    private data: DataService
  ) {
    this.dishes = dishes;
    this.reviews = reviews;
  }

  ngOnInit(): void {
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    this.role = this.route.snapshot.queryParams.role;

    this.data.changeRestaurantId(this.restaurantId);
    this.data.changeRole(this.role);

    // generate restaurant page
    this.restaurantsService
      .getRestaurant(this.restaurantId)
      .subscribe((data) => {
        this.restaurantDetails = data;
      });

    // generate restaurant menu
    this.restaurantsService
      .getRestaurantFood(this.restaurantId)
      .subscribe((data) => {
        this.restaurantMenu = data.Dishes;
      });
  }

  @HostListener('window:resize', ['$event'])
  onResize() {
    var el1 = document.getElementById('info-col1');
    var el2 = document.getElementById('info-col2');
    var el3 = document.getElementById('info-row');

    if (window.innerWidth < 750) {
      el1.classList.remove('col-md-7');
      el2.classList.remove('col-md-5');
      el3.classList.remove('row');
    } else {
      el1.classList.add('col-md-7');
      el2.classList.add('col-md-5');
      el3.classList.add('row');
    }
  }

  editMenu() {
    this.router.navigate(['/menu-edit'], {
      queryParams: { role: this.role, restaurantId: this.restaurantId },
    });
  }

  editOwner() {
    this.router.navigate(['/owner-edit'], {
      queryParams: { role: this.role, restaurantId: this.restaurantId },
    });
  }
}
