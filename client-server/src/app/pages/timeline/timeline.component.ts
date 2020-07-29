import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NgbModal } from '@ng-bootstrap/ng-bootstrap';
import { faTrash } from '@fortawesome/free-solid-svg-icons';
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
  content: string = '';
  postModalRef: any;
  deleteModalRef: any;
  deletePostId: string = '';
  deletePostIndex: number;

  faPlus = faPlus;
  faTrash = faTrash;

  constructor(
    private data: DataService,
    private timeline: TimelineService,
    private restaurantsService: RestaurantsService,
    private route: ActivatedRoute,
    private router: Router,
    private postModalService: NgbModal,
    private deleteModalService: NgbModal
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

      this.timeline.createPost(postObj);

      this.timeline.getAllPosts().subscribe((data) => {
        const len = data.Posts.length;
        this.posts.push(data.Posts[len - 1]);
        this.postModalRef.close();
        this.content = '';
      });
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
