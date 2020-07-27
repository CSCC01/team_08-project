import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { DataService } from 'src/app/service/data.service';

@Component({
  selector: 'app-timeline',
  templateUrl: './timeline.component.html',
  styleUrls: ['./timeline.component.scss'],
})
export class TimelineComponent implements OnInit {
  restaurantId: string = '';
  role: string = '';

  constructor(
    private data: DataService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.role = this.route.snapshot.queryParams.role;
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;

    this.data.changeRole(this.role);
    this.data.changeRestaurantId(this.restaurantId);

    this.loadTimeline(this.restaurantId);
  }

  loadTimeline(id) {
    // if id is there, its the individual timeline list
    // it not, its the overall timeline list
    // call the endpoint accordingly
  }
}
