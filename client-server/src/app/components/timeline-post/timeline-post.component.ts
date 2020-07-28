import { Component, OnInit, Input } from '@angular/core';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { TimelineService } from 'src/app/service/timeline.service';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import { LoginService } from 'src/app/service/login.service';
import { AuthService } from 'src/app/auth/auth.service';

@Component({
  selector: 'app-timeline-post',
  templateUrl: './timeline-post.component.html',
  styleUrls: ['./timeline-post.component.scss'],
})
export class TimelinePostComponent implements OnInit {
  @Input() role: string;
  @Input() id: string;
  @Input() post: any;

  currentUser: any = {};
  comments: any[] = [];

  postId: string = '';
  userId: string = '';
  restaurantId: string = '';

  faTrash = faTrash;
  inputComment: string = '';

  constructor(
    public auth: AuthService,
    private timeline: TimelineService,
    private restaurantsService: RestaurantsService,
    private loginService: LoginService
  ) {}

  ngOnInit(): void {
    this.restaurantsService
      .getRestaurant(this.post.restaurant_id)
      .subscribe((data) => {
        this.post.restaurant_name = data.name;
      });

    this.loadComments();

    if (this.id != undefined && this.id != '') {
      this.loginService.getUser({ email: this.id }).subscribe((data) => {
        this.currentUser.pic_url = data.picture;
      });
    }
  }

  loadRestaurant() {}

  loadComments() {
    for (var i = 0; i < this.post.comments.length; i++) {
      this.timeline.getComment(this.post.comments[i]).subscribe((data) => {
        const userData = {
          email: data.user_email,
        };
        this.loginService.getUser(userData).subscribe((user) => {
          data.user_name = user.name;
          data.user_pic = user.picture;
          this.comments.push(data);
        });
      });
    }
  }

  addComment() {
    if (this.inputComment != '') {
    }

    this.inputComment = '';
  }
}
