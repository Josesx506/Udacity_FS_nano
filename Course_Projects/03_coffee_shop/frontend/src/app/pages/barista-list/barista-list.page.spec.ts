import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BaristaListPage } from './barista-list.page';

describe('BaristaListPage', () => {
  let component: BaristaListPage;
  let fixture: ComponentFixture<BaristaListPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BaristaListPage ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BaristaListPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
