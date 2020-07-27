import { Component, OnInit, Input } from '@angular/core';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { TimelineService } from 'src/app/service/timeline.service';
import { RestaurantsService } from 'src/app/service/restaurants.service';

@Component({
  selector: 'app-timeline-post',
  templateUrl: './timeline-post.component.html',
  styleUrls: ['./timeline-post.component.scss'],
})
export class TimelinePostComponent implements OnInit {
  @Input() role: string;
  @Input() post: any;

  comments: any[] = [];

  postId: string = '';
  userId: string = '';
  restaurantId: string = '';

  faTrash = faTrash;
  inputComment: string = '';

  constructor(
    private timeline: TimelineService,
    private restaurantsService: RestaurantsService
  ) {}

  ngOnInit(): void {
    this.restaurantsService
      .getRestaurant(this.post.restaurant_id)
      .subscribe((data) => {
        this.post.restaurant_name = data.name;
      });

    this.loadComments();

    // pass in post
    // set the ids somewhere
    // need do to stuff with comment list id
  }

  loadRestaurant() {}

  loadComments() {
    for (var i = 0; i < this.post.comments.length; i++) {
      this.timeline.getComment(this.post.comments[i]).subscribe((data) => {
        this.comments.push(data);
      });
    }
  }

  addComment() {
    if (this.inputComment != '') {
      // call the endpoint to add comment to post using id
    }

    this.inputComment = '';
    // reload comments for the post
  }
}
