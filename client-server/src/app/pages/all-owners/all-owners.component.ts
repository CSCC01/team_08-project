import { Component, OnInit } from '@angular/core';
import { RestaurantsService } from '../../service/restaurants.service';

@Component({
  selector: 'app-all-owners',
  templateUrl: './all-owners.component.html',
  styleUrls: ['./all-owners.component.scss'],
})
export class AllOwnersComponent implements OnInit {
  allStories: any[];

  constructor(private restaurantsService: RestaurantsService) {}

  ngOnInit(): void {
    this.loadRestaurants();
  }

  loadRestaurants() {
    this.allStories = [];
    this.restaurantsService.listRestaurants().subscribe((data) => {
      for (let i = 0; i < data.Restaurants.length; i++) {
        this.allStories[i] = {
          type: 'story',
          name: data.Restaurants[i].owner_name,
          profile_pic: data.Restaurants[i].owner_picture_url,
          bio: data.Restaurants[i].owner_story,
          restaurant: data.Restaurants[i].name,
          _id: data.Restaurants[i]._id,
        };
      }
    });
  }
}
