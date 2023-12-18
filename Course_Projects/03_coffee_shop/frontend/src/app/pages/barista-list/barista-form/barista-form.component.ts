import { Component, OnInit, Input } from '@angular/core';
import { Barista, BaristasService } from 'src/app/services/baristas.service';
import { ModalController } from '@ionic/angular';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-barista-form',
  templateUrl: './barista-form.component.html',
  styleUrls: ['./barista-form.component.scss'],
})
export class BaristaFormComponent implements OnInit {
  @Input() barista: Barista;
  @Input() isNew: boolean;
  availableFlavors: string[] = [
    "Americano",
    "Chocolate",
    "Caramel",
    "Hazelnut",
    "Hot Chocolate",
    "Hot Water",
    "Latte",
    "Mocha",
    "Nitro",
    "Vanilla",
    ];

  constructor(
    public auth: AuthService,
    private modalCtrl: ModalController,
    private baristaService: BaristasService
    ) { }

  ngOnInit() {
    if (this.isNew) {
      this.barista = {
        id: -1,
        name: '',
        flavors: [],
        proficiency: 1,
        image_url: '',
      };
      this.addDetails();
    }
  }

  customTrackBy(index: number, obj: any): any {
    return index;
  }

  addDetails(i: number = 0) {
    this.barista.flavors.splice(i + 1, 0, );
  }

  removeDetails(i: number) {
    this.barista.flavors.splice(i, 1);
  }

  closeModal() {
    this.modalCtrl.dismiss();
  }

  saveClicked() {
    this.baristaService.saveBarista(this.barista);
    this.closeModal();
  }

  deleteClicked() {
    this.baristaService.deleteBarista(this.barista);
    this.closeModal();
  }
}
