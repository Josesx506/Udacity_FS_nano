import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Routes, RouterModule } from '@angular/router';

import { IonicModule } from '@ionic/angular';

import { BaristaListPage } from './barista-list.page';
import { BaristaGraphicComponent } from './barista-graphic/barista-graphic.component';
import { BaristaFormComponent } from './barista-form/barista-form.component';

const routes: Routes = [
  {
    path: '',
    component: BaristaListPage
  }
];

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    RouterModule.forChild(routes)
  ],
  entryComponents: [BaristaFormComponent],
  declarations: [BaristaListPage, BaristaGraphicComponent, BaristaFormComponent],
})
export class BaristaListPageModule {}
