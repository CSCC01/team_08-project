import { Component, OnInit, Input } from '@angular/core';
import { faTrash } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-timeline-post',
  templateUrl: './timeline-post.component.html',
  styleUrls: ['./timeline-post.component.scss'],
})
export class TimelinePostComponent implements OnInit {
  @Input() role: string;
  @Input() post: any;
  @Input() comments: any;

  postId: string = '';
  userId: string = '';
  restaurantId: string = '';

  faTrash = faTrash;
  inputComment: string = '';

  constructor() {}

  ngOnInit(): void {
    // pass in post
    // set the ids somewhere
    // need do to shit with comment list id
  }

  addComment() {
    console.log(this.inputComment);
    if (this.inputComment != '') {
      // call the endpoint to add comment to post using id
    }

    this.inputComment = '';
    // reload comments for the post
  }
}
