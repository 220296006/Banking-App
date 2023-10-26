import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AngularMaterialModule } from './modules/material/material.module';
import { LoginComponent } from './components/login/login.component';
import { LoginService } from './services/login.service';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HomeComponent } from './components/home/home.component';
import { HomeLoanComponent } from './components/home-loan/home-loan.component';
import { InvestmentCalculatorComponent } from './components/investment-calculator/investment-calculator.component';
import { SideBarNavComponent } from './components/side-bar-nav/side-bar-nav.component';
import { MatIconModule } from '@angular/material/icon';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    HomeLoanComponent,
    InvestmentCalculatorComponent,
    SideBarNavComponent,
    ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    AngularMaterialModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule,
    MatIconModule
  ],
  providers: [LoginService],
  bootstrap: [AppComponent]
})
export class AppModule { }
