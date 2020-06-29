import { Component, OnInit, HostListener } from '@angular/core';
import { AuthService } from '../../auth/auth.service';
import { faSearch, faUserCircle } from '@fortawesome/free-solid-svg-icons';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {
  title = 'client-server';
  faSearch = faSearch;
  faUserCircle = faUserCircle;

  constructor(public auth: AuthService) {}

  @HostListener('window:resize', ['$event'])
  onResize() {
    var el = document.getElementById('footer-main-links');
    if (window.innerWidth < 850) {
      el.classList.remove('row');
    } else {
      el.classList.add('row');
    }
  }

  ngOnInit() {}
}