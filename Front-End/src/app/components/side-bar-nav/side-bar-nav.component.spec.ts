import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SideBarNavComponent } from './side-bar-nav.component';

describe('SideBarNavComponent', () => {
  let component: SideBarNavComponent;
  let fixture: ComponentFixture<SideBarNavComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SideBarNavComponent]
    });
    fixture = TestBed.createComponent(SideBarNavComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
