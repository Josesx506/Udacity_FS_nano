import { Component, OnInit, Input } from '@angular/core';
import { Barista } from 'src/app/services/baristas.service';

@Component({
  selector: 'app-barista-graphic',
  templateUrl: './barista-graphic.component.html',
  styleUrls: ['./barista-graphic.component.scss'],
})
export class BaristaGraphicComponent implements OnInit {
  @Input() barista: Barista;

  constructor() { }

  ngOnInit() {}

}
