import { Component, OnInit } from '@angular/core';
import { BaristasService, Barista } from '../../services/baristas.service';
import { ModalController } from '@ionic/angular';
import { BaristaFormComponent } from './barista-form/barista-form.component';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-barista-list',
  templateUrl: './barista-list.page.html',
  styleUrls: ['./barista-list.page.scss'],
})
export class BaristaListPage implements OnInit {
  Object = Object;

  constructor(
    private auth: AuthService,
    private modalCtrl: ModalController,
    public baristas: BaristasService
    ) { }

  ngOnInit() {
    this.baristas.getBaristas();
  }

  async openForm(activebarista: Barista = null) {
    if (!this.auth.can('get:baristas')) {
      return;
    }

    const modal = await this.modalCtrl.create({
      component: BaristaFormComponent,
      componentProps: { barista: activebarista, isNew: !activebarista }
    });

    modal.present();
  }

}
