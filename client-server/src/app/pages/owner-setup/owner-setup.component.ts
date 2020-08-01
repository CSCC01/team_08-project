import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestaurantsService } from '../../service/restaurants.service';

@Component({
  selector: 'app-owner-setup',
  templateUrl: './owner-setup.component.html',
  styleUrls: ['./owner-setup.component.scss'],
})
export class OwnerSetupComponent implements OnInit {
  restaurantId: string = '';
  userId: string = '';
  role: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
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
  }

  updateOwner() {
    var restaurantInfo = {
      restaurant_id: this.restaurantId,
      owner_name: (<HTMLInputElement>document.getElementById('owner-name'))
        .value,
      owner_story: (<HTMLInputElement>document.getElementById('owner-story'))
        .value,
    };
    if (restaurantInfo.owner_name == '' || restaurantInfo.owner_story == '') {
      alert('Please enter all requried information about the owner!');
    } else {
      this.restaurantsService.editRestaurant(restaurantInfo);
      this.router.navigate(['/menu-setup']);
    }
  }
}
