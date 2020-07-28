import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DataService } from 'src/app/service/data.service';
import { TimelineService } from 'src/app/service/timeline.service';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import { faPlus } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss'],
})
export class TimelineComponent implements OnInit {
  restaurantId: string = '';
  userId: string = '';
  role: string = '';
  restaurantName: string = '';

  posts: any[] = [];

  faPlus = faPlus;

  constructor(
    private data: DataService,
    private timeline: TimelineService,
    private restaurantsService: RestaurantsService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.role = this.route.snapshot.queryParams.role;
    this.userId = this.route.snapshot.queryParams.userId;
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;

    this.data.changeRole(this.role);
    this.data.changeUserId(this.userId);
    this.data.changeRestaurantId(this.restaurantId);

    if (this.restaurantId == undefined || this.restaurantId == '') {
      this.loadTimeline();
    } else {
      this.getRestaurantName();
      this.loadTimeline(this.restaurantId);
    }
  }

  getRestaurantName() {
    this.restaurantsService
      .getRestaurant(this.restaurantId)
      .subscribe((data) => {
        this.restaurantName = data.name;
      });
  }

  loadTimeline(id?) {
    if (id == undefined) {
      this.timeline.getAllPosts().subscribe((data) => {
        this.posts = data.Posts;
      });
    } else {
      this.timeline.getRestaurantPosts(id).subscribe((data) => {
        this.posts = data.Posts;
      });
    }
  }
}
