import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DataService } from 'src/app/service/data.service';
import { RestaurantsService } from '../../service/restaurants.service';

@Component({
  selector: 'app-owner-edit',
  templateUrl: './owner-edit.component.html',
  styleUrls: ['./owner-edit.component.scss'],
})
export class OwnerEditComponent implements OnInit {
  restaurantId: string = '';
  role: string = '';

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private data: DataService,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    this.role = this.route.snapshot.queryParams.role;
    //   if (!this.restaurantId || this.role !== 'RO') {
    //     this.router.navigate([''], {
    //       queryParams: { role: this.role, restaurantId: this.restaurantId },
    //     });
    //     alert('No matching restaurant found for this profile!');
    //   } else {
    //     this.data.changeRestaurantId(this.restaurantId);
    //     this.data.changeRole(this.role);
    //   }
  }
}
