import { Component, OnInit, Input } from '@angular/core';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
import { TimelineService } from 'src/app/service/timeline.service';
import { RestaurantsService } from 'src/app/service/restaurants.service';
import { LoginService } from 'src/app/service/login.service';
import { AuthService } from 'src/app/auth/auth.service';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';

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

  deleteModalRef: any;
  deleteCommentId: string = '';
  deleteCommentIndex: number;

  faTrash = faTrash;
  inputComment: string = '';

  constructor(
    public auth: AuthService,
    private timeline: TimelineService,
    private restaurantsService: RestaurantsService,
    private loginService: LoginService,
    private deleteModalService: NgbModal
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
        this.currentUser.user_name = data.name;
        this.currentUser.user_pic = data.picture;
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
      var commentObj = {};
      commentObj['post_id'] = this.post._id;
      commentObj['user_email'] = this.id;
      commentObj['content'] = this.inputComment;
      this.timeline.createComment(commentObj);

      commentObj['user_name'] = this.currentUser.user_name;
      commentObj['user_pic'] = this.currentUser.user_pic;

      this.comments.push(commentObj);
    }

    this.inputComment = '';
  }

  openDeleteModal(content, id, index) {
    this.deleteCommentId = id;
    this.deleteCommentIndex = index;

    this.deleteModalRef = this.deleteModalService.open(content, { size: 's' });
  }

  deleteComment() {
    this.timeline.deleteComment(this.deleteCommentId);

    if (this.deleteCommentIndex > -1) {
      this.comments.splice(this.deleteCommentIndex, 1);
    }

    this.deleteCommentId = '';
    this.deleteCommentIndex = 0;

    this.deleteModalRef.close();
  }
}
