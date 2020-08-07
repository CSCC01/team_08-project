import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'app-cart-card',
  templateUrl: './cart-card.component.html',
  styleUrls: ['./cart-card.component.scss'],
})
export class CartCardComponent implements OnInit {
  @Input() dish: any;
  value: number = 0;

  constructor() {}

  ngOnInit(): void {}
}
