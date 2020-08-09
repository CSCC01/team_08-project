import {
  Component,
  OnInit,
  ɵCompiler_compileModuleSync__POST_R3__,
} from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
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
  ROrestaurantId: string = '';
  userId: string = '';
  role: string = '';
  updates: string = 'false';
  restaurantName: string = '';

  posts: any[] = [];
  content: string = '';
  postModalRef: any;
  deleteModalRef: any;
  deletePostId: string = '';
  deletePostIndex: number;

  faPlus = faPlus;
  faTrash = faTrash;

  constructor(
    private timeline: TimelineService,
    private restaurantsService: RestaurantsService,
    private route: ActivatedRoute,
    private router: Router,
    private postModalService: NgbModal,
    private deleteModalService: NgbModal
  ) {}

  ngOnInit(): void {
    this.restaurantId = this.route.snapshot.queryParams.restaurantId;
    this.updates = this.route.snapshot.queryParams.updates;

    this.role = sessionStorage.getItem('role');
    this.userId = sessionStorage.getItem('userId');
    this.ROrestaurantId = sessionStorage.getItem('restaurantId');

    if (this.updates == 'true' || this.ROrestaurantId) {
      if (this.ROrestaurantId != null) {
        this.restaurantId = this.ROrestaurantId;
      }

      this.getRestaurantName();
      this.loadTimeline(this.restaurantId);
    } else {
      this.restaurantId = '';
      this.loadTimeline();
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

  openPostModal(content) {
    this.postModalRef = this.postModalService.open(content, { size: 'lg' });
  }

  openDeleteModal(content, id, index) {
    this.deletePostId = id;
    this.deletePostIndex = index;
    this.deleteModalRef = this.deleteModalService.open(content, { size: 's' });
  }

  createPost() {
    if (this.content == '') {
      alert('Please enter your content before posting!');
    } else {
      const postObj = {
        restaurant_id: this.restaurantId,
        user_email: this.userId,
        content: this.content,
      };

      this.timeline.createPost(postObj).subscribe((data) => {
        this.posts.unshift(data);
        this.postModalRef.close();
      });

      this.content = '';
    }
  }

  deleteContent() {
    this.timeline.deletePost(this.deletePostId);

    if (this.deletePostIndex > -1) {
      this.posts.splice(this.deletePostIndex, 1);
    }

    this.deletePostId = '';
    this.deletePostIndex = 0;
    this.deleteModalRef.close();
  }
}
