import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { RestaurantsService } from '../../service/restaurants.service';

@Component({
  selector: 'app-owner-edit',
  templateUrl: './owner-edit.component.html',
  styleUrls: ['./owner-edit.component.scss'],
})
export class OwnerEditComponent implements OnInit {
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

    // generate restaurant page
    this.restaurantsService
      .getRestaurant(this.restaurantId)
      .subscribe((data) => {
        this.restaurantDetails = data;
      });
  }

  updateOwnerInfo() {
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
      this.router.navigate(['/restaurant']);
    }
  }

  cancel() {
    this.router.navigate(['/restaurant']);
  }
}
