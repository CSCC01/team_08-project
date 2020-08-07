import { Component, OnInit, Output, Input, EventEmitter } from '@angular/core';
import {FormControl} from '@angular/forms';

@Component({
  selector: 'app-validated-form-control',
  templateUrl: './validated-form-control.component.html',
  styleUrls: ['./validated-form-control.component.scss']
})
export class ValidatedFormControlComponent implements OnInit {
    @Input() errorMessage: string;
    @Output() form: EventEmitter<any> = new EventEmitter<any>();

    message: string;
    style: string;

  constructor() { }

  ngOnInit(): void { }

  onValid(){
    this.message = this.errorMessage
  }

  onInvalid(){
    this.message = ''
  }
  
  sendData(){
    const formData = {
        value: this.value
    }
    this.form.emit(formData)
  }

}
