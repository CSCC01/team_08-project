import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-all-order-card',
  templateUrl: './all-order-card.component.html',
  styleUrls: ['./all-order-card.component.scss'],
})
export class AllOrderCardComponent implements OnInit {
  @Input() order: any;

  constructor() {}

  ngOnInit(): void {}
}
