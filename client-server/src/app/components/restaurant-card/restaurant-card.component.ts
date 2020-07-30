import { Component, OnInit, Input } from '@angular/core';
import { DataService } from 'src/app/service/data.service';

@Component({
  selector: 'app-restaurant-card',
  templateUrl: './restaurant-card.component.html',
  styleUrls: ['./restaurant-card.component.scss'],
})
export class RestaurantCardComponent implements OnInit {
  @Input() restaurant: any;

  role: string = '';
  userId: string = '';

  totalStars = 5;

  constructor(private data: DataService) {}

  ngOnInit(): void {
    this.data.role.subscribe((role) => (this.role = role));
    this.data.userId.subscribe((userId) => (this.userId = userId));
  }
}
