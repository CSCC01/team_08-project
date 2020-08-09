import { Component, OnInit, Output, EventEmitter, Input } from '@angular/core';
import { StarRatingComponent } from 'ng-starrating';

@Component({
  selector: 'app-review-card',
  templateUrl: './review-card.component.html',
  styleUrls: ['./review-card.component.scss'],
})
export class ReviewCardComponent implements OnInit {
  @Input() width: number;
  @Output() review: EventEmitter<any> = new EventEmitter<any>();

  totalStars = 5;
  starRating: StarRatingComponent;
  rating: number;
  title: string = '';
  comments: string = '';

  constructor() {}

  ngOnInit(): void {
    var el = document.getElementById('cardBox');
    el.style.width = this.width + 'px';
  }

  onRate($event: {
    oldValue: number;
    newValue: number;
    starRating: StarRatingComponent;
  }) {
    this.rating = $event.newValue;
    this.starRating = $event.starRating;
  }

  sendReview() {
    if (this.title == '' || this.comments == '') {
      alert('Please provide comments for your review!');
    } else {
      const reviewObj = {
        rating: this.rating,
        title: this.title,
        content: this.comments,
      };
      this.review.emit(reviewObj);

      this.starRating.value = 0;
      this.rating = 0;
      this.title = '';
      this.comments = '';
    }
  }
}
