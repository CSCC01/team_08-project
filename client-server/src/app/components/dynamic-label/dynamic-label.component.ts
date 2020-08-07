import { Component, OnInit, Output, Input, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-dynamic-label',
  templateUrl: './dynamic-label.component.html',
  styleUrls: ['./dynamic-label.component.scss']
})
export class DynamicLabelComponent implements OnInit {
  @Input() name: string;
  @Input() message: string;
  @Input() open: boolean = false;

  constructor() { }

  ngOnInit(): void { }

}
