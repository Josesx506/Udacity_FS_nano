import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { AuthService } from './auth.service';
import { environment } from 'src/environments/environment';

export interface Barista {
  id: number;
  name: string;
  flavors: string[]; // Array of strings representing flavors
  proficiency: number;
}

@Injectable({
  providedIn: 'root'
})
export class BaristasService {

  url = environment.apiServerUrl;

  public items: {[key: number]: Barista} = {};
  //  = {
  //                                         1: {
  //                                         id: 1,
  //                                         name: 'Padre Thomas',
  //                                         flavors: ['latte', 'mocha'],
  //                                         proficiency: 2
  //                                       }
  //                                     };


  constructor(private auth: AuthService, private http: HttpClient) { }

  getHeaders() {
    const header = {
      headers: new HttpHeaders()
        .set('Authorization',  `Bearer ${this.auth.activeJWT()}`)
    };
    return header;
  }

  getBaristas() {
    if (this.auth.can('get:baristas')) {
      this.http.get(this.url + '/baristas', this.getHeaders())
      .subscribe((res: any) => {
        this.baristasToItems(res.baristas);
        console.log(res);
      });
    } 
  }

  saveBarista(barista: Barista) {
    if (barista.id >= 0) { // patch
      this.http.patch(this.url + '/baristas/' + barista.id, barista, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.baristasToItems(res.baristas);
        }
      });
    } else { // insert
      this.http.post(this.url + '/baristas', barista, this.getHeaders())
      .subscribe( (res: any) => {
        if (res.success) {
          this.baristasToItems(res.baristas);
        }
      });
    }

  }

  deleteBarista(barista: Barista) {
    delete this.items[barista.id];
    this.http.delete(this.url + '/baristas/' + barista.id, this.getHeaders())
    .subscribe( (res: any) => {

    });
  }

  baristasToItems( baristas: Array<Barista>) {
    for (const barista of baristas) {
      this.items[barista.id] = barista;
    }
  }
}
